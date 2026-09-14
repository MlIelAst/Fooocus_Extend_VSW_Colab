# Fooocus_extend · VSW Google Colab

Google-Colab-Notebook für **Fooocus_extend** zur Nutzung in Schulungen, Workshops und Demonstrationen.

Das Repository enthält **nicht Fooocus_extend selbst**. Beim Start wird der Programmcode aus dem Originalprojekt [`shaitanzx/Fooocus_extend`](https://github.com/shaitanzx/Fooocus_extend) geladen.

---

## ▶ Direkt in Google Colab starten

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MlIelAst/Fooocus_Extend_VSW_Colab/blob/main/Fooocus_Extend_VSW_Colab.ipynb)

Direkter Link:

```text
https://colab.research.google.com/github/MlIelAst/Fooocus_Extend_VSW_Colab/blob/main/Fooocus_Extend_VSW_Colab.ipynb
```

---

# Robuste VSW-Fassung: isolierte Python-Umgebung

Fooocus_extend benötigt einen anderen Paketstand als die jeweils aktuelle Google-Colab-Systemumgebung. Die VSW-Fassung verändert deshalb **nicht mehr** Colabs vorinstallierte Torch-, CUDA-, cuDNN- oder NumPy-Pakete.

Stattdessen wird automatisch eine eigene Umgebung angelegt:

```text
/content/fooocus_venv
```

Dadurch werden Konflikte wie

```text
torch ... requires nvidia-... but you have ...
opencv-python-headless ... requires numpy>=2 but you have numpy 1.26.4
```

nicht mehr durch globale Paket-Downgrades erzeugt.

---

## Empfohlene Runtime

Für den VSW-Kurs vorgesehen:

- **Colab Runtime 2025.07**
- **Python 3.11**
- **NVIDIA GPU**, bevorzugt T4

Die Metadaten sind im Notebook hinterlegt. Sind Python-Version, GPU oder freier Speicher ungeeignet, bricht der Launcher **vor** der langen Installation verständlich ab.

---

# Start

1. Notebook öffnen.
2. Einstellungen wählen.
3. Auf **▶ Fooocus_extend STARTEN / NEUSTARTEN** klicken.
4. Beim ersten Start die Einrichtung abwarten.
5. Sobald `[100%] WEBOBERFLÄCHE BEREIT` erscheint, den angezeigten `gradio.live`-Link öffnen.

Ein zusätzlicher Kernel-Neustart nur wegen Fooocus-Abhängigkeiten ist in der isolierten Fassung nicht vorgesehen.

---

# Einstellungen im Notebook

Direkt auswählbar:

- `Fooocus_Profile`: `default`, `realistic`, `anime`
- `Fooocus_Theme`: `dark`, `light`
- `Tunnel`: `gradio`, `cloudflared`
- `Memory_patch`
- `GoogleDrive_output`
- `Use_latest_main`
- `Force_rebuild_environment`
- `Civitai_Checkpoints`
- `Civitai_LoRAs`
- `Use_Civitai_Secret`

Empfehlung:

```text
Fooocus_Profile = realistic
Fooocus_Theme = dark
Tunnel = gradio
Memory_patch = True
GoogleDrive_output = False
Use_latest_main = False
Force_rebuild_environment = False
```

---

# Eigene Modelle und LoRAs aus Civitai nutzen

Ja: Modelle und LoRAs von **Civitai** können direkt über den Colab-Code geladen werden. Das ist besonders praktisch, wenn für eine Schulung reproduzierbar immer dieselben Modelle bereitstehen sollen.

Fooocus verwendet standardmäßig folgende Ordner:

```text
/content/Fooocus_extend/models/checkpoints
/content/Fooocus_extend/models/loras
```

Die offizielle Fooocus-Konfiguration verwendet ebenfalls getrennte Checkpoint- und LoRA-Verzeichnisse. In der Oberfläche können diese Dateien anschließend über die Model-/LoRA-Auswahl verwendet werden.

## Welche Modelle sind geeignet?

Für den unkomplizierten Betrieb mit Fooocus sollten bevorzugt verwendet werden:

- **SDXL-Checkpoints** als Base Model
- **SDXL-LoRAs**, die zum verwendeten SDXL-Checkpoint passen

