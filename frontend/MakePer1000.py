#!/usr/bin/env python
# coding: utf-8

import AllPrograms_db
import sys, argparse

def main(argv):
    parser = argparse.ArgumentParser(
        prog="MakePer1000.py",
        description="Clean and re-populate the state, cd and county"
                    " _per_1000 tables based on the last 5 years of data."
                    "Write the data into the regions.db SQLite database.",
    )
    parser.add_argument(
        "-f",
        "--focus_year",
        required=True,
        help="The year on which the report will focus",
    )
    my_args = parser.parse_args()

    _region_mode = 'County'
    focus_year = str(my_args.focus_year)
    AllPrograms_db.clean_per_1000()
    AllPrograms_db.make_per_1000(focus_year)

def usage():
    print("Usage:  MakePer1000.py -f <focus_year>")
    exit


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    else:
        main(sys.argv[1])