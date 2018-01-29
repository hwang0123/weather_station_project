import tarfile,os
import sys
from os.path import isfile, join
import csv
import io

tar_path = 'C:\Users\Hannah\Documents'

tar = tarfile.open(join(tar_path, "js2.gz"))

results = []

for member in tar.getmembers():
    if member.isfile():
        f=tar.extractfile(member)

        csv_file = io.StringIO(f.read().decode('ascii'))
        reader = csv.DictReader(csv_file, fieldnames=['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8'])
        tmax = None
        tmin = None
        tcums = 0
        station = None
        for row in reader:
            if station is None:
                station = row['V1']
            if row['V3'] == 'TMAX':
                if tmax is None:
                    tmax = int(row['V4'])
                elif tmax < int(row['V4']):
                    tcums = tcums + 1
                    tmax = int(row['V4'])
            elif row['V3'] == 'TMIN':
                if tmin is None:
                    tmin = int(row['V4'])
                elif tmin > int(row['V4']):
                    tcums = tcums - 1
                    tmin = int(row['V4'])

        results.append({'station': station, 'tcums': tcums, 'tmin': tmin, 'tmax': tmax})
tar.close()

with open(join(tar_path, 'results.csv'), 'wb') as csv_output_file:
    fieldnames = ['station', 'tcums', 'tmin', 'tmax']
    writer = csv.DictWriter(csv_output_file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(results)



