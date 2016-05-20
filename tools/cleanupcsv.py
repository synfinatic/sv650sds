#!/usr/bin/env python3

__doc__ = """Does a basic clean up of the OLS CSV file to make them easier to
work with"""

import argparse
import string


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("infile", type=str, help="Input CSV")
    parser.add_argument("outfile", type=str, help="Output CSV")

    args = parser.parse_args()

    if args.infile == args.outfile:
        raise argparse.ArgumentError(
            "input file can't also be the output file!")

    infile = open(args.infile, "r")
    outfile = open(args.outfile, "w")

    for line in infile:
        newline = ''.join(filter(lambda x: x in string.printable, line))
        outfile.write(newline)
