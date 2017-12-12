""" Stochastic simulation tutorial

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-08-30
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
from numpy import linalg
from scipy import integrate
from scipy import optimize
from scipy import stats


OUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'docs', 'cell_modeling', 'simulation')
#:obj:`str`: directory to save graphs


class OdeSimulation(object):
    """ Represents an ODE simulation of mRNA and protein synthesis and degradation

    Attributes:
        k_m (:obj:`float`): mRNA synthesis rate constant (molecules h\ :sup:`-1`\ )
        k_n (:obj:`float`): protein synthesis rate constant (\ :sup:`-1`\  h\ :sup:`-1`\ )
        gamma_m (:obj:`float`): mRNA degradation rate constant (h\ :sup:`-1`\ )
        gamma_n (:obj:`float`): protein degradation rate constant (h\ :sup:`-1`\ )
        m_0 (:obj:`float`): initial mRNA number (molecules)
        n_0 (:obj:`float`): initial protein number (molecules)
    """

    def __init__(self, k_m=5, k_n=20, gamma_m=numpy.log(2) * 60 / 3, gamma_n=numpy.log(2) / 10, m_0=1, n_0=98):
        """
        Args:
            k_m (:obj:`float`, optional): mRNA synthesis rate constant (molecules h\ :sup:`-1`\ )
            k_n (:obj:`float`, optional): protein synthesis rate constant (\ :sup:`-1`\  h\ :sup:`-1`\ )
            gamma_m (:obj:`float`, optional): mRNA degradation rate constant (h\ :sup:`-1`\ )
            gamma_n (:obj:`float`, optional): protein degradation rate constant (h\ :sup:`-1`\ )
            m_0 (:obj:`float`, optional): initial mRNA number (molecules)
            n_0 (:obj:`float`, optional): initial protein number (molecules)
        """
        self.k_m = k_m
        self.k_n = k_n
        self.gamma_m = gamma_m
        self.gamma_n = gamma_n
        self.m_0 = m_0
        self.n_0 = n_0

    # reaction rates
    def r_m_syn(self, m, n):
        """ Calculate the mRNA synthesis rate

        Args:
            m (:obj:`float`): mRNA number (molecules)
            n (:obj:`float`): protein number (molecules)

        Returns:
            :obj:`float`: mRNA synthesis rate (molecules h\ :sup:`-1`\ )
        """
        return self.k_m

    def r_n_syn(self, m, n):
        """ Calculate the protein synthesis rate

        Args:
            m (:obj:`float`): mRNA number (molecules)
            n (:obj:`float`): protein number (molecules)

        Returns:
            :obj:`float`: protein synthesis rate (molecules h\ :sup:`-1`\ )
        """
        return m * self.k_n

    def r_m_deg(self, m, n):
        """ Calculate the mRNA degradation rate

        Args:
            m (:obj:`float`): mRNA number (molecules)
            n (:obj:`float`): protein number (molecules)

        Returns:
            :obj:`float`: mRNA degradation rate (molecules h\ :sup:`-1`\ )
        """
        return m * self.gamma_m

    def r_n_deg(self, m, n):
        """ Calculate the protein degradation rate

        Args:
            m (:obj:`float`): mRNA number (molecules)
            n (:obj:`float`): protein number (molecules)

        Returns:
            :obj:`float`: protein degradation rate (molecules h\ :sup:`-1`\ )
        """
        return n * self.gamma_n

    # species differentials
    def dm_dt(self, m, n):
        """ Calculate the rate of change of mRNA

        Args:
            m (:obj:`float`): mRNA number (molecules)
            n (:obj:`float`): protein number (molecules)

        Returns:
            :obj:`float`: rate of change of mRNA (molecules h\ :sup:`-1`\ )
        """
        return self.r_m_syn(m, n) - self.r_m_deg(m, n)

    def dn_dt(self, m, n):
        """ Calculate the rate of change of proteins

        Args:
            m (:obj:`float`): mRNA number (molecules)
            n (:obj:`float`): protein number (molecules)

        Returns:
            :obj:`float`: rate of change of proteins (molecules h\ :sup:`-1`\ )
        """
        return self.r_n_syn(m, n) - self.r_n_deg(m, n)

    # vector form
    def dx_dt(self, x):
        """ Calculate the rate of change of the system (mRNA and proteins)

        Args:
            x (:obj:`numpy.array`): numbers of particles (tuple of mRNA and proteins numbers) (molecules)

        Returns:
            :obj:`float`: rate of change of the system (tuple of the rates of change of mRNA and proteins) (molecules h\ :sup:`-1`\ )
        """
        m = x[0]
        n = x[1]
        return numpy.array([self.dm_dt(m, n), self.dn_dt(m, n)])

    def x(self, m, n):
        """ Generate a vector of species numbers

        Args:
            m (:obj:`float`): mRNA number (molecules)
            n (:obj:`float`): protein number (molecules)

        Returns:
            :obj:`numpy.array`: numbers of particles (tuple of mRNA and proteins numbers) (molecules)
        """
        return numpy.array([m, n])

    @property
    def x_0(self):
        return numpy.array([self.m_0, self.n_0])
        # return (self.k_m - self.gamma_m * x[0], self.k_n * x[0] - self.gamma_n * x[1])

    def jacobian(self, x):
        """ Calculate the Jacobian of the system

        Args:
            x (:obj:`numpy.array`): numbers of particles (tuple of mRNA and proteins numbers) (molecules)

        Returns:
            :obj:`numpy.array`: Jacobian (h\ :sup:`-1`\ )
        """
        return numpy.array([[-self.gamma_m, 0], [self.k_n, -self.gamma_n]])

    def plot_vector_field(self):
        """ Plot vector field

        Returns:
            :obj:`matplotlib.figure.Figure`: figure
        """
        fig, axes = pyplot.subplots(nrows=1, ncols=1)

        m, n = numpy.meshgrid(
            numpy.linspace(0, 3, 21),
            numpy.linspace(70, 130, 21))
        dm = numpy.array(list(map(self.dm_dt, m, n)))
        dn = numpy.array(list(map(self.dn_dt, m, n)))

        max_mag = numpy.max(numpy.power(dm, 2) + numpy.power(dn, 2))

        axes.quiver(m, n, dm / max_mag, dn / max_mag, pivot='mid')
        axes.set_xlim(m[0, (0, -1)])
        axes.set_ylim(n[(0, -1), 0])
        axes.set_xlabel('mRNA')
        axes.set_ylabel('Protein')
        axes.grid('on')

        return fig

    def get_steady_state(self):
        """ Calculate the steady state

        Returns:
            :obj:`float`: steady-state mRNA number (molecules)
            :obj:`float`: steady-state protein number (molecules)
            :obj:`str`: stability of the steady state
        """
        m = self.k_m / self.gamma_m
        n = self.k_n / self.gamma_n * self.k_m / self.gamma_m

        jacobian = self.jacobian(self.x(m, n))
        stability = self.get_steady_stability(jacobian)

        return (m, n, stability)

    def get_steady_stability(self, jacobian):
        """ Get the stability of a steady state

        Args:
            jacobian (:obj:`numpy.ndarray`): jacobian of the model

        Returns:
            :obj:`str`: stability of the steady state
        """
        w, _ = linalg.eig(jacobian)
        if numpy.all(numpy.imag(w) == 0):
            if numpy.all(w < 0):
                return 'stable sink'
            elif numpy.all(w > 0):
                return 'unstable source'
            else:
                return 'unstable saddle'
        else:
            if numpy.all(numpy.real(w) < 0):
                return 'stable spiral sink'
            else:
                return 'unstable spiral source'

    def simulate(self, t_0=0., t_end=100., t_step=1.):
        """ Run the simulation

        Args:
            t_0 (:obj:`float`, optional): initial time (h)
            t_end (:obj:`float`, optional): end time (h)
            t_step (:obj:`float`, optional): frequency at which to record predicted mRNA and proteins

        Return:
            :obj:`tuple`:
                * :obj:`numpy.array`: simulation time (h)
                * :obj:`numpy.array`: predicted mRNA (molecules)
                * :obj:`numpy.array`: predicted proteins (molecules)
        """
        assert ((t_end - t_0) / t_step % 1 == 0)
        t = numpy.linspace(t_0, t_end, int((t_end - t_0) / t_step) + 1)
        x = integrate.odeint(lambda x, t: self.dx_dt(x), self.x_0, t, Dfun=lambda x, t: self.jacobian(x))
        return (t, x[:, 0], x[:, 1])

    def plot_simulation_results(self, t, m, n):
        """ Plot simulation results

        Args:
            t (:obj:`numpy.array`): simulation time (h)
            m (:obj:`numpy.array`): predicted mRNA (molecules)
            n (:obj:`numpy.array`): predicted proteins (molecules)

        Returns:
            :obj:`matplotlib.figure.Figure`: figure
        """
        fig, axes = pyplot.subplots(nrows=1, ncols=1)

        axes_m = axes
        axes_n = axes.twinx()

        axes_m.plot(t, m, 'g')
        axes_m.set_ylim([0.35, numpy.max(m)])
        axes_m.set_ylabel('mRNA', color='g')
        axes_m.tick_params('y', colors='g')

        axes_n.plot(t, n, 'b')
        axes_n.set_ylim([85, 105])
        axes_n.set_ylabel('Protein', color='b')
        axes_n.tick_params('y', colors='b')

        axes_m.set_xlim((t[0], t[-1]))
        axes_n.set_xlim((t[0], t[-1]))
        axes_m.set_xlabel('Time (h)')

        return fig


def deterministic_exercise():
    sim = OdeSimulation()

    ##########################################################
    # Write the system in vector form
    ##########################################################
    sim.x_0
    sim.dx_dt(sim.x_0)

    ##########################################################
    # Plot the vector field
    ##########################################################
    fig = sim.plot_vector_field()
    # fig.show()
    filename = os.path.join(OUT_DIR, 'mrna-and-protein-using-several-methods-deterministic-vector-field.png')
    fig.savefig(filename, transparent=True, bbox_inches='tight')
    matplotlib.pyplot.close(fig)

    ##########################################################
    # Calculate the Jacobian
    ##########################################################
    sim.jacobian(sim.x_0)

    ##########################################################
    # Calculate the critical point(s) and their stability
    ##########################################################
    m_ss, n_ss, stability = sim.get_steady_state()

    ##########################################################
    # Execute deterministic simulation
    ##########################################################
    t, m, n = sim.simulate(t_end=100, t_step=1)

    fig = sim.plot_simulation_results(t, m, n)
    # fig.show()
    filename = os.path.join(OUT_DIR, 'mrna-and-protein-using-several-methods-deterministic-simulation.png')
    fig.savefig(filename, transparent=True, bbox_inches='tight')
    matplotlib.pyplot.close(fig)


class CmeSimulation(object):
    """ Represents a CME simulation of mRNA and protein synthesis and degradation

    Attributes:
        k_m (:obj:`float`): mRNA synthesis rate constant (molecules h\ :sup:`-1`\ )
        k_n (:obj:`float`): protein synthesis rate constant (\ :sup:`-1`\  h\ :sup:`-1`\ )
        gamma_m (:obj:`float`): mRNA degradation rate constant (h\ :sup:`-1`\ )
        gamma_n (:obj:`float`): protein degradation rate constant (h\ :sup:`-1`\ )
        m_min (:obj:`int`): minimum mRNA copy number to simulate
        m_max (:obj:`int`): maximum protein copy number to simulate
        n_min (:obj:`int`): minimum mRNA copy number to simulate
        n_max (:obj:`int`): maximum protein copy number to simulate
        p_0 (:obj:`float`): matrix of initial probability of each combination of mRNA and protein number (dimensionless)
    """

    def __init__(self,
                 k_m=5, k_n=20, gamma_m=numpy.log(2) * 60 / 3, gamma_n=numpy.log(2) / 10,
                 m_min=None, m_max=None, n_min=None, n_max=None,
                 p_0=None):
        """
        Args:
            k_m (:obj:`float`, optional): mRNA synthesis rate constant (molecules h\ :sup:`-1`\ )
            k_n (:obj:`float`, optional): protein synthesis rate constant (\ :sup:`-1`\  h\ :sup:`-1`\ )
            gamma_m (:obj:`float`, optional): mRNA degradation rate constant (h\ :sup:`-1`\ )
            gamma_n (:obj:`float`, optional): protein degradation rate constant (h\ :sup:`-1`\ )
            m_min (:obj:`int`, optional): minimum mRNA copy number to simulate
            m_max (:obj:`int`, optional): maximum protein copy number to simulate
            n_min (:obj:`int`, optional): minimum mRNA copy number to simulate
            n_max (:obj:`int`, optional): maximum protein copy number to simulate
            p_0 (:obj:`float`, optional): matrix of initial probability of each (mRNA, protein) state (dimensionless)
        """
        self.k_m = k_m
        self.k_n = k_n
        self.gamma_m = gamma_m
        self.gamma_n = gamma_n

        if m_min is None:
            m_min = int(max(0, numpy.floor(self.k_m / self.gamma_m - 4 * numpy.sqrt(self.k_m / self.gamma_m))))
        if m_max is None:
            m_max = int(numpy.ceil(self.k_m / self.gamma_m + 4 * numpy.sqrt(self.k_m / self.gamma_m)))
        if n_min is None:
            mean, var = stats.gamma.stats(self.k_m / self.gamma_n, scale=self.k_n / self.gamma_m)
            n_min = int(max(0, numpy.floor(mean - 4 * numpy.sqrt(var))))
        if n_max is None:
            mean, var = stats.gamma.stats(self.k_m / self.gamma_n, scale=self.k_n / self.gamma_m)
            n_max = int(numpy.ceil(mean + 4 * numpy.sqrt(var)))

        self.m_min = m_min
        self.m_max = m_max
        self.n_min = n_min
        self.n_max = n_max

        if p_0 is None:
            p_0 = numpy.zeros((m_max + 1, n_max + 1))
            p_0[0, 0] = 1
        self.p_0 = p_0

    def partial_vector_to_partial_matrix(self, vec):
        """ Convert a partial vector to a partial matrix

        Args:
            vec (:obj:`numpy.array`): vector of size ((m_max - m_min + 1) * (n_max - n_min + 1), 1) that represents
                mRNA = {m_min .. m_max} and protein = {n_min .. n_max}

        Returns:
            :obj:`numpy.array`: matrix with size (m_max - m_min + 1, n_max - n_min + 1) that represents
                mRNA = {m_min .. m_max} and protein = {n_min .. n_max}
        """
        return vec.reshape((self.m_max - self.m_min + 1, self.n_max - self.n_min + 1))

    def partial_matrix_to_partial_vector(self, mat):
        """ Convert a partial matrix to a partial vector

        Args:
            mat (:obj:`numpy.array`): matrix with size (m_max - m_min + 1, n_max - n_min + 1) that represents
                mRNA = {m_min .. m_max} and protein = {n_min .. n_max}

        Returns:
            :obj:`numpy.array`: vector of size ((m_max - m_min + 1) * (n_max - n_min + 1), 1) that represents
                mRNA = {m_min .. m_max} and protein = {n_min .. n_max}
        """
        return mat.flatten()

    def full_matrix_to_partial_matrix(self, full_matrix):
        """ Convert a full matrix to a partial vector

        Args:
            full_matrix (:obj:`numpy.array`): matrix with size (m_max + 1, n_max + 1) that represents
                mRNA = {0 .. m_max} and protein = {0 .. n_max}

        Returns:
            :obj:`numpy.array`: matrix with size (m_max - m_min + 1, n_max - n_min + 1) that represents
                mRNA = {m_min .. m_max} and protein = {n_min .. n_max}
        """
        return full_matrix[self.m_min:, self.n_min:]

    def partial_matrix_to_full_matrix(self, partial_matrix):
        """ Convert a partial vector to a full matrix

        Args:
            partial_matrix (:obj:`numpy.array`): matrix with size (m_max - m_min + 1, n_max - n_min + 1) that represents
                mRNA = {m_min .. m_max} and protein = {n_min .. n_max}

        Returns:
            :obj:`numpy.array`: matrix with size (m_max + 1, n_max + 1) that represents
                mRNA = {0 .. m_max} and protein = {0 .. n_max}
        """
        full_matrix = numpy.zeros((self.m_max + 1, self.n_max + 1))
        full_matrix[self.m_min:, self.n_min:] = partial_matrix
        return full_matrix

    def full_matrix_to_partial_vector(self, full_matrix):
        """ Convert a full matrix to a partial vector

        Args:
            full_matrix (:obj:`numpy.array`): matrix with size (m_max + 1, n_max + 1) that represents
                mRNA = {0 .. m_max} and protein = {0 .. n_max}

        Returns:
            :obj:`numpy.array`: vector of size ((m_max - m_min + 1) * (n_max - n_min + 1), 1) that represents
                mRNA = {m_min .. m_max} and protein = {n_min .. n_max}
        """
        part_matrix = self.full_matrix_to_partial_matrix(full_matrix)
        return self.partial_matrix_to_partial_vector(part_matrix)

    def partial_vector_to_full_matrix(self, partial_vector):
        """ Convert a partial vector to a full matrix

        Args:
            partial_vector (:obj:`numpy.array`): vector of size ((m_max - m_min + 1) * (n_max - n_min + 1), 1) that represents
                mRNA = {m_min .. m_max} and protein = {n_min .. n_max}

        Returns:
            :obj:`numpy.array`: matrix with size (m_max + 1, n_max + 1) that represents
                mRNA = {0 .. m_max} and protein = {0 .. n_max}
        """
        return self.partial_matrix_to_full_matrix(self.partial_vector_to_partial_matrix(partial_vector))

    def dp_dt(self, p_part_vec):
        """ Calculate the time derivative of the probability of each (mRNA, protein) state

        Args:
            p_part_vec (:obj:`numpy.array`): vector of probability of each (mRNA, protein) state (dimensionless)

        Returns:
            adf
        """

        p_part_mat = self.partial_vector_to_partial_matrix(p_part_vec)

        dp_dt_part_mat = numpy.zeros(p_part_mat.shape)
        for i, m in enumerate(range(self.m_min, self.m_max + 1)):
            for j, n in enumerate(range(self.n_min, self.n_max + 1)):
                if m > self.m_min:
                    dp_dt_part_mat[i, j] += self.k_m * p_part_mat[i - 1, j]
                    dp_dt_part_mat[i - 1, j] -= self.k_m * p_part_mat[i - 1, j]

                if m < self.m_max:
                    dp_dt_part_mat[i, j] += self.gamma_m * (m + 1) * p_part_mat[i + 1, j]
                    dp_dt_part_mat[i + 1, j] -= self.gamma_m * (m + 1) * p_part_mat[i + 1, j]

                if n > self.n_min:
                    dp_dt_part_mat[i, j] += self.k_n * m * p_part_mat[i, j - 1]
                    dp_dt_part_mat[i, j - 1] -= self.k_n * m * p_part_mat[i, j - 1]

                if n < self.n_max:
                    dp_dt_part_mat[i, j] += self.gamma_n * (n + 1) * p_part_mat[i, j + 1]
                    dp_dt_part_mat[i, j + 1] -= self.gamma_n * (n + 1) * p_part_mat[i, j + 1]

        return self.partial_matrix_to_partial_vector(dp_dt_part_mat)

    def simulate(self, t_0=0., t_end=100., t_step=1.):
        """ Run the simulation

        Args:
            t_0 (:obj:`float`, optional): initial time (h)
            t_end (:obj:`float`, optional): end time (h)
            t_step (:obj:`float`, optional): frequency at which to record predicted mRNA and proteins

        Return:
            :obj:`tuple`:
                * :obj:`numpy.array`: simulation time (h)
                * :obj:`numpy.array`: predicted probability of each (mRNA, protein) state at each time point (dimensionless)
        """
        assert ((t_end - t_0) / t_step % 1 == 0)
        t = numpy.linspace(t_0, t_end, int((t_end - t_0) / t_step) + 1)
        p_part_vec = integrate.odeint(lambda p, t: self.dp_dt(p), self.full_matrix_to_partial_vector(self.p_0), t)
        p = numpy.zeros((t.size, self.p_0.shape[0], self.p_0.shape[1]))
        p[:, self.m_min:, self.n_min:] = p_part_vec.reshape((t.size, self.m_max - self.m_min + 1, self.n_max - self.n_min + 1))
        return (t, p)

    def plot_simulation_results(self, t, p):
        """ Plot simulation results

        Args:
            t (:obj:`numpy.array`): simulation time (h)
            p (:obj:`numpy.array`): predicted probability of each (mRNA, protein) state at each time point (dimensionless)

        Returns:
            :obj:`matplotlib.figure.Figure`: figure
        """
        fig, axes = pyplot.subplots(nrows=1, ncols=1)

        # axes.semilogy(t, p[:, 0,  64], color='c', linestyle='-', label='mRNA={}, Protein={}'.format(0,  64))
        # axes.semilogy(t, p[:, 1,  64], color='c', linestyle=':', label='mRNA={}, Protein={}'.format(1,  64))
        axes.semilogy(t, p[:, 0,  98], color='r', linestyle='-', label='mRNA={}, Protein={}'.format(0,  98))
        axes.semilogy(t, p[:, 1,  98], color='r', linestyle=':', label='mRNA={}, Protein={}'.format(1,  98))
        axes.semilogy(t, p[:, 0, 101], color='g', linestyle='-', label='mRNA={}, Protein={}'.format(0, 101))
        axes.semilogy(t, p[:, 1, 101], color='g', linestyle=':', label='mRNA={}, Protein={}'.format(1, 101))
        axes.semilogy(t, p[:, 0, 104], color='b', linestyle='-', label='mRNA={}, Protein={}'.format(0, 104))
        axes.semilogy(t, p[:, 1, 104], color='b', linestyle=':', label='mRNA={}, Protein={}'.format(1, 104))
        # axes.semilogy(t, p[:, 0, 144], color='m', linestyle='-', label='mRNA={}, Protein={}'.format(0, 144))
        # axes.semilogy(t, p[:, 1, 144], color='m', linestyle=':', label='mRNA={}, Protein={}'.format(1, 144))

        axes.set_xlim((t[0], t[-1]))
        axes.set_xlabel('Time (h)')
        axes.set_ylabel('Probability')
        axes.legend()

        return fig

    def get_steady_state(self):
        """ Calculate the steady state probability distribution

        Returns:
            :obj:`numpy.array`: steay-state probability of each (mRNA, protein) state (dimensionless)
        """
        part_mat_shape = (self.m_max - self.m_min + 1, self.n_max - self.n_min + 1)
        part_mat_size = part_mat_shape[0] * part_mat_shape[1]

        A = numpy.zeros((part_mat_size, part_mat_size))
        for i, m in enumerate(range(self.m_min, self.m_max + 1)):
            for j, n in enumerate(range(self.n_min, self.n_max + 1)):
                i_row = numpy.ravel_multi_index((i, j), part_mat_shape)

                if m > self.m_min:
                    i_col = numpy.ravel_multi_index((i - 1, j), part_mat_shape)
                    A[i_row, i_col] += self.k_m
                    A[i_col, i_col] -= self.k_m

                if m < self.m_max:
                    i_col = numpy.ravel_multi_index((i + 1, j), part_mat_shape)
                    A[i_row, i_col] += self.gamma_m * (m + 1)
                    A[i_col, i_col] -= self.gamma_m * (m + 1)

                if n > self.n_min:
                    i_col = numpy.ravel_multi_index((i, j - 1), part_mat_shape)
                    A[i_row, i_col] += self.k_n * m
                    A[i_col, i_col] -= self.k_n * m

                if n < self.n_max:
                    i_col = numpy.ravel_multi_index((i, j + 1), part_mat_shape)
                    A[i_row, i_col] += self.gamma_n * (n + 1)
                    A[i_col, i_col] -= self.gamma_n * (n + 1)

        # calculate null space
        u, s, vh = linalg.svd(A)
        atol = 1e-13
        rtol = 0
        tol = max(atol, rtol * s[0])
        nnz = (s >= tol).sum()
        p_part_vec = vh[nnz:].conj().T
        assert(p_part_vec.shape[1] == 1)
        assert(numpy.all(p_part_vec >= 0))
        p_part_vec = p_part_vec / numpy.sum(p_part_vec)
        return self.partial_vector_to_full_matrix(p_part_vec)

    def plot_probability_distribution(self, p):
        """ Plot steady state

        Args:
            p (:obj:`numpy.array`): probability of each (mRNA, protein) state (dimensionless)

        Returns:
            :obj:`matplotlib.figure.Figure`: figure
        """
        fig, axes = pyplot.subplots(nrows=1, ncols=1)

        img = axes.imshow(numpy.flipud(self.full_matrix_to_partial_matrix(p).transpose()),
                          norm=colors.LogNorm(),
                          extent=(self.m_min - 0.5, self.m_max + 0.5, self.n_min - 0.5, self.n_max + 0.5),
                          aspect='auto')
        axes.set_xticks(numpy.arange(self.m_min, self.m_max + 1))
        axes.set_xlabel('mRNA (molecules)')
        axes.set_ylabel('Protein (molecules)')
        fig.colorbar(img, label='Probability')

        return fig


def probability_distribution_exercise():
    sim = CmeSimulation()

    # initial conditions
    sim.p_0[:] = 0
    sim.p_0[1, 98] = 1

    ##########################################################
    # Generate the master equation
    ##########################################################
    sim.dp_dt

    ##########################################################
    # Simulate the temporal dynamics
    ##########################################################
    t, p = sim.simulate(t_end=2, t_step=0.01)
    fig = sim.plot_simulation_results(t, p)
    # fig.show()
    filename = os.path.join(OUT_DIR, 'mrna-and-protein-using-several-methods-probability-distribution-simulation.png')
    fig.savefig(filename, transparent=True, bbox_inches='tight')
    matplotlib.pyplot.close(fig)

    ##########################################################
    # Calculate the steady state
    ##########################################################
    # calculate steady-state
    p_ss = sim.get_steady_state()

    # get mode
    mode_mn = numpy.argmax(p_ss.flatten())
    mode_m, mode_n = numpy.unravel_index(mode_mn, p_ss.shape)

    # plot
    fig = sim.plot_probability_distribution(p_ss)
    # fig.show()
    filename = os.path.join(OUT_DIR, 'mrna-and-protein-using-several-methods-probability-distribution-steady-state.png')
    fig.savefig(filename, transparent=True, bbox_inches='tight')
    matplotlib.pyplot.close(fig)


class SsaSimulation(object):
    """ Represents an SSA simulation of mRNA and protein synthesis and degradation

    Attributes:
        k_m (:obj:`float`): mRNA synthesis rate constant (molecules h\ :sup:`-1`\ )
        k_n (:obj:`float`): protein synthesis rate constant (\ :sup:`-1`\  h\ :sup:`-1`\ )
        gamma_m (:obj:`float`): mRNA degradation rate constant (h\ :sup:`-1`\ )
        gamma_n (:obj:`float`): protein degradation rate constant (h\ :sup:`-1`\ )
        m_0 (:obj:`float`): initial mRNA number (molecules)
        n_0 (:obj:`float`): initial protein number (molecules)
    """

    def __init__(self, k_m=5, k_n=20, gamma_m=numpy.log(2) * 60 / 3, gamma_n=numpy.log(2) / 10, m_0=1, n_0=98):
        """
        Args:
            k_m (:obj:`float`, optional): mRNA synthesis rate constant (molecules h\ :sup:`-1`\ )
            k_n (:obj:`float`, optional): protein synthesis rate constant (\ :sup:`-1`\  h\ :sup:`-1`\ )
            gamma_m (:obj:`float`, optional): mRNA degradation rate constant (h\ :sup:`-1`\ )
            gamma_n (:obj:`float`, optional): protein degradation rate constant (h\ :sup:`-1`\ )
            m_0 (:obj:`float`, optional): initial mRNA number (molecules)
            n_0 (:obj:`float`, optional): initial protein number (molecules)
        """
        self.k_m = k_m
        self.k_n = k_n
        self.gamma_m = gamma_m
        self.gamma_n = gamma_n
        self.m_0 = m_0
        self.n_0 = n_0

    # reaction rates
    def r_m_syn(self, m, n):
        """ Calculate the mRNA synthesis rate

        Args:
            m (:obj:`float`): mRNA number (molecules)
            n (:obj:`float`): protein number (molecules)

        Returns:
            :obj:`float`: mRNA synthesis rate (molecules h\ :sup:`-1`\ )
        """
        return self.k_m

    def r_n_syn(self, m, n):
        """ Calculate the protein synthesis rate

        Args:
            m (:obj:`float`): mRNA number (molecules)
            n (:obj:`float`): protein number (molecules)

        Returns:
            :obj:`float`: protein synthesis rate (molecules h\ :sup:`-1`\ )
        """
        return m * self.k_n

    def r_m_deg(self, m, n):
        """ Calculate the mRNA degradation rate

        Args:
            m (:obj:`float`): mRNA number (molecules)
            n (:obj:`float`): protein number (molecules)

        Returns:
            :obj:`float`: mRNA degradation rate (molecules h\ :sup:`-1`\ )
        """
        return m * self.gamma_m

    def r_n_deg(self, m, n):
        """ Calculate the protein degradation rate

        Args:
            m (:obj:`float`): mRNA number (molecules)
            n (:obj:`float`): protein number (molecules)

        Returns:
            :obj:`float`: protein degradation rate (molecules h\ :sup:`-1`\ )
        """
        return n * self.gamma_n

    def sample_initial_conditions(self):
        """ Sample initial mRNA and protein copy numbers

        Returns:
            :obj:`tuple`:
                * :obj:`int`: initial mRNA copy number
                * :obj:`int`: initial protein copy number
        """
        m = numpy.random.poisson(self.k_m / self.gamma_m)
        n = numpy.round(numpy.random.gamma(self.k_m / self.gamma_n, self.k_n / self.gamma_m))
        return (m, n)

    def simulate(self, t_0=0., t_end=100., t_step=1.):
        """ Run the simulation

        Args:
            t_0 (:obj:`float`, optional): initial time (h)
            t_end (:obj:`float`, optional): end time (h)
            t_step (:obj:`float`, optional): frequency at which to record predicted mRNA and proteins

        Return:
            :obj:`tuple`:
                * :obj:`numpy.array`: simulation time (h)
                * :obj:`numpy.array`: predicted mRNA (molecules)
                * :obj:`numpy.array`: predicted proteins (molecules)
        """
        assert ((t_end - t_0) / t_step % 1 == 0)
        t_hist = numpy.linspace(t_0, t_end, int((t_end - t_0) / t_step) + 1)

        # data structure to store predicted copy numbers
        m_hist = numpy.full(t_hist.shape, self.m_0)
        n_hist = numpy.full(t_hist.shape, self.n_0)

        # initial conditions
        t = t_hist[0]
        m = self.m_0
        n = self.n_0

        # iterate over time
        while t < t_hist[-1]:
            # calculate reaction properties/rates
            propensities = numpy.array([
                self.r_m_syn(m, n),
                self.r_m_deg(m, n),
                self.r_n_syn(m, n),
                self.r_n_deg(m, n),
            ])
            total_propensity = numpy.sum(propensities)

            # select the length of the time step from an exponential distributuon
            dt = numpy.random.exponential(1. / total_propensity)

            # select the next reaction to fire
            i_reaction = numpy.random.choice(4, p=propensities / total_propensity)

            # update the time
            t += dt

            # update the copy numbers based on the selected reaction
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

        return (t_hist, m_hist, n_hist)

    def simulate_ensemble(self, n_trajectories=50, t_0=0., t_end=100., t_step=1.):
        """ Run multiple simulations

        Args:
            n_trajectories (:obj:`int`, optional): number of simulation to run
            t_0 (:obj:`float`, optional): initial time (h)
            t_end (:obj:`float`, optional): end time (h)
            t_step (:obj:`float`, optional): frequency at which to record predicted mRNA and proteins

        Return:
            :obj:`tuple`:
                * :obj:`numpy.array`: simulation time (h)
                * :obj:`numpy.array`: predicted mRNA (molecules)
                * :obj:`numpy.array`: predicted proteins (molecules)
        """
        assert ((t_end - t_0) / t_step % 1 == 0)
        t = numpy.linspace(t_0, t_end, int((t_end - t_0) / t_step) + 1)
        m = numpy.zeros((t.size, n_trajectories))
        n = numpy.zeros((t.size, n_trajectories))
        for i_trajectory in range(n_trajectories):
            self.m_0, self.n_0 = self.sample_initial_conditions()
            _, m[:, i_trajectory], n[:, i_trajectory] = self.simulate(t_0=t_0, t_end=t_end, t_step=t_step)

        return (t, m, n)

    def plot_trajectories(self, t, m, n):
        """ Plot multiple trajectories

        Args:
            t (:obj:`numpy.array`): simulation time (h)
            m (:obj:`numpy.array`): predicted mRNA (molecules)
            n (:obj:`numpy.array`): predicted proteins (molecules)

        Return:
            :obj:`matplotlib.figure.Figure`: figure
        """
        fig, axes = pyplot.subplots(nrows=2, ncols=1)

        n_trajectories = m.shape[1]

        for i_trajectory in range(n_trajectories):
            if n_trajectories == 1:
                gray = 0.
            else:
                gray = 0.5 - 0.5 * i_trajectory / (n_trajectories - 1)
            axes[0].plot(t, m[:, i_trajectory], color=(gray, gray, gray))
            axes[1].plot(t, n[:, i_trajectory], color=(gray, gray, gray))

        axes[0].set_xlim((t[0], t[-1]))
        axes[1].set_xlim((t[0], t[-1]))

        axes[0].set_ylim([0, numpy.max(m) + 1])
        axes[1].set_ylim([numpy.min(n) - 5, numpy.max(n) + 5])

        axes[1].set_xlabel('Time (h)')
        axes[0].set_ylabel('mRNA (molecules)')
        axes[1].set_ylabel('Protein (molecules)')

        return fig

    def plot_average_trajectory(self, t, m, n):
        """ Plot the average of multiple trajectories

        Args:
            t (:obj:`numpy.array`): simulation time (h)
            m (:obj:`numpy.array`): predicted mRNA (molecules)
            n (:obj:`numpy.array`): predicted proteins (molecules)

        Return:
            :obj:`matplotlib.figure.Figure`: figure
        """

        m_percentiles = numpy.zeros((t.size, 7))
        n_percentiles = numpy.zeros((t.size, 7))
        for i, _ in enumerate(t):
            m_percentiles[i, :] = [
                numpy.percentile(m[i, :], 1),
                numpy.percentile(m[i, :], 5),
                numpy.percentile(m[i, :], 33.33),
                numpy.percentile(m[i, :], 50),
                numpy.percentile(m[i, :], 66.67),
                numpy.percentile(m[i, :], 95),
                numpy.percentile(m[i, :], 99),
            ]
            n_percentiles[i, :] = [
                numpy.percentile(n[i, :], 1),
                numpy.percentile(n[i, :], 5),
                numpy.percentile(n[i, :], 33.33),
                numpy.percentile(n[i, :], 50),
                numpy.percentile(n[i, :], 66.67),
                numpy.percentile(n[i, :], 95),
                numpy.percentile(n[i, :], 99),
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

        axes[0].set_ylim([0, numpy.max(m) + 1])
        axes[1].set_ylim([numpy.min(n) - 5, numpy.max(n) + 5])

        axes[1].set_xlabel('Time (h)')
        axes[0].set_ylabel('mRNA (molecules)')
        axes[1].set_ylabel('Protein (molecules)')

        return fig

    def plot_mrna_protein_distribution(self, m, n):
        """ Plot the average of multiple trajectories

        Args:
            m (:obj:`numpy.array`): predicted mRNA (molecules)
            n (:obj:`numpy.array`): predicted proteins (molecules)

        Return:
            :obj:`matplotlib.figure.Figure`: figure
        """
        fig, axes = pyplot.subplots(nrows=2, ncols=1)

        kernel_m = stats.gaussian_kde(m.flatten())
        kernel_n = stats.gaussian_kde(n.flatten())
        m = range(int(numpy.min(m)), int(numpy.max(m)) + 1)
        n = range(int(numpy.min(n)), int(numpy.max(n)) + 1)
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

        return fig


def trajectory_exercise():
    sim = SsaSimulation()

    ##########################################################
    # Implement SSA
    ##########################################################
    sim.simulate

    ##########################################################
    # Simulate one trajectory
    ##########################################################
    # seed random number generator
    numpy.random.seed(0)

    # simulate
    t, m, n = sim.simulate_ensemble(1, t_end=5., t_step=0.001)

    # plot
    fig = sim.plot_trajectories(t, m, n)
    # fig.show()
    filename = os.path.join(OUT_DIR, 'mrna-and-protein-using-several-methods-trajectory-simulation.png')
    fig.savefig(filename, transparent=True, bbox_inches='tight')
    matplotlib.pyplot.close(fig)

    ##########################################################
    # Simulate several trajectories
    ##########################################################
    # simulate
    n_trajectories = 50
    t, m, n = sim.simulate_ensemble(n_trajectories, t_end=2., t_step=0.2)

    # plot
    fig = sim.plot_trajectories(t, m, n)
    # fig.show()
    filename = os.path.join(OUT_DIR, 'mrna-and-protein-using-several-methods-trajectory-simulations.png')
    fig.savefig(filename, transparent=True, bbox_inches='tight')
    matplotlib.pyplot.close(fig)

    ##########################################################
    # Plot the average of multiple trajectories
    ##########################################################
    fig = sim.plot_average_trajectory(t, m, n)
    # fig.show()
    filename = os.path.join(OUT_DIR, 'mrna-and-protein-using-several-methods-trajectory-average.png')
    fig.savefig(filename, transparent=True, bbox_inches='tight')
    matplotlib.pyplot.close(fig)

    fig = sim.plot_mrna_protein_distribution(m, n)
    # fig.show()
    filename = os.path.join(OUT_DIR, 'mrna-and-protein-using-several-methods-trajectory-histogram.png')
    fig.savefig(filename, transparent=True, bbox_inches='tight')
    matplotlib.pyplot.close(fig)
