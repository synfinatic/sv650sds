#!/usr/bin/env python3

__doc__ = """Generate a nice decode report from the CSV file"""

import argparse
import csv

__headers__ = """
index => 0
start-time => 25.40ms
end-time => 25.40ms
event? => false
event-type =>
RxD-event =>
TxD-event =>
RxD-data => 0
TxD-data =>

if event? = 'true' and event-type = 'FRAME' then we had a serial framing error.
Assuming we triggered off the 25ms initalization sequence then we should
see one of these at the beginning of the file, about 25ms in (2nd record).

We never have any TxD events or data, so we can ignore those fields

RxD data is in decimal
"""

IGNORE_KEYS = ['TxD-event', 'TxD-data', 'end-time']
EVENT_KEYS = ['event?', 'event-type', 'RxD-event']

def convert_time(time):
    if 'ms' in time:
        ms = float(time.replace('ms', ''))
        return ms / 1000.0
    else:
        return float(time.replace('s', ''))

def process_file(csvreader, keys, outfile):
    """Process the given input file and write the output to outfile"""

    lastms =  0.0
    for row in csvreader:
        start_time = convert_time(row['start-time'])
        end_time = convert_time(row['end-time'])

        delay = start_time - lastms
        lastms = start_time
        print("----- %.2fms -----" % (delay * 1000))

        no_event = False
        if row['event?'] == 'false':
            no_event = True

        for key in keys:
            if key in IGNORE_KEYS:
                continue
            if no_event and key in EVENT_KEYS:
                continue
            if key == 'RxD-data' and row[key]:
                value = int(row[key])
                print("%s => %s [0x%02x]" % (key, row[key], value))
            else:
                print("%s => %s" % (key, row[key]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('infile', help="Input CSV")
    parser.add_argument('outfile', help="Output Report")

    args = parser.parse_args()
    outfile = open(args.outfile, 'w')

    with open(args.infile, 'r') as csvfile:
        header = csvfile.readline()
        keys = []
        for key in header.replace('\n', '').split(','):
            keys.append(key.replace('"', '').replace(' ', '-'))

        csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"',
                                   fieldnames=keys)
        process_file(csvreader, keys, outfile)

