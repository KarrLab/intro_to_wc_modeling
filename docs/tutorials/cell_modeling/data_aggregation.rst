Data aggregation
================
Building dynamical models of individual cells requires multivariate temporal data that captures the dynamics and variation of individual cells to inform the structure of the model and the value of each parameter. Extensive data is available to build cell models. However, this data is highly heterogeneous and incomplete because there is no single technology that can capture the high-dimensional dynamics and variation of individual cells. Furthermore, this data is highly dispersed across a large number of databases and individual manuscripts. Thus, a major challenge in cell modeling is to aggregate and merge this data into a consistent understanding of cell biology. In particular, we must merge data that is incomplete, that was obtained using multiple measurement methods for multiple genetic and environmental conditions and species and measured with different granularities, that includes relatively little dynamic data, and that includes relatively little single-cell data.

Broadly, there are two types of data that can be used to build cell models: experimental observations and prediction tools. The major advantages of prediction tools are that they provide complete data and that they can provide data for the exact genetics and environment that you wish to model. However, only a limited number of prediction tools are available.

Broadly, there are two types of data sources that can be used to build cell models: individual manuscripts and databases. The major advantage of databases is that other researchers have already done much of the time-consuming and tedious work needed to extract data from manuscripts. Thus, databases can save you a lot of time. However, there are many types of data that are not contained in databases and the most databases do not contain all of the contextual information (e.g. environmental condition of the measurement) that is needed to interpret their data.

The goal of this tutorial is to familiarize you with some of the most important data types and data sources for cell modeling.


Common data types and data sources
----------------------------------

* Metabolites

    * Structures: Mass-spectrometry; ChEBI, PubChem
    * Concentrations: Mass-spectrometry; ECMDB, YMDB, HMDB

* RNA
    
    * Sequences: Sequencing; GenBank
    * Modifications: Sequencing, mass-spectometry: Modomics
    * Concentrations: Microarray, RNA-seq; Array Express, GEO
    * Localization: FISH, microscopy; individual papers
    * Half-lives: Microarray, RNA-seq; individual papers

* Proteins

    * Sequences: UniProt
    * Modifications: Mass-spectrometry; UniMod
    * 3D structures: X-ray crystallography, NMR; PDB
    * Complexes: chromatograpy, yeast 2 hybrid; EcoCyc, UniProt
    * Localization: microscopy; PSORT, WolfSort
    * Concentrations: mass-spectometry; Pax-DB
    * Half-lives: mass-spectrometry; individual papers

* Interactions
    
    * DNA-Protein: ChIP-seq; DBD, DBTBS
    * Protein-metabolite: DrugBank, STICH, SuperTarget, UniProt
    * Protein-Protein: BioGRID, DIP, IntAct, STRING

* Reactions:

    * Catalysis: UniProt
    * Stoichiometry: BioCyc, KEGG
    * Kinetics: BRENDA, SABIO-RK, BioNumbers


Finding data sources
------------------------
There are several meta-databases which contain lists of datasources that are helpful for finding appropriate data source

* `BioCatalogue <https://www.biocatalogue.org>`_
* `BioMart <http://www.biomart.org>`_
* `BioMoby <http://biomoby.open-bio.org>`_
* `BioSWR <http://inb.bsc.es/BioSWR>`_
* `ELIXIR <https://www.elixir-europe.org>`_
* `NAR Database Summary <http://www.oxfordjournals.org/nar/database/c>`_


Finding relevant data for models
--------------------------------
When you aggregate data to inform a model, it is important to aggregate data that is relevant to the model. Where possible try to find data that was observed for

* Taxonomically close organisms
* Similar genetic variants
* Chemically similar species and reactions
* Similar environmental conditions: temperature, pH, media, pressure


Data aggregation tools
----------------------
`BIOSERVICES <https://pythonhosted.org/bioservices>`_ is a helpful tool for aggregating data from approximately 25 of the largest molecular biology databases. However, BIOSERVICES only supports a few databases and provides minimal support for identifying relevant data for a model. Unfortunately, there are few tools for aggregating relevant data for models. Consequently, we must develop better tools for aggregating the data needed to build models.


Determing the consensus of multiple observations
------------------------------------------------
In some cases, you may be lucky enough to find multiple observations to estimate a parameter value. In this case, we recommend estimating the parameter value by calculating the mean of the individual observations weighted by their relevance (taxonomic distance, species/reaction similarity, environmental similarity, etc.) to the model.


Exercise
--------

#. Download a model from BioModels
#. Ignore the provided parameter values
#. Use the databases and prediction tools listed above to estimate the values of all of the parameters of the model
    
    * Determine was metadata is provided about the observed organism, genetic, environmental conditions, etc.
    * Try to identify data that were observed under similar conditions to the model

#. Track the provenance of each value that you identify
        
    * Observed value and uncertainty
    * Observed units
    * Observed species
    * Observed condition
    * Measurement method
    * Reference
