Using the wc_lang package to define whole-cell models
=======================================================

This tutorial teaches you how to use the ``wc_lang`` package to access and create whole-cell models.
``wc_lang`` provides a foundation for defining, writing, reading and manipulating biochemical models composed of species,
reactions, compartments and other parts of a biochemical system.
It can be used to define models of entire cells, or models of smaller biochemical systems.
``wc_lang`` contains methods to read and write models from two types of files --
Excel spreadsheet workbooks and sets of delimited files. It also includes methods that
analyze or transform models -- e.g., methods that validate, compare, and normalize them.

``wc_lang`` depends heavily on the ``obj_model`` package which defines a generic language for declaring
interrelated Python objects, converting them to and from data records,
transferring the records to and from files, and validating their values.
``obj_model`` is essentially an object-relational mapping (ORM) system that stores data in files
instead of databases.
However, users of ``wc_lang`` do not need to use ``obj_model`` directly.

Semantics of a ``wc_lang`` biochemical Model
----------------------------------------------
A ``wc_lang`` biochemical model represents a biochemical system as ``Species`` (we indicate
classes in ``wc_lang`` by capitalized names in ``fixed-width`` text) that get transformed by reactions.

A ``SpeciesType`` describes a biochemical molecule, including its ``name`` (following Python
convention, attributes
of classes are lowercase names), ``structure``, ``molecular_weight``,
``charge`` and other properties.
The concentration of a ``SpeciesType`` in a compartment is stored by a ``Species`` instance
that references instances of ``SpeciesType``, ``Compartment``, and ``Concentration``, which provide
the ``Species``' location and concentration.
A compartment may represent an organelle or a conceptual region of a model.
Adjacency relationships among compartments are implied by reactions that transfer
species among them, but physical relationships between compartments or their 3D positions
are not represented.

The data in
a ``wc_lang`` model is organized in a highly-interconnected graph of related Python objects, each of
which is an ``obj_model.core.Model`` instance.
For example, a ``Species`` instance contains ``reaction_participants``,
which references each ``Reaction`` in which the ``Species`` participates.
The graph contains many convenience relationships like this, which make it easy to
follow the relationships between ``obj_model.core.Model`` instances anywhere in a ``wc_lang`` model.

A ``wc_lang`` model also supports some metadata.
Named ``Parameter`` entities store arbitrary values, such as input parameters.
Published data sources used by a model should be recorded in ``Reference`` entities,
or in a ``CrossReference`` objects that identify a biological or chemical database.

``wc_lang`` models are typically used to describe the initial state of a model -- a ``wc_lang``
description lacks any notion of time.
More generally, a comprehensive ``wc_lang`` model should provide a complete description of a model,
including its data sources and comments about model components.


``wc_lang`` Classes Used to Define biochemical Models
------------------------------------------------------

This subsection enumerates the ``obj_model.core.Model`` classes that store data in ``wc_lang`` models.

When using an existing model the attributes of these classes are frequently accessed, although
their definitions are not typically imported.
However, they must be imported when they are being instantiated programmatically.

Many of these classes implement the methods ``deserialize()`` and ``serialize()``.
``deserialize()`` parses an object's string representation -- as would be stored in a text file or spreadsheet
representation of a biochemical model -- into one or more ``obj_model.core.Model`` instances.
``serialize()`` performs the reverse, converting a ``wc_lang`` class instance into a string representation.
Thus, the ``deserialize()`` methods are used when reading models from files and ``serialize()`` 
is used when writing a model to disk. 
``deserialize()`` returns an error when a string representation cannot be parsed into a
Python object.

Static Enumerations
~~~~~~~~~~~~~~~~~~~

Static attributes of these classes are used as attributes of ``wc_lang`` model components.

``TaxonRank``
    The names of biological taxonomic ranks: *domain*, *kingdom*, *phylum*, etc.

``SubmodelAlgorithm``
    The names of algorithms that can integrate submodels: *dfba*, *ode*, and *ssa*.

``SpeciesTypeType``
    Types of species types: *metabolite*, *protein*, *dna*, *rna*, and *pseudo_species*.

``RateLawDirection``
    The direction of a reaction rate law: *backward* or *forward*.

``ReferenceType``
    Reference types, such as *article*, *book*, *online*, *proceedings*, etc.

``wc_lang`` Model Components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These classes are instantiated as components of a ``wc_lang`` model.
When a model is stored on disk all the instances of each class are
usually stored in a separate table, either an Excel workbook's worksheet or delimiter-separated file.
In the former case, the model is stored in one workbook, while in the latter it is stored in a set of files.

``Taxon``
    The taxonomic rank of a model.

``Submodel``
    A part of a whole-cell model which is to be simulated with a particular ``algorithm`` from the
    enumeration ``SubmodelAlgorithm``. Each ``Submodel``
    is associated with a ``Compartment`` that contains the ``Species`` it models, and all the reactions
    that transform them. A ``Submodel`` may also have parameters.

``Compartment``
    A named physical container in the biochemical system being modeled.
    It could represent an organelle, a cell's cytoplasm, or another physical or conceptual structure.
    It includes an ``initial_volume`` in liters,
    and references to the initial concentrations of the ``Species`` it contains.
    A compartment can have a semi-permeable membrane, which is modeled by
    reactions that transform reactant species in the compartment to product species in another compartment.
    These are called *membrane-transfer* reactions. A membrane-transfer reaction that moves
    species from compartment *x* to compartment *y* implies that *x* and *y* are adjacent.

``SpeciesType``
    The biochemical type of a species. It contains the type's ``name``, ``structure`` -- which is
    represented in InChI for metabolites and as sequences for DNA, RNA, and proteins, ``empirical_formula``,
    ``molecular_weight``, and ``charge``. A species' ``type`` is drawn from the attributes of
    ``SpeciesTypeType``.

``Species``
    A particular ``SpeciesType`` contained in a particular ``Compartment`` at a particular concentration.

``Concentration``
    The molar concentration (M) of a species.

``Reaction``
    A biochemical reaction. Each ``Reaction`` belongs to one ``submodel``. It consists of a list
    of the species that participate in the reaction, stored as a list of references to
    ``ReactionParticipant`` instances in ``participants``.
    A reaction
    that's simulated by a dynamic algorithm, such as an ODE system or SSA, must have a forward
    rate law. A Boolean indicates whether the reaction is thermodynamically ``reversible``.
    If ``reversible`` is ``True``, then the reaction must also have a backward rate law. Rate laws are
    stored in the ``rate_laws`` list, and their directions are drawn from the attributes of
    ``RateLawDirection``.

..
    # todo: document the syntax and semantics of a serialized reaction ``participants`` attribute.

``ReactionParticipant``
    ``ReactionParticipant`` combines a ``Species`` and its stoichiometric reaction coefficient.
    Coefficients are negative for reactants and positive for products.

``RateLaw``
    A rate law contains a textual ``equation`` which stores the mathematical expression of the rate law.
    It contains the ``direction`` of the rate law, encoded with a ``RateLawDirection`` attribute.
    ``k_cat`` and ``k_m`` attributes for a Michaelis–Menten kinetics model are provided, but
    their use isn't required.

``RateLawEquation``
    A rate law equation's ``expression`` contains a textual, mathematical expression of the rate law. A rate law can be
    used by more than one ``Reaction``.
    The expression will be transcoded into a valid Python expression, stored in the ``transcoded``
    attribute, and
    evaluated as a Python expression by a simulator. This evaluation must produce a number.

    The expression is constructed from species names, compartment names, stoichiometric
    reaction coefficients, k_cat and k_m, and Python functions and mathematical operators.
    ``SpeciesType`` and ``Compartment`` names must be valid Python identifiers, and the entire
    expression must be a valid Python expression.
    A species composed of a ``SpeciesType`` named
    ``species_x`` located in a ``Compartment`` named ``c`` is written ``species_x[c]``.
    When a rate law equation is evaluated during the simulation of a model the expression ``species_x[c]``
    is interpreted as the current concentration of ``species_x`` in compartment ``c``. 

