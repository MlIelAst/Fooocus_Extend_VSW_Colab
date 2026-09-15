import os
import re
import subprocess
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path


def classify_runtime_line(line: str):
    low = line.lower()
    if any(x in low for x in ("unchecked runtime.lasterror", "sentry.init", "content.js")):
        return (
            "Browser-Erweiterung",
            "wahrscheinlich externe Browser-Erweiterung; nicht automatisch ein Fooocus-Fehler",
            "Inkognito-Fenster ohne Erweiterungen testen",
        )
    if any(x in low for x in ("unexpected token '<'", "<!doctype", "404 /run/predict", "failed to parse json", "unexpected token")):
        return (
            "Gradio / Tunnel / Frontend",
            "das Frontend hat keine erwartete JSON-Antwort erhalten; häufig ist der öffentliche Tunnel abgerissen oder liefert eine HTML-Fehlerseite",
            "lokalen Fooocus-Server prüfen; wenn lokal OK und öffentlich fehlerhaft, Tunnel neu aufbauen statt Fooocus neu zu installieren",
        )
    if "websocket" in low and any(x in low for x in ("failed", "closed", "queue/join")):
        return (
            "Öffentlicher Tunnel / WebSocket",
            "die Queue-Verbindung zwischen Browser und Fooocus ist unterbrochen",
            "lokalen Server und öffentlichen Tunnel getrennt prüfen",
        )
    if any(x in low for x in ("cuda out of memory", "outofmemoryerror", "out of memory")):
        return (
            "GPU-Speicher",
            "CUDA-/VRAM-Speicher ist sehr wahrscheinlich erschöpft",
            "Bildanzahl und Zusatzmodule reduzieren; High-VRAM-Modus deaktivieren; danach erneut testen",
        )
    if "photopea" in low and any(x in low for x in ("error", "failed", "404", "exception")):
        return (
            "Optionales Modul: Photopea",
            "Zusatzmodul betroffen; Bildgenerierung kann trotzdem funktionieren",
            "Standard-Generate ohne Photopea prüfen",
        )
    return None


