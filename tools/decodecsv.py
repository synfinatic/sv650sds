#!/usr/bin/env python3

__doc__ = """Generate a nice decode report from the CSV file"""

import argparse
import csv
import sys


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

# This is the maximum number of msec between bytes which makes a single
# message.  This value was picked by examining some data and finding the
# smallest value which made all messages have valid checksums.  Not sure
# what the actual KWP-2000 spec says?
INTERMESSAGE_GAP = 10.1
ECU_ID = 0x12  # KWP-2000 ECU ID
SDT_ID = 0xf1  # KWP-2000 Suzuki diagnostic tool ID


debug_enabled = False


def debug(msg):
    if debug_enabled:
        print(msg)


def convert_time(time):
    """Converts the given time string into a consistent float value
    representing the msec"""

    if 'ms' in time:
        ms = float(time.replace('ms', ''))
        return ms / 1000
    else:
        return float(time.replace('s', ''))


def checksum(bites):
    """Calculate the checksum for the given array of bytes"""
    x = 0
    for i in bites:
        x = (i + x) % 256
    return x


def bytes2str(bites):
    """Converts a list to a string"""
    return ','.join(map(lambda x: "0x%02x" % (x,), bites))


def process_message(outfile, message, delay):
    """Processes the bytes in a given message"""
    msg_len = len(message)
    if msg_len < 2:
        # need at least two bytes!
        return

    csum = message.pop()
    csum_verify = checksum(message)
    direction = "FromECU"
    if message[1] == ECU_ID:
        direction = "ToECU"

    if csum_verify != csum:
        outfile.write("Bad [%.3fms] %s: %s csum:0x%02x != 0x%02x [%d]\n" % (
            delay * 1000, direction, bytes2str(message), csum, csum_verify, msg_len))
    else:
        outfile.write("OK [%.3fms] %s: %s csum:0x%02x [%d]\n" % (
            delay * 1000, direction, bytes2str(message), csum, msg_len))


def process_file(csvreader, keys, outfile):
    """Process the given input file and write the output to outfile"""

    lastms = 0.0
    message = []
    for row in csvreader:
        start_time = convert_time(row['start-time'])

        delay = start_time - lastms
        lastms = start_time

        if row['event?'] == 'false':
            if delay * 1000 > INTERMESSAGE_GAP:
                process_message(outfile, message, delay)
                message = [int(row['RxD-data'])]
            else:
                # Continue existing message
                message.append(int(row['RxD-data']))

        debug("----- %.2fms -----" % (delay * 1000))

        event_triggered = False
        if row['event?'] == 'true':
            event_triggered = True

        for key in keys:
            # figure out what keys we should ignore
            if key in IGNORE_KEYS:
                continue
            if not event_triggered and key in EVENT_KEYS:
                continue

            if key == 'RxD-data' and row[key]:
                value = int(row[key])
                debug("%s => %s [0x%02x]" % (key, row[key], value))
            else:
                debug("%s => %s" % (key, row[key]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('infile', help="Input CSV")
    parser.add_argument('outfile', help="Output Report")
    parser.add_argument('-d', dest='debug', action='store_true', help='Debug')

    args = parser.parse_args()
    debug_enabled = args.debug
    if args.outfile != '-':
        outfile = open(args.outfile, 'w')
    else:
        outfile = sys.stdout

    with open(args.infile, 'r') as csvfile:
        header = csvfile.readline()
        keys = []
        for key in header.replace('\n', '').split(','):
            keys.append(key.replace('"', '').replace(' ', '-'))

        csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"',
                                   fieldnames=keys)
        process_file(csvreader, keys, outfile)
