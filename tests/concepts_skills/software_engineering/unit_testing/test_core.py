""" Example tests

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-05-12
:Copyright: 2017, Karr Lab
:License: MIT
"""

from intro_to_wc_modeling.concepts_skills.software_engineering.unit_testing import core
import capturer
import numpy
import unittest


class TestSimulation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Code to execute before all of the tests. For example, this can be used to create temporary
        files.
        """
        pass

    @classmethod
    def tearDownClass(cls):
        """ Code to execute after all of the tests. For example, this can be used to clean up temporary
        files.
        """
        pass

    def setUp(self):
        """ Code to execute before each test. """
        pass

    def tearDown(self):
        """ Code to execute after each test. """
        pass

    def test_run(self):
        sim = core.Simulation(k_syn=1, k_deg=0.25)
        hist = sim.run(value_init=4, time_max=10)

        # the result is an instance of core.Trajectory
        self.assertIsInstance(hist, core.Trajectory)

        # the timepoints are 0, 1, 2, ..., 10
        numpy.testing.assert_equal(hist.times, numpy.arange(0., 11., 1.))

        # all of the predicted values are positive
        self.assertTrue(numpy.all(hist.values >= 0))

    def test_statistics(self):
        sim = core.Simulation(k_syn=1, k_deg=0.25)

        time_max = 100
        n_sample = 100

        values = numpy.full((time_max + 1, n_sample), numpy.nan)
        for i_sample in range(n_sample):
            hist = sim.run(value_init=4, time_max=time_max)
            values[:, i_sample] = hist.values

        numpy.testing.assert_allclose(numpy.mean(values[:]), 4., rtol=1e-1)

    def test_stdout(self):
        sim = core.Simulation(k_syn=1, k_deg=0.25, verbose=True)
        with capturer.CaptureOutput() as captured:
            sim.run(value_init=4, time_max=10)
            stdout = captured.get_text()
            lines = stdout.rstrip().split('\n')
            for line in lines:
                self.assertRegex(line, r'^Time \d+: \d+ molecules$')

    def test_invalid_inputs(self):
        sim = core.Simulation()

        with self.assertRaisesRegex(ValueError, '`value_init` must be a non-negative integer'):
            sim.run(value_init=-1, time_max=10)

        with self.assertRaisesRegex(ValueError, '`time_max` must be a non-negative integer'):
            sim.run(value_init=4, time_max=-1)

    def test_trajectory_exception(self):
        with self.assertRaisesRegex(ValueError, '`time_max` must be a non-negative integer'):
            core.Trajectory(-1)

        with self.assertRaisesRegex(ValueError, '`time_max` must be a non-negative integer'):
            core.Trajectory(1.5)
