# CSV Unpivot

Ein Python-CLI-Tool zur Transformation von CSV-Dateien mit Zeitwerten in ein zeilenbasiertes Format, inklusive Pivot und Splitting ab 8 MB Dateigröße.

## Installation

```bash
git clone https://github.com/dkuester/csv-unpivot.git
cd csv-unpivot
pip install -r requirements.txt
```

## Nutzung

```bash
python csv_unpivot.py input1.csv input2.csv -o output.csv
```

## Parameter

- `input1.csv input2.csv ...`
Beliebig viele CSV-Dateien als Eingabe (durch Leerzeichen getrennt)
- `-o`, `--output`
Pfad und Name der Ausgabedatei (Standard: `transformed.csv`). Bei Überschreiten von 8 MB wird automatisch auf `transformed_1.csv`, `transformed_2.csv` usw. gesplittet.

### Beispiel

```bash
python csv_unpivot.py data/januar.csv data/februar.csv -o export/gesamt.csv
```

Erzeugt eine oder mehrere Ausgabedateien unter export/, z. B.:
- `gesamt.csv`
- `gesamt_1.csv`
- `gesamt_2.csv`

### Ausgabeformat

Die Ausgabedateien enthalten folgende Spalten:
- `curve_event_type_id`
- `curve_id`
- `curve_version_id`
- `date`
- `raster`
- `uhrzeit`
- `Alle_Anrufe`
- `Annahme`
