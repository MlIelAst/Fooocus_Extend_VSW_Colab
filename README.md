# Fooocus_extend · VSW Google Colab

Ein vereinfachtes und für Schulungen vorbereitetes **Google-Colab-Notebook für Fooocus_extend**.

Der Schwerpunkt liegt auf einem möglichst einfachen Start, einer reproduzierbaren Colab-Umgebung und einer klaren Trennung zwischen **dauerhaftem Notebook**, **temporärer Programmumgebung** und **optional gespeicherten Bildern**.

> Dieses Repository enthält **nicht Fooocus_extend selbst**. Das Notebook lädt beim Start den aktuellen Stand des Originalprojekts von [`shaitanzx/Fooocus_extend`](https://github.com/shaitanzx/Fooocus_extend).

---

## ▶ Direkt in Google Colab starten

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MlIelAst/Fooocus_Extend_VSW_Colab/blob/main/Fooocus_Extend_VSW_Colab.ipynb)

**Direkter Teilnehmer-Link:**

```text
https://colab.research.google.com/github/MlIelAst/Fooocus_Extend_VSW_Colab/blob/main/Fooocus_Extend_VSW_Colab.ipynb
```

Diesen Link kannst du direkt an Teilnehmende weitergeben.

---

## Schnellstart

1. **Notebook öffnen** – oben auf **Open in Colab** klicken.
2. **GPU aktivieren** – in Colab: `Laufzeit → Laufzeittyp ändern → GPU`.
3. **Vorbereitung ausführen** – **Zelle 1** starten. Benötigte Paketversionen werden geprüft und bei Bedarf angepasst.
4. **Nach dem automatischen Neustart Zelle 2 ausführen** – Fooocus_extend wird installiert bzw. aktualisiert und gestartet.
5. **Gradio-Link öffnen** – am Ende erscheint eine Adresse wie `https://....gradio.live`. Diese im Browser öffnen.

Beim allerersten Start kann die Einrichtung etwas länger dauern, weil Modelle und Abhängigkeiten geladen werden.

---

## Was wurde für die VSW-Schulung angepasst?

Das Notebook basiert auf dem Colab-Start von Fooocus_extend, wurde aber für eine möglichst einfache und wiederholbare Schulungsnutzung überarbeitet.

### Automatische Vorbereitung

Das Notebook prüft die für Fooocus_extend derzeit benötigten Versionen von:

- `nvidia-cudnn-cu12`
- `pygit2`
- `numpy`

Weichen die Versionen in Colab ab, werden sie automatisch angepasst. Anschließend startet Colab einmal neu.

### GPU- und CUDA-Prüfung

Vor dem Start wird geprüft, ob tatsächlich eine NVIDIA-GPU verfügbar ist. Dadurch erscheint bei einer versehentlich gestarteten CPU-Laufzeit eine verständliche Fehlermeldung statt eines schwer lesbaren CUDA-Abbruchs.

### Sauberer Neustart

Bei erneutem Ausführen werden vorhandene Fooocus-Prozesse beendet. Das verhindert Konflikte, wenn die Anwendung innerhalb derselben Colab-Sitzung neu gestartet wird.

### Installation und Updates

- Ist Fooocus_extend noch nicht vorhanden, wird es automatisch installiert.
- Ist es bereits vorhanden, wird der Programmcode auf den aktuellen `main`-Stand des Originalprojekts aktualisiert.
- Der frühere Fehler `destination path already exists` wird dadurch vermieden.

### Google Drive nur optional

`GoogleDrive_output` ist standardmäßig auf **False** gesetzt.

Dadurch bleiben generierte Bilder zunächst nur in der temporären Colab-Umgebung. Wer Ergebnisse dauerhaft speichern möchte, kann die Option bewusst auf **True** setzen.

### Profile und Oberfläche

Direkt in der Startzelle auswählbar:

- `realistic`
- `default`
- `anime`
- helles oder dunkles Theme
- Gradio oder optional Cloudflared
- Memory Patch für Colab-GPUs
- optionales Speichern in Google Drive

---

# Was ist Fooocus_extend?

Fooocus_extend ist ein erweiterter Fork von **Fooocus**. Die Oberfläche bleibt vergleichsweise einfach, ergänzt Fooocus aber um zahlreiche zusätzliche Funktionen für Bildgenerierung und Bildbearbeitung. Die folgenden Funktionen stammen aus dem Originalprojekt und können sich mit zukünftigen Updates verändern. fileciteturn36file0

## Bildgenerierung

**Prompt & Negative Prompt**  
Beschreibe im Prompt, was erzeugt werden soll. Im Negative Prompt können unerwünschte Merkmale ausgeschlossen werden.

**Modelle und LoRAs**  
Eigene Checkpoints und LoRAs können geladen und kombiniert werden. Bei LoRAs lassen sich unter anderem Gewichtung und Trigger-Wörter verwenden.

**OneButtonPrompt**  
Hilft dabei, automatisch neue Prompts oder Variationen eines bestehenden Prompts zu erzeugen.

