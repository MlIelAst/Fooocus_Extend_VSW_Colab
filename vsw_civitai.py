import os
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path


def _safe_name(name: str) -> str:
    name = Path(name).name.strip().replace("\x00", "")
    return re.sub(r"[^A-Za-z0-9._()\- +]", "_", name) or "download.safetensors"


def _filename_from_headers(headers, fallback: str) -> str:
    cd = headers.get("Content-Disposition", "")
    m = re.search(r"filename\*=UTF-8''([^;]+)", cd, re.I)
    if m:
        return _safe_name(urllib.parse.unquote(m.group(1)))
    m = re.search(r'filename="?([^";]+)"?', cd, re.I)
    if m:
        return _safe_name(m.group(1))
    return _safe_name(fallback)


def _parse_specs(raw: str):
    return [x.strip() for x in re.split(r"[;\n]+", raw or "") if x.strip()]


def download_extra_models(raw: str, target_dir: Path, label: str) -> None:
    """Download Civitai model versions or direct HTTP(S) files.

    Supported item syntax, separated by semicolons/newlines:
      123456
      123456|custom_name.safetensors
      https://civitai.com/api/download/models/123456
      https://example.org/model.safetensors|custom_name.safetensors

    For protected Civitai downloads, set CIVITAI_TOKEN in the environment.
    """
    specs = _parse_specs(raw)
    if not specs:
        return

    target_dir.mkdir(parents=True, exist_ok=True)
    token = os.getenv("CIVITAI_TOKEN", "").strip()
    print(f"\nZusätzliche {label}: {len(specs)} Download(s)", flush=True)

    for i, spec in enumerate(specs, 1):
        value, sep, explicit_name = spec.partition("|")
        value = value.strip()
        explicit_name = explicit_name.strip() if sep else ""

        if value.isdigit():
            url = f"https://civitai.com/api/download/models/{value}"
            fallback = f"civitai_{value}.safetensors"
        elif value.startswith(("https://", "http://")):
            url = value
            fallback = Path(urllib.parse.urlparse(url).path).name or f"{label.lower()}_{i}.safetensors"
        else:
            raise RuntimeError(
                f"Ungültiger {label}-Eintrag: {spec!r}. "
                "Erwartet wird eine Civitai-Version-ID oder direkte HTTP(S)-URL."
            )

        headers = {"User-Agent": "VSW-Fooocus-Colab/1.0"}
        if token and "civitai.com" in urllib.parse.urlparse(url).netloc:
            headers["Authorization"] = f"Bearer {token}"

        print(f"[{i}/{len(specs)}] {label}: {value}", flush=True)
        req = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                final_url = resp.geturl()
                filename = _safe_name(explicit_name) if explicit_name else _filename_from_headers(
                    resp.headers,
                    Path(urllib.parse.urlparse(final_url).path).name or fallback,
                )
                if not Path(filename).suffix:
                    filename += ".safetensors"

                dest = target_dir / filename
                tmp = dest.with_suffix(dest.suffix + ".part")
                total = resp.headers.get("Content-Length")
                total = int(total) if total and total.isdigit() else None
                got = 0
                last_print = time.time()

                with tmp.open("wb") as fh:
                    while True:
                        chunk = resp.read(1024 * 1024)
                        if not chunk:
                            break
                        fh.write(chunk)
                        got += len(chunk)
                        if time.time() - last_print > 5:
                            if total:
                                print(f"  {got/1024**2:.0f}/{total/1024**2:.0f} MB", flush=True)
                            else:
                                print(f"  {got/1024**2:.0f} MB", flush=True)
                            last_print = time.time()

                if got < 1024 * 1024:
                    tmp.unlink(missing_ok=True)
                    raise RuntimeError("Download ist ungewöhnlich klein; möglicherweise Login/Token erforderlich.")

                tmp.replace(dest)
                print(f"  ✓ gespeichert: {dest.name} ({got/1024**2:.0f} MB)", flush=True)

        except Exception as exc:
            raise RuntimeError(
                f"{label}-Download fehlgeschlagen: {value}\n"
                f"Ziel: {target_dir}\n"
                "Hinweis: Bei zugriffsbeschränkten Civitai-Modellen das Colab-Secret "
                "'CIVITAI_TOKEN' verwenden.\n"
                f"Ursache: {exc}"
            ) from exc
