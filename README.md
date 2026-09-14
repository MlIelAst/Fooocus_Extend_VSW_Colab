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

# Neue robuste VSW-Fassung: isolierte Python-Umgebung

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
2. Auf **▶ Fooocus_extend STARTEN / NEUSTARTEN** klicken.
3. Beim ersten Start die Einrichtung abwarten.
4. Den anschließend angezeigten `gradio.live`-Link öffnen.

Ein zusätzlicher Kernel-Neustart nur wegen Fooocus-Abhängigkeiten ist in der neuen isolierten Fassung nicht mehr vorgesehen.

---

# Fortschritt und Zeit-Richtwerte

Der Launcher zeigt sieben Phasen:

1. System prüfen
2. Fooocus-Code bereitstellen
3. isolierte Python-Umgebung vorbereiten
4. PyTorch/CUDA-Pakete in der VENV installieren
5. Fooocus-Abhängigkeiten installieren
6. optionale Dienste vorbereiten
7. Fooocus starten und ggf. Modelle laden

Während längerer Schritte erscheint regelmäßig ein Heartbeat, z. B.:

```text
… läuft weiter | Fooocus-Abhängigkeiten | gesamt 06:42
```

Die Zeitangaben sind **Richtwerte**, keine exakte ETA. Colab-Auslastung, Paketserver und Modelldownloads können stark schwanken.

Der erste Start kann ungefähr **8–30 Minuten** dauern. Ein erneuter Start in derselben Colab-Runtime ist meist deutlich schneller.

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

# Einstellungen im Notebook

Direkt auswählbar:

- `Fooocus_Profile`: `default`, `realistic`, `anime`
- `Fooocus_Theme`: `dark`, `light`
- `Tunnel`: `gradio`, `cloudflared`
- `Memory_patch`
- `GoogleDrive_output`
- `Use_latest_main`
- `Force_rebuild_environment`

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

## 6. Wiederverwendung

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

Bei einem Fehler werden zusätzlich die letzten Logzeilen und zentrale Versionsinformationen ausgegeben. Damit ist ein Fehler wesentlich besser einzuordnen als ein alleiniger `CalledProcessError`.

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

---

# Sitzung beenden

Nach der Übung:

**Laufzeit → Laufzeit trennen und löschen**

Dadurch werden Fooocus-Code, virtuelle Umgebung und temporär gespeicherte Bilder verworfen. In Google Drive gespeicherte Dateien bleiben erhalten und müssen bei Bedarf separat gelöscht werden.

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
