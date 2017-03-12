#!/usr/bin/env python

import argparse
from serial import Serial
import sys
import time
import os

__doc__ = """ Decodes SDS messages from sds_tool.ino """


def process(line):
    """ Tries to decode the given line in csv format """
    bts = line.split(',')
    values = []
    for x in bts:
        values.append(int(x, 16))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-p', dest='port', help="Serial port")
    parser.add_argument('-s', default=9600, type=int, dest='speed',
                        help='Serial port speed')
    parser.add_argument('-f', dest='file', help="Load log file")
    parser.add_argument('-w', dest='output', help='Output log file')
    parser.add_argument('-d', dest='debug', action='store_true', help='Debug')

    args = parser.parse_args()
    debug_enabled = args.debug

    if not args.port and not args.file:
        print "Please specify a serial port or log file"
        sys.exit(1)

    if args.port and not os.path.exists(args.port):
        print "Serial device does not exist: %s" % (args.port)
        sys.exit(1)

    if args.file and not os.path.exists(args.file):
        print "Log file does not exist: %s" % (args.file)
        sys.exit(1)

    if args.port:
        teensy = Serial(port=args.port, baudrate=args.speed, timeout=0.005)
        buff = ""

        while True:
            buff = str(teensy.read(2000))
            if buff.find("\n") > -1:
                (line, buff) = buff.split("\n", 1)
                (prefix, btes) = line.split(": ", 1)
                process(btes)
    else:
        with open(args.file) as f:
            while line = f.readline():
                process(line)


