# Fooocus_extend · VSW Google Colab

Google-Colab-Notebook für **Fooocus_extend** zur Nutzung in Schulungen, Workshops und Demonstrationen.

Das Repository enthält **nicht Fooocus_extend selbst**. Der Programmcode wird beim Start aus dem Originalprojekt [`shaitanzx/Fooocus_extend`](https://github.com/shaitanzx/Fooocus_extend) bezogen.

---

## ▶ Direkt in Google Colab starten

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MlIelAst/Fooocus_Extend_VSW_Colab/blob/main/Fooocus_Extend_VSW_Colab.ipynb)

**Direkter Colab-Link**

```text
https://colab.research.google.com/github/MlIelAst/Fooocus_Extend_VSW_Colab/blob/main/Fooocus_Extend_VSW_Colab.ipynb
```

---

## Wichtige Runtime-Vorgabe

Für diese Schulungsfassung wird **Colab Runtime 2025.07 mit Python 3.11.13** verwendet.

Der Hintergrund: Die aktuelle Fooocus-/Fooocus_extend-Abhängigkeitsbasis ist auf Python 3.11 ausgelegt. Unter Python 3.12 können Installations- und Importfehler auftreten. Das Notebook prüft deshalb die Python-Version **vor** dem langwierigen Fooocus-Start und bricht bei einer ungeeigneten Runtime sofort mit einer verständlichen Anleitung ab.

Wenn Colab die hinterlegte Runtime ausnahmsweise nicht übernimmt:

**Laufzeit → Laufzeittyp ändern → Runtime-Version 2025.07 → GPU/T4**

Google führt Runtime 2025.07 weiterhin als verfügbare vergangene Runtime mit Python 3.11.13.

---

## Was wurde für den Schulungseinsatz verbessert?

- Runtime 2025.07 / Python 3.11 und GPU sind im Notebook hinterlegt.
- Falsche Python-Versionen werden sofort erkannt, bevor lange Installationen starten.
- Fortschrittsphasen und vergangene Zeit werden angezeigt.
- Während längerer Phasen erscheint regelmäßig ein Status-Heartbeat.
- Restzeiten werden als **Richtwert** je Phase angezeigt.
- Der Fooocus-Start läuft ungepuffert, damit Logzeilen möglichst sofort sichtbar sind.
- Das vollständige Startprotokoll wird nach `/content/fooocus_extend_startup.log` geschrieben.
- Bei einem Fehler werden automatisch die letzten Logzeilen und bekannte Fehlerbilder ausgegeben.
- Der doppelte Updater wurde entfernt: Das Notebook synchronisiert den Code selbst und startet danach direkt `launch.py`.
- Der Git-Clone erfolgt flach (`--depth 1`) und spart Zeit.
- Für Schulungen ist standardmäßig ein **getesteter Fooocus_extend-Stand v9.3.5** fixiert.
- Optional kann auf den jeweils aktuellen `main`-Stand umgestellt werden.
- `GoogleDrive_output = False` bleibt der datensparsame Standard.

---

## Typischer Ablauf

1. Notebook öffnen.
2. **▶ Fooocus_extend STARTEN / NEUSTARTEN** ausführen.
3. Falls Paketversionen angepasst werden müssen, startet Colab einmal automatisch neu.
4. Nach der Wiederverbindung dieselbe Zelle erneut ausführen.
5. Fortschritt und aktuelle Phase beobachten.
6. Sobald ein `gradio.live`-Link erscheint, die Oberfläche öffnen.

Beim ersten erfolgreichen Start sind längere Wartezeiten normal, weil Pakete und Modelldateien geladen werden. Die Dauer hängt stark von Colab- und Download-Auslastung ab; deshalb zeigt das Notebook bewusst nur Zeit-Richtwerte und keine scheinpräzise ETA.

---

## Fortschrittsanzeige

Die Prozentwerte zeigen die **Startphase**, nicht den exakten Byte-Fortschritt sämtlicher Downloads:

- **0–20 %** Runtime, GPU, CUDA und Basis-Abhängigkeiten
- **20–35 %** Fooocus_extend bereitstellen
- **35–55 %** Python-Pakete
- **55–90 %** Modelle und Hilfsdateien
- **90–100 %** Weboberfläche und Tunnel

Bei Downloads zeigt Fooocus bzw. pip zusätzlich eigene Fortschrittsangaben, sofern der jeweilige Downloader diese bereitstellt.

---

## Diagnose

Bei Startfehlern wird automatisch ein Diagnoseblock ausgegeben.

Zusätzlich steht das vollständige Protokoll unter:

```text
/content/fooocus_extend_startup.log
```

Wenn Support benötigt wird, reichen in der Regel die **letzten 50–100 Logzeilen** vor dem Diagnoseblock.

---

## Datenhaltung

| Bereich | Standard | Bedeutung |
|---|---|---|
| Notebook | dauerhaft | GitHub bzw. optional eigene Drive-Kopie |
| Fooocus_extend | temporär | `/content/Fooocus_extend` in der Colab-VM |
| Modelle / Downloads | temporär | innerhalb der laufenden Colab-Sitzung |
| Generierte Bilder | temporär | solange `GoogleDrive_output = False` |
| Google-Drive-Ausgabe | aus | bei Aktivierung Speicherung in `MyDrive/outputs` |

> **Notebook dauerhaft · Programmumgebung temporär · Bilder optional dauerhaft**

---

## Sicherheit

- Google Drive nur verbinden, wenn eine dauerhafte Speicherung erforderlich ist.
- Keine Passwörter, Tokens oder API-Keys in Codezellen, Zell-Ausgaben oder ein öffentliches Repository schreiben.
- Keine vertraulichen oder besonders schutzbedürftigen Inhalte für öffentliche Demo-Sitzungen verwenden.
- Den `gradio.live`-Link nicht öffentlich veröffentlichen.
- Nach der Übung: **Laufzeit → Laufzeit trennen und löschen**.

---

## Zwei Notebook-Dateinamen

Aus Kompatibilitätsgründen liegen derzeit zwei Dateinamen im Repository:

- `Fooocus_Extend_VSW_Colab.ipynb` – **kanonische und empfohlene Fassung**
- `Fooocus_extend_VSW_Colab.ipynb` – ältere Schreibweise aus früheren Unterlagen

Für neue Schulungslinks und Dokumentationen bitte ausschließlich die kanonische Fassung mit großem **E** in `Extend` verwenden.

---

## Originalprojekt

- Fooocus_extend: https://github.com/shaitanzx/Fooocus_extend
- Fooocus: https://github.com/lllyasviel/Fooocus

Dieses Repository stellt lediglich die angepasste VSW-Colab-Starthilfe bereit.

---

## Lizenz

Fooocus_extend steht unter der **GNU Affero General Public License v3.0 (AGPL-3.0)**. Siehe [`LICENSE`](LICENSE).
