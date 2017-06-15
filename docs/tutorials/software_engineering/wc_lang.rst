Using the wc_lang Package to Define Whole-Cell Models
=======================================================

This tutorial teaches you how to use the ``wc_lang`` package to define whole-call models.
``wc_lang`` provides a foundation for defining and accessing bio-chemical models composed of species,
reactions, compartments and other interrelated structures.
``wc_lang`` contains methods to read and write models from two types of files --
spreadsheet workbooks and sets of delimited files. It also includes methods that transform
and summarize models.


Semantics of a ``wc_lang`` Bio-chemical Model
----------------------------------------------
A ``wc_lang`` bio-chemical model represents a biochemical system as ``Species`` (we indicate
classes in ``wc_lang`` by capitalized names in ``fixed-width`` text) which get transformed by
``Reaction``s. The spatial structure of the system is captured by ``Compartment``s which contain
``Species``. However, physical relationships between compartments or their 3D positions
are not represented. Adjacency between compartments is only implied by reactions that transfer
species among them.

A ``SpeciesType`` describes a biochemical molecule, including its ``name`` (we indicate attributes
of classes by lowercase names in ``fixed-width`` text), ``structure``, ``molecular_weight``,
``charge`` and other properties.
The concentration of a ``SpeciesType`` in a compartment is stored by a ``Species`` instance
that references instances of ``SpeciesType``, ``Compartment``, and ``Concentration``.

More generally,
a ``wc_lang`` model is a highly-interconnected graph of objects (``obj_model.Model`` instances).
For example, a ``Species`` instance also contains ``reaction_participants``, a list of ``Reaction``s
in which the ``Species`` participates. The graph contains more connections than necessary to represent
the model because the additional references make it easier to retrieve useful related data.

A ``wc_lang`` model may also contain named ``Parameter``s which are arbitrary values. It can also
contain ``Reference``s to published data sources, and ``CrossReference``s to biological or chemical
databases.

You should think of a ``wc_lang`` model as the description of a model in its initial state.
A ``wc_lang`` model contains much information not required for the simulation of a model, such as
``Reference``s and lacks any notion of time.

``wc_lang`` depends heavily on the ``obj_model`` package, but users of ``wc_lang`` do not need to
use ``obj_model`` directly.

The next subsection enumerates all the classes which contain model data in ``wc_lang``.

``wc_lang`` Classes Used to Define Bio-chemical Models
------------------------------------------------------

Static Enumerations
~~~~~~~~~~~~~~~~~~~

Instances of these classes are used as attributes of ``wc_lang`` model components.

``TaxonRank``
    The names of biological taxonomic ranks: domain, kingdom, phylum, etc.

``SubmodelAlgorithm``
    The names of algorithms that can solve submodels: dfba, ode, and ssa.

``SpeciesTypeType``
    Types of species types: metabolite, protein, rna, and pseudo_species.

``RateLawDirection``
    The direction of a reaction rate law: backward or forward.

``ReferenceType``
    Reference types, such as article, book, online, proceedings, etc.

``wc_lang`` Model Components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These classes are instantiated as components of a ``wc_lang`` model. Unless noted otherwise, each is
stored in a separate table, either a workbook's worksheet or delimiter-separated file.

``Taxon``
    The taxonomic rank of a model.

``Submodel``
    Part of a whole-cell model which is to be simulated with a particular algorithm. Each ``Submodel``
    is associated with a ``Compartment`` that contains its ``Species``, and a set of ``Reaction``s
    that transform them. A ``Submodel`` may also have some ``Parameter``s.

``Compartment``
    A named physical container for part of a model. It includes an ``initial_volume`` in liters,
    and references to the initial ``Concentration``s of ``Species`` it contains.

``SpeciesType``
    The biochemical type of a species. Contains the type's ``name``, ``structure`` (InChI for
    metabolites; sequence for DNA, RNA, proteins), ``empirical_formula``, ``molecular_weight``,
    ``charge``, and ``type``, which is its ``SpeciesTypeType``.

``Species``
    A particular ``SpeciesType`` contained in a particular ``Compartment``.

``Concentration``
    The Molar concentration (M) of a species.

``Reaction``
    A bio-chemical reaction. Each ``Reaction`` belongs to one ``submodel``. It consists of a list
    of ``participants``, the species that participate in the reaction.
    A boolean indicates whether the reaction is thermodynamically ``reversible``. A reaction
    that's simulated by a dynamic algorithm, such as an ODE system or SSA, must have a forward
    rate law and must also have a reverse rate law if ``reversible`` is ``True``. Rate laws are
    stored in the ``rate_laws`` list.

``ReactionParticipant``
    ``ReactionParticipant`` combines a ``Species`` and its stoichiometric reaction coefficient.
    Coefficients are negative for reactants and positive for products.

``RateLaw``
    A rate law contains a textual ``equation`` which contains the mathematical expression of the rate law.
    It contains the ``direction`` of the rate law, encoded as a ``RateLawDirection`` object.
    Attributes for ``k_cat`` and ``k_m`` for a Michaelis–Menten kinetics model are provided, but
    their use isn't required.

``RateLawEquation``
    ``expression`` contains textual a mathematical expression of the rate law provided by the model.
    The expression will be transcoded into a valid Python expression, stored in ``transcoded``, and
    evaluated as Python by a simulator. Evaluating the transcoded expression must produce a number.
    [Expand this:]
    The expression must be written as a function of species names, compartment names, stoichiometric
    reaction coefficients, k_cat and k_m, and Python functions and mathematical operators.
    ``SpeciesType`` and ``Compartment`` names must be valid Python identifiers.
    A species composed of a ``SpeciesType`` named
    ``species_x`` located in a ``Compartment`` named ``c`` is written ``species_x[c]``. Evaluating
    the rate law converts species into their concentration

``Parameter``
    A ``Parameter`` holds an arbitrary floating point ``value``. It is named, associated with a
    a set of ``submodels``, and should include a modifier indicating the value's ``units``.

``Reference``
    A ``Reference`` holds a reference to a publication that contains data used in the model.

It is not necessary to import these types; rather, their attributes should be accessed when using a model.

Many classes contain the methods ``serialize()`` and ``deserialize()``, which invert each other.
``serialize()`` converts a python object instance into a string representation, whereas
``deserialize()`` parses an object's string representation -- as would be stored in a file or spreadsheet
representation of a bio-chemical model -- into a python object instance.
``deserialize()`` returns an error when the string representation cannot be parsed into the
python object.


Using ``wc_lang``
-----------------
``wc_lang`` is used in several ways. To read and use a model defined in one or more files, follow these steps:

0. Setup the tutorial::

    # In a Unix shell:
    git clone https://github.com/KarrLab/karr_lab_tutorials.git
    cd karr_lab_tutorials/software_engineering/wc_lang
    python core.py

1. Import the ``wc_lang`` model reader::

    import os
    from wc_lang.io import Reader

2. Read a model from a file::

Read a model from a workbook; each worksheet stores the instances of one class (with occasional exceptions
for Inline classes).

    MODEL_FILENAME = os.path.join(os.path.dirname(__file__), 'examples', 'test_wc_lang.xlsx')
    model = Reader().run(MODEL_FILENAME)

Define a pattern of tsv filenames for the model; each file stores the instances of one class

    MODEL_FILENAME_PATTERN = os.path.join(os.path.dirname(__file__), 'examples', 'test_wc_lang-*.tsv')

Make a set of tsv files that contain the same model

    from wc_lang.io import Writer
    Writer().run(MODEL_FILENAME_PATTERN)

Read from tsv files; they must match the glob pattern in ``MODEL_FILENAME_PATTERN``.
The glob must match the names of ``wc_lang`` classes; e.g., ``test_wc_lang-Model.tsv``,
``test_wc_lang-Submodels.tsv``, etc.

    model_tsv = Reader().run(MODEL_FILENAME_PATTERN)

csv files can be used similarly.

3. Use the model::

For example, list each submodel's id and name:

    for lang_submodel in model.get_submodels():
        print('submodel:', 'id:', lang_submodel.id, 'name:', lang_submodel.name)

Documentation for ``wc_lang`` is available at: xxx

More usefully, let's access the model and evaluate an aspect of its integrity.

The ``Model`` object in ``wc_lang`` provides a set of convenience methods for accessing a model's elements.
These are:

* ``get_compartments()``

* ``get_species_types()``

* ``get_submodels()``

* ``get_species()``

* ``get_concentrations()``

* ``get_reactions()``

* ``get_rate_laws()``

* ``get_parameters()``

* ``get_references()``

Each of these methods returns a list
containing all of the model's instances of the component type in the method's name.
E.g., ``get_rate_laws()`` returns all of the model's ``RateLaw`` instances.

While the schema ensures that a model provided by ``wc_lang`` has local integrity it does not
evaluate global integrity. For example, a ``wc_lang`` model may associate a compartment with each
submodel and must associate a submodel with each reaction. But it does not ensure that the reactants in
a submodel's reactions are located in the submodel's compartment.
The function ``verify_reactant_compartments`` below evaluates this consistency.
This and other global model
properties must be checked after a model is instantiated. Other such properties include:

* The model does not contain dead-end species which are only consumed or produced

* Reactions are balanced

* Reactions in dynamic submodels contain fully specified rate laws

``verify_reactant_compartments`` uses ```` to iterate through all submodels. It accesses
each submodel's compartment attribute with ``lang_submodel.compartment``, and
each submodel's reactions with ``lang_submodel.reactions``.

    def verify_reactant_compartments(model):
        '''Verify that all reactants in each submodel's reactions are in the submodel's compartment

        Returns:
            `list`: errors
        '''
        errors = []
        for lang_submodel in model.get_submodels():
            compartment = lang_submodel.compartment
            if compartment is None:
                errors.append("submodel '{}' must contain a compartment attribute".format(lang_submodel.id))
                continue
            for reaction in lang_submodel.reactions:
                for participant in reaction.participants:
                    if participant.coefficient < 0:     # select reactants
                        if participant.species.compartment != compartment:
                            error = "submodel '{}' models compartment {}, but its reaction {} uses "\
                            "specie {} in another compartment: {}".format(lang_submodel.id,
                                compartment.id, reaction.id, participant.species.species_type.id,
                                participant.species.compartment.id)
                            errors.append(error)
        return errors

    print('\n'.join(verify_reactant_compartments(model)))

Other uses of a ``wc_lang`` model work similarly.