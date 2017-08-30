""" Stochastic simulation tutorial

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-06-22
:Copyright: 2017, Karr Lab
:License: MIT
"""

import matplotlib
import numpy
import os
# matplotlib.use('TkAgg')
matplotlib.use('Agg')
from matplotlib import colors
from matplotlib import pyplot
from scipy import integrate
from scipy import optimize
from scipy import stats

# parameters
k_m = 5  # mRNA h^-1
k_n = 20  # protein mRNA^-1 h^-1
gamma_m = numpy.log(2) * 60 / 3  # h^-1
gamma_n = numpy.log(2) / 10  # h^-1


def deterministic_exercise():
    # equations
    dm_dt = lambda x, t: k_m - gamma_m * x[0]
    dn_dt = lambda x, t: k_n * x[0] - gamma_n * x[1]

    # initial conditions
    m_0 = 1  # mRNA
    n_0 = 98  # proteins

    ##########################################################
    # A. Write the system in vector form
    ##########################################################
    dx_dt = lambda x, t: (k_m - gamma_m * x[0], k_n * x[0] - gamma_n * x[1])
    x_0 = (m_0, n_0)

    ##########################################################
    # B. Plot the vector field
    ##########################################################
    m, n = numpy.meshgrid(
        numpy.linspace(0, 3, 21),
        numpy.linspace(70, 130, 21))
    dm = numpy.array(list(map(lambda m, n: k_m - gamma_m * m, m, n)))
    dn = numpy.array(list(map(lambda m, n: k_n * m - gamma_n * n, m, n)))

    max_mag = numpy.max(numpy.power(dm, 2) + numpy.power(dn, 2))

    pyplot.quiver(m, n, dm / max_mag, dn / max_mag, pivot='mid')
    pyplot.xlim(m[0, (0, -1)])
    pyplot.ylim(n[(0, -1), 0])
    pyplot.xlabel('mRNA')
    pyplot.ylabel('Protein')
    pyplot.grid('on')

    # pyplot.show()

    filename = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'docs', 'tutorials',
                            'cell_modeling', 'simulation', 'stochastic-exercises-deterministic-vector-field.png')
    matplotlib.pyplot.savefig(filename, transparent=True, bbox_inches='tight')
    matplotlib.pyplot.close()

    ##########################################################
    # C. Calculate the Jacobian
    ##########################################################
    jacobian = numpy.array([[-gamma_m, 0], [k_n, -gamma_n]])

    ##########################################################
    # D. Calculate the critical point(s) and their stability
    ##########################################################
    m_ss = k_m / gamma_m
    n_ss = k_n / gamma_n * k_m / gamma_m

    w, v = numpy.linalg.eig(jacobian)

    ##########################################################
    # E. Execute deterministic simulation
    ##########################################################
    dx_dt = lambda x, t: (k_m - gamma_m * x[0], k_n * x[0] - gamma_n * x[1])
    jacobian = lambda x, t: numpy.array([[-gamma_m, 0], [k_n, -gamma_n]])
    t = numpy.linspace(0, 100, 1001)
    x = integrate.odeint(dx_dt, x_0, t, Dfun=jacobian)

    fig, ax1 = pyplot.subplots()
    ax1.plot(t, x[:, 0], 'g')
    ax1.set_xlim((t[0], t[-1]))
    ax1.set_ylim([0.35, numpy.max(x[:, 0])])
    ax1.set_xlabel('Time (h)')
    ax1.set_ylabel('mRNA', color='g')
    ax1.tick_params('y', colors='g')

    ax2 = ax1.twinx()
    ax2.plot(t, x[:, 1], 'b')
    ax2.set_ylim([85, 105])
    ax2.set_ylabel('Protein', color='b')
    ax2.tick_params('y', colors='b')

    filename = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'docs', 'tutorials',
                            'cell_modeling', 'simulation', 'stochastic-exercises-deterministic-simulation.png')
    matplotlib.pyplot.savefig(filename, transparent=True, bbox_inches='tight')
    matplotlib.pyplot.close(fig)

    # fig.show()


