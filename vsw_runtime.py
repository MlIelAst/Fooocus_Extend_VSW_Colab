import os
import re
import subprocess
import threading
import time


def classify_runtime_line(line: str):
    low = line.lower()
    if any(x in low for x in ("unchecked runtime.lasterror", "sentry.init", "content.js")):
        return (
            "Browser-Erweiterung",
            "wahrscheinlich externe Browser-Erweiterung; nicht automatisch ein Fooocus-Fehler",
            "Inkognito-Fenster ohne Erweiterungen testen",
        )
    if any(x in low for x in ("404 /run/predict", "failed to parse json", "unexpected token")):
        return (
            "Gradio / Frontend",
            "möglicher UI-, API- oder Erweiterungsfehler",
            "Seite neu laden, Inkognito testen und Standard-Generate ohne Zusatzmodule prüfen",
        )
    if "photopea" in low and any(x in low for x in ("error", "failed", "404", "exception")):
        return (
            "Optionales Modul: Photopea",
            "Zusatzmodul betroffen; Bildgenerierung kann trotzdem funktionieren",
            "Standard-Generate ohne Photopea prüfen",
        )
    return None


def run_fooocus(cmd, cwd, log_path, tunnel, start_time):
    """Run Fooocus and stop the artificial heartbeat once the UI is ready.

    Browser-console-only errors cannot be captured by the Colab process. If matching
    messages do reach stdout/stderr, they are classified here. The README explains
    the client-side limitation explicitly.
    """
    print("$ " + " ".join(map(str, cmd)), flush=True)
    env = os.environ.copy()
    env.update(PYTHONUNBUFFERED="1", PYTHONNOUSERSITE="1", PIP_DISABLE_PIP_VERSION_CHECK="1")

    stop_heartbeat = threading.Event()
    ready = threading.Event()
    local_url = None
    public_url = None
    reported = set()

    def elapsed():
        seconds = int(time.time() - start_time)
        return f"{seconds//60:02d}:{seconds%60:02d}"

    def beat():
        while not stop_heartbeat.wait(20):
            print(f"… läuft weiter | Fooocus starten / Modelle laden | gesamt {elapsed()}", flush=True)

    heartbeat = threading.Thread(target=beat, daemon=True)
    heartbeat.start()

    with log_path.open("a", encoding="utf-8") as log:
        process = subprocess.Popen(
            [str(x) for x in cmd],
            cwd=str(cwd),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        tail = []

        for line in process.stdout:
            print(line, end="", flush=True)
            log.write(line)
            log.flush()
            tail = (tail + [line.rstrip()])[-80:]

            match = re.search(r"Running on local URL:\s*(https?://\S+)", line)
            if match:
                local_url = match.group(1).rstrip(".,)")

            match = re.search(r"Running on public URL:\s*(https?://\S+)", line)
            if match:
                public_url = match.group(1).rstrip(".,)")

            if "trycloudflare.com" in line:
                match = re.search(r"https://[A-Za-z0-9.-]+\.trycloudflare\.com", line)
                if match:
                    public_url = match.group(0)

            should_ready = bool(public_url) if tunnel in ("gradio", "cloudflared") else bool(local_url)
            if should_ready and not ready.is_set():
                ready.set()
                stop_heartbeat.set()
                print("\n" + "═" * 68, flush=True)
                print("[100%] WEBOBERFLÄCHE BEREIT", flush=True)
                print("Fooocus_extend läuft erfolgreich.", flush=True)
                print(f"Lokale URL:      {local_url or 'http://127.0.0.1:7865'}", flush=True)
                print(f"Öffentliche URL: {public_url or 'nicht aktiviert'}", flush=True)
                print(f"Gesamte Startzeit: {elapsed()}", flush=True)
                print("\nHinweis:", flush=True)
                print(
                    "Browser-Konsoleinträge von Erweiterungen werden nicht automatisch als Fooocus-Fehler gewertet.",
                    flush=True,
                )
                print(
                    "Bei UI-Problemen zuerst Inkognito ohne Erweiterungen und anschließend Standard-Generate ohne Zusatzmodule testen.",
                    flush=True,
                )
                print("═" * 68 + "\n", flush=True)

            diag = classify_runtime_line(line)
            if diag:
                signature = (diag[0], line.strip())
                if signature not in reported:
                    reported.add(signature)
                    area, meaning, next_step = diag
                    print("\n[VSW-HINWEIS] Frontend-/Modulmeldung erkannt:", flush=True)
                    print(f"Bereich: {area}", flush=True)
                    print(f"Meldung: {line.strip()[:500]}", flush=True)
                    print(f"Einordnung: {meaning}.", flush=True)
                    print(f"Empfohlener Prüfschritt: {next_step}.", flush=True)

        return_code = process.wait()

    stop_heartbeat.set()
    heartbeat.join(timeout=1)

    if return_code:
        print("\nVSW-DIAGNOSE – Fooocus-Prozess wurde beendet.", flush=True)
        print("\n".join(tail[-30:]), flush=True)
        raise RuntimeError(
            f"Fooocus wurde mit Exit {return_code} beendet. Vollständiges Log: {log_path}"
        )