def _probe(base_url: str, path: str = "/config", timeout: int = 5):
    if not base_url:
        return {"ok": False, "status": None, "content_type": None, "preview": "keine URL"}
    url = base_url.rstrip("/") + path
    req = urllib.request.Request(url, headers={"User-Agent": "VSW-Fooocus-Healthcheck/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read(512)
            text = raw.decode("utf-8", errors="replace").strip().replace("\n", " ")
            content_type = response.headers.get("content-type", "")
            status = getattr(response, "status", 200)
            looks_json = "json" in content_type.lower() or text.startswith("{") or text.startswith("[")
            return {
                "ok": 200 <= status < 400 and looks_json,
                "status": status,
                "content_type": content_type,
                "preview": text[:160],
            }
    except urllib.error.HTTPError as exc:
        try:
            raw = exc.read(512)
            text = raw.decode("utf-8", errors="replace").strip().replace("\n", " ")
        except Exception:
            text = ""
        return {
            "ok": False,
            "status": exc.code,
            "content_type": exc.headers.get("content-type", "") if exc.headers else "",
            "preview": text[:160],
        }
    except Exception as exc:
        return {"ok": False, "status": None, "content_type": None, "preview": repr(exc)}


def _gpu_snapshot():
    cmd = [
        "nvidia-smi",
        "--query-gpu=name,memory.used,memory.total,utilization.gpu",
        "--format=csv,noheader,nounits",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode:
        return "nicht verfügbar"
    parts = [x.strip() for x in result.stdout.strip().split(",")]
    if len(parts) >= 4:
        return f"{parts[0]} | VRAM {parts[1]}/{parts[2]} MiB | GPU {parts[3]} %"
    return result.stdout.strip() or "nicht verfügbar"


def _extract_public_url(log_path: Path):
    if not log_path.exists():
        return None
    text = log_path.read_text(encoding="utf-8", errors="replace")
    matches = re.findall(r"https://[A-Za-z0-9.-]+(?:\.gradio\.live|\.trycloudflare\.com)", text)
    return matches[-1] if matches else None


def _process_running():
    result = subprocess.run(
        ["bash", "-lc", "pgrep -af 'launch.py|entry_with_update.py' | grep -v pgrep || true"],
        capture_output=True,
        text=True,
    )
    return bool(result.stdout.strip()), result.stdout.strip()


def _log_findings(log_path: Path):
    findings = []
    if not log_path.exists():
        return findings
    lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    needles = (
        "cuda out of memory",
        "outofmemoryerror",
        "killed",
        "traceback",
        "runtimeerror",
        "exception",
        "faceenhancer",
    )
    for line in lines[-300:]:
        low = line.lower()
        if any(n in low for n in needles):
            findings.append(line.strip())
    return findings[-12:]


def print_runtime_diagnosis(
    log_path="/content/fooocus_extend_startup.log",
    local_url="http://127.0.0.1:7865",
    public_url=None,
    process=None,
    tunnel=None,
):
    log_path = Path(log_path)
    if public_url is None:
        public_url = _extract_public_url(log_path)

    if process is not None:
        process_alive = process.poll() is None
        process_info = f"PID {process.pid}" if process_alive else f"beendet (Exit {process.poll()})"
    else:
        process_alive, process_info = _process_running()
        process_info = process_info or "kein Fooocus-Prozess gefunden"

    local = _probe(local_url)
    public = _probe(public_url) if public_url else {"ok": False, "status": None, "content_type": None, "preview": "keine öffentliche URL im Log"}

    print("\n" + "═" * 72)
    print("VSW RUNTIME-DIAGNOSE")
    print("═" * 72)
    print(f"Fooocus-Prozess:    {'ONLINE' if process_alive else 'OFFLINE'} | {process_info}")
    print(f"Lokaler /config:    {'OK' if local['ok'] else 'FEHLER'} | Status {local['status']} | {local['content_type']}")
    print(f"Öffentlicher Tunnel:{' OK' if public['ok'] else ' FEHLER'} | Status {public['status']} | {public['content_type']}")
    print(f"Lokale URL:         {local_url}")
    print(f"Öffentliche URL:    {public_url or 'nicht gefunden'}")
    print(f"GPU:                {_gpu_snapshot()}")

    if local["ok"] and not public["ok"] and public_url:
        print("\nDIAGNOSE: Fooocus läuft lokal, aber der öffentliche Tunnel antwortet nicht korrekt.")
        print("AKTION: Öffentlichen Tunnel neu aufbauen bzw. Sitzung mit Cloudflared neu starten.")
        if public.get("preview", "").lower().startswith("<!doctype") or "text/html" in str(public.get("content_type", "")).lower():
            print("HINWEIS: Der Tunnel liefert HTML statt JSON. Das erklärt Fehler wie 'Unexpected token <'.")
    elif not local["ok"] and not process_alive:
        print("\nDIAGNOSE: Fooocus-Backend ist beendet. Der Tunnel-Fehler ist wahrscheinlich eine Folge davon.")
        print("AKTION: Log auf CUDA-OOM, Killed, Traceback oder Zusatzmodulfehler prüfen.")
    elif not local["ok"] and process_alive:
        print("\nDIAGNOSE: Prozess läuft, aber der lokale Gradio-Endpunkt reagiert nicht korrekt.")
        print("AKTION: Backend-/Gradio-Log prüfen; Prozess kann hängen oder sich noch im Start befinden.")
    elif local["ok"] and public["ok"]:
        print("\nDIAGNOSE: Lokales Backend und öffentlicher Tunnel sind erreichbar.")
        print("AKTION: Bei fortbestehendem Browserfehler Seite hart neu laden oder Inkognito ohne Erweiterungen testen.")
    else:
        print("\nDIAGNOSE: Öffentlicher Tunnel ist nicht bestimmbar. Lokalen Backendstatus als Primärsignal verwenden.")

    findings = _log_findings(log_path)
    if findings:
        print("\nRelevante Log-Hinweise:")
        for line in findings:
            print("- " + line[:220])

    if not local["ok"]:
        print("\nLokale Antwort:", local.get("preview", "")[:200])
    if public_url and not public["ok"]:
        print("Öffentliche Antwort:", public.get("preview", "")[:200])
    print("═" * 72 + "\n")

    return {
        "process_alive": process_alive,
        "local": local,
        "public": public,
        "public_url": public_url,
        "gpu": _gpu_snapshot(),
        "tunnel": tunnel,
    }


def run_fooocus(cmd, cwd, log_path, tunnel, start_time):
    """Run Fooocus with startup progress and post-start health monitoring."""
    print("$ " + " ".join(map(str, cmd)), flush=True)
    env = os.environ.copy()
    env.update(PYTHONUNBUFFERED="1", PYTHONNOUSERSITE="1", PIP_DISABLE_PIP_VERSION_CHECK="1")

    stop_heartbeat = threading.Event()
    stop_health = threading.Event()
    ready = threading.Event()
    state = {"local_url": "http://127.0.0.1:7865", "public_url": None}
    reported = set()

    def elapsed():
        seconds = int(time.time() - start_time)
        return f"{seconds//60:02d}:{seconds%60:02d}"

    def beat():
        while not stop_heartbeat.wait(20):
            print(f"… läuft weiter | Fooocus starten / Modelle laden | gesamt {elapsed()}", flush=True)

    heartbeat = threading.Thread(target=beat, daemon=True)
    heartbeat.start()

    process = subprocess.Popen(
        [str(x) for x in cmd],
        cwd=str(cwd),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    def health_monitor():
        previous = None
        while not stop_health.wait(30):
            if not ready.is_set() or process.poll() is not None:
                continue
            local = _probe(state["local_url"])
            public = _probe(state["public_url"]) if state["public_url"] else {"ok": False}
            current = (local.get("ok"), public.get("ok"), local.get("status"), public.get("status"))
            if current == previous:
                continue
            previous = current
            if local.get("ok") and state["public_url"] and not public.get("ok"):
                print("\n[VSW-WARNUNG] Öffentlicher Tunnel antwortet nicht korrekt, Fooocus lokal aber schon.", flush=True)
                print("Lokaler Server: OK | Öffentlicher Tunnel: FEHLER", flush=True)
                print("Wenn im Browser 'Reconnect' oder 'Unexpected token <' erscheint: nicht neu installieren; Tunnel neu aufbauen.", flush=True)
            elif not local.get("ok"):
                print("\n[VSW-WARNUNG] Lokaler Fooocus-/Gradio-Endpunkt ist nicht erreichbar.", flush=True)
                print("Bitte Log und GPU-Speicher prüfen; Backend kann beendet oder blockiert sein.", flush=True)

    health = threading.Thread(target=health_monitor, daemon=True)
    health.start()

    tail = []
    with Path(log_path).open("a", encoding="utf-8") as log:
        for line in process.stdout:
            print(line, end="", flush=True)
            log.write(line)
            log.flush()
            tail = (tail + [line.rstrip()])[-100:]

            match = re.search(r"Running on local URL:\s*(https?://\S+)", line)
            if match:
                state["local_url"] = match.group(1).rstrip(".,)")

            match = re.search(r"Running on public URL:\s*(https?://\S+)", line)
            if match:
                state["public_url"] = match.group(1).rstrip(".,)")

            if "trycloudflare.com" in line:
                match = re.search(r"https://[A-Za-z0-9.-]+\.trycloudflare\.com", line)
                if match:
                    state["public_url"] = match.group(0)

            should_ready = bool(state["public_url"]) if tunnel in ("gradio", "cloudflared") else bool(state["local_url"])
            if should_ready and not ready.is_set():
                ready.set()
                stop_heartbeat.set()
                print("\n" + "═" * 68, flush=True)
                print("[100%] WEBOBERFLÄCHE BEREIT", flush=True)
                print("Fooocus_extend läuft erfolgreich.", flush=True)
                print(f"Lokale URL:      {state['local_url']}", flush=True)
                print(f"Öffentliche URL: {state['public_url'] or 'nicht aktiviert'}", flush=True)
                print(f"Tunnel:          {tunnel}", flush=True)
                print(f"GPU:             {_gpu_snapshot()}", flush=True)
                print(f"Gesamte Startzeit: {elapsed()}", flush=True)
                print("\nHinweis:", flush=True)
                print("Bei Reconnect-/JSON-Fehlern zuerst die VSW-Diagnose ausführen. Sie trennt Backend-, Tunnel- und VRAM-Probleme.", flush=True)
                print("═" * 68 + "\n", flush=True)

            diag = classify_runtime_line(line)
            if diag:
                signature = (diag[0], line.strip())
                if signature not in reported:
                    reported.add(signature)
                    area, meaning, next_step = diag
                    print("\n[VSW-HINWEIS] Laufzeitmeldung erkannt:", flush=True)
                    print(f"Bereich: {area}", flush=True)
                    print(f"Meldung: {line.strip()[:500]}", flush=True)
                    print(f"Einordnung: {meaning}.", flush=True)
                    print(f"Empfohlener Prüfschritt: {next_step}.", flush=True)

        return_code = process.wait()

    stop_heartbeat.set()
    stop_health.set()
    heartbeat.join(timeout=1)
    health.join(timeout=1)

    if return_code:
        print("\nVSW-DIAGNOSE – Fooocus-Prozess wurde beendet.", flush=True)
        print_runtime_diagnosis(
            log_path=log_path,
            local_url=state["local_url"],
            public_url=state["public_url"],
            process=process,
            tunnel=tunnel,
        )
        print("Letzte Logzeilen:\n" + "\n".join(tail[-30:]), flush=True)
        raise RuntimeError(
            f"Fooocus wurde mit Exit {return_code} beendet. Vollständiges Log: {log_path}"
        )