def probability_distribution_exercise_mrna():
    # parameters
    k_m = 50  # mRNA h^-1

    # truncation conditions
    max_m = 12

    # initial conditions
    p_0 = numpy.zeros((max_m + 1, ))
    p_0[2] = 1

    ##########################################################
    # A. Generate the master equation
    ##########################################################
    def dp_dt(p):
        dp_dt = numpy.zeros(p.shape)
        for m in range(max_m + 1):
            if m > 0:
                dp_dt[m] += k_m * p[m - 1]
                dp_dt[m - 1] -= k_m * p[m - 1]

            if m < max_m:
                dp_dt[m] += gamma_m * (m + 1) * p[m + 1]
                dp_dt[m + 1] -= gamma_m * (m + 1) * p[m + 1]

        return dp_dt

    ##########################################################
    # B. Simulate the temporal dynamics
    ##########################################################
    t = numpy.linspace(0, 2, 101)
    p = integrate.odeint(lambda p, t: dp_dt(p), p_0, t)

    pyplot.semilogy(t, p[:, 2], color='r', linestyle='-', label='m={}'.format(2))
    pyplot.semilogy(t, p[:, 3], color='g', linestyle='-', label='m={}'.format(3))
    pyplot.semilogy(t, p[:, 4], color='b', linestyle='-', label='m={}'.format(4))

    pyplot.xlim((t[0], t[-1]))
    pyplot.xlabel('Time (h)')
    pyplot.ylabel('Probability')
    matplotlib.pyplot.legend()

    # pyplot.show()

    filename = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'docs', 'tutorials',
                            'cell_modeling', 'simulation', 'stochastic-exercises-probability-distribution-simulation-mRNA.png')
    matplotlib.pyplot.savefig(filename, transparent=True, bbox_inches='tight')
    matplotlib.pyplot.close()

    ##########################################################
    # C. Calculate the steady state
    ##########################################################
    # write in vector form
    A = numpy.zeros((max_m + 1, max_m + 1))
    for m in range(max_m + 1):
        if m > 0:
            A[m, m - 1] += k_m
            A[m - 1, m - 1] -= k_m
        if m < max_m:
            A[m, m + 1] += gamma_m * (m + 1)
            A[m + 1, m + 1] -= gamma_m * (m + 1)

    # calculate null space
    u, s, vh = numpy.linalg.svd(A)
    atol = 1e-13
    rtol = 1e-13
    tol = max(atol, rtol * s[0])
    nnz = (s >= tol).sum()
    p_ss = vh[nnz:].conj().T
    assert(p_ss.shape[1] == 1)

    pyplot.plot(range(max_m + 1), -p_ss.flatten(), 'b', label='PDF')
    pyplot.plot(k_m / gamma_m * numpy.array([1, 1]), [0, numpy.max(-p_ss) + 0.01], 'r:', label='Deterministic steady state')
    pyplot.xlim([0, max_m])
    pyplot.ylim([0, numpy.max(-p_ss) + 0.01])
    pyplot.xlabel('mRNA (molecules)')
    pyplot.ylabel('Probability')
    matplotlib.pyplot.legend()

    # pyplot.show()

    filename = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'docs', 'tutorials',
                            'cell_modeling', 'simulation', 'stochastic-exercises-probability-distribution-steady-state-mRNA.png')
    matplotlib.pyplot.savefig(filename, transparent=True, bbox_inches='tight')
    matplotlib.pyplot.close()


def probability_distribution_exercise():
    # truncation conditions
    min_m = 0
    max_m = 3
    min_n = 54
    max_n = 154
    m_range = range(min_m, max_m + 1)
    n_range = range(min_n, max_n + 1)

    # initial conditions
    p_0_full_mat = numpy.zeros((max_m + 1, max_n + 1))
    p_0_full_mat[1, 98] = 1
    p_0_part_mat = p_0_full_mat[min_m:, min_n:]
    p_0_part_vec = p_0_part_mat.reshape((p_0_part_mat.size, ))

    ##########################################################
    # A. Generate the master equation
    ##########################################################
    def dp_dt(p_part_vec):
        p_part_mat = p_part_vec.reshape(p_0_part_mat.shape)

        dp_dt_part_mat = numpy.zeros(p_part_mat.shape)
        for i, m in enumerate(m_range):
            for j, n in enumerate(n_range):
                if m > min_m:
                    dp_dt_part_mat[i, j] += k_m * p_part_mat[i - 1, j]
                    dp_dt_part_mat[i - 1, j] -= k_m * p_part_mat[i - 1, j]

                if m < max_m:
                    dp_dt_part_mat[i, j] += gamma_m * (m + 1) * p_part_mat[i + 1, j]
                    dp_dt_part_mat[i + 1, j] -= gamma_m * (m + 1) * p_part_mat[i + 1, j]

                if n > min_n:
                    dp_dt_part_mat[i, j] += k_n * m * p_part_mat[i, j - 1]
                    dp_dt_part_mat[i, j - 1] -= k_n * m * p_part_mat[i, j - 1]

                if n < max_n:
                    dp_dt_part_mat[i, j] += gamma_n * (n + 1) * p_part_mat[i, j + 1]
                    dp_dt_part_mat[i, j + 1] -= gamma_n * (n + 1) * p_part_mat[i, j + 1]

        return dp_dt_part_mat.reshape(p_part_vec.shape)

    ##########################################################
    # B. Simulate the temporal dynamics
    ##########################################################
    t = numpy.linspace(0, 2, 101)
    p_part_vec = integrate.odeint(lambda p, t: dp_dt(p), p_0_part_vec, t)
    p_part_mat = p_part_vec.reshape((len(t), p_0_part_mat.shape[0], p_0_part_mat.shape[1]))
    p_full_mat = numpy.zeros((len(t), max_m + 1, max_n + 1))
    p_full_mat[:, min_m:, min_n:] = p_part_mat

    #pyplot.semilogy(t, p_full_mat[:, 0,  64], color='c', linestyle='-', label='mRNA={}, Protein={}'.format(0,  64))
    #pyplot.semilogy(t, p_full_mat[:, 1,  64], color='c', linestyle=':', label='mRNA={}, Protein={}'.format(1,  64))
    pyplot.semilogy(t, p_full_mat[:, 0,  98], color='r', linestyle='-', label='mRNA={}, Protein={}'.format(0,  98))
    pyplot.semilogy(t, p_full_mat[:, 1,  98], color='r', linestyle=':', label='mRNA={}, Protein={}'.format(1,  98))
    pyplot.semilogy(t, p_full_mat[:, 0, 101], color='g', linestyle='-', label='mRNA={}, Protein={}'.format(0, 101))
    pyplot.semilogy(t, p_full_mat[:, 1, 101], color='g', linestyle=':', label='mRNA={}, Protein={}'.format(1, 101))
    pyplot.semilogy(t, p_full_mat[:, 0, 104], color='b', linestyle='-', label='mRNA={}, Protein={}'.format(0, 104))
    pyplot.semilogy(t, p_full_mat[:, 1, 104], color='b', linestyle=':', label='mRNA={}, Protein={}'.format(1, 104))
    #pyplot.semilogy(t, p_full_mat[:, 0, 144], color='m', linestyle='-', label='mRNA={}, Protein={}'.format(0, 144))
    #pyplot.semilogy(t, p_full_mat[:, 1, 144], color='m', linestyle=':', label='mRNA={}, Protein={}'.format(1, 144))

    pyplot.xlim((t[0], t[-1]))
    pyplot.xlabel('Time (h)')
    pyplot.ylabel('Probability')
    matplotlib.pyplot.legend()

    # pyplot.show()

    filename = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'docs', 'tutorials',
                            'cell_modeling', 'simulation', 'stochastic-exercises-probability-distribution-simulation.png')
    matplotlib.pyplot.savefig(filename, transparent=True, bbox_inches='tight')
    matplotlib.pyplot.close()

    ##########################################################
    # C. Calculate the steady state
    ##########################################################
    # write in vector form
    A = numpy.zeros((len(m_range) * len(n_range), len(m_range) * len(n_range)))
    for i, m in enumerate(m_range):
        for j, n in enumerate(n_range):
            i_row = numpy.ravel_multi_index((i, j), (len(m_range), len(n_range)))

            if m > min_m:
                i_col = numpy.ravel_multi_index((i - 1, j), (len(m_range), len(n_range)))
                A[i_row, i_col] += k_m
                A[i_col, i_col] -= k_m

            if m < max_m:
                i_col = numpy.ravel_multi_index((i + 1, j), (len(m_range), len(n_range)))
                A[i_row, i_col] += gamma_m * (m + 1)
                A[i_col, i_col] -= gamma_m * (m + 1)

            if n > min_n:
                i_col = numpy.ravel_multi_index((i, j - 1), (len(m_range), len(n_range)))
                A[i_row, i_col] += k_n * m
                A[i_col, i_col] -= k_n * m

            if n < max_n:
                i_col = numpy.ravel_multi_index((i, j + 1), (len(m_range), len(n_range)))
                A[i_row, i_col] += gamma_n * (n + 1)
                A[i_col, i_col] -= gamma_n * (n + 1)

    # calculate null space
    u, s, vh = numpy.linalg.svd(A)
    atol = 1e-13
    rtol = 0
    tol = max(atol, rtol * s[0])
    nnz = (s >= tol).sum()
    p_ss_part_vec = vh[nnz:].conj().T
    assert(p_ss_part_vec.shape[1] == 1)
    assert(numpy.all(p_ss_part_vec <= 0))
    p_ss_part_mat = -p_ss_part_vec.reshape((len(m_range), len(n_range)))
    p_ss_part_mat = p_ss_part_mat / numpy.sum(p_ss_part_mat)
    p_ss_full_mat = numpy.zeros(p_0_full_mat.shape)
    p_ss_full_mat[min_m:max_m + 1, min_n:max_n + 1] = p_ss_part_mat

    mode_mn = numpy.argmax(p_ss_full_mat.flatten())
    mode_m, mode_n = numpy.unravel_index(mode_mn, p_ss_full_mat.shape)

    pyplot.imshow(numpy.flipud(p_ss_part_mat.transpose()),
                  norm=colors.LogNorm(),
                  extent=(min_m - 0.5, max_m + 0.5, min_n - 0.5, max_n + 0.5),
                  aspect='auto')
    pyplot.xticks(numpy.arange(min_m, max_m + 1))
    pyplot.xlabel('mRNA (molecules)')
    pyplot.ylabel('Protein (molecules)')
    pyplot.colorbar(label='Probability')

    # pyplot.show()

    filename = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'docs', 'tutorials',
                            'cell_modeling', 'simulation', 'stochastic-exercises-probability-distribution-steady-state.png')
    matplotlib.pyplot.savefig(filename, transparent=True, bbox_inches='tight')
    matplotlib.pyplot.close()