Nicht jedes Modell auf Civitai ist automatisch kompatibel. Insbesondere Modelle für andere Architekturen wie SD 1.5 oder FLUX sollten nicht einfach als SDXL-Base-Model verwendet werden.

Vor dem Download auf Civitai daher prüfen:

1. **Base Model / Architektur**
2. empfohlene Auflösung
3. Trigger-Wörter bei LoRAs
4. empfohlene LoRA-Stärke
5. Lizenz und erlaubte Nutzung
6. ggf. spezielle VAE- oder Scheduler-Hinweise

## Variante A – direkt im VSW-Colab

Im Notebook gibt es jetzt zwei Felder:

```text
Civitai_Checkpoints
Civitai_LoRAs
```

Dort kann entweder eine **Civitai-Version-ID** oder eine direkte Download-URL eingetragen werden.

### Beispiel: ein Checkpoint

```text
123456
```

### Beispiel: mehrere LoRAs

```text
654321;789012
```

### Optional mit eigenem Dateinamen

```text
123456|mein_realismus_modell.safetensors
```

### Direkte URL

```text
https://civitai.com/api/download/models/123456
```

Mehrere Einträge werden mit `;` getrennt.

Der Launcher legt die Dateien automatisch in den richtigen Fooocus-Ordner und startet anschließend die Oberfläche.

## Wo finde ich die Civitai-Version-ID?

Eine Civitai-Modellseite kann mehrere Versionen enthalten. Benötigt wird deshalb nicht nur die Modell-ID, sondern die **Version-ID** der konkret gewünschten Version.

Sie ist häufig in der URL sichtbar, z. B.:

```text
...?modelVersionId=123456
```

oder Bestandteil des konkreten Downloadlinks:

```text
https://civitai.com/api/download/models/123456
```

## Geschützte Downloads / Civitai API Token

Einige Downloads können eine Anmeldung bzw. einen API-Token benötigen.

Den Token **niemals direkt in GitHub oder in das Notebook schreiben**.

Stattdessen in Google Colab unter **Secrets** ein Secret mit dem Namen

```text
CIVITAI_TOKEN
```

anlegen und anschließend

```text
Use_Civitai_Secret = True
```

aktivieren.

Der Launcher liest den Token dann nur aus den Colab Secrets und verwendet ihn für Civitai-Downloads.

## Variante B – Civitai Helper in Fooocus_extend

Fooocus_extend besitzt zusätzlich einen **Civitai Helper**. Wer Modelle lieber direkt über die Weboberfläche verwaltet, kann diesen nach dem Start verwenden.

Für eine Schulung ist die Colab-Konfiguration über Versions-IDs häufig besser reproduzierbar; zum freien Experimentieren ist der Civitai Helper komfortabler.

## Nachträglich Modelle hinzufügen

Wer eine Datei manuell hochlädt, verwendet:

```text
/content/Fooocus_extend/models/checkpoints
```

für vollständige Modelle und

```text
/content/Fooocus_extend/models/loras
```

für LoRAs.

Danach in Fooocus **Refresh All Files** verwenden. Fooocus führt Base Models und LoRAs in getrennten Auswahllisten.

---

# Fortschritt und Zeit-Richtwerte

Der Launcher zeigt sieben Phasen:

1. System prüfen
2. Fooocus-Code bereitstellen
3. isolierte Python-Umgebung vorbereiten
4. PyTorch/CUDA-Pakete in der VENV installieren
5. Fooocus-Abhängigkeiten installieren
6. optionale Dienste und zusätzliche Modelle vorbereiten
7. Fooocus starten und Modelle laden

Während längerer Schritte erscheint regelmäßig ein Heartbeat, z. B.:

```text
… läuft weiter | Fooocus-Abhängigkeiten | gesamt 06:42
```

Die Zeitangaben sind **Richtwerte**, keine exakte ETA. Colab-Auslastung, Paketserver und Modelldownloads können stark schwanken.

Der erste Start kann ungefähr **8–30 Minuten** dauern. Zusätzliche große Civitai-Checkpoints verlängern den Start entsprechend. Ein erneuter Start in derselben Colab-Runtime ist meist deutlich schneller.

---

# Launcher-Optimierung und Fehlererkennung

