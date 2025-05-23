# CSV Unpivot Tool

Ein CLI-Tool zum Transformieren und Kombinieren von CSV-Dateien mit 15-Minuten-Zeitwerten. Die Daten werden gruppiert, normalisiert und nach Datum/Uhrzeit sortiert ausgegeben. Die Ausgabedatei wird bei Erreichen von 8 MB automatisch gesplittet.

Entwickelt von [@dkuester](https://github.com/dkuester).

---

## 📦 Funktionen

- Verarbeitung aller `.csv`-Dateien aus einem angegebenen Verzeichnis
- Umwandlung von 96-Wert-Zeilen in Einträge mit Uhrzeit
- Gruppierung und Pivotierung nach verschiedenen `curve_value_type_id`
- Unterstützung von 9 unterschiedlichen Wertetypen
- Automatische Aufteilung der Ausgabe in mehrere Dateien bei >8 MB
- Sortierte Ausgabe nach Datum und Uhrzeit

---

## 🛠 Unterstützte Wertetypen

| `curve_value_type_id` | Spaltenname            |
|-----------------------|------------------------|
| 1001                  | Alle_Anrufe            |
| 1020                  | Belegung               |
| 1003                  | Annahme                |
| 1021                  | Besetzte               |
| 1023                  | Abfall < 5 Sekunden    |
| 1022                  | Abfall > 5 Sekunden    |
| 1024                  | Annahme < 10 Sekunden  |
| 1026                  | Annahme < 20 Sekunden  |
| 1027                  | Überlauf               |

---

## 📥 Eingabeformat

- Dateien mit `;` als Trennzeichen
- Enthalten 96 Spalten `values.0` bis `values.95`
- Wichtige Felder: `curve_event_type_id`, `curve_id`, `curve_version_id`, `date`, `raster`, `curve_value_type_id`

---

## 📤 Ausgabeformat

- Eine oder mehrere `transformed_1.csv`, `transformed_2.csv`, …
- Spalten:  
  `curve_event_type_id`, `curve_id`, `curve_version_id`, `date`, `raster`, `uhrzeit`  
  plus alle relevanten Wertetypen wie `Alle_Anrufe`, `Annahme`, etc.
- Zeilen mit `wert <= 0` werden ignoriert
- Sortiert nach Datum und Uhrzeit

---

## 🚀 Nutzung

```bash
python csv_unpivot.py --input-dir /pfad/zum/csv-ordner -o transformed.csv
```

## Beispiel:

```
python csv_unpivot.py --input-dir ./daten -o ergebnis.csv
```

→ erzeugt ergebnis_1.csv, ergebnis_2.csv … bei Bedarf

## 🧰 Abhängigkeiten

Nur Standardbibliotheken von Python 3:

- `csv`
- `argparse`
- `os`
- `datetime`
- `collections`
