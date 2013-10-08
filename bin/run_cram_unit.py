#!/usr/bin/env python
import os
import sys
import argparse
import logging
import time
import warnings
import glob

import cram_unit
import cram_unit.crammer as crammer

__version__ = cram_unit.get_version()

log = logging.getLogger()


def _setup_log(level=logging.DEBUG):
    handler = logging.StreamHandler(sys.stdout)
    str_formatter = '[%(levelname)s] %(asctime)-15s [%(name)s %(funcName)s %(lineno)d] %(message)s'
    formatter = logging.Formatter(str_formatter)
    handler.setFormatter(formatter)
    handler.setLevel(level)
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)


def _get_parser():
    """Return an instance of ArgumentParser"""
    p = argparse.ArgumentParser(version=__version__)

    p.add_argument('cram_tests_dir', help="Cram test directory to run.")

    p.add_argument("--debug", action="store_true",
                   help='Turn on debug mode and log to stdout.')

    p.add_argument('-x', dest='xunit_file', default="cram_xunit.xml",
                   help="Name of file to write Xunit.xml output to.")
    p.add_argument("--cram_prefix", default=None,
                   help="Prefix that will be added to the test case name. \
                   (e.g., test_{PREFIX}_{CRAM_FILE})")

    return p


def main():
    """Main Point of Entry"""
    p = _get_parser()

    args = p.parse_args()

    xunit_file = args.xunit_file
    debug = args.debug
    cram_tests_dir = args.cram_tests_dir
    cram_prefix = args.cram_prefix

    if not os.path.exists(cram_tests_dir):
        msg = "Unable to Find directory {c}".format(c=cram_tests_dir)
        sys.stderr.write(msg + "\n")
        return -1

    if debug:
        _setup_log(logging.DEBUG)

    # Hacky kinda of interface now. Just grab all the *.t files from the dir.
    cram_files = [os.path.abspath(f) for f in glob.glob("{d}/*.t".format(d=cram_tests_dir))]

    if not cram_files:
        msg = "Unable to find any *.t files in {x}".format(x=cram_tests_dir)
        warnings.warn(msg + "\n")
        return 0

    #print cram_files
    log.info("Found {n} cram files to test {c}".format(n=len(cram_files), c=cram_files))

    started_at = time.time()

    state = crammer.run(cram_files, xunit_file, prefix=cram_prefix, debug=debug)
    run_time = time.time() - started_at

    rcode = 0 if state else -1

    log.info("Exiting {f} with rcode {r} in {s:.2f} sec.".format(f=os.path.basename(__file__), r=rcode, s=run_time))
    return rcode


if __name__ == '__main__':
    sys.exit(main())