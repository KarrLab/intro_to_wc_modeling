""" Boolean simulation tutorial

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-06-22
:Copyright: 2017, Karr Lab
:License: MIT
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot
import numpy
import os

################################
# regulatory logic functions
#   A --| B --| C --| A
################################
regulatory_functions = {
    'A': lambda nodes: not nodes['C'],
    'B': lambda nodes: not nodes['A'],
    'C': lambda nodes: not nodes['B'],
}

################################
# initial conditions
################################
initial_state = {
    'A': False,
    'B': True,
    'C': True
}

################################
# numerical simulations
################################


def simulate(regulatory_functions, initial_state, n_steps, update_scheme):
    """ Simulates a Boolean network for :obj:`n_steps` using :obj:`update_scheme`

    Args:
        regulatory_functions (:obj:`dict` of :obj:`str`, :obj:`function`): dictionary of regulatory functions for each species
        initial_state (:obj:`dict` of :obj:`str`, :obj:`bool`): dictionary of initial values of each species
        n_steps (:obj:`int`): number of steps to simulate
        update_scheme (:obj:`method`): update schema

    Returns:
        :obj:`tuple`:

            * :obj:`numpy.ndarray`: array of step numbers
            * :obj:`dict` of :obj:`str`, :obj:`numpy.ndarray`: dictionary of histories of each species
    """

    # initalize data structures to store predicted time course and copy initial state to state history
    step_history = numpy.array(range(n_steps + 1))
    state_history = {}
    for node_name, node_initial_state in initial_state.items():
        state_history[node_name] = numpy.full(n_steps + 1, False, bool)
        state_history[node_name][0] = node_initial_state

    # set current state to initial state
    current_state = initial_state

    # iterate over time steps
    for step in range(1, n_steps + 1):
        # update state according to :obj:`update_scheme`
        current_state = update_scheme(regulatory_functions, step, current_state)

        # store current value
        for node_name, node_current_state in current_state.items():
            state_history[node_name][step] = node_current_state

    # return predicted dynamics
    return (step_history, state_history)


def sync_update_scheme(regulatory_functions, step, current_state):
    """ Synchronously update species values

    Args:
        regulatory_functions (:obj:`dict` of :obj:`str`, :obj:`function`): dictionary of regulatory functions for each species
        step (:obj:`int`): step iteration
        current_state (:obj:`dict` of :obj:`str`, :obj:`bool`): dictionary of values of each species

    Returns:
         :obj:`dict` of :obj:`str`, :obj:`bool`: dictionary of values of each species
    """
    # calculate next state
    next_state = {}
    for node_name in current_state.keys():
        next_state[node_name] = regulatory_functions[node_name](current_state)

    # return state
    return next_state


def deterministic_async_update_scheme(regulatory_functions, step, current_state):
    """ Asynchronously update species values in a deterministic order

    Args:
        regulatory_functions (:obj:`dict` of :obj:`str`, :obj:`function`): dictionary of regulatory functions for each species
        step (:obj:`int`): step iteration
        current_state (:obj:`dict` of :obj:`str`, :obj:`bool`): dictionary of values of each species

    Returns:
         :obj:`dict` of :obj:`str`, :obj:`bool`: dictionary of values of each species
    """
    # calculate next state
    node_names = sorted(current_state.keys())
    node_name = node_names[(step-1) % 3]
    current_state[node_name] = regulatory_functions[node_name](current_state)

    # return state
    return current_state


def random_async_update_scheme(regulatory_functions, step, current_state):
    """ Asynchronously update species values in a random order

    Args:
        regulatory_functions (:obj:`dict` of :obj:`str`, :obj:`function`): dictionary of regulatory functions for each species
        step (:obj:`int`): step iteration
        current_state (:obj:`dict` of :obj:`str`, :obj:`bool`): dictionary of values of each species

    Returns:
         :obj:`dict` of :obj:`str`, :obj:`bool`: dictionary of values of each species
    """
    # calculate next state
    node_name = numpy.random.choice(list(current_state.keys()))
    current_state[node_name] = regulatory_functions[node_name](current_state)

    # return state
    return current_state

# seed random number generator
numpy.random.seed(0)

# simulate
n_steps = 10
sync_time_hist, sync_hist = simulate(regulatory_functions, initial_state, 20, sync_update_scheme)
det_async_time_hist, det_async_hist = simulate(regulatory_functions, initial_state, 20 * 3, deterministic_async_update_scheme)
rand_sync_time_hist, rand_sync_hist = simulate(regulatory_functions, initial_state, 20 * 3, random_async_update_scheme)

det_async_time_hist = det_async_time_hist / 3
rand_sync_time_hist = rand_sync_time_hist / 3

# plot
axis = matplotlib.pyplot.subplot(3, 1, 1)
line_a, = matplotlib.pyplot.plot(sync_time_hist, sync_hist['A'], 'r-', label='A')
line_b, = matplotlib.pyplot.plot(sync_time_hist, sync_hist['B'], 'g-', label='B')
line_c, = matplotlib.pyplot.plot(sync_time_hist, sync_hist['C'], 'b-', label='C')
matplotlib.pyplot.legend([line_a, line_b, line_c], ['A', 'B', 'C'])
matplotlib.pyplot.xlim(0, n_steps)
matplotlib.pyplot.ylim(-0.1, 1.1)
matplotlib.pyplot.yticks([0, 1])
matplotlib.pyplot.xlabel('Step')
matplotlib.pyplot.ylabel('Value')
axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

axis = matplotlib.pyplot.subplot(3, 1, 2)
line_a, = matplotlib.pyplot.plot(det_async_time_hist, det_async_hist['A'], 'r-', label='A')
line_b, = matplotlib.pyplot.plot(det_async_time_hist, det_async_hist['B'], 'g-', label='B')
line_c, = matplotlib.pyplot.plot(det_async_time_hist, det_async_hist['C'], 'b-', label='C')
matplotlib.pyplot.xlim(0, n_steps)
matplotlib.pyplot.ylim(-0.1, 1.1)
matplotlib.pyplot.yticks([0, 1])
matplotlib.pyplot.xlabel('Step')
matplotlib.pyplot.ylabel('Value')
axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

axis = matplotlib.pyplot.subplot(3, 1, 3)
line_a, = matplotlib.pyplot.plot(rand_sync_time_hist, rand_sync_hist['A'], 'r-', label='A')
line_b, = matplotlib.pyplot.plot(rand_sync_time_hist, rand_sync_hist['B'], 'g-', label='B')
line_c, = matplotlib.pyplot.plot(rand_sync_time_hist, rand_sync_hist['C'], 'b-', label='C')
matplotlib.pyplot.xlim(0, n_steps)
matplotlib.pyplot.ylim(-0.1, 1.1)
matplotlib.pyplot.yticks([0, 1])
matplotlib.pyplot.xlabel('Step')
matplotlib.pyplot.ylabel('Value')
axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

# display figure
# matplotlib.pyplot.show()

# save figure
filename = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'docs', 'tutorials',
                        'cell_modeling', 'simulation', 'boolean-results.png')
matplotlib.pyplot.savefig(filename, transparent=True, bbox_inches='tight')
matplotlib.pyplot.close()