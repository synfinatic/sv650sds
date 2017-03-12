#!/usr/bin/env python

import argparse
from serial import Serial
import sys
import time
import os

__doc__ = """ Decodes SDS messages from sds_tool.ino """

DECODE_MAP = [
    [ 'RPM', 25, 26, 'rpm'],
    [ 'TPS', 19, None, 'tps'],
    [ 'ECT', 29, None, 'temp'],
    [ 'IAT', 30, None, 'temp'],
    [ 'IAP', 31, None, 'iap'],
    [ 'GPS', 34, None, 'hex'],
    [ 'TPS', 27, None, 'tps'],
    [ 'STVA', 54, None, 'stva'],
    [ 'Fuel1', 40, None, 'decimal'],
    [ 'Fuel2', 42, None, 'decimal'],
    [ 'Ign1', 49, None, 'decimal'],
    [ 'Ign2', 50, None, 'decimal'],
    [ 'PAIR', 51, None, 'decimal'],
    [ 'Battery', 32, None, 'battery'],
    [ 'Neutral', 53, None, 'hex'],
    [ 'Clutch/FuelMap', 52, None, 'hex'],
]
class Decode(object):
    def __init__(self, name, method, bytea, byteb=None):
        self.name = name
        self.method = method
        self.bytea = bytea
        self.byteb = byteb

    def decode_str(self):
        if self.byteb:
            vals = "%02x%02x" % (self.bytea, self.byteb)
        else:
            vals = "%02x" % (self.bytea)

        return "%s [%s]: %s" % (self.name, vals, self.decode())

    def decode(self):
        return getattr(self, self.method)()

    def decimal(self):
        if not self.byteb:
            return "%d" % (self.bytea,)
        else:
            return "%d%d" % (self.bytea, self.byteb)

    def hex(self):
        if not self.byteb:
            return "0x%02x" % (self.bytea,)
        else:
            return "0x%02x%02x" % (self.bytea, self.byteb)

    def iap(self):
        """ Air Intake Pressure
        (a - 153) * 133 / 4 / 255 """
        val = (float)(self.bytea - 153.0) * 133.0 / 4.0 / 255.0
        return "%.2f" % (val,)

    def battery(self):
        """ Battery Voltage
        a / 1.26"""
        val = (float)(self.bytea) / 1.260
        return "%.2f" % (val,)

    def temp(self):
        """ Temperature
        (a - 48) * .625"""
        val = (float)(self.bytea - 48) * 0.625;
        return "%.2f" % (val,)

    def temp2(self):
        """ Temperature 2
        ((a * 160) / 255) - 30"""
        val = ((float)(a * 160) / 255.0) - 30.0
        return "%0.2f" % (val,)

    def rpm(self):
        """ Engine RPM
        (a * 100) + b"""
        return "%d" % ((self.bytea * 100) + self.byteb)

    def tps(self):
        """ Throttle Position Sensor
        (a - 55) / 1.69"""
        val = (float)(self.bytea - 55) / 1.69
        return "%.2f" % (val,)

    def stva(self):
        """ Secondary Throttle
        (a / 2.55)"""
        val = (float)(self.bytea) / 2.55
        return "%.2f" % (val,)


def print_bytes(bstr):
    """ Prints the actual message bytes as a pair of 4 byte columns """
    btes = bstr.split(',')
    start = 0
    increment = 4
    last = increment
    newline = 0
    sys.stdout.write("==> %02d: " % start)
    fmt = "%s" * increment
    fmt = "%s  " % fmt
    while last < len(btes):
        sys.stdout.write(fmt % tuple(btes[start:last]))
        newline += 1
        last += increment
        start += increment
        if (newline % 2) == 0:
            sys.stdout.write("\n==> %02d: " % start)
    cnt = len(btes[start:len(btes)])
    sys.stdout.write("%s" * cnt % tuple(btes[start:len(btes)]))
    sys.stdout.write("\n")


def process(line):
    """ Tries to decode the given line in csv format """
    bts = line.split(',')
    values = []
    for x in bts:
        if (len(x) > 2):
            break
        values.append(int(x, 16))
    if len(values) == 57:
        print_bytes(line)
        for val in DECODE_MAP:
            bytea = values[val[1]]
            byteb = None
            if val[2]:
                byteb = values[val[2]]
            code = Decode(val[0], val[3], bytea, byteb)
            print code.decode_str()
    else:
        sys.stdout.write("*** Wrong len (%d): %s" % (len(values), line))


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

    if args.output:
        outfile = open(args.output, "w")

    if args.port:
        teensy = Serial(port=args.port, baudrate=args.speed, timeout=0.005)
        buff = ""

        while True:
            buff = str(teensy.read(2000))
            if buff.find("\n") > -1:
                (line, buff) = buff.split("\n", 1)
                (prefix, btes) = line.split(": ", 1)
                if args.output:
                    outfile.write(btes + "\n")
                process(btes)
    else:
        with open(args.file) as f:
            line = f.readline()
            while line:
                process(line.rstrip())
                line = f.readline()


