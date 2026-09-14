# Fooocus_extend · VSW Google Colab

Google-Colab-Notebook für **Fooocus_extend** zur Nutzung in Schulungen, Workshops und Demonstrationen.

Das Repository enthält **nicht Fooocus_extend selbst**. Beim Start lädt das Notebook automatisch den aktuellen Stand des Originalprojekts von [`shaitanzx/Fooocus_extend`](https://github.com/shaitanzx/Fooocus_extend).

---

## ▶ Direkt in Google Colab starten

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MlIelAst/Fooocus_Extend_VSW_Colab/blob/main/Fooocus_Extend_VSW_Colab.ipynb)

**Direkter Colab-Link:**

```text
https://colab.research.google.com/github/MlIelAst/Fooocus_Extend_VSW_Colab/blob/main/Fooocus_Extend_VSW_Colab.ipynb
```

---

## ✅ Runtime und GPU sind bereits hinterlegt

Das Notebook ist auf **Colab Runtime 2025.07 (Python 3.11)** und eine **T4-GPU** ausgelegt.

Im Normalfall ist keine manuelle Auswahl unter **Laufzeit → Laufzeittyp ändern** erforderlich.

### Ablauf

1. Notebook öffnen.
2. **▶ Fooocus_extend STARTEN / NEUSTARTEN** ausführen.
3. Beim allerersten Start die automatische Wiederverbindung von Colab abwarten.
4. Dieselbe Start-Zelle erneut ausführen.
5. Den anschließend angezeigten `gradio.live`-Link öffnen.

> Falls Colab die hinterlegte Runtime oder GPU ausnahmsweise nicht bereitstellt, zeigt das Notebook eine verständliche Fehlermeldung mit dem manuellen Ersatzweg an.

Beim ersten Start kann die Einrichtung etwas länger dauern, da Abhängigkeiten und Modelle geladen werden.

---

## Anpassungen für den Schulungseinsatz

Das Notebook basiert auf dem Colab-Start von Fooocus_extend und wurde für einen möglichst einfachen, wiederholbaren und verständlichen Einsatz angepasst.

### Runtime und GPU automatisch vorgegeben

Das Notebook fordert direkt **Runtime 2025.07** und eine **T4-GPU** an. Dadurch entfällt im Regelfall die manuelle Konfiguration der Laufzeit.

### Automatische Vorbereitung

Die Start-Zelle prüft automatisch die benötigten Versionen von:

- `nvidia-cudnn-cu12`
- `pygit2`
- `numpy`

Weichen die Versionen beim ersten Start ab, werden sie automatisch angepasst. Anschließend verbindet sich Colab einmal neu.

### GPU- und CUDA-Prüfung

Vor dem Start wird geprüft, ob tatsächlich eine NVIDIA-GPU verfügbar ist. Dadurch erscheint bei einer CPU-Laufzeit eine verständliche Meldung statt eines schwer lesbaren CUDA-Abbruchs.

### Wiederholbarer Start

- vorhandene Fooocus-Prozesse werden vor einem Neustart beendet,
- Fooocus_extend wird nur geklont, wenn es noch nicht vorhanden ist,
- eine vorhandene Installation wird auf den aktuellen `main`-Stand aktualisiert,
- typische Fehler wie `destination path already exists` werden vermieden.

### Google Drive nur optional

`GoogleDrive_output` ist standardmäßig auf **False** gesetzt.

Dadurch bleiben generierte Bilder zunächst nur in der temporären Colab-Umgebung. Für eine dauerhafte Speicherung kann die Option bewusst auf **True** gesetzt werden.

### Direkt auswählbare Einstellungen

- Profil: `realistic`, `default` oder `anime`
- helles oder dunkles Theme
- Gradio oder optional Cloudflared
- Memory Patch für Colab-GPUs
- optionales Speichern in Google Drive

---

# Was ist Fooocus_extend?

