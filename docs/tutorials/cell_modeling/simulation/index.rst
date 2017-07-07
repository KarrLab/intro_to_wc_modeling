Mathematical representations and simulation algorithms
======================================================

There is wide range of mathematical representations that can be used model cells, ranging from coarse-grained representations such as Boolean networks to fine-grained representations such as spatial stochastic models. Below are several considerations for choosing a mathematical representation for a model.

* What is the model's purpose? What properties of the cell are being analyzed by the model?
* What are the relevant physical scales of the biology? Deterministic models are valid approximations when the fluctuations are small which often occurs when the flux scale is large. Conversely, stochastic models should be used when the fluctuations are large and/or they critically impact behavior.
* How much information is known about the biology? If significant information is known, then fine-grained models are possible. Conversely, if the biology is not well-characterized a fine-grained representation may be infeasible and a coarse-grained representation should be used.
* How much computational cost is acceptable? If you need a model to execute quickly or you anticipate running large numbers of simulations, it may be best to use a coarse-grained representation. Alternatively, if you want to build the most detailed model possible, you should use a fine-grained representation.
* What simulation software tools are available? Several tools are available to simulate single-algorithm models. However, there are few tools for simulating hybrid models. If you don't want to spend a lot of energy writing numerical simulation code, we recommend you focus on well-established mathematical representations.

The goal of this tutorial is to introduce you to the most common mathematical representations, simulation algorithms, simulation experiment description formats, and simulation software programs for cell modeling. In addition, this tutorial will highlight the advantages and disadvantages of each method and tool, particularly for large-scale modeling.


Boolean/logical models
----------------------
Boolean models are composed of composed Boolean variables and logical functions which describe how the value of each variable is influenced by other variables. Logical or multi-level models are a generalization of Boolean models in which the variables can have two or more possible values. Importantly, Boolean models have no quantitative parameters or explicit timescales. Similarly, logical models have few quantitative parameters. Consequently, Boolean and logical models are often used to describe biological systems that have not yet been quantitatively characterized, as well as to build large models that contain many more variables/species and functions/interactions than could be calibrated in a more quantitative model.

Boolean models are simulated with timestep algorithms which divide simulations into many small timesteps during which the logical functions are evaluated and the Boolean variables are updated according to a specific *update scheme*. Below are some of the most commonly used update schemes:

* Synchronous updating: during each timestep, all of the functions are evaluated with the same node states and all of the nodes are updated with the results of the functions
* Asynchronous updating: during each timestep, only one or a subset of the logical functions are evaluated and only the corresponding subset of nodes are updated

    * Deterministic asynchronous updating: the timesteps iterate over the functions/rules in a deterministic order
    * Random asynchronous updating: at each timestep, the simulator randomly chooses one or more functions/nodes to update

There are also several generalizations of Boolean and logical-valued models including probabilistic Boolean models that describe each variable as a probability and temporal Boolean models that have explicit time scales.


Ordinary differential equations (ODEs)
--------------------------------------
Ordinary differential equations (ODEs) is one of the most commonly used approaches for modeling dynamical systems. ODE models are based on microscopic analyses of how the concentration of each species in the cell changes over time in response to the concentrations of other species. Because ODE assume that cells are well-mixed and that they behave deterministically, ODE models are most appropriate for small systems that involve large concentrations and high fluxes. 

ODE models can be simulated by numerically integrating the differential equations. The most basic ODE integration method is Euler's method. Euler's method is a time stepped algorithm in which the next state is computed by adding the current state and the multiplication of the current differentials with the timestep.

.. math::

    y(t+\Delta t) = y(t) + \Delta t \frac{dy}{dt}

Euler's method estimates :math:`y(t+\Delta t)` using a first-order approximation. ODE models can be simulated more accurately using higher order estimates, or Taylor series, of :math:`y(t+\Delta t)`. One of the most popular algorithms which implements this approach is the Runge-Kutta 4th order method. Yet more advanced integration methods select the time step adaptively. Some of the most sophisticated ODE integration packages include ODEPACK (lsoda) and Sundials (vode). These packages can be used in Python via scipy's integrate module.


Stochastic simulation
---------------------
Like ODE models, stochastic models are based on microscopic analyses of how the concentration of each species in the cell changes over time in response to the concentrations of other species. However, stochastic simulation algorithms relax the assumption that cells behave deterministically. Instead, stochastic simulation algorithms assume that the rate of each reaction is Poisson-distributed. As a result, stochastic simulation algorithms generate sequences of reaction events at which the state of the cell discretely changes.

