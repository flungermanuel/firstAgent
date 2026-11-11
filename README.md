# firstAgent

Ein kleiner Konsolen-Agent auf Basis der Anthropic Messages API mit Tool Use.
Der Agent beantwortet Fragen zu Textdateien in einem Ordner. Dafür ruft er
selbstständig das Tool `find_txt_and_md_files` auf und fasst das Ergebnis auf
Deutsch zusammen. Der Gesprächsverlauf bleibt innerhalb einer Sitzung erhalten.

## Funktionsweise

1. Du stellst eine Frage, z. B. „Welche Textdateien liegen im Ordner notizen?“.
2. Claude entscheidet, ob das Tool gebraucht wird, und liefert den Ordnernamen.
3. `find_txt_and_md_files` listet die `.txt`- und `.md`-Dateien des Ordners.
4. Das Ergebnis geht zurück an Claude, das die Antwort formuliert.

Die Schleife ist auf maximal 5 Runden pro Frage begrenzt.

## Projektstruktur

```
firstAgent/
├── agent.py                   # Agent-Schleife und Konsolen-Chat
├── find_txt_and_md_files.py   # Tool: listet .txt/.md-Dateien eines Ordners
├── notizen/                   # Beispieldaten zum Ausprobieren
├── requirements.txt
├── .env.example
└── README.md
```

## Voraussetzungen

- Python 3.10 oder neuer
- Ein Anthropic-API-Key

## Installation

```bash
python -m venv .venv
# Windows (PowerShell): .venv\Scripts\Activate.ps1
# macOS/Linux:          source .venv/bin/activate
pip install -r requirements.txt
```

Lege eine `.env` nach dem Vorbild von `.env.example` an und trage deinen Key ein:

```
ANTHROPIC_API_KEY=dein-key
```

## Nutzung

```bash
python agent.py
```

Beispiel:

```
Du: Welche Textdateien liegen im Ordner notizen?
```

Beenden mit `exit`, `quit` oder `schließen`.

## Hinweise

- Die `.env` enthält deinen API-Key und ist per `.gitignore` vom Repository ausgeschlossen.
- Das Modell ist in `agent.py` über die Konstante `MODEL` einstellbar.
