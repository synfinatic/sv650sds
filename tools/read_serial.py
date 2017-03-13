#!/usr/bin/env python

import argparse
from serial import Serial
import sys
import os

__doc__ = """ Decodes SDS messages from the sds_print utility """

DECODE_MAP = [
    ['RPM', 25, 26, 'rpm'],
    ['TPS', 19, None, 'tps'],
    ['TPS2', 27, None, 'tps'],
    ['ECT', 29, None, 'temp'],
    ['IAT', 30, None, 'temp'],
    ['IAP', 31, None, 'iap'],
    ['GPS', 34, None, 'hex'],
    ['STVA', 54, None, 'stva'],
    ['Fuel1', 40, None, 'decimal'],
    ['Fuel2', 42, None, 'decimal'],
    ['Ign1', 49, None, 'decimal'],
    ['Ign2', 50, None, 'decimal'],
    ['PAIR', 51, None, 'decimal'],
    ['Battery', 32, None, 'battery'],
    ['Neutral', 53, None, 'hex'],
    ['Clutch/FuelMap', 52, None, 'hex'],
]


class Decode(object):
    limits = []
    quiet = False  # print message in hex
    minmax = False  # print min/max values
    maximums = dict()
    minimums = dict()

    def __init__(self, name, method, bytea, byteb=None):
        self.name = name
        self.method = method
        self.bytea = bytea
        self.byteb = byteb
        self.value = None

    @staticmethod
    def set_limits(names):
        for limit in names:
            Decode.limits.append(limit)

    @staticmethod
    def set_quiet(tf):
        Decode.quiet = tf

    @staticmethod
    def set_minmax(tf):
        Decode.minmax = tf

    def update(self, bytea=None, byteb=None, value=None, ret=None):
        if value is None:
            self.min(self.bytea, self.byteb, self.value, self.ret)
            self.max(self.bytea, self.byteb, self.value, self.ret)
        else:
            self.min(bytea, byteb, value, ret)
            self.max(bytea, byteb, value, ret)

    def max(self, bytea=None, byteb=None, value=None, ret=None):
        if ret is None:
            return self.__decode_bytes(Decode.maximums[self.name][1],
                                    Decode.maximums[self.name][2])
        if self.name in Decode.maximums:
            if value > Decode.maximums[self.name][0]:
                Decode.maximums[self.name] = [value, bytea, byteb, ret]
        else:
            Decode.maximums[self.name] = [value, bytea, byteb, ret]
        return self.decode_max()

    def min(self, bytea=None, byteb=None, value=None, ret=None):
        if ret is None:
            return self.__decode_bytes(Decode.minimums[self.name][1],
                                    Decode.minimums[self.name][2])

        if self.name in Decode.minimums:
            if value < Decode.minimums[self.name][0]:
                Decode.minimums[self.name] = [value, bytea, byteb, ret]
        else:
            Decode.minimums[self.name] = [value, bytea, byteb, ret]
        return self.decode_min()

    def decode_min(self):
        return Decode.minimums[self.name][3]

    def decode_max(self):
        return Decode.maximums[self.name][3]

    def decode_str(self):
        if not Decode.limits:
            return self.__decode_str()
        else:
            for limit in Decode.limits:
                if limit.lower() in self.name.lower():
                    return self.__decode_str()
        return ""

    def __decode_bytes(self, bytea, byteb=None):
        if byteb is None:
            vals = "%02x" % (bytea)
        else:
            vals = "%02x%02x" % (bytea, byteb)
        return vals

    def __decode_str(self):
        vals = self.__decode_bytes(self.bytea, self.byteb)
        decoded = "{:>14s} [{:>4s}] decode: {:6s}".format(
            self.name, vals, self.decode())
        if self.minmax:
            decoded = "{}\tmin: [{:>4s}] {:6s}\tmax: [{:>4s}] {:6s}".format(
                decoded, self.min(), self.decode_min(),
                self.max(), self.decode_max())
        return decoded

    def decode(self):
        return getattr(self, self.method)()

    def decimal(self):
        if self.byteb is None:
            self.value = self.bytea
            self.ret = "%d" % (self.bytea,)
            self.update()
            return self.ret
        else:
            self.value = self.bytea * 255 + self.byteb
            self.ret = "%d%d" % (self.bytea, self.byteb)
            self.update()
            return self.ret

    def hex(self):
        if self.byteb is None:
            self.value = self.bytea
            self.ret = "0x%02x" % (self.bytea,)
            self.update()
            return self.ret
        else:
            self.value = self.bytea * 255 + self.byteb
            self.ret = "0x%02x%02x" % (self.bytea, self.byteb)
            self.update()
            return self.ret

    def iap(self):
        """ Air Intake Pressure
        (a - 153) * 133 / 4 / 255 """
        self.value = (float)(self.bytea - 153.0) * 133.0 / 4.0 / 255.0
        self.ret = "%.2f" % (self.value,)
        self.update()
        return self.ret

    def battery(self):
        """ Battery Voltage
        a / 1.26"""
        self.value = (float)(self.bytea) / 1.260
        self.ret = "%.2f" % (self.value,)
        self.update()
        return self.ret

    def temp(self):
        """ Temperature
        (a - 48) * .625"""
        self.value = (float)(self.bytea - 48) * 0.625
        self.ret = "%.2f" % (self.value,)
        self.update()
        return self.ret

    def temp2(self):
        """ Temperature 2
        ((a * 160) / 255) - 30"""
        self.value = ((float)(self.bytea * 160) / 255.0) - 30.0
        self.ret = "%0.2f" % (self.value,)
        self.update()
        return self.ret

    def rpm(self):
        """ Engine RPM
        (a * 100) + b"""
        self.value = (self.bytea * 100) + self.byteb
        self.ret = "%05u" % (self.value,)
        self.update()
        return self.ret

    def tps(self):
        """ Throttle Position Sensor
        (a - 55) / 1.69"""
        self.value = (float)(self.bytea - 55) / 1.69
        self.ret = "%.2f" % (self.value,)
        self.update()
        return self.ret

    def stva(self):
        """ Secondary Throttle
        (a / 2.55)"""
        self.value = (float)(self.bytea) / 2.55
        self.ret = "%.2f" % (self.value,)
        self.update()
        return self.ret


def print_bytes(bstr):
    """ Prints the actual message bytes as a pair of 4 byte columns """

    if Decode.quiet:
        print "*" * 79
        return

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
            if val[2] is not None:
                byteb = values[val[2]]
            code = Decode(val[0], val[3], bytea, byteb)
            decoded = code.decode_str()
            if decoded:
                print decoded
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
    parser.add_argument('-l', dest='limit', action='append',
                        help='Limit decode output')
    parser.add_argument('-q', dest='quiet', action='store_true', default=False,
                        help="Don't print raw message")
    parser.add_argument('-m', dest='minmax', action='store_true',
                        default=False, help='Print min/max values')

    args = parser.parse_args()
    debug_enabled = args.debug
    if args.limit:
        Decode.set_limits(args.limit)
    Decode.set_quiet(args.quiet)
    Decode.set_minmax(args.minmax)

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
