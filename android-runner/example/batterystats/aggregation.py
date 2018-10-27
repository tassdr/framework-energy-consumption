import sys
import os
import csv
from collections import OrderedDict


def list_subdir(a_dir):
    """List immediate subdirectories of a_dir"""
    # https://stackoverflow.com/a/800201
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def aggregate_android(logs_dir):
    def add_row(accum, new):
        row = {k: v + float(new[k]) for k, v in accum.items() if k != 'count'}
        count = accum['count'] + 1
        return dict(row, **{'count': count})

    runs = []
    for run_file in [f for f in os.listdir(logs_dir) if os.path.isfile(os.path.join(logs_dir, f))]:
        with open(os.path.join(logs_dir, run_file), 'rb') as run:
            reader = csv.DictReader(run)
            init = dict({fn: 0 for fn in reader.fieldnames if fn != 'datetime'}, **{'count': 0})
            run_total = reduce(add_row, reader, init)
            runs.append({k: v / run_total['count'] for k, v in run_total.items() if k != 'count'})
    runs_total = reduce(lambda x, y: {k: v + y[k] for k, v in x.items()}, runs)
    return OrderedDict(
        sorted({'android_' + k: v / len(runs) for k, v in runs_total.items()}.items(), key=lambda x: x[0]))


def aggregate_trepn(logs_dir):
    def format_stats(accum, new):
        column_name = new['Name']
        if '[' in new['Type']:
            column_name += ' [' +new['Type'].split('[')[1]
        accum.update({column_name: float(new['Average'])})
        return accum
    runs = []
    for run_file in [f for f in os.listdir(logs_dir) if os.path.isfile(os.path.join(logs_dir, f))]:
        with open(os.path.join(logs_dir, run_file), 'rb') as run:
            contents = run.read()   # Be careful with large files, this loads everything into memory
            system_stats = contents.split('System Statistics:')[1].strip().splitlines()
            reader = csv.DictReader(system_stats)
            runs.append(reduce(format_stats, reader, {}))
    runs_total = reduce(lambda x, y: {k: v + y[k] for k, v in x.items()}, runs)
    return OrderedDict(sorted({k: v / len(runs) for k, v in runs_total.items()}.items(), key=lambda x: x[0]))


def aggregate(data_dir):
    rows = []
    for device in list_subdir(data_dir):
        row = OrderedDict({'device': device})
        device_dir = os.path.join(data_dir, device)
        for subject in list_subdir(device_dir):
            row.update({'subject': subject})
            subject_dir = os.path.join(device_dir, subject)
            if os.path.isdir(os.path.join(subject_dir, 'android')):
                row.update(aggregate_android(os.path.join(subject_dir, 'android')))
            if os.path.isdir(os.path.join(subject_dir, 'trepn')):
                row.update(aggregate_trepn(os.path.join(subject_dir, 'trepn')))
            rows.append(row)
    return rows


def write_to_file(filename, rows):
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main(device, output_root):
    print('Output root: {}'.format(output_root))
    data_dir = os.path.join(output_root, 'data')
    rows = aggregate(data_dir)
    filename = os.path.join(output_root, 'aggregated_results.csv')
    write_to_file(filename, rows)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
