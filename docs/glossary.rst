##################
Appendix: Glossary
##################

.. glossary::
    :sorted:

    combinatorial complexity
        The large number of species and interactions that can occur in biological systems due to the noisy interfaces between biomolecules. Examples of combinatorial complexity include the large number of possible phosphorylation states of each protein; the large number of possible subunit compositions of each protein complex; the large number of RNA transcripts that can result from multiple transcription start and stop sites, splicing, RNA editing, and RNA degradation. To capture the combinatorial complexity of cell biology, WC models should be represented using rules and simulating using network-free simulation.
    
    continuous integration (CI)
        A method for finding errors quickly by executing unit tests each time a system is revised, typically each time a revised system is pushed to a version control system such as Git.

    curse of dimensionality
        The phenomenon that it is challenging to model high-dimensional systems due to sparsity of high-dimensional data and the combinatorial complexity of high-dimensional systems :cite:`keogh2011curse`.
    
    data model
        A description of the types of entities and the attributes of each type of entity, including attributes which describe relationships among types of entities.
        
        *See also:* :term:`schema`

    discrete event simulation (DES)
        A dynamical simulation framework in which the simulated system evolves in discrete steps that represented as event messages.

    flux balance analysis (FBA)
        A constraint-based framework that is frequently used to predict the steady state reaction fluxes of large metabolic networks.

    Gillespie's algorithm
        An algorithm for exactly simulating biochemical networks.
        
        *See also:* :term:`Stochastic Simulation Algorithm (SSA)`

    Stochastic Simulation Algorithm (SSA)
        An algorithm for exactly simulating biochemical networks.
        
        *See also:* :term:`Gillespie's algorithm`

    IUPAC International Chemical Identifier (InChI)
        A textual format for describing the structure of a chemical compound including its chemical formula, bond connectivity, protonation, charge, stereochemistry, and isotope composition.
        
        *See also:* :term:`simplified molecular-input line-entry system (SMILES)`

    Minimum Information About a Simulation Experiment (MIASE)
        Standard for the minimum metadata that should be recorded about a simulation experiment :cite:`waltemath2011minimum`.

    multi-algorithmic simulation
        A simulation in which multiple submodels are simultaneously simulated using different simulation algorithms such as ODE integration, SSA, and FBA :cite:`takahashi2004multi`. Multi-algorithmic simulations are frequently used to simultaneously simulate both well-characterized pathways with fine-grained simulation algorithms and poorly-characterized pathways with coarse-grained simulation algorithms.

    model calibration
        The process of determining the parameters values of models, typically by numerically minimizing the distance between model predictions and experimental observations.

    model organism database
        A database that contains integrated experimental information about a single species.

        *See also:* :term:`pathway/genome database (PGDB)`

    model reduction
        The process of reducing a model to reduced model.
        
        *See also:* :term:`reduced model`

    network-free simulation
        A methodology for efficient stochastic simulation of models that are described using rules. In contrast to conventional simulation methods which enumerate the entire reaction network (each species and each reaction) prior to simulation, network-free simulations dynamically discover the reaction network during simulation as states become occupied and reactions gain non-zero propensities. Network-free simulation is particularly effective for simulating combinatorially large state spaces that are sparsely occupied by small numbers of particles.

    ontology
        A controlled vocabulary of terms, as well as the relationships among the terms. For example, the Unit of Measurement Ontology (UO) defines standard names for several common units and their relationship to the SI units and prefixes.

    parallel discrete event simulation (PDES)
        A parallel implementation of discrete event simulation.

    pathway/genome database (PGDB)
        A model organism database that contains integrated experimental information about the molecular biology of a single species such as its genome sequence, genes, protein complexes, and metabolic reactions.

        *See also:* :term:`model organism database`

    provenance
        Metadata about the origin of data or models such as how a model was developed including who developed the model; when the model was developed; and the data source, assumptions, and design decisions that were used to build the model.

    reaction network modeling
        The conventional, low-level representation of biochemical models which enumerates each individual species and each individual reaction. In contrast, rule-based modeling is an abstraction for representing reaction networks in terms of species and reaction patterns that can generate all of the individual species and reactions.

    reconstruction
        The process of determining the molecular species and reactions of a biological process.

    reduced model
        A smaller, less complex, and/or computationally cheaper model that approximates the behavior of the original model. Reduced models can be created either by lumping species, reactions, and/or parameters to create a second smaller, mechanistic model or by fitting model predictions to a smaller data-driven model.
        
        *See also:* :term:`model reduction`

    rule-based modeling
        An abstraction for representing models in terms of species and reaction patterns which describe multiple individual species and reaction instances. Rule-based modeling is particularly effective for describing models with large numbers of species and reactions that emerge from the combinatorial interactions among species. Rule-based models can be simulated using conventional methods by statistically enumerating the reaction network or using network-free simulation which dynamically discovers the reaction network during simulation.    

    schema
       A description of the types of entities and the attributes of each type of entity, including attributes which describe relationships among types of entities.
       
       *See also:* :term:`data model`

    simplified molecular-input line-entry system (SMILES)
        A textual format for describing the structure of a chemical compound. However, we recommend using InChI rather than SMILES because InChI is an open standard.
        
        *See also:* :term:`IUPAC International Chemical Identifier (InChI)`

    Stochastic Simulation Algorithm (SSA)
        An algorithm for exactly simulating biochemical networks.

    surrogate model
        A, typically computationally cheaper, model which approximates the behavior of another model.
        
        *See also:* :term:`model reduction`, :term:`reduced model`

    Systems Biology Markup Language (SBML)
        An extensible format for describing cell models in terms of species and reactions.

    test coverage
        The fraction of a system which is tested by a set of unit tests. To verify that a system is implemented correctly, 100% of the system should be tested. For example, computer code should be verified by testing every line of code and ranch. Similarly, models should be verified by testing the behavior of each species, reaction, and submodel at the edge cases of each rate law.

    unit testing
        A methodology for organizing multiple tests to verify that a system is implemented correctly. These tests typically consist of tests of individual components, groups of components, and the entire system. For example, tests of model can test individual species, reactions, and submodels, as well as groups of submodels and entire models.

    validation
        The process of checking that a system fulfills its intended purpose. For example, models can be validated by checking that they recapitulate the true biology (i.e., independent experimental data that was not used for model construction).

    verification
        The process of checking that a system is implemented correctly. For example, models can be verified by checking that they recapitulate the known biology (i.e., the data that was used for model construction).

    version control
        A methodology for tracking and merging changes to one or more documents which facilitates collaboration development of large systems such as models. One of the most popular version control systems for computer code is Git.