Because stochastic simulations are random, stochastic models should generally be simulated multiple times to sample the distribution of predicted cell behaviors. In general, these simulations should be run both using different random number generator seeds and different random initial conditions.

Stochastic simulation should be used to model systems that are sensitive to small fluctuations such as systems that involve small concentrations and small fluxes. However, stochastic simulation can be computationally expensive for large numbers due to the needs to resolve the exact order of every reaction and the need to run multiple simulations to sample the distribution of predicted cell behaviors.

Gillespie Algorithm / Stochastic Simulation Algorithm / Direct Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Below is pseudo-code for the simplest stochastic simulation algorithm which is also known as the Gillespie algorithm::
    
    import numpy

    # represent the reaction and rate laws of the model
    reaction_stochiometries = numpy.array([ ... ])
    kinetic_laws = [...]

    # initialize the time and cell state
    time = 0
    copy_numbers = numpy.array([ ... ])
    
    while time < time_max:
        # calculate reaction properties/rates
        propensities = [kinetic_law(copy_numbers) for kinetic_law in kinetic_laws]
        total_propensity = sum(propensities)

        # select the length of the time step from an exponential distributuon
        dt = numpy.random.exponential(1 / total_propensity)

        # select the next reaction to fire
        i_reaction = numpy.random.choice(len(propensities), p=propensities / total_propensity)
        
        # reject the selected reaction if there are insufficient copies of the reactants for the reaction

        # update the time and cell state based on the selected reaction
        time += dt
        copy_numbers += reaction_stochiometries[:, i_reaction]

Tau leaping
^^^^^^^^^^^
In addition to the Gillespie algorithm, there are many algorithms which approximate its results with significantly lower computational costs. One of the most common of these approximate simulation algorithms is the `tau-leaping algorithm <https://en.wikipedia.org/wiki/Tau-leaping>`_. The tau-leaping is a time-stepped algorithm similar to Euler's method which samples the number of firings of each reaction from a Poisson distribution with lambda equal to the product of the propensity of each reaction and the time step. Below is pseudocode for the tau-leaping algorithm::

    # represent the reaction and rate laws of the model
    reaction_stochiometries = numpy.array([ ... ])
    kinetic_laws = [...]
    
    # select the desired time step
    dt = 1
   
    # initialize the simulated state
    time = 0
    copy_numbers = numpy.array([...])
    
    # iterate over time
    while time < time_max:
        # calculate the rate of each reaction
        propensities = [kinetic_law(copy_numbers) for kinetic_law in kinetic_laws]
        
        # sample the number of firings of each reaction
        n_reactions = numpy.random.poisson(propensities * dt)
        
        # adjust the time step or reject reactions for which there are insufficient reactants
        
        # advance the time and copy numbers
        time += dt
        copy_numbers += reaction_stochiometries * n_reactions
        
The tau-leaping algorithm can be improved by adpatively optimizing time step:

.. math::
   
    g_i &= -\min_j { S_{ij} } \\
    \mu_i &= \sum_j { S_{ij} R_j (x) } \\
    \sigma_i^2 &= \sum_j { S_{ij}^2 R_j (x) } \\
    dt &= \min_i { \left\{ 
            \frac{
                \max{ \left\{ 
                    \epsilon x_i / g_i, 1 
                \right\} }  
            }{
            |\mu_i (x)|
            }  ,
            \frac{
                \max { \left\{
                    \epsilon x_i / g_i, 1 
                \right\} }^2
            }{
            \sigma_i^2
            }  
        \right\} } \\
        
where :math:`x_i` is the copy number of species :math:`i`, :math:`S_{ij}` is the stochiometry of species :math:`i` in reaction :math:`j`, :math:`R_j (x)` is the rate law for reaction :math:`j`, and :math:`\epsilon \approx 0.03` is the desired tolerance.


Network-free simulation
-----------------------
Network-free simulation is a variant of stochastic simulation for simulating rule-based models in which the occupied species and active reactions are discovered dynamically during simulation rather than statistically enumerating all possible species and reactions prior to simulation. Network-free simulation is a mathematically equivalent algorithm for stochastic simulation. The key advantage of network-free simulation is that it can simulate models with very large or infinitely large state state spaces that cannot be simulated with conventional simulation algorithms.


Flux balance analysis (FBA)
---------------------------
Flux balance analysis (FBA) is a popular approach to simulating metabolism. Like ODE models, FBA is based on microscopic analyses of how the concentration of each species in the cell changes over time in response to the concentrations of other species. However, FBA leverages two additional sets of data and two additional assumptions. First, FBA incorporates estimates of the minimum and maximum possible flux of each reaction which, for a subset of reactions, can be obtained from experimental observations. Second, FBA incorporates an additional reaction which represents the assembly of metabolites into a cell and can be calibrated based on the observed cellular composition. Third, FBA assumes that the each species is at steady-state (:math:`\frac{dx}{dt} = 0`). This assumptions greatly constrains the model, thereby reducing the amount of data needed to build the model. However, this assumption also prevents FBA from making predictions about the dynamics of metabolic networks. Fourth, FBA assumes that cells have evolved to grow maximally fast. Together, these additional data and assumptions pose cell simulation as a linear optimization problem which can be solved using linear programming.

.. math::

    \text{Maximize}~ v_\text{growth} &= f' v \\
    \text{Subject to}~\\
    S v &= 0 \\
    v^\text{min} &\leq v \leq v^\text{max}, \\

where :math:`S_{ij}` is the stochiometry of species :math:`i` in reaction :math:`j`, :math:`v_j` is the flux of reaction :math:`j`, :math:`v^\text{min}_{j}` and :math:`v^\text{max}_j` are the upper and lower bounds of the flux of reaction :math:`j`, and :math:`f_\mu` is 1 for the biomass composition and 0 otherwise.

In addition, there are a variety of generalizations of FBA for using genomic and other experimental data to generate more accurate flux bounds (see `review <https://doi.org/10.1371/journal.pcbi.1003580>`_), dynamic FBA simulations (dFBA), and combined regulatory and FBA metabolism simulations (`rFBA <http://doi.org/10.1038/nature02456>`_, `PROM <http://doi.org/10.1073/pnas.1005139107>`_).

dFBA enables dynamic simulations by (1) assuming that cells quickly reach pseudo-steady states with their environment because their internal dynamics are significantly faster than that of the external environment, (2) iteratively forming and solving FBA models, and (3) updating the extracellular concentrations based on the predicted fluxes. Below is pseudo-code for dFBA::

    Set the initial biomass concentration
    Set the initial conditions of the environment
    From the starting time to the final time
        Set the upper and lower bounds of the exchange reactions based on the currnt biomass concentration and environmental conditions
        Solve for the maximum growth rate and optimal fluxes
        Update the biomass concentration based on the predicted growth rate
        Update the environmental conditions based on the predicted exchange fluxes


Multi-algorithmic simulation
----------------------------
To efficiently simulate entire cells, we must represent each aspect of a cell using the most appropriate mathematics and concurrently integrate or co-simulate the combined hybrid or multi-algorithmic model. For example, we must represent transcription as a stochastic model and represent metabolism as an FBA model. Hybrid simulation is an open area of research. Below is a summarize of several increasingly sophisticated hybrid simulation algorithms.

* Serial simulation: Divide the simulation into multiple small time steps. Within each time step, iteratively simulate the submodel and update the cell state. Optionally, simulate the models in a random order at each time step. This is a simple algorithm to implement. However, this algorithm violates the arrow of time by integrating submodels based on different states within each time step.
* Partitioning and merging: Divide the simulation into multiple small time steps. With each time step, partition the pool of each species into separate pools for each submodel. Simulate the submodels independently using the independent pools. Update the global species pools by merging the submodel pools. Species can be partitioned uniformly, based on their utilization during the previous time point, or based on a preliminary integration of the submodels. This is a relatively simple algorithm to implement for models whose state only represents concentrations and/or species copy number. However, it can be challenging to partition and merge rule-based models whose states are represented by graphs.
* Interpolation: For models that are composed of one discrete and one continuous model, we can append the continuous model to the discrete model as a single pseudo reaction, fire the reaction immediately after each discrete reaction, and periodically calculate the coefficients of the pseudo reaction by numerically integrating the continuous model. Furthermore, we could adaptive choose the frequency at which the continuous model is simulated based on the sensitivity of its predictions to its inputs from the discrete model. Overall, we believe this algorithm provides a good balance of accuracy and speed.
* Scheduling: Build a higher-order stochastic model which contains one pseudo-reaction per submodel. Set the propensity of each pseudo-reaction to the total propensity of the submodel. Use the Gillespie method to schedule the firing of the pseudo-reactions/submodels. This is the strategy used by E-Cell (Takahashi et al., 2004).
* Upscaling: For models that are composed of one discrete and one continuous model, we can append all of the continuous reactions model to the discrete model; periodically set their propensities by evaluating their kinetic laws, or in the case of FBA, calculating the optimal flux distribution; and select and fire the continuous reactions using the same mechanism as the discrete reactions. This algorithm is compelling, but is computationally expensive due to the need to resolve the order of every reaction including every continuous reaction.


