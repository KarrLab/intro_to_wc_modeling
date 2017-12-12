""" Example command line interface tests

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-05-12
:Copyright: 2017, Karr Lab
:License: MIT
"""

from intro_to_wc_modeling.concepts_skills.software_engineering.unit_testing import __main__
import capturer
import mock
import unittest


class TestMain(unittest.TestCase):

    def test_cli_api(self):
        # array of command line arguments, just as they would be supplied at the command line except
        # each should be an element of an array
        argv = ['value']

        with __main__.App(argv=argv) as app:
            with capturer.CaptureOutput() as captured:
                app.run()
                self.assertEqual(captured.get_text(), 'Arg = `{}`'.format(argv[0]))

    def test_raw_cli(self):
        with mock.patch('sys.argv', ['unit_testing', '--help']):
            with self.assertRaises(SystemExit) as context:
                __main__.main()
                self.assertRegexpMatches(context.Exception, 'usage: intro_to_wc_modeling')
