import csv
import argparse
import os
from datetime import datetime, timedelta
from collections import defaultdict

MAX_FILE_SIZE = 8 * 1024 * 1024  # 8 MB in Bytes

def parse_arguments():
    parser = argparse.ArgumentParser(description='Transformiere und kombiniere CSV-Dateien.')
    parser.add_argument('input_files', nargs='+', help='Pfad zu einer oder mehreren Eingabe-CSV-Dateien')
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
    pivoted = defaultdict(lambda: {'Alle_Anrufe': 0, 'Annahme': 0})
    for row in rows:
        key = (row['curve_event_type_id'], row['curve_id'], row['curve_version_id'], row['date'], row['raster'], row['uhrzeit'])
        if row['curve_value_type_id'] == '1001':
            pivoted[key]['Alle_Anrufe'] = row['wert']
        elif row['curve_value_type_id'] == '1003':
            pivoted[key]['Annahme'] = row['wert']
    return pivoted

def write_transformed_csv(pivoted_data, output_path):
    fieldnames = ['curve_event_type_id', 'curve_id', 'curve_version_id', 'date', 'raster', 'uhrzeit', 'Alle_Anrufe', 'Annahme']
    file_index = 1
    output_file = f"{output_path}_{file_index}.csv"
    
    # Open the first file
    csvfile = open(output_file, 'w', newline='')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()

    for key, values in pivoted_data.items():
        row = dict(zip(fieldnames[:6], key))
        row.update(values)
        writer.writerow(row)
        
        # Check if the file size exceeds the limit and split if necessary
        if os.path.getsize(output_file) >= MAX_FILE_SIZE:
            # Close the current file and open a new one
            csvfile.close()
            file_index += 1
            output_file = f"{output_path}_{file_index}.csv"
            csvfile = open(output_file, 'w', newline='')
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
    
    # Close the last file after writing all rows
    csvfile.close()

def main():
    args = parse_arguments()
    all_rows = []
    for file in args.input_files:
        all_rows.extend(read_and_transform_csv(file))
    pivoted = pivot_data(all_rows)
    write_transformed_csv(pivoted, args.output)

if __name__ == '__main__':
    main()
