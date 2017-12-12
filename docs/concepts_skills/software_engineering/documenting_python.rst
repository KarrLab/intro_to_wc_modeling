Documenting Python code with Sphinx
===================================

The goal of this tutorial is to teach you how to document Python code to help
other programmers -- and yourself in the future -- understand your code.
We recommend that you document each attribute, argument, method and class, and also document
each module and package.

reStructuredText is the most commonly used markup format for documenting Python code and Sphinx is the most commonly used tool for compiling Python documentation.


Required packages
---------------------------
Execute the following commands to install the packages required for this tutorial::

    apt-get install \
        python \
        python-pip
    pip install \
        configparse \                            # configuration file parser
        robpol86-sphinxcontrib-googleanalytics \ # sphinx support for Google analytics
        sphinx \                                 # documentation generator
        sphinx-rtd-theme                         # sphinx HTML theme


File naming and organization
-----------------------------
Our convention is to place all top-level documentation within a separate ``docs`` directory within each repository and to embed all API documentation in the source code.::

    /path/to/repo/
        docs/                  # directory for all of the documentation files
            index.rst          # main documentation file
            conf.py            # Sphinx configuration
            requirements.txt   # packages required to compile the documentation
        setup.cfg              # contains a setting which specifies the packages for which
                               # API documentation should be generated


Generating a Sphinx configuration file
--------------------------------------
Sphinx is highly configurable and can be configured using the ``docs/conf.py`` file.

You can generate a Sphinx configuration file by running the ``sphinx-quickstart`` utility and following the on screen instructions.

Note: we are using a heavily modified Sphinx configuration file. See ``karr_lab_build_utils.templates.docs.conf.py`` for our template. In particular, we are enabling the ``napoleon`` extension to support Google-style argument and attribute doc strings.


Writing documentation
-----------------------
In the remainder of the tutorial, we will write tests for the code located in ``/path/to/this/repo/intro_to_wc_modeling/concepts_skills/software_engineering/unit_testing/``.

Using the `napoleon` style, you can document each class, method, and attribute. See ``intro_to_wc_modeling/concepts_skills/software_engineering/unit_testing/core.py`` for a complete example.

Classes
^^^^^^^
.. code-block:: Python

    class Class():
        """ Description

        Attributes:
            name (:obj:`core.Simulation`): description
        """

        ...

Methods
^^^^^^^
.. code-block:: Python

    def method():
        """ Description

        Args:
            name (:obj:`type`): description
            name (:obj:`type`, optional): description

        Returns:
            :obj:`type`: description

        Raises:
            :obj:`type`: description
        """

        ...

Top-level documentation
^^^^^^^^^^^^^^^^^^^^^^^
We can also add top-level documentation to ``docs/index.rst`` using the reStructuredText markup language. See the
`reStructuredText primer <http://www.sphinx-doc.org/en/stable/rest.html#rst-primer>`_ for a brief tutorial
about the reStructuredText markup language.


README
^^^^^^^^^^^^^^^^^^^^^^^
In addition to this documentation, we also recommend providing a brief README file with each repository and we recommend embedded status badges at the top of this file. These badges can be embedded as shown in the example below::

    <!-- [![PyPI package](https://img.shields.io/pypi/v/intro_to_wc_modeling.svg)](https://pypi.python.org/pypi/intro_to_wc_modeling) -->
    [![Documentation](https://readthedocs.org/projects/karrlab_intro_to_wc_modeling/badge/?version=latest)](http://karrlab_intro_to_wc_modeling.readthedocs.org)
    [![Test results](https://circleci.com/gh/KarrLab/intro_to_wc_modeling.svg?style=shield)](https://circleci.com/gh/KarrLab/intro_to_wc_modeling)
    [![Test coverage](https://coveralls.io/repos/github/KarrLab/intro_to_wc_modeling/badge.svg)](https://coveralls.io/github/KarrLab/intro_to_wc_modeling)
    [![Code analysis](https://codeclimate.com/github/KarrLab/intro_to_wc_modeling/badges/gpa.svg)](https://codeclimate.com/github/KarrLab/intro_to_wc_modeling)
    [![License](https://img.shields.io/github/license/KarrLab/intro_to_wc_modeling.svg)](LICENSE)
    ![Analytics](https://ga-beacon.appspot.com/UA-86759801-1/intro_to_wc_modeling/README.md?pixel)


Compiling the documentation
---------------------------
Run the following to compile the documentation::

    sphinx-build docs docs/_build/html

Sphinx will print out any errors in the documentation. These must be fixed to properly generate the documentation.

It can be viewed by opening ``docs/_build/html/index.html`` in your browser.
