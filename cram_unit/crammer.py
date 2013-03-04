"""Tool to generate python unittest classes and results (e.g., nosetests.xml)
from cram tests.

$> python run_cram_unit.py /path/to/mytests --xunit nose_mytests.xml

"""
import os
import sys
import re
import subprocess
import warnings
import logging
import unittest
import types
import tempfile
import time
import shlex
import itertools

import nose

import cram_unit

try:
    #this isn't explicitly used here, but subprocess.Process will call cram.
    # this is essentially a `which cram`
    import cram
except ImportError:
    msg = "Unable to find cram. Please install cram."
    sys.stderr.write(msg + "\n")
    sys.exit(-1)

_version = cram_unit.get_version()

log = logging.getLogger(__name__)


def _run_cmd(cmd):
    started_at = time.time()

    args = shlex.split(cmd)

    # Capture std out and err
    ferr = tempfile.TemporaryFile()
    fout = tempfile.TemporaryFile()

    process = subprocess.Popen(args, stderr=ferr, stdout=fout)

    #TODO Add a timeout
    process.poll()
    while process.returncode is None:
        process.poll()
        time.sleep(2)

    run_time = time.time() - started_at

    returncode = process.returncode
    log.info("returncode is {r} in {s:.2f} sec.".format(r=process.returncode, s=run_time))

    ferr.seek(0)
    stderr = ferr.read()

    fout.seek(0)
    stdout = fout.read()

    log.debug("Closing tmp stdout/err files.")

    return returncode, stderr, stdout


def _wrapper(file_name):
    msg = "Running cram on file_name {f}".format(f=file_name)

    # Don't use itertools.wrap. Need to explicitly set the doc string.
    def _runner(self):
        cmd = "cram {f}".format(f=file_name)

        rcode, sterr, stdout = _run_cmd(cmd)
        error_msg = "Cram task of {f} was UNSUCCESSFUL.".format(f=file_name)

        self.assertTrue(rcode == 0, error_msg)

        #log.info("Mock running of cmd {c}".format(c=cmd))
        log.info(msg)
        # this shouldn't really return anything
        return rcode

    _runner.__doc__ = msg
    return _runner


def _sanitize(file_name):
    """covert the file name into a valid python function name.

    Will replace invalid chars with '_'

    .. note:: This is still a bit weak and there are obvious edge
    cases (e.g., cram_1.t cram-1.t)"""

    name, ext_ = os.path.splitext(os.path.basename(file_name))

    rx = re.compile(r'([a-zA-Z]|_)')

    s_name = ''
    for c in name:
        if rx.match(c):
            s_name += c
        else:
            s_name += '_'

    if s_name is not name:
        msg = "Sanitized {n} to {s} from cram file {f}".format(n=name, s=s_name, f=file_name)
        log.warn(msg)

    return s_name


class CramUnitTest(unittest.TestCase):
    """This class will should be overwritten"""

    CRAM_FILES = None
    # The test names/methods can be prefixed e.g, test_mytest_{cram_file_name}
    CRAM_PREFIX = None

    @classmethod
    def monkey_patch(cls):

        if cls.CRAM_FILES:
            for file_name in cls.CRAM_FILES:
                # use the base name of the file as the test name
                cram_file_name, ext = os.path.splitext(os.path.basename(file_name))

                #Todo sanitize name
                if cls.CRAM_PREFIX is not None:
                    name = "_".join(["test", cls.CRAM_PREFIX, cram_file_name])
                else:
                    name = "test_{n}".format(n=cram_file_name)

                # Dynamically Add method
                f = _wrapper(file_name)
                m = types.MethodType(f, None, cls)

                log.info("Adding method {m} to cls {c} with {n}".format(m=m, c=cls.__name__, n=name))

                if hasattr(cls, name):
                    msg = "Unable to add method {n} to class {c}".format(n=name, c=cls.__name__)
                    log.warn(msg)
                    sys.stderr.write("Warning --> {m}\n".format(m=msg))
                else:
                    setattr(cls, name, m)
        else:
            msg = "No CRAM TestFiles are defined. No tests to add to {c}".format(c=cls.__name__)
            warnings.warn(msg)
            log.warn(msg)

        log.debug("Exiting monkey patching class {c}".format(c=cls.__name__))


def _run_suite(suite, xunit_file):
    """Run cram in subprocess and return the return code.

    cmd Example -> 'cram /abspath/to/stuff/sort.t'
    """
    to_exit = False

    env = {"NOSE_XUNIT_FILE": xunit_file, "NOSE_WITH_XUNIT": 1,
           'NOSE_VERBOSE': 1}

    # Using itertools here is the magic that makes the Xunit plugins and
    # the test cases to work as expected.
    nx = nose.core.main(env=env, suite=itertools.chain(suite), exit=to_exit)

    log.info("Nose output {o}".format(o=nx))

    return True


def run(test_files, xunit_file_name, debug=False, prefix=None):
    """Call a cram subprocess."""

    test_cls = CramUnitTest
    test_cls.CRAM_FILES = test_files

    if prefix:
        test_cls.CRAM_PREFIX = prefix

    test_cls.monkey_patch()
    log.info("Files defined on {m}".format(m=test_cls.CRAM_FILES))

    # Make sure we've add the methods. This should have
    # test_{file_name} method/test or test_{prefix}_{file_name}
    #print dir(test_cls)

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(test_cls)

    # run the unittests
    state = _run_suite(suite, xunit_file_name)

    return state