..
    # todo: expand this documentation of the syntax and semantics of RateLawEquation expressions.

..
    # todo: include biomass component and biomass reaction

``Parameter``
    A ``Parameter`` holds an arbitrary floating point ``value``. It is named, associated with a
    a set of ``submodels``, and should include a modifier indicating the value's ``units``.

``wc_lang`` Model Data Sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These classes record the sources of a model's data.

``Reference``
    A ``Reference`` holds a reference to a publication that contains data used in the model.

``CrossReference``
    A ``Reference`` describes a biological or chemical database that provided data for the model.


Using ``wc_lang``
-----------------
The following tutorial shows several ways to use ``wc_lang``, including
reading a model from disk, defining a model programmatically and writing it to disk,
and using these models:

#. Install the required software for the tutorial:

    * Python
    * Pip

#. Install the tutorial and the whole-cell packages that it uses:

.. code-block:: bash

    git clone https://github.com/KarrLab/intro_to_wc_modeling.git
    pip install --upgrade \
        ipython \
        git+https://github.com/KarrLab/wc_lang.git#egg=wc_lang \
        git+https://github.com/KarrLab/wc_utils.git#egg=wc_utils

#. Change to the directory for this tutorial:

.. code-block:: bash

    cd intro_to_wc_modeling/intro_to_wc_modeling/wc_modeling/wc_lang_tutorial

#. Open an interactive python interpreter:

.. code-block:: bash

    ipython

#. Import the ``os`` and ``wc_lang.io`` modules::

    import os
    import wc_lang.io

#. Read a model from an Excel file

    ``wc_lang`` can read and write models from specially formatted Excel workbooks in which each worksheet represents
    one of the model component classes above, each row
    represents a class instance, each column represents an instance attribute, each cell represents the value of an attribute of an
    instance, and string identifiers are used to indicate relationships among objects.

    In addition to defining a model, these Excel files should contain all of the annotation needed to understand the biological semantic meaning of
    the model. Ideally, this should include:

    * NCBI Taxonomy ID for the taxon
    * Gene Ontology (GO) annotations for each submodel
    * The structure of each species: InChI for small molecules; sequences for polymers
    * Where possible, ChEBI ids for each small molecule
    * Where possible, ids for each gene, transcript, and protein
    * Where possible, EC numbers or KEGG ids for each reaction
    * `Cell Component Ontology <http://brg.ai.sri.com/CCO>`_ (CCO) annotations for each compartment
    * `Systems Biology Ontology <http://www.ebi.ac.uk/sbo>`_ (SBO) annotations for each parameter
    * The citations which support each model decision
    * PubMed id, DOI, ISBN, or URL for each citation

    This example illustrates how to read a model from an Excel file:

    .. literalinclude:: ../../intro_to_wc_modeling/wc_modeling/wc_lang_tutorial/core.py
        :language: Python
        :start-after: This example illustrates how to read a model from an Excel file
        :lines: 2
        :dedent: 4

    (You may ignore a ``UserWarning`` generated by these commands.)

    If a model file is invalid (for example, it defines two species types with the same id, or
    a concentration that refers to a species type that is not defined), this operation
    will raise an exception which contains a list of all of the errors in the model definition.

    ``wc_lang`` can also read and write a model from a specially formatted set of delimiter-separated files.
    ``wc_lang`` uses filename glob patterns to indicate sets of delimited files. The supported delimiters
    are *commas* for .csv files and *tabs* for .tsv files. These files use the same
    format as the Excel workbook format, except that each worksheet is saved as a separate file.
    Excel workbooks are easier to read and edit interactively,
    but changes to delimiter-separated files can be tracked in code version control systems such as Git.

    This example illustrates how to write a model to a set of .tsv files:

    .. literalinclude:: ../../intro_to_wc_modeling/wc_modeling/wc_lang_tutorial/core.py
        :language: Python
        :start-after: This example illustrates how to write a model to a set of .tsv files
        :lines: 1-3
        :dedent: 4

    Continuing the previous example, this command reads this set of .tsv files into a model:

    .. literalinclude:: ../../intro_to_wc_modeling/wc_modeling/wc_lang_tutorial/core.py
        :language: Python
        :start-after: This example illustrates how to read a model from a set of .tsv files
        :lines: 1
        :dedent: 4

    csv files can be used similarly.

#. Access properties of the model

    A ``wc_lang`` model (an instance of ``wc_lang.core.Model``) has multiple attributes:

    .. literalinclude:: ../../intro_to_wc_modeling/wc_modeling/wc_lang_tutorial/core.py
        :language: Python
        :start-after: ``wc_lang`` models have many attributes
        :lines: 1-10
        :dedent: 4

    These provide access to the parts of a ``wc_lang`` model that are directly referenced by a model instance.

    ``wc_lang`` also provides some convenience methods that get all of the elements of a specific type
    which are part of a model. Each of these methods returns a list of the instances of requested type.

    .. literalinclude:: ../../intro_to_wc_modeling/wc_modeling/wc_lang_tutorial/core.py
        :language: Python
        :start-after: ``wc_lang`` also provides many convenience methods
        :lines: 1-10
        :dedent: 4

    For example, ``get_reactions()`` returns a list of all of the reactions in a model's submodels.
    As illustrated below,
    this can be used to obtain the id of each reaction and the name of its submodel:

    .. literalinclude:: ../../intro_to_wc_modeling/wc_modeling/wc_lang_tutorial/core.py
        :language: Python
        :start-after: ``get_reactions()`` returns a list of all of the reactions in a model's submodels
        :lines: 1-4
        :dedent: 4


#. Programmatically build a new model and edit its model properties

    You can also use the classes and methods in ``wc_lang.core`` to programmatically build and edit models.
    While modelers typically will not create models programmatically, creating model components
    in this way gives you a feeling for how models are built.

    The following illustrates how to build a simple model programmatically:

    .. literalinclude:: ../../intro_to_wc_modeling/wc_modeling/wc_lang_tutorial/core.py
        :language: Python
        :start-after: The following illustrates how to build a simple model programmatically
        :end-before: The previous illustrates how to build a simple model programmatically
        :dedent: 4

    Similar code can be used to create any part of a model. All ``wc_lang`` objects that are subclassed from
    ``wc_lang.BaseModel`` (an alias for ``obj_model.core.Model``) can be instantiated in the normal fashion,
    as shown for ``Model``, ``Submodel``, ``Compartment``, ``SpeciesType`` and ``Reaction`` above.
    Each subclass of ``wc_lang.BaseModel`` contains a ``Meta`` attribute that is a class which
    stores meta information about the subclass. 
    The attributes that can be initialized when a ``wc_lang.BaseModel`` class is instantiated can be
    obtained from the class' ``Meta`` attribute, which is a dictionary that maps from attribute name to attribute instance:

    .. literalinclude:: ../../intro_to_wc_modeling/wc_modeling/wc_lang_tutorial/core.py
        :language: Python
        :start-after: The attribues that can be initialized when a ``wc_lang.BaseModel`` class is instantiated
        :lines: 1-4
        :dedent: 4

    For example, ``Reaction`` has the following attributes in ``wc_lang.core.Reaction.Meta.attributes.keys()``::

        ['comments', 'id', 'max_flux', 'min_flux', 'name', 'participants', 'references',
            'reversible', 'submodel']

    These attributes can also be set programmatically:

    .. literalinclude:: ../../intro_to_wc_modeling/wc_modeling/wc_lang_tutorial/core.py
        :language: Python
        :start-after: The following illustrates how to edit a model programmatically
        :lines: 1-2
        :dedent: 4

    In addition, the ``create`` method can be used to add elements to lists of related ``wc_lang.BaseModel``
    objects, as illustrated by ``atp_hydrolysis.participants.create()`` above. This avoids creating
    unnecessary identifiers.

