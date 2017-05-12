""" Example python code

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-05-12
:Copyright: 2017, Karr Lab
:License: MIT
"""

""" other required modules, classes, functions, and variables """
# Note: preferable import modules rather than individual classes, methods, functions, or variables
from numpy import random
import numpy


class Simulation(object):  # all classes should inherit from `object`
    """ Simulates the synesis and degradation of a species

    Attributes:
        k_syn (:obj:`float`): zeroth-order synthesis rate
        k_keg (:obj:`float`): first-order degradation rate
        verbose (:obj:`bool`): if :obj:`True`, print status information to stdout
    """

    def __init__(self, k_syn=1., k_deg=1., verbose=False):
        """
        Args:
            k_syn (:obj:`float`, optional): zeroth-order synthesis rate
            k_keg (:obj:`float`, optional): first-order degradation rate
            verbose (:obj:`bool`, optional): if :obj:`True`, print status information to stdout
        """
        self.k_syn = k_syn
        self.k_deg = k_deg
        self.verbose = verbose

    def run(self, value_init=5, time_max=10):
        """ Runs a simulation for `time_max` seconds starting with `value_init` molecules

        Args:
            value_init (:obj:`float`, optional): initial number of species
            time_max (:obj:`int`, optional): simulation length in s

        Returns:
            :obj:`Trajectory`: simulated trajectory

        Raises:
            :obj:`ValueError`: if :obj:`time_max` is negative
        """

        # Validate inputs
        if value_init < 0 or numpy.ceil(value_init) != value_init:
            raise ValueError('`value_init` must be a non-negative integer')  # example of how to format a string
        if time_max < 0 or numpy.ceil(time_max) != time_max:
            raise ValueError('`time_max` must be a non-negative integer')

        # simulate
        time = 0
        value = value_init
        rand_state = random.RandomState()

        hist = Trajectory(time_max)
        hist.times[0] = time
        hist.values[0] = value

        if self.verbose:
            print('Time {}: {} molecules'.format(0, value))

        while time < time_max:
            # calculate propensities
            props = numpy.array([
                self.k_syn,
                value * self.k_deg,
            ])
            prop_tot = numpy.sum(props)

            # select time to next reaction
            dt = rand_state.exponential(1. / prop_tot)

            # Select next reaction
            i_rxn = rand_state.choice(2, p=props / prop_tot)

            # store history
            i_prev_timepoint = int(numpy.floor(time))
            i_timepoint = int(numpy.floor(time + dt))
            if i_timepoint > i_prev_timepoint:
                hist.values[i_prev_timepoint+1:i_timepoint+1] = value

                if self.verbose:
                    for i in range(i_prev_timepoint+1, i_timepoint+1):
                        print('Time {}: {} molecules'.format(i_prev_timepoint, value))

            # update time
            time += dt

            # fire reaction
            if i_rxn == 0:
                value += 1
            else:
                value -= 1

        return hist


class Trajectory(object):
    """ Represents a simulated trajectory

    Attributes:
        times (:obj:`numpy.ndarray`): array of times of predicted values in s
        values (:obj:`numpy.ndarray` of :obj:`float`): array of predicted values
    """

    def __init__(self, time_max):
        """
        Args:
            time_max (:obj:`int`): simulation length in s
        """
        if time_max < 0 or numpy.ceil(time_max) != time_max:
            raise ValueError('`time_max` must be a non-negative integer')

        self.times = numpy.arange(0., float(time_max) + 1., 1.)
        self.values = numpy.full(time_max + 1, numpy.nan)