Der VSW-Launcher beendet die reine Fortschrittsanzeige automatisch, sobald die Weboberfläche erfolgreich bereitsteht. Ab diesem Zeitpunkt wird kein künstlicher „läuft weiter“-Status mehr ausgegeben, sondern ein klarer Bereitschaftsstatus mit Link, Startdauer und Hinweis auf die aktive Sitzung.

Beispiel:

```text
[100%] WEBOBERFLÄCHE BEREIT

Fooocus_extend läuft erfolgreich.
Lokale URL:      http://127.0.0.1:7865
Öffentliche URL: https://xxxx.gradio.live
Gesamte Startzeit: 11:22

Hinweis:
Browser-Konsoleinträge von Erweiterungen werden nicht automatisch als Fooocus-Fehler gewertet.
Bei UI-Problemen zuerst Inkognito ohne Erweiterungen und anschließend Standard-Generate ohne Zusatzmodule testen.
```

Zusätzlich werden typische Meldungen, **soweit sie im Fooocus-/Gradio-Prozesslog auftauchen**, sauberer eingeordnet:

- **Browser-Erweiterungsmeldungen** wie `Unchecked runtime.lastError`, `content.js` oder `Sentry.init` werden nicht automatisch als Fooocus-Fehler bewertet.
- **Gradio-/Frontendfehler** wie `404 /run/predict`, `Failed to parse JSON` oder `Unexpected token` werden als mögliche UI-, API- oder Erweiterungsprobleme markiert.
- **Optionale Modulfehler**, z. B. im Zusammenhang mit Photopea, werden getrennt ausgewiesen, damit erkennbar bleibt, ob nur ein Zusatzmodul oder die eigentliche Bildgenerierung betroffen ist.

Beispiel:

```text
[VSW-HINWEIS] Frontend-/Modulmeldung erkannt:
Bereich: Gradio / Frontend
Meldung: 404 /run/predict
Einordnung: möglicher UI-, API- oder Erweiterungsfehler.
Empfohlener Prüfschritt: Seite neu laden, Inkognito testen und Standard-Generate ohne Zusatzmodule prüfen.
```

## Wichtige technische Grenze

Reine **Browser-Konsoleinträge** entstehen clientseitig im Browser. Der Colab-Launcher kann sie deshalb nicht zuverlässig direkt sehen oder abfangen.

Wenn ein Fehler nur in den Chrome-/Edge-DevTools erscheint, gilt weiterhin:

1. Seite neu laden
2. Inkognito-Fenster ohne Erweiterungen testen
3. Standard-Generate ohne Zusatzmodule prüfen
4. danach erst Photopea, Erweiterungen oder weitere Module aktivieren

Diese Abgrenzung verhindert, dass Browser-Extension-Fehler fälschlich Fooocus zugerechnet werden.

---

# Reproduzierbarer Schulungsstand

Standardmäßig verwendet der Launcher den getesteten Fooocus_extend-Stand:

```text
v9.3.5
Commit: 7d32c923c172644023f77243bd7af4183ecb3737
```

Für Schulungen empfohlen:

```text
Use_latest_main = False
```

Wer bewusst den aktuellen Upstream-Stand testen möchte, kann auf `True` umstellen. Dadurch sinkt die Reproduzierbarkeit.

---

# Was geschieht technisch?

## 1. Vorprüfung

Vor großen Downloads werden Python-Version, NVIDIA-GPU und verfügbarer Speicher geprüft.

## 2. Fooocus-Code

Der Code wird schlank geklont und auf den gewünschten Stand gesetzt.

## 3. Virtuelle Umgebung

Fooocus erhält eine eigene Python-Umgebung:

```text
/content/fooocus_venv
```

Falls das Standardmodul `venv` ausnahmsweise nicht verfügbar sein sollte, fällt der Launcher auf `virtualenv` zurück.

## 4. PyTorch

Innerhalb der isolierten Umgebung wird installiert:

```text
torch 2.1.0
torchvision 0.16.0
CUDA-Wheels 12.1
```

Die systemweiten Colab-Pakete bleiben unangetastet.

## 5. Fooocus-Abhängigkeiten

Danach wird die Upstream-Datei `requirements_versions.txt` innerhalb derselben Umgebung installiert und anschließend mit `pip check` geprüft.

