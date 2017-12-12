Model representation
====================
There are multiple ways to represent a model.


Custom numerical simulation code
--------------------------------
At the lowest level, a model can be represented as a numerical simulation algorithm. For example, a stochastic model could be represented in Python code which implements the Gillespie algorithm. This approach provides a modeler with the most control over the numerical simulation of the model which can be helpful for efficiently simulating large models, but this approach leads to models that are difficult for other scientists to understand because they may need to read a large amount of code. Furthermore, because this approach
has the disadvantage that it requires the modeler devote significant time writing and testing a large amount of code.

Exercise
^^^^^^^^^
Write a program which implements the Gillespie algorithm and uses this to simulate a stochastic model.


Standard numerical simulation packages
--------------------------------------
Alternatively, models can be described more abstractly using a modeling language and then simulating using a simulator which is able to interpret that language. Continuing with our stochastic simulation example, one slightly more abstract way to represent a stochastic model is as a function which calculates the rate of each reaction and a vector of initial conditions. Models represented in this form can then be simulated with the `StochPy package <http://stochpy.sourceforge.net/>`_. Compared to the lowest level of representation, this approach requires significantly less code and less unit testing, freeing the modeler to focus more of their efforts on building models and using them to discovery biology. However, models described this way cannot easily be simulated by other simulators and this representation obscures the biological semantics of models.

Exercise
^^^^^^^^^
Write a program that uses StochPy to simulate a stochastic model.


Enumerated modeling languages
-----------------------------
Alternatively, models can be described using domain-specific modeling languages such as `CellML <https://www.cellml.org>`_ and `SBML (Systems Biology Markup Language) <http://sbml.org>`_ that are supported by many programs and that explicitly capture the biological semantics of models. SBML models are composed of the elements listed below, and the SBML specification precisely defines how to simulate models encoded in SBML which can be accomplished by compiling models to a lower level.

* Compartments
* Species
* Reactions
* Kinetic laws
* Parameters
* Rules
* Constraints
* Events
* Function definitions
* Unit definitions
* Annotations

This approach creates models that are much more comprehensible than models that are described directly in terms of their numerical integration. However, for large models this approach can require intractably many species and reactions to represent all possible states and reactions. Furthermore, this enumerated representation becomes highly inefficient when the state space gets very large.

Exercise
^^^^^^^^^
Encode the same stochastic model in SBML and simulate the model using `COPASI <http://copasi.org/>`_.


Ruled-based modeling languages
------------------------------
Alternatively, models can be described using rule patterns which describe families of related species and reactions. This enables large models with large state spaces to be concisely represented. This approach also emphasizes the biology/chemistry/physics which is pertinent to each rule. Furthermore, models that are described with rules can be efficiently simulated using network-free simulation which is an agent-based simulation technique which takes advantage of the typical low occupancy of models with large state spaces. The most popular rule-based modeling languages include `BioNetGen <http://bionetgen.org>`_ and `Kappa <http://dev.executableknowledge.org/>`_. The most popular network-free simulators including `NFSim <http://michaelsneddon.net/nfsim/>`_ and `KaSim <http://dev.executableknowledge.org/>`_.

However, all of the existing rule-based languages have a few critical limitations. First, they provide little support for semantic annotations. Second, they only support one specific type of combinatorial complexity, namely the combinatorial complexity that arises from having multiple binding sites per protein. In particular, the existing languages cannot easily described reactions that involve DNA, RNA, or protein sequences such as protein-DNA binding reactions.

Exercise
^^^^^^^^^
Encode the same stochastic model in BioNetGen.


Rule-based modeling API
-----------------------
The `PySB <http://pysb.org/>`_ rule-based modeling API overcomes some of the limitations of BioNetGen and Kappa by allowing modelers to define their own higher level abstractions which could be used to represent other types of combinatorial complexity. However, this requires modelers to develop their own unique higher level abstractions which again requires modeler to read lots of code to understand a model. Furthermore, models that are described in PySB have to be complied to BioNetGen models which diminishes the advantages of network-free simulation.

Exercise
^^^^^^^^^
Describe the same stochastic model with PySB.


High-level rule-based modeling language
---------------------------------------
To overcome the above limitations, we are developing a new higher-level rule-based modeling language and a corresponding higher-level network-free simulator.
