Model composition
=================
Abstraction and composition are essential strategies for building large engineered systems such as software programs. Abstraction allows engineers to build complex systems with sophisticated internal details and only expose a few relevant details about their external interfaces to other engineers, allowing other engineers to ignore much of their internal details. Composition enables engineers to build complex systems by combining multiple parts, each which has a simple external interface. In this way, abstraction and composition enable engineers to transform challenging high-dimensional problems into multiple, simpler lower dimensional problems. In particular, abstraction and composition enable teams of engineers to collaboratively build complex systems by enabling individual engineers to independently and simultaneously building individual components.

Because models are engineering software systems, abstraction and composition can also be powerful approaches to build large models. In particular, abstraction and composition can enable teams of modelers to work together to build large models by enabling individual modelers to model individual components. Furthermore, abstraction and composition are reasonable approximations due to the relatively fast dynamics of individual cellular pathways compared to dynamics of interactions between pathways. For example, the time scale of transcription is :math:`10^{1}` s whereas the time scale of the transcriptome, which is the timescale of the impact of RNA on translation, is :math:`10^2` s.

Broadly, there are two types of model composition: composition of mathematically-like models and composition of mathematically-dissimilar models into hybrid or multi-algorithmic models. Mathematically-like models can be merged analytically simply by taking the union of their variables/species and equations/reactions. Mathematically-dissimilar models must be merged computationally by concurrently integrating the individual models. In addition to mathematically and/or computationally merging models, it is often also necessary to align the models to a common namespace and representation.


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
    #. Computationally merge the groups of mathematically-dissimilar models by simultaneously integrating the models.


Software tools
--------------

* Model merging

    * semanticSBML: helps users annotate models and identify common elements
    * SemGen: helps users annotate models and identify common elements

* Numerical simulation of composite multi-algorithmic models

    * E-Cell: multi-algorithmic simulator
    * iBioSim: implements a hierarchical SSA algorithm that can simulate merged SSA models


Exercise
--------

* Download and install SemGen
* Obtain the SemGen paper
* Use SemGen to replicate the model merging example described in the paper