Fooocus_extend ist ein erweiterter Fork von **Fooocus**. Die Oberfläche bleibt vergleichsweise einfach, ergänzt Fooocus aber um zahlreiche zusätzliche Funktionen für Bildgenerierung und Bildbearbeitung.

## Bildgenerierung

**Prompt & Negative Prompt**  
Im Prompt wird beschrieben, was erzeugt werden soll. Im Negative Prompt können unerwünschte Merkmale ausgeschlossen werden.

**Modelle und LoRAs**  
Eigene Checkpoints und LoRAs können geladen und kombiniert werden. LoRA-Gewichtung und Trigger-Wörter lassen sich direkt verwenden.

**OneButtonPrompt**  
Erzeugt automatisch neue Prompts oder Variationen eines bestehenden Prompts.

**Prompt Translate**  
Übersetzt positive und negative Prompts und erleichtert die Arbeit mit englischsprachigen Bildmodellen.

## Personen und Gesichter

**InstantID**  
Erzeugt Bilder auf Basis eines Referenzgesichts. Optional kann zusätzlich eine Pose vorgegeben werden.

**FaceEnhancer**  
Verbessert Gesichter, kann hochskalieren und bietet Funktionen zur Gesichtsbearbeitung bzw. zum Face Swap.

> **Hinweis:** Referenzbilder realer Personen nur verwenden, wenn dies rechtlich und organisatorisch zulässig ist. Keine vertraulichen oder besonders sensiblen Personenbilder in eine öffentliche Demo hochladen.

## Bearbeiten und kontrollieren

**Inpaint**  
Markierte Bereiche eines Bildes gezielt neu erzeugen oder verändern.

**Outpaint**  
Ein Bild über seine ursprünglichen Grenzen hinaus erweitern. Fooocus_extend unterstützt dabei auch eine Zielauflösung.

**ADetailer**  
Erkennt beispielsweise Gesichter oder andere Objekte und kann diese automatisch gezielt nachbearbeiten.

**ControlNet**  
Unter anderem verfügbar:

- OpenPose – Körperhaltung bzw. Pose übernehmen
- Recolor – Farbgebung beeinflussen
- Scribble – aus einer Skizze ein Bild entwickeln
- Manga Recolor – Graustufen-Animebilder kolorieren

**OpenPoseEditor**  
Posen bzw. Skelettstrukturen bearbeiten und anschließend als Vorlage verwenden.

## Weitere nützliche Erweiterungen

**Omost** – unterstützt komplexere Bildkompositionen.  
**Image Batch** – mehrere Bilder nacheinander verarbeiten oder als Referenzen einsetzen.  
**Prompt Batch** – mehrere Prompts automatisch nacheinander generieren lassen.  
**X/Y/Z Plot** – unterschiedliche Modelle, Sampler, Steps, CFG- oder LoRA-Einstellungen vergleichen.  
**Remove Background** – Bildhintergründe entfernen.  
**Cleaner** – unerwünschte Bild- oder Videoelemente anhand einer Maske entfernen.  
**Civitai Helper** – Modelle und LoRAs von Civitai finden, prüfen und herunterladen.  
**TextMask** – Text und passende Masken für Inpainting oder ControlNet erzeugen.  
**Vector / SVGcode** – geeignete Rastergrafiken in Vektorgrafiken umwandeln.  
**Photopea** – browserbasierte Bildbearbeitung.

Die vollständige und jeweils aktuelle Funktionsbeschreibung befindet sich im Originalprojekt.

---

# Datenhaltung und Sicherheit

Für die Nutzung in Schulungen ist die Trennung der Speicherorte besonders wichtig:

| Bereich | Standard | Was passiert? |
|---|---|---|
| **Notebook** | dauerhaft | Liegt auf GitHub bzw. optional als Kopie im eigenen Google Drive. |
| **Fooocus_extend-Installation** | temporär | Wird unter `/content/Fooocus_extend` in der Colab-VM eingerichtet. |
| **Modelle / temporäre Downloads** | temporär | Liegen in der Colab-Laufzeit und werden mit der Runtime verworfen. |
| **Generierte Bilder** | temporär | Standardmäßig innerhalb der Colab-VM. |
| **Google-Drive-Ausgabe** | aus | Erst bei `GoogleDrive_output = True` werden Bilder dauerhaft in `MyDrive/outputs` gespeichert. |

> **Notebook dauerhaft · Programmumgebung temporär · Bilder optional dauerhaft**

## Google Drive

Google Drive wird **nicht automatisch** verbunden.

Wenn `GoogleDrive_output = True` aktiviert wird, erhält der Notebook-Code Zugriff auf das eingebundene Google Drive. Daher gelten folgende Grundsätze:

- Drive nur verbinden, wenn eine dauerhafte Speicherung erforderlich ist.
- Nur Notebook-Code aus vertrauenswürdigen Quellen ausführen.
- Keine Passwörter, Tokens oder vertraulichen Daten in Codezellen oder gespeicherten Ausgaben hinterlegen.

## Öffentlicher Gradio-Link

Bei `Tunnel = "gradio"` erzeugt Fooocus einen öffentlichen `gradio.live`-Link.

Dieser Link ist während der laufenden Sitzung über das Internet erreichbar. Daher:

- den Link nicht öffentlich veröffentlichen,
- ihn nur für die jeweilige Sitzung verwenden,
- keine vertraulichen oder besonders sensiblen Daten für öffentliche Demos verwenden,
- die Colab-Laufzeit nach der Übung beenden.

## Nicht in ein öffentliches Repository gehören

- Passwörter
- API-Keys
- Tokens
- personenbezogene Referenzbilder
- generierte Bilder mit sensiblen Inhalten
- vertrauliche Unternehmensdaten
- interne Dokumente
- eigene Modelle oder LoRAs, sofern deren Veröffentlichung nicht ausdrücklich vorgesehen ist

---

# Sitzung sicher beenden

Nach der Nutzung in Google Colab:

**Laufzeit → Laufzeit trennen und löschen**

Damit wird die aktuelle Colab-VM einschließlich der dort temporär gespeicherten Fooocus-Dateien und Bilder verworfen.

Dateien, die zuvor bewusst in Google Drive gespeichert wurden, bleiben dort erhalten und müssen bei Bedarf separat gelöscht werden.

---

# Hinweise

- Das Notebook fordert automatisch **Runtime 2025.07** und eine **T4-GPU** an.
- Eine kostenlose Colab-GPU ist trotzdem nicht jederzeit garantiert verfügbar.
- Colab kann längere oder ressourcenintensive Sitzungen beenden.
- Die Rechenleistung kommt aus der Colab-Cloud; eine leistungsfähige lokale Grafikkarte ist deshalb nicht erforderlich.
- Das Notebook lädt Code und Modelle von externen Projekten. Für produktive oder besonders sensible Daten sind die jeweils geltenden Datenschutz-, Sicherheits- und Organisationsvorgaben zu beachten.

---

# Originalprojekt

Fooocus_extend wird von **shaitanzx** entwickelt und basiert auf Fooocus.

- Originalprojekt: https://github.com/shaitanzx/Fooocus_extend
- Original Fooocus: https://github.com/lllyasviel/Fooocus

Dieses Repository stellt eine **angepasste Colab-Starthilfe für VSW-Schulungen und Workshops** bereit. Die technische Dokumentation und die jeweils aktuellen Funktionen von Fooocus_extend befinden sich im Originalprojekt.

---

# Lizenz

Fooocus_extend steht unter der **GNU Affero General Public License v3.0 (AGPL-3.0)**. Dieses angepasste Colab-Notebook wird ebenfalls unter der AGPL-3.0 bereitgestellt. Die Rechte an Fooocus_extend und den darin enthaltenen Komponenten verbleiben bei den jeweiligen Urheberinnen und Urhebern.

Siehe [`LICENSE`](LICENSE).