#. Validating a programmatically generated Model

    The ``wc_lang.core.Model.validate`` method determines whether a model is valid. If
    the model is invalid validate return a list of all of the model's errors. It performs the following checks:

    * Check that only one model and taxon are defined
    * Check that each submodel, compartment, species type, reaction, and reference is defined only once
    * Check that each the species type and compartment referenced in each concentration and reaction exist
    * Check that values of the correct types are provided for each attribute

        * ``wc_lang.core.Compartment.initial_volume``: float
        * ``wc_lang.core.Concentration.value``: float
        * ``wc_lang.core.Parameter.value``: float
        * ``wc_lang.core.RateLaw.k_cat``: float
        * ``wc_lang.core.RateLaw.k_m``: float
        * ``wc_lang.core.Reaction.reversible``: bool
        * ``wc_lang.core.ReactionParticipant.coefficient``: float
        * ``wc_lang.core.Reference.year``: integer
        * ``wc_lang.core.SpeciesType.charge``: integer
        * ``wc_lang.core.SpeciesType.molecular_weight``: float

    * Check that valid values are provided for each enumerated attribute

        * ``wc_lang.core.RateLaw.direction``
        * ``wc_lang.core.Reference.type``
        * ``wc_lang.core.SpeciesType.type``
        * ``wc_lang.core.Submodel.algorithm``
        * ``wc_lang.core.Taxon.rank``

    This example illustrates how to validate ``prog_model``:

    .. literalinclude:: ../../intro_to_wc_modeling/wc_modeling/wc_lang_tutorial/core.py
        :language: Python
        :start-after: This example illustrates how to validate ``prog_model``
        :lines: 1
        :dedent: 4

#. Compare and difference Models

    ``wc_lang`` provides methods that determine if two models are semantically equal and report any semantic
    differences between two models. The ``is_equal`` method determines if two models are semantically equal
    (the two models recursively have the same attribute values, ignoring the order of the attributes which has
    no semantic meaning). The following code compares the semantic equality of
    ``model`` and ``model_from_tsv``. Since ``model_from_tsv`` was generated by writing ``model``
    to tsv files, ``is_equal`` should return ``True``:

    .. literalinclude:: ../../intro_to_wc_modeling/wc_modeling/wc_lang_tutorial/core.py
        :language: Python
        :start-after: compare the semantic equality of ``model`` and ``model_from_tsv``
        :lines: 1
        :dedent: 4

    The ``difference`` method produces a textual description of the differences between two models. The following
    code excerpt prints the differences between ``model`` and ``model_from_tsv``. Since they are
    equal, the differences should be the empty string:

    .. literalinclude:: ../../intro_to_wc_modeling/wc_modeling/wc_lang_tutorial/core.py
        :language: Python
        :start-after: produces a textual description of the differences between two models
        :lines: 1
        :dedent: 4

#. Normalize ``model`` into a reproducible order to facilitate reproducible numerical simulations

    The attribute order has no semantic meaning in ``wc_lang``. However, numerical simulation results derived from
    models described in ``wc_lang`` can be sensitive to the attribute order. To facilitate reproducible simulation results,
    ``wc_lang`` provides a ``normalize`` to sort models into a reproducible order.

    The following code excerpt will normalize ``model`` into a reproducible order:

    .. literalinclude:: ../../intro_to_wc_modeling/wc_modeling/wc_lang_tutorial/core.py
        :language: Python
        :start-after: The following code excerpt will normalize ``model`` into a reproducible order
        :lines: 1
        :dedent: 4

#. Please see `http://code.karrlab.org <http://code.karrlab.org/>`_ for documentation of the entire ``wc_lang`` API.


..
    # todo: Furthermore, ``obj_model`` automatically creates reverse references for 
    reference attributes 

..
    Complete and add this section:
    #. Examine model global consistency

    While the schema ensures that a model provided by ``wc_lang`` has local integrity it does not
    evaluate global integrity. For example, we can infer the compartment which each submodel
    represents by looking at the compartments of the reactants in the submodel's species.
    But a submodel should not represent reactions in multiple compartments.
    The function ``infer_submodel_compartments`` below evaluates this consistency.

    This and other global model
    properties must be checked after a model is instantiated. Other such properties include:

