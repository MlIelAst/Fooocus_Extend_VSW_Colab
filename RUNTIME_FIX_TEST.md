# VSW Runtime-Fix – Testplan

Arbeitsbranch: `work/runtime-health-cloudflared`

## Ziel

Dieser Branch behebt bzw. diagnostiziert den beobachteten Fehlerpfad:

1. Generierung läuft, z. B. `FaceEnhancer in progress ...`
2. Browser zeigt `Error` / `Reconnect`
3. WebSocket zu `gradio.live/queue/join` bricht ab
4. Nach Reconnect erscheint `Unexpected token '<' ... <!DOCTYPE ... is not valid JSON`

Die neue Schulungsfassung trennt deshalb drei Fehlerklassen:

- Fooocus-Backend / Python-Prozess
- öffentlicher Tunnel / Gradio-WebSocket
- GPU-/VRAM-Probleme

## Änderungen

- Cloudflared ist im Testbranch Standardtunnel.
- Gradio Share bleibt als Fallback auswählbar.
- `Memory_patch` ist auf T4 standardmäßig aus.
- Der Launcher warnt, wenn High-VRAM auf einer Schulungs-T4 aktiviert wird.
- `vsw_runtime.py` prüft lokalen `/config`-Endpunkt, öffentlichen `/config`-Endpunkt und GPU-Status.
- Nach dem Start läuft ein zustandsbasierter Healthcheck; er meldet nur Statuswechsel, nicht permanent Debug-Ausgaben.
- Neue Notebook-Zelle `🩺 VSW-DIAGNOSE` erlaubt eine manuelle Diagnose nach einem Browser-/Generate-Fehler.
- `Unexpected token '<'` wird als typisches Symptom für HTML statt erwarteter JSON-Antwort eingeordnet.

## Colab-Test

Branch-Notebook öffnen:

```text
https://colab.research.google.com/github/MlIelAst/Fooocus_Extend_VSW_Colab/blob/work/runtime-health-cloudflared/Fooocus_Extend_VSW_Colab.ipynb
```

Empfohlener erster Test:

```text
Fooocus_Profile = realistic
Tunnel = cloudflared
Memory_patch = False
GoogleDrive_output = False
Use_latest_main = False
```

In Fooocus zunächst:

- 1 Bild
- Speed
- 896 × 1152 kann bleiben
- ADetailer aus
- Enhance / FaceEnhancer aus

Danach schrittweise:

1. ADetailer aktivieren
2. FaceEnhancer aktivieren
3. 2 Bilder
4. 4 Bilder
5. 6 Bilder

Nach jedem Fehler die Zelle `🩺 VSW-DIAGNOSE` ausführen.

## Erwartete Diagnosebilder

### Tunnelproblem

```text
Fooocus-Prozess: ONLINE
Lokaler /config: OK
Öffentlicher Tunnel: FEHLER
```

Dann Fooocus nicht neu installieren. Tunnel bzw. Sitzung neu aufbauen.

### Backend-/Crashproblem

```text
Fooocus-Prozess: OFFLINE
Lokaler /config: FEHLER
```

Dann Log prüfen auf:

- `CUDA out of memory`
- `OutOfMemoryError`
- `Killed`
- `Traceback`
- `RuntimeError`
- FaceEnhancer-/ADetailer-Fehler

## Vor Merge nach `main`

Vor dem Merge muss im Notebook:

```python
VSW_Code_Ref = "work/runtime-health-cloudflared"
```

an beiden Stellen auf

```python
VSW_Code_Ref = "main"
```

geändert werden.

Erst nach erfolgreichem Colab-Test den Branch mergen.