def trajectory_exercise():
    ##########################################################
    # A. Implement SSA
    ##########################################################
    def run_ssa(m_0, n_0, t_hist):
        """ Run a stochastic simulation

        Args:            
            m_0 (:obj:`int`): initial number of mRNA
            n_0 (:obj:`int`): initial number of proteins
            t_hist (:obj:`float`): time points to record

        Returns:
            :obj:`tuple`:
                * :obj:`numpy.ndarray`: predicted mRNA number at each time point
                * :obj:`numpy.ndarray`: predicted protein number at each time point
        """

        # data structure to store predicted copy numbers
        m_hist = numpy.full(t_hist.shape, m_0)
        n_hist = numpy.full(t_hist.shape, n_0)

        # initial conditions
        t = t_hist[0]
        m = m_0
        n = n_0

        # iterate over time
        while t < t_hist[-1]:
            # calculate reaction properties/rates
            propensities = numpy.array([k_m, m * gamma_m, m * k_n, n * gamma_n])
            total_propensity = numpy.sum(propensities)

            # select the length of the time step from an exponential distributuon
            dt = numpy.random.exponential(1. / total_propensity)

            # select the next reaction to fire
            i_reaction = numpy.random.choice(4, p=propensities / total_propensity)

            # update the time and copy number based on the selected reaction
            t += dt
            if i_reaction == 0:
                m += 1
            elif i_reaction == 1:
                m -= 1
            elif i_reaction == 2:
                n += 1
            else:
                n -= 1

            # store copy number history
            m_hist[t < t_hist] = m
            n_hist[t < t_hist] = n

        return (m_hist, n_hist)

    ##########################################################
    # B. Simulate several trajectories
    ##########################################################
    n_trajectories = 50
    t = numpy.linspace(0, 20, 101)
    numpy.random.seed(0)

    fig, axes = pyplot.subplots(nrows=2, ncols=1)

    m_hist = numpy.zeros((len(t), n_trajectories))
    n_hist = numpy.zeros((len(t), n_trajectories))
    for i_trajectory in range(n_trajectories):
        m_0 = numpy.random.poisson(k_m / gamma_m)
        n_0 = numpy.round(numpy.random.gamma(k_m / gamma_n, k_n / gamma_m))
        m_hist[:, i_trajectory], n_hist[:, i_trajectory] = run_ssa(m_0, n_0, t)

        gray = 0.5 + 0.5 * i_trajectory / (n_trajectories - 1)
        axes[0].plot(t, m_hist[:, i_trajectory], color=(gray, gray, gray))
        axes[1].plot(t, n_hist[:, i_trajectory], color=(gray, gray, gray))

    axes[0].set_xlim((t[0], t[-1]))
    axes[1].set_xlim((t[0], t[-1]))

    axes[0].set_ylim([0, numpy.max(m_hist) + 1])
    axes[1].set_ylim([numpy.min(n_hist) - 5, numpy.max(n_hist) + 5])

    axes[1].set_xlabel('Time (h)')
    axes[0].set_ylabel('mRNA (molecules)')
    axes[1].set_ylabel('Protein (molecules)')

    # pyplot.show()

    filename = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'docs', 'tutorials',
                            'cell_modeling', 'simulation', 'stochastic-exercises-trajectory-simulation.png')
    matplotlib.pyplot.savefig(filename, transparent=True, bbox_inches='tight')
    matplotlib.pyplot.close(fig)

    ##########################################################
    # C. Plot the average of multiple trajectories
    ##########################################################

    m_percentiles = numpy.zeros((t.size, 7))
    n_percentiles = numpy.zeros((t.size, 7))
    for i, _ in enumerate(t):
        m_percentiles[i, :] = [
            numpy.percentile(m_hist[i, :], 1),
            numpy.percentile(m_hist[i, :], 5),
            numpy.percentile(m_hist[i, :], 33.33),
            numpy.percentile(m_hist[i, :], 50),
            numpy.percentile(m_hist[i, :], 66.67),
            numpy.percentile(m_hist[i, :], 95),
            numpy.percentile(m_hist[i, :], 99),
        ]
        n_percentiles[i, :] = [
            numpy.percentile(n_hist[i, :], 1),
            numpy.percentile(n_hist[i, :], 5),
            numpy.percentile(n_hist[i, :], 33.33),
            numpy.percentile(n_hist[i, :], 50),
            numpy.percentile(n_hist[i, :], 66.67),
            numpy.percentile(n_hist[i, :], 95),
            numpy.percentile(n_hist[i, :], 99),
        ]

    fig, axes = pyplot.subplots(nrows=2, ncols=1)

    axes[0].plot(t, m_percentiles[:, 1], label=r'$-2 \sigma$')
    axes[0].plot(t, m_percentiles[:, 2], label=r'$-1 \sigma$')
    axes[0].plot(t, m_percentiles[:, 3], label=r'$0 \sigma$')
    axes[0].plot(t, m_percentiles[:, 4], label=r'$1 \sigma$')
    axes[0].plot(t, m_percentiles[:, 5], label=r'$2 \sigma$')

    axes[1].plot(t, n_percentiles[:, 1], label=r'$-2 \sigma$')
    axes[1].plot(t, n_percentiles[:, 2], label=r'$-1 \sigma$')
    axes[1].plot(t, n_percentiles[:, 3], label=r'$0 \sigma$')
    axes[1].plot(t, n_percentiles[:, 4], label=r'$1 \sigma$')
    axes[1].plot(t, n_percentiles[:, 5], label=r'$2 \sigma$')

    axes[0].legend()

    axes[0].set_xlim((t[0], t[-1]))
    axes[1].set_xlim((t[0], t[-1]))

    axes[0].set_ylim([0, numpy.max(m_hist) + 1])
    axes[1].set_ylim([numpy.min(n_hist) - 5, numpy.max(n_hist) + 5])

    axes[1].set_xlabel('Time (h)')
    axes[0].set_ylabel('mRNA (molecules)')
    axes[1].set_ylabel('Protein (molecules)')

    # pyplot.show()

    filename = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'docs', 'tutorials',
                            'cell_modeling', 'simulation', 'stochastic-exercises-trajectory-average.png')
    matplotlib.pyplot.savefig(filename, transparent=True, bbox_inches='tight')
    matplotlib.pyplot.close(fig)

    fig, axes = pyplot.subplots(nrows=2, ncols=1)

    kernel_m = stats.gaussian_kde(m_hist.flatten())
    kernel_n = stats.gaussian_kde(n_hist.flatten())
    m = range(int(numpy.min(m_hist)), int(numpy.max(m_hist)) + 1)
    n = range(int(numpy.min(n_hist)), int(numpy.max(n_hist)) + 1)
    p_m = kernel_m(m).T
    p_n = kernel_n(n).T
    p_m = p_m / numpy.sum(p_m)
    p_n = p_n / numpy.sum(p_n)

    axes[0].plot(m, p_m)
    axes[1].plot(n, p_n)

    axes[0].set_xlim((m[0], m[-1]))
    axes[1].set_xlim((n[0], n[-1]))

    axes[0].set_xlabel('mRNA (molecules)')
    axes[1].set_xlabel('Protein (molecules)')

    axes[0].set_ylabel('PDF')
    axes[1].set_ylabel('PDF')

    # pyplot.show()

    filename = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'docs', 'tutorials',
                            'cell_modeling', 'simulation', 'stochastic-exercises-trajectory-histogram.png')
    matplotlib.pyplot.savefig(filename, transparent=True, bbox_inches='tight')
    matplotlib.pyplot.close(fig)
