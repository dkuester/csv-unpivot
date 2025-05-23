import csv
import argparse
import os
from datetime import datetime, timedelta
from collections import defaultdict

# Mapping für die Wertetypen
VALUE_TYPE_MAP = {
    '1001': 'Alle_Anrufe',
    '1020': 'Belegung',
    '1003': 'Annahme',
    '1021': 'Besetzte',
    '1023': 'Abfall < 5 Sekunden',
    '1022': 'Abfall > 5 Sekunden',
    '1024': 'Annahme < 10 Sekunden',
    '1026': 'Annahme < 20 Sekunden',
    '1027': 'Überlauf',
}

def parse_arguments():
    parser = argparse.ArgumentParser(description='Transformiere und kombiniere CSV-Dateien aus einem Ordner.')
    parser.add_argument('--input-dir', required=True, help='Pfad zum Eingabe-Ordner mit CSV-Dateien')
    parser.add_argument('-o', '--output', default='transformed.csv', help='Pfad zur Ausgabedatei')
    return parser.parse_args()

def minutes_to_time(index):
    return (datetime(1900, 1, 1) + timedelta(minutes=15 * index)).strftime('%H:%M')

def read_and_transform_csv(filepath):
    transformed_rows = []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            base_data = {
                'curve_event_type_id': row['curve_event_type_id'],
                'curve_id': row['curve_id'],
                'curve_version_id': row['curve_version_id'],
                'date': row['date'],
                'raster': row['raster'],
                'curve_value_type_id': row['curve_value_type_id'],
            }
            for i in range(96):
                value_str = row.get(f'values.{i}', '').strip()
                if value_str == '' or float(value_str) <= 0:
                    continue
                base_data_copy = base_data.copy()
                base_data_copy['uhrzeit'] = minutes_to_time(i)
                base_data_copy['wert'] = int(float(value_str))
                transformed_rows.append(base_data_copy)
    return transformed_rows

def pivot_data(rows):
    pivoted = defaultdict(lambda: {name: 0 for name in VALUE_TYPE_MAP.values()})
    for row in rows:
        value_type = row['curve_value_type_id']
        if value_type not in VALUE_TYPE_MAP:
            continue
        key = (
            row['curve_event_type_id'],
            row['curve_id'],
            row['curve_version_id'],
            row['date'],
            row['raster'],
            row['uhrzeit'],
        )
        column_name = VALUE_TYPE_MAP[value_type]
        pivoted[key][column_name] = row['wert']
    return pivoted

def write_transformed_csv(pivoted_data, output_path):
    fieldnames = ['curve_event_type_id', 'curve_id', 'curve_version_id', 'date', 'raster', 'uhrzeit'] + list(VALUE_TYPE_MAP.values())

    # Sortiere nach Datum und Uhrzeit
    sorted_items = sorted(
        pivoted_data.items(),
        key=lambda item: (item[0][3], item[0][5])  # [3]=date, [5]=uhrzeit
    )

    file_index = 1
    max_size_bytes = 8 * 1024 * 1024  # 8 MB
    output_base, ext = os.path.splitext(output_path)
    output_file = f"{output_base}_{file_index}{ext}"
    csvfile = open(output_file, 'w', newline='')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    current_file_size = csvfile.tell()

    for key, values in sorted_items:
        row = dict(zip(fieldnames[:6], key))
        row.update(values)
        writer.writerow(row)
        current_file_size = csvfile.tell()
        if current_file_size >= max_size_bytes:
            csvfile.close()
            file_index += 1
            output_file = f"{output_base}_{file_index}{ext}"
            csvfile = open(output_file, 'w', newline='')
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()

    csvfile.close()

def main():
    args = parse_arguments()
    input_dir = args.input_dir

    all_rows = []
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.csv'):
            filepath = os.path.join(input_dir, filename)
            all_rows.extend(read_and_transform_csv(filepath))

    pivoted = pivot_data(all_rows)
    write_transformed_csv(pivoted, args.output)

if __name__ == '__main__':
    main()
