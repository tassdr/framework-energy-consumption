import sys
import os
import csv
from collections import OrderedDict
from functools import reduce


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

    # tmp = OrderedDict(
    #     sorted({'android_' + k: v for k, v in runs}, key=lambda x: x[0])
    # )

    tmp = dict()
    for run in runs:
        for k, v in run.items():
            if 'android_' + k in tmp.keys():
                tmp['android_' + k].append(v)
            else:
                tmp['android_' + k] = [v]
    return tmp
    # return OrderedDict(
    #    sorted({'android_' + k: v / len(runs) for k, v in runs_total.items()}.items(), key=lambda x: x[0]))


def aggregate_trepn(logs_dir):
    def format_stats(accum, new):
        column_name = new['Name']
        if '[' in new['Type']:
            column_name += ' [' + new['Type'].split('[')[1]
        accum.update({column_name: float(new['Average'])})
        return accum

    runs = []
    time = 0
    for run_file in [f for f in os.listdir(logs_dir) if os.path.isfile(os.path.join(logs_dir, f))]:
        with open(os.path.join(logs_dir, run_file), 'rb') as run:
            contents = run.read()  # Be careful with large files, this loads everything into memory
            system_stats = contents.split('System Statistics:')[1].strip().splitlines()

            duration = contents.split('\n')
            duration = duration[1].split(',')[4]
            duration = duration.strip('"').split(' ')
            time = int(duration[0]) * 60 + int(duration[2])

            reader = csv.DictReader(system_stats)
            runs.append(reduce(format_stats, reader, {}))
            runs.append({'duration(s)': time})
    # runs_total = reduce(lambda x, y: {k: v + y[k] for k, v in x.items()}, runs)

    # runs.append({'duration': time})
    tmp = dict()
    # print (runs)
    for run in runs:
        for k, v in run.items():
            if k in tmp.keys():
                tmp[k].append(v)
            else:
                tmp[k] = [v]
    # print (tmp)
    return tmp
    # return OrderedDict(sorted({k: v / len(runs) for k, v in runs_total.items()}.items(), key=lambda x: x[0]))


def aggregate(data_dir):
    rows = []
    for device in list_subdir(data_dir):
        #row = OrderedDict({'device': device})
        device_dir = os.path.join(data_dir, device)
        for subject in list_subdir(device_dir):
            #row.update({'subject': subject})
            subject_dir = os.path.join(device_dir, subject)
            for browser in list_subdir(subject_dir):
                #row.update({'browser': browser})

                browser_dir = os.path.join(subject_dir, browser)

                # if os.path.isdir(os.path.join(browser_dir, 'android')):
                #
                #     data = aggregate_android(os.path.join(browser_dir, 'android'))
                #     # print(data)
                #
                #     for l in range(len(data['android_mem'])):
                #         row = OrderedDict({'device': device})
                #         row.update({'subject': subject})
                #         row.update({'browser': browser})
                #         for d in data:
                #             # print (d, data[d][l])
                #             row.update({d: data[d][l]})
                #         #print(row)
                #         rows.append(row)

                if os.path.isdir(os.path.join(browser_dir, 'trepn')):
                    data = aggregate_trepn(os.path.join(browser_dir, 'trepn'))

                    for l in range(len(data['Battery Status'])):
                        row = OrderedDict({'device': device})
                        row.update({'subject': subject})
                        row.update({'browser': browser})
                        for d in data:
                            row.update({d: data[d][l]})
                        rows.append(row)
                    print (rows)

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
    # print (sys.argv[0])
    # print (sys.argv[1])
    # print (sys.argv[2])

    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