## 6. Zusätzliche Modelle

Optional angegebene Checkpoints und LoRAs werden erst nach der Fooocus-Bereitstellung in die passenden Modellordner geladen.

## 7. Wiederverwendung

Ein erfolgreicher Einrichtungsstand wird unter

```text
/content/fooocus_venv/.vsw_setup.json
```

markiert. Stimmen Code und Requirements weiterhin überein, werden die schweren Installationsschritte bei einem erneuten Start derselben Runtime übersprungen.

---

# Diagnose bei Fehlern

Das vollständige Startprotokoll liegt unter:

```text
/content/fooocus_extend_startup.log
```

Bei einem Fehler werden zusätzlich die letzten Logzeilen und zentrale Versionsinformationen ausgegeben.

---

# Datenhaltung

| Bereich | Standard | Bedeutung |
|---|---|---|
| Notebook | dauerhaft | GitHub bzw. optional eigene Drive-Kopie |
| Fooocus-Code | temporär | `/content/Fooocus_extend` |
| isolierte Python-Umgebung | temporär | `/content/fooocus_venv` |
| Modelle / Downloads | temporär | Colab-VM |
| generierte Bilder | temporär | Standard ohne Drive |
| Google-Drive-Ausgabe | aus | nur bei `GoogleDrive_output = True` dauerhaft |

> **Notebook dauerhaft · Programmumgebung temporär · Bilder optional dauerhaft**

---

# Google Drive

`GoogleDrive_output = False` ist absichtlich der Standard.

Nur wenn eine dauerhafte Speicherung benötigt wird, `GoogleDrive_output = True` setzen. Dann wird `MyDrive/outputs` verwendet.

---

# Öffentlicher Gradio-Link

Bei `Tunnel = "gradio"` entsteht ein temporärer öffentlicher `gradio.live`-Link.

Daher:

- Link nicht öffentlich veröffentlichen,
- nur für die jeweilige Sitzung verwenden,
- keine vertraulichen Inhalte für öffentliche Demos laden,
- Sitzung nach dem Workshop beenden.

---

# Sicherheit

Nicht in Notebook, öffentliche Ausgaben oder Repository schreiben:

- Passwörter
- API-Keys
- Tokens
- vertrauliche Unternehmensdaten
- nicht freigegebene personenbezogene Bilder
- interne Dokumente
- sensible Outputs

Bei Civitai-Modellen zusätzlich vor dem Einsatz Lizenz, Herkunft und Modellbeschreibung prüfen. Modelle und LoRAs sind ausführbarer ML-Inhalt im weiteren Sinne und sollten nur aus vertrauenswürdigen Quellen bezogen werden. Wenn möglich `.safetensors` bevorzugen.

---

# Sitzung beenden

Nach der Übung:

**Laufzeit → Laufzeit trennen und löschen**

Dadurch werden Fooocus-Code, virtuelle Umgebung, temporär geladene Modelle und temporär gespeicherte Bilder verworfen. In Google Drive gespeicherte Dateien bleiben erhalten und müssen bei Bedarf separat gelöscht werden.

---

# Fooocus_extend

Fooocus_extend erweitert Fooocus u. a. um Funktionen für:

- Text-to-Image
- Modelle und LoRAs
- OneButtonPrompt
- Prompt Translate
- InstantID
- FaceEnhancer
- Inpaint / Eraser
- Outpaint mit Zielauflösung
- ControlNet / OpenPose
- ADetailer
- Omost
- Image Batch
- Prompt Batch
- X/Y/Z Plot
- Remove Background
- Cleaner
- Civitai Helper
- TextMask
- Vector / SVGcode
- Photopea

Die jeweils aktuelle technische Funktionsbeschreibung befindet sich im Originalprojekt.

---

# Originalprojekt

- Fooocus_extend: https://github.com/shaitanzx/Fooocus_extend
- Fooocus: https://github.com/lllyasviel/Fooocus

Dieses Repository stellt eine angepasste Colab-Starthilfe für VSW-Schulungen und Workshops bereit.

---

# Lizenz

Fooocus_extend steht unter der **GNU Affero General Public License v3.0 (AGPL-3.0)**.

Siehe [`LICENSE`](LICENSE).
