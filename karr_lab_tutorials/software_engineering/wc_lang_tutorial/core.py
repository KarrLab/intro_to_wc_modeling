''' wc_lang tutorial

:Author: Arthur Goldberg, Arthur.Goldberg@mssm.edu
:Date: 2017-06-13
:Copyright: 2017, Karr Lab
:License: MIT
'''

import os

from wc_lang.io import Reader

# 2. Read a model from a file::

# read a model from a workbook; each worksheet stores the instances of one class (with occasional exceptions)
MODEL_FILENAME = os.path.join(os.path.dirname(__file__), 'examples', 'test_wc_lang.xlsx')
model = Reader().run(MODEL_FILENAME)

# define a pattern of tsv filenames for the model; each file stores the instances of one class
MODEL_FILENAME_PATTERN = os.path.join(os.path.dirname(__file__), 'examples', 'test_wc_lang-*.tsv')

# make a set of tsv files that contain the same model
from wc_lang.io import Writer
Writer().run(MODEL_FILENAME_PATTERN, model)

# Read from tsv files; they must match the glob pattern in MODEL_FILENAME_PATTERN.
# The glob must match the names of wc_lang classes; e.g., test_wc_lang-Model.tsv, test_wc_lang-Submodels.tsv, etc.
model_tsv = Reader().run(MODEL_FILENAME_PATTERN)

# csv files can be used similarly
# (You may ignore SchemaWarning messages if you receive them.)

# 3. Use the model::
# models differ because of problems with 'reaction_participants'
print(model.difference(model_tsv))

# For example, list each submodel's id and name
for lang_submodel in model.get_submodels():
    print('submodel:', 'id:', lang_submodel.id, 'name:', lang_submodel.name)

# Documentation for wc_lang is available at: 
'''
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
'''
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

# Other uses of a ``wc_lang`` model work similarly.