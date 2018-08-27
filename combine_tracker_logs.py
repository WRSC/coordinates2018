"""Combine data files from the tracker SD cards into a CSV file for each track.
"""
import csv
from datetime import datetime
from glob import glob
import os.path as osp
import sys

def combine_to_csv(track_dir):
    out_file = track_dir.rstrip('/') + '.csv'

    columns = {}
    fields = ['datetime', 'latitude', 'longitude', 'speed', 'course']

    datetime_f = glob(osp.join(track_dir, 'datetime*.txt'))[0]
    with open(datetime_f, 'r') as f:
        datetimes = [datetime.strptime(str(int(float(s))), '%Y%m%d%H%M%S')
                     for s in f.read().split('_')[:-1]]
        columns['datetime'] = [d.isoformat() + 'Z' for d in datetimes]

    for field in fields[1:]:
        filename = glob(osp.join(track_dir, field + '*.txt'))[0]
        with open(filename, 'r') as f:
            columns[field] = f.read().split('_')[:-1]
            
        if len(columns[field]) != len(datetimes):
            raise ValueError(f"{len(columns[field])} {field} values != {len(datetimes)} datetimes")

    with open(out_file, 'w') as f:
        cw = csv.writer(f)
        cw.writerow(fields)
        for row in zip(*[columns[t] for t in fields]):
            cw.writerow(row)
    
    print("Written", out_file)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("No track directories passed")
    for track_dir in sys.argv[1:]:
        combine_to_csv(track_dir)
