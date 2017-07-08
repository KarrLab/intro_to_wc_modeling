Model composition
=================
Abstraction and composition are essential strategies for building large engineered systems such as big software programs. Abstraction allows engineers to build highly functional systems with complex and sophisticated internal implementations while only exposing
the functional features that users of the systems need.
The exposed features are called the system's external interface.
Accessing the interface lets users obtain all the benefits of a system's
sophisticated implementation without needing to understand the
implementation.
For example, the Python collection data structures like list, dictionary, and set are all built using sophisticated implementations, but
Python programmers just use simple operations like insert, find and delete.

Composition of abstracted modules enables engineers to build complex systems by combining multiple parts, each of which has a simple external interface. In this way, abstraction and composition enable engineers to transform challenging high-dimensional problems into multiple, simpler lower dimensional problems. In particular, abstraction and composition enable teams of engineers to collaboratively build complex systems by enabling smaller groups or individual engineers to independently and simultaneously building individual components.

Because models are engineering software systems, abstraction and composition can also be powerful approaches to build large models. In particular, abstraction and composition can enable teams of modelers to work together to build large models by enabling smaller groups of modelers to model individual components.

Biological pathways are natural subsystems to abstract in dynamical biochemical models because they tend to interact tightly on fast timescales, and teams of microbiologists tend to focus their expertise on pathways.
Furthermore, composition of
models of pathways is a reasonable approximation due to the relatively fast dynamics of individual cellular pathways compared to dynamics of interactions between pathways. For example, the timescale of transcription is :math:`10^{1}` s whereas the timescale of the transcriptome, which is the timescale of the impact of RNA on translation, is :math:`10^2` s.

Broadly, there are two types of model composition: composition of mathematically-like models and composition of mathematically-dissimilar models into hybrid or multi-algorithmic models. Mathematically-like models can be merged analytically simply by taking the union of their variables/species and equations/reactions. Mathematically-dissimilar models must be merged computationally by concurrently integrating the individual models. In addition to merging models mathematically and/or computationally, it is often also necessary to align the models to a common namespace and representation.


Model composition procedure
---------------------------
Below are the five steps to merging models

#. Align the models to a common namespace and representation.

    #. Annotate the species and reactions using a common ontology
    #. Identify the common species and reactions
    #. Convert all models into explicit time-driven models. For example, convert Boolean models into stochastic models by assuming typical time and copy number scales.
    #. Resolve all conflicting species or reactions such as species or reactions that are represented with different granularities across the models

#. Mathematically and/or computationally merge the aligned models

    #. Merge all of the mathematically-like models analytically by computing the unions of their species and reactions. For example, ODE models can be merged by taking the union of the state variables and summing the differentials across the models.
    #. Computationally merge the groups of mathematically-dissimilar models by using a hybrid or multi-algorithmic simulator to simultaneously integrating the models.


Software tools
--------------

* Model merging

    * semanticSBML: helps users annotate models and identify common elements
    * SemGen: helps users annotate models and identify common elements

* Numerical simulation of composite multi-algorithmic models

    * E-Cell: multi-algorithmic simulator
    * iBioSim: implements a hierarchical SSA algorithm that can simulate merged SSA models
    * COPASI: partitions a biochemical network into a high partical count subnet simulated by ODE and a low particle count subnet simulated by SSA


Exercises
---------

* Obtain COPASI and create and run a hybrid simulation
* Download and install SemGen
* Obtain the SemGen paper
* Use SemGen to replicate the model merging example described in the paper
