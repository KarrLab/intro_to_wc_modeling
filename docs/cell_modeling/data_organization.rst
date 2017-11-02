Input data organization
=======================
Building large models requires a large amount of input data to inform the structure of the model and the value of each parameter. Consequently, it is helpful to organize this data into a readily understandable and computable database. 

Unfortunately, there are few tools specifically designed to organize the input data needed for mechanistic models. However, Pathway/genome databases (PGDBs) or model organism databases (MOD) are conceptually similar and the existing PGDB tools provide much of the functionality needed to organize the input data for mechanistic models. In fact, the Pathway Tools PDB tool includes a module called MetaFlux which can be used to build flux balance analysis models of metabolism. In particular, PGDBs can track detailed molecular information at the genomic-scale for individual organisms. Some of the major limitations of the existing PGDBs are that they provide limited support for non-metabolic pathways and that they provide limited support for quantitative data.


Schema
------
The input data used to build models can be organized with the following schema
   
* Value
* Uncertainty
* Units
* Genetic conditions

    * Taxon
    * Variant

* Environmental conditions

    * Temperature
    * pH
    * Media

* Localization

    * Intracellular compartment
    * Tissue

* Timepoint

    * Cell cycle phase
    * Growth phase
    * Time post-perturbation

* Measurement method

    * Parameters
    * Version

* Experiment: collection of values observed in the same experiment
* Reference

Several ontologies such as the CCO and CL can be used to describe components of the schema.


Software tools
--------------
Below are some of the best tools for organizing the input data used to build models. Unfortunately, all of these tools have significant limitations. Consequently, we must develop better tools for organizing the input data used to build models.

* `GMOD <http://gmod.org>`_
* `Pathway Tools <http://brg.ai.sri.com/ptools>`_
* `SEEK <https://fair-dom.org/platform/seek>`_
* `WholeCellKB <http://www.wholecellkb.org>`_


Exercises
---------

EcoCyc and Pathway Tools
^^^^^^^^^^^^^^^^^^^^^^^^

#. Browse the webpages of BioCyc
#. Observe the types of data EcoCyc contains and how it is organized
#. Read the schema documentation


WholeCellKB
^^^^^^^^^^^

#. Browse the webpages of WholeCellKB
#. Observe the types of data WholeCellKB contains and how it is organized
#. Read the schema documentation