Simulating individual submodels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For calibration and testing, it is useful to simulate individual submodels of a larger model. To meaningfully simulate a submodel, you must `mock` the impact of all of the other submodels that the submodel interacts with. This can be done by creating coarse-grained versions of all of the other submodels which mimic their external behavior at a lower computational cost.


Reproducing stochastic simulations
----------------------------------
To run stochastic simulations reproducibly, every simulation input must be identical, including the order in which the reactions are defined and the state of the random number generator.

The state of the ``numpy`` random number generator can be set using the ``seed`` method::

    numpy.random.seed(0)


Simulation descriptions
-----------------------
To simulate a model, we must specify every aspect of the simulation including 

* The model that we want to simulate
* Any modifications of the model that we wish to simulate (e.g. modified parameter values)
* The initial conditions of the simulation
* The desired simulation algorithm
* The parameters of the simulation algorithm such as the initial seed and state of the random number generator

The `Simulation Experiment Description Markup Language <http://sed-ml.org>`_ (SED-ML) is one of the most commonly used languages for describing simulations. SED-ML is primarily designed to describe simulations of XML-based models such as models encoded in CellML and SBML. However, SED-ML can be used to describe the simulation of any model. `Simulation Experiment Specification via a Scala Layer <http://sessl.org>`_ (SESSL) is competing langauge simulation description language. 


Software tools
--------------
Below is a list of some of the most commonly used simulation software programs for cell modeling:

* Desktop programs:
    
    * `CellNOpt <http://www.cellnopt.org/>`_: Boolean simulator    
    * `COPASI <http://copasi.org>`_: ODE and stochastic simulator
    * `ECell <http://www.e-cell.org>`_: multi-algorithmic simulator    
    * `iBioSim <http://www.async.ece.utah.edu/ibiosim>`_
    * `NFSim <http://michaelsneddon.net/nfsim/>`_: stochastic network-free simulator
    * `VCell <http://vcell.org/>`_: ODE, stochastic, and spatial simulator

* Web-based programs

    * `Cell Collective <https://cellcollective.org>`_: online Boolean simulator
    * `JWS Online <http://jjj.biochem.sun.ac.za/>`_: online ODE and stochastic simulator    

* Python libraries
    
    * `BooleanNet <https://github.com/ialbert/booleannet>`_: Boolean simulation
    * `COBRApy <https://opencobra.github.io/>`_: FBA simulation
    * `libRoadRunner <http://libroadrunner.org/>`_: ODE simulation
    * `LibSBMLSim <http://fun.bio.keio.ac.jp/software/libsbmlsim/>`_: ODE simulation
    * `PySB <http://pysb.org/>`_: rule-based simulation
    * `StochPy <http://pythonhosted.org/StochPy/>`_: stochastic simulation


Exercises
---------

Required software
^^^^^^^^^^^^^^^^^
For Ubuntu, the following commands can be used to install all of the software required for the exercises::

    sudo apt-get install \
        python \
        python-pip
    sudo pip install \
        matplotlib \
        numpy \
        optlang \
        scipy


Boolean simulation
^^^^^^^^^^^^^^^^^^
In this exercise we will simulate the gene Boolean network shown below using both synchronous and asynchronous updating.

.. image:: boolean-model.png

First, define a set of functions which represent the edges of the network::
    
    regulatory_functions = {
        'A': lambda nodes: not nodes['C'],
        'B': lambda nodes: not nodes['A'],
        'C': lambda nodes: not nodes['B'],
    }

Second, define the initial state of the network::

    initial_state = {
        'A': False,
        'B': True,
        'C': True
    }

Third, write a Boolean simulator and synchronous, asynchronous deterministic, and asynchronous random update schemes by completing the code fragments below::

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

        # initialize data structures to store predicted time course and copy initial state to state history
        ...

        # set current state to initial state
        ...

        # iterate over time steps
        for step in range(1, n_steps + 1):
            # update state according to :obj:`update_scheme`
            ...

            # store current value
            ...

        # return predicted dynamics
        ...


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
        ...

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
        ...
        
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
        ...
        
        # return state
        return current_state

Fourth, seed numpy's random number generator so that we can reproducibly simulate the model::

    numpy.random.seed(0)

Fifth, use the simulation functions to simulate the model::

    n_steps = 10
    sync_time_hist, sync_hist = simulate(regulatory_functions, initial_state, 20, sync_update_scheme)
    det_async_time_hist, det_async_hist = simulate(regulatory_functions, initial_state, 20 * 3, deterministic_async_update_scheme)
    rand_sync_time_hist, rand_sync_hist = simulate(regulatory_functions, initial_state, 20 * 3, random_async_update_scheme)

    det_async_time_hist = det_async_time_hist / 3
    rand_sync_time_hist = rand_sync_time_hist / 3

Next, use ``matplotlib`` to plot the simulation results. You should see results similar to those below.

..
    todo: plot values as step functions

.. image:: boolean-results.png

Finally, compare the simulation results from the different update schemes. How do they differ? Which ones reach steady states or repitive oscillations?


ODE simulation
^^^^^^^^^^^^^^
In this exercise we will use lsoda to simulate the Goldbeter 1991 cell cycle model of cyclin, cdc2, and cyclin protease (`doi: 10.1073/pnas.88.20.9107 <https://doi.org/10.1073/pnas.88.20.9107>`_, `BIOMD0000000003 <http://www.ebi.ac.uk/biomodels-main/BIOMD0000000003>`_).

.. image:: ode-model.png

First, open the `BioModels entry <http://www.ebi.ac.uk/biomodels-main/BIOMD0000000003>`_ for the model in your web browser. Identify the reactions, their rate laws, the parameter values, and the initial conditions of the model. Note, that the model uses two assignment rules for :math:`V1` and :math:`V3` which are not displayed on the BioModels page. These assignment rules must be identified from the SBML version of the model which can be exported from the BioModels page.

Second, write a function to calculate the time derivative of the cyclin, cd2, and protease concentrations/activities by completing the code fragment below::

    def d_conc_d_t(concs, time):
        """ Calculate differentials for Goldbeter 1991 cell cycle model 
        (`BIOMD0000000003 <http://www.ebi.ac.uk/biomodels-main/BIOMD0000000003>`_)

        Args:
            time (obj:`float`): time
            concs (:obj:`numpy.ndarray`): array of current concentrations

        Returns:
            :obj:`numpy.ndarray
        """
        ...

Next, create a vector to represent the initial conditions by completing this code fragment::

    init_concs = ...

Next, use ``scipy.integrate.odeint`` which implements the lsoda algorithm to simulate the model by completing this code fragment::

    time_max = 100
    time_step = 0.1
    time_hist = numpy.linspace(0., time_max, time_max / time_step + 1)
    conc_hist = scipy.integrate.odeint(...)

Finally, use ``matplotlib`` to plot the simulation results. You should see results similar to those below.

.. image:: ode-results.png


Stochastic simulation
^^^^^^^^^^^^^^^^^^^^^
In this exercise we will simulate the stochastic synthesis and degradation of a single RNA using the Gillespie algorithm.

.. math::

    \text{Synthesis:}~\emptyset &\rightarrow \text{mRNA} \\
    \text{Degradation:}~\text{mRNA} &\rightarrow \emptyset \\
    r_\text{syn} &= k_\text{syn}\\
    r_\text{deg} &= k_\text{deg} \text{mRNA}\\
    k_\text{syn} &= 2.5\,\text{s}^{-1}\\
    k_\text{deg} &= 0.5\,\text{s}^{-1}\,\text{molecule}^{-1}\\
    \text{mRNA}(t=0) &= 10\,\text{molecules} \\ 

First, define data structures to represent the stoichiometries are rate laws of the reactions::

    reaction_stochiometries = [1, -1]

    k_syn = 2.5 # 1/s
    k_deg = 0.5 # 1/s/molecule
    def kinetic_laws(copy_number):
        return numpy.array([
            k_syn, 
            k_deg * copy_number,
            ])

Second, define the initial copy number::

    init_copy_number = 10

Third, implement the Gillepsie algorithm by completing the code skeleton below::

    def simulate(reaction_stochiometries, kinetic_laws, init_copy_number, time_max, time_step):
        """ Run a stochastic simulation

        Args:
           reaction_stochiometries (:obj:`list` of :obj:`int`): list of stoichiometries of the protein in each reaction
           kinetic_laws (:obj:`list` of :obj:`function`): list of kinetic law function
           init_copy_number (:obj:`int`): initial copy number
           time_max (:obj:`float`): simulation length
           time_step (:obj:`float`): freuency to record predicted dynamics

        Returns:
            :obj:`tuple`:

                * :obj:`numpy.ndarray`: time points
                * :obj:`numpy.ndarray`: predicted copy number at each time point
        """

        # data structure to store predicted copy numbers
        time_hist = numpy.linspace(0., time_max, time_max / time_step + 1)
        copy_number_hist = numpy.full(int(time_max / time_step + 1), numpy.nan)
        copy_number_hist[0] = init_copy_number

        # initial conditions
        time = 0
        copy_number = init_copy_number

        # iterate over time
        while time < time_max:
            # calculate reaction properties/rates
            propensities = ...

            # calculate total propensity
            total_propensity = ...

            # select the length of the time step from an exponential distributuon
            dt = ...

            # select the next reaction to fire
            i_reaction = ...

            # update the time and copy number based on the selected reaction
            time += ..
            copy_number += ...

            # store copy number history
            #print(time)
            if time < time_max:            
                copy_number_hist[int(numpy.ceil(time / time_step)):] = copy_number

        return (time_hist, copy_number_hist)

Fourth, seed random number generator so that we can reproducibly simulate the model::

    numpy.random.seed(0)

Fifth, use the ``simulate`` function to run 100-25 s simulations, store the results, and use ``matplotlib`` to visualize the results. You should see results similar to those below.

.. image:: stochastic-results.png

Finally, examine the result simulation results. Is the simulation approaching steady-state? How could you analytically calculate the steady-state?


Network-free simulation of rule-based models
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Please see the `PySB tutorial <http://pysb.readthedocs.io/en/latest/tutorial.html>`_ to learn about how to simulate rule-based models from Python


FBA simulation
^^^^^^^^^^^^^^
In this exercise we will use the ``optlang`` package to simulate the mock metabolic dFBA model illustrated below.

.. image:: fba-model.png

First, create an ``optlang`` model::

    # import optlang
    import optlang

    # create a model
    model = optlang.Model()

Second, add a variable for each reaction flux. For example, the following two commands will create variables for the glucose transport and exchange reactions::

    glc_tx = optlang.Variable('glc_tx', lb=0)
    glc_ex = optlang.Variable('glc_ex', lb=0)

Next, add a constraint to represent the rate of change of each species. For example, the following command will create a variable for the rate of change of the extracellular concentration of glucose and constrain that rate to zero::

    glc_e = optlang.Constraint(glc_ex - glc_tx, lb=0, ub=0)
    model.add([glc_e])

Next, set the objective to maximize growth::

    model.objective = optlang.Objective(growth, direction='max')

Next, set the initial conditions::

    init_conc_glc_e = 200.
    init_conc_aa_e = 120.
    init_conc_biomass = 1.

Next, setup a data structure to store the predicted concentrations::

    time_max = 70
    time_hist = numpy.array(range(time_max + 1))
    flux_hist = numpy.full((time_max + 1, len(model.variables)), numpy.nan)
    growth_hist = numpy.full(time_max + 1, numpy.nan)
    conc_hist = numpy.full((time_max + 1, 3), numpy.nan)

Next, complete the code fragment below to simulate the model::

    variable_names = model.variables.keys()
    conc_glc_e = init_conc_glc_e
    conc_aa_e = init_conc_aa_e
    conc_biomass = init_conc_biomass
    for i_time in range(time_max + 1):
        # constrain fluxes based on avialable nutrients
        glc_tx.ub = ...
        aa_tx.ub = ...

        # solve for the maximum growth and optimal fluxes
        status = model.optimize()
        assert(status == 'optimal')

        # store history
        growth_hist[i_time] = model.objective.value
        for i_var, var_name in enumerate(variable_names):
            flux_hist[i_time, i_var] = model.variables[var_name].primal

        conc_hist[i_time, 0] = conc_glc_e
        conc_hist[i_time, 1] = conc_aa_e
        conc_hist[i_time, 2] = conc_biomass

        # update concentrations
        conc_glc_e -= ...
        conc_aa_e -= ...
        conc_biomass += ...

Next, use ``matplotlib`` to plot the predicted concentration dynamics. You should see results similar to those below.

.. image:: fba-results.png


Hybrid simulation
^^^^^^^^^^^^^^^^^
* Write a hybrid FBA/SSA simulator
* Build a composite model and simulate one of its submodels by coupling it to coarse-grained versions of all of the other submodels
