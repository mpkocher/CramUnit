import os
import unittest
import logging
import tempfile

from cram_unit.crammer import run_command
from cram_unit.io import XunitTestSuite

log = logging.getLogger(__name__)

_EXE = 'run_cram_unit.py'


class TestIntegration(unittest.TestCase):
    def test_basic(self):
        file_name = "test_version.t"
        dir_name = os.path.dirname(__file__)
        t = tempfile.NamedTemporaryFile(suffix="_cram_unit.xml")
        t.close()
        xunit_file = t.name
        # this is the file that is should be called
        #cram_file_name = os.path.join(dir_name, file_name)

        cmd_str = "{e} --verbose --debug -x {x} {d}"
        d = dict(e=_EXE, x=xunit_file, d=dir_name)
        cmd = cmd_str.format(**d)
        rcode, stdout, stderr = run_command(cmd)
        log.info(cmd)
        self.assertEqual(rcode, 0, stderr)

        x = XunitTestSuite.from_xml(xunit_file)

        self.assertIsNotNone(x)

        self.assertEqual(x.ntests, 1)
        log.info(str(x))