**Prompt Translate**  
Kann positive und negative Prompts übersetzen und so die Arbeit mit englischsprachigen Bildmodellen erleichtern.

---

## Personen und Gesichter

**InstantID**  
Erzeugt Bilder auf Basis eines Referenzgesichts. Optional kann zusätzlich eine Pose vorgegeben werden.

**FaceEnhancer**  
Verbessert Gesichter, kann hochskalieren und bietet Funktionen zur Gesichtsbearbeitung bzw. zum Face Swap.

> **Hinweis für Schulungen:** Referenzbilder realer Personen nur verwenden, wenn dies rechtlich und organisatorisch zulässig ist. Keine vertraulichen oder besonders sensiblen Personenbilder in eine öffentliche Demo hochladen.

---

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

---

## Nützliche Erweiterungen

**Omost**  
Unterstützt komplexere Bildkompositionen und beschreibt einzelne Bildbereiche strukturiert.

**Image Batch**  
Mehrere Bilder nacheinander verarbeiten, skalieren oder als Referenzen einsetzen.

**Prompt Batch**  
Mehrere Prompts automatisch nacheinander generieren lassen.

**X/Y/Z Plot**  
Vergleicht unterschiedliche Einstellungen in einem Raster – beispielsweise Modelle, Sampler, Steps, CFG oder LoRAs.

**Remove Background**  
Entfernt Bildhintergründe und unterstützt verschiedene Freistellungsmodelle.

**Cleaner**  
Entfernt kleinere unerwünschte Bild- oder Videoelemente anhand einer Maske.

**Civitai Helper**  
Unterstützt beim Finden, Prüfen und Herunterladen kompatibler Modelle und LoRAs von Civitai.

**TextMask**  
Erstellt Text und dazu passende Masken, die anschließend beispielsweise für Inpainting oder ControlNet verwendet werden können.

**Vector / SVGcode**  
Unterstützt die Umwandlung geeigneter Rastergrafiken in Vektorgrafiken.

**Photopea**  
Bindet eine browserbasierte Bildbearbeitung ein.

---

# Datenhaltung und Sicherheit

Für die Schulungsnutzung ist die Trennung der Speicherorte besonders wichtig:

| Bereich | Standard | Was passiert? |
|---|---|---|
| **Notebook** | dauerhaft | Liegt auf GitHub bzw. optional als Kopie im eigenen Google Drive. |
| **Fooocus_extend-Installation** | temporär | Wird unter `/content/Fooocus_extend` in der Colab-VM eingerichtet. |
| **Modelle / temporäre Downloads** | temporär | Liegen in der Colab-Laufzeit und verschwinden mit der gelöschten Runtime. |
| **Generierte Bilder** | temporär | Standardmäßig innerhalb der Colab-VM. |
| **Google-Drive-Ausgabe** | aus | Erst bei `GoogleDrive_output = True` werden Bilder dauerhaft in `MyDrive/outputs` gespeichert. |

Kurz gesagt:

> **Notebook dauerhaft · Programmumgebung temporär · Bilder optional dauerhaft**

## Google Drive

Google Drive wird **nicht automatisch** verbunden. Das ist bewusst so gewählt.

Wenn `GoogleDrive_output = True` aktiviert wird, erhält der Notebook-Code Zugriff auf das eingebundene Google Drive. Deshalb:

- Drive nur verbinden, wenn die dauerhafte Speicherung wirklich benötigt wird.
- Keine Zugangsdaten oder vertraulichen Dateien unnötig in der gemounteten Umgebung verwenden.
- Nur Notebook-Code aus vertrauenswürdigen Quellen ausführen.

## Öffentlicher Gradio-Link

Bei der Standardoption `Tunnel = "gradio"` erzeugt Fooocus einen öffentlichen `gradio.live`-Link.

Dieser Link ist während der laufenden Sitzung über das Internet erreichbar. Deshalb:

- Link nicht öffentlich posten.
- Nur an die Person weitergeben, die die jeweilige Sitzung benutzt.
- Keine vertraulichen oder besonders sensiblen Daten für öffentliche Demonstrationen verwenden.
- Nach der Übung die Colab-Laufzeit beenden.

## Keine Geheimnisse ins Notebook

Nicht in das öffentliche GitHub-Repository oder gespeicherte Notebook-Ausgaben schreiben:

- Passwörter
- API-Keys
- Tokens
- personenbezogene Referenzbilder
- vertrauliche Unternehmensdaten
- interne Dokumente

Falls beispielsweise ein Civitai-API-Key benötigt wird, sollte dieser nicht fest in das veröffentlichte Notebook eingetragen werden.

---

# Sitzung sicher beenden

Nach der Übung in Google Colab:

**Laufzeit → Laufzeit trennen und löschen**

Damit wird die aktuelle Colab-VM einschließlich der dort temporär gespeicherten Fooocus-Dateien und Bilder verworfen.

Dateien, die vorher bewusst in Google Drive gespeichert wurden, bleiben selbstverständlich dort erhalten und müssen bei Bedarf separat gelöscht werden.

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
