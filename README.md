# Fooocus_extend · VSW Google Colab

Ein vereinfachtes und für Schulungen vorbereitetes **Google-Colab-Notebook für Fooocus_extend**.

Das Repository enthält **nicht Fooocus_extend selbst**. Beim Start lädt das Notebook den aktuellen Stand des Originalprojekts von [`shaitanzx/Fooocus_extend`](https://github.com/shaitanzx/Fooocus_extend).

---

## ▶ Direkt in Google Colab starten

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MlIelAst/Fooocus_Extend_VSW_Colab/blob/main/Fooocus_Extend_VSW_Colab.ipynb)

**Direkter Teilnehmer-Link:**

```text
https://colab.research.google.com/github/MlIelAst/Fooocus_Extend_VSW_Colab/blob/main/Fooocus_Extend_VSW_Colab.ipynb
```

Diesen Link kannst du direkt an Teilnehmende weitergeben.

---

## ⚠️ Wichtig seit September 2026: Runtime 26.07 verwenden

Google Colab stellt aktuell standardmäßig auf **Python 3.13** um. Fooocus_extend verwendet mehrere ältere Abhängigkeiten, die derzeit unter Python 3.13 nicht zuverlässig installiert werden können.

Darum vor dem ersten Start bitte einmal:

1. In Colab **`Strg + Shift + P`** drücken oder die **Befehlspalette** öffnen.
2. **`Change runtime version` / `Laufzeitversion ändern`** auswählen.
3. **Runtime `26.07`** auswählen. Alternativ funktioniert auch **`26.04`**.
4. Anschließend: **Laufzeit → Laufzeittyp ändern → GPU**.
5. Danach mit **Zelle 1** beginnen.

> Colab speichert die gewählte Runtime-Version derzeit nicht dauerhaft. Bei einer neuen Sitzung muss dieser Schritt ggf. erneut durchgeführt werden.

Das Notebook prüft die Python-Version zusätzlich selbst. Wird Python 3.13 erkannt, verändert es **keine Pakete**, sondern zeigt die obigen Schritte an.

---

## Schnellstart

1. **Notebook öffnen** – oben auf **Open in Colab** klicken.
2. **Runtime 26.07 wählen** – über die Befehlspalette.
3. **GPU aktivieren** – `Laufzeit → Laufzeittyp ändern → GPU`.
4. **Zelle 1 ausführen** – die benötigten Paketversionen werden geprüft und bei Bedarf angepasst.
5. Falls Colab einmal neu startet: kurz warten und danach **Zelle 2 ausführen**.
6. **Gradio-Link öffnen** – am Ende erscheint eine Adresse wie `https://....gradio.live`.

Beim ersten Start kann die Einrichtung länger dauern, weil Modelle und Abhängigkeiten geladen werden.

---

## Was wurde für die VSW-Schulung angepasst?

Das Notebook basiert auf dem Colab-Start von Fooocus_extend, wurde aber für eine möglichst einfache und wiederholbare Schulungsnutzung überarbeitet.

### Python-/Runtime-Prüfung

Das Notebook erkennt den aktuellen Python-Stand der Colab-Sitzung. Python 3.13 wird abgefangen, bevor inkompatible Pakete verändert werden.

### Automatische Vorbereitung

Unter der kompatiblen Python-3.12-Runtime prüft das Notebook die benötigten Versionen von:

- `nvidia-cudnn-cu12`
- `pygit2`
- `numpy`

Weichen diese ab, werden sie angepasst. Anschließend startet Colab einmal neu.

### GPU- und CUDA-Prüfung

Vor dem Start wird geprüft, ob tatsächlich eine NVIDIA-GPU verfügbar ist. Dadurch gibt es bei einer versehentlich gestarteten CPU-Laufzeit eine verständliche Meldung statt eines schwer lesbaren CUDA-Abbruchs.

### Wiederholbarer Start

- vorhandene Fooocus-Prozesse werden vor einem Neustart beendet,
- Fooocus_extend wird nur geklont, wenn es noch nicht vorhanden ist,
- eine vorhandene Installation wird auf den aktuellen `main`-Stand aktualisiert,
- Fehler wie `destination path already exists` werden vermieden.

### Google Drive nur optional

`GoogleDrive_output` ist standardmäßig auf **False** gesetzt.

Dadurch bleiben generierte Bilder zunächst nur in der temporären Colab-Umgebung. Wer Ergebnisse dauerhaft speichern möchte, kann die Option bewusst auf **True** setzen.

### Direkt auswählbar

- Profil: `realistic`, `default` oder `anime`
- helles oder dunkles Theme
- Gradio oder optional Cloudflared
- Memory Patch für Colab-GPUs
- optionales Speichern in Google Drive

---

# Was ist Fooocus_extend?

Fooocus_extend ist ein erweiterter Fork von **Fooocus**. Die Oberfläche bleibt vergleichsweise einfach, ergänzt Fooocus aber um zusätzliche Funktionen für Bildgenerierung und Bildbearbeitung.

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

Für die Schulungsnutzung ist die Trennung der Speicherorte besonders wichtig:

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

Wenn `GoogleDrive_output = True` aktiviert wird, erhält der Notebook-Code Zugriff auf das eingebundene Google Drive. Deshalb:

- Drive nur verbinden, wenn die dauerhafte Speicherung wirklich benötigt wird.
- Nur Notebook-Code aus vertrauenswürdigen Quellen ausführen.
- Keine Passwörter, Tokens oder vertraulichen Daten in Codezellen oder gespeicherten Ausgaben hinterlegen.

## Öffentlicher Gradio-Link

Bei `Tunnel = "gradio"` erzeugt Fooocus einen öffentlichen `gradio.live`-Link.

Dieser Link ist während der laufenden Sitzung über das Internet erreichbar. Deshalb:

- den Link nicht öffentlich posten,
- ihn nur für die jeweilige Sitzung verwenden,
- keine vertraulichen oder besonders sensiblen Daten für öffentliche Demos verwenden,
- die Colab-Laufzeit nach der Übung beenden.

## Nicht in das öffentliche Repository gehören

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

Nach der Übung in Google Colab:

**Laufzeit → Laufzeit trennen und löschen**

Damit wird die aktuelle Colab-VM einschließlich der dort temporär gespeicherten Fooocus-Dateien und Bilder verworfen.

Dateien, die vorher bewusst in Google Drive gespeichert wurden, bleiben dort erhalten und müssen bei Bedarf separat gelöscht werden.

---

# Hinweise für Teilnehmende

- Eine kostenlose Colab-GPU ist nicht jederzeit garantiert verfügbar.
- Colab kann längere oder ressourcenintensive Sitzungen beenden.
- Die Rechenleistung kommt aus der Colab-Cloud; eine leistungsfähige lokale Grafikkarte ist deshalb nicht erforderlich.
- Das Notebook lädt Code und Modelle von externen Projekten. Für produktive oder besonders sensible Daten sollten die jeweils geltenden Datenschutz-, Sicherheits- und Organisationsvorgaben geprüft werden.

---

# Originalprojekt

Fooocus_extend wird von **shaitanzx** entwickelt und basiert auf Fooocus.

- Originalprojekt: https://github.com/shaitanzx/Fooocus_extend
- Original Fooocus: https://github.com/lllyasviel/Fooocus

Dieses Repository ist eine **angepasste Colab-Starthilfe für VSW-Schulungen** und kein Ersatz für die Dokumentation oder das Repository des ursprünglichen Projekts.

---

# Lizenz

Fooocus_extend steht unter der **GNU Affero General Public License v3.0 (AGPL-3.0)**. Dieses angepasste Colab-Notebook wird ebenfalls unter der AGPL-3.0 bereitgestellt. Die Rechte an Fooocus_extend und den darin enthaltenen Komponenten verbleiben bei den jeweiligen Urheberinnen und Urhebern.

Siehe [`LICENSE`](LICENSE).
