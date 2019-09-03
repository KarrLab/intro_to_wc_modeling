Structuring Python projects
===========================
We recommend using the following principles to organize Python projects:

* Use separate repositories for each project
* Store only one package in each repository
* Structure each package as outlined below following the recommendations provided by `The Hitchhiker's Guide To Python<https://docs.python-guide.org/writing/structure/#structure-of-the-repository>`_:

    .. code-block :: text

        repository_name/                # source code directory
            __init__.py                 # each source code directory must contain an ``__init__.py`` file
            __main__.py                 # optional, for command line programs
            VERSION                     # text file with version number
            data/                       # directory for data files needed by the code
        tests/                          # directory for test code
            fixtures/                   # fixtures for tests
                secret/                 # git-ignored fixtures that contain usernames, passwords, and tokens
            requirements.txt            # packages required to run the tests, but not required by the project; used by CircleCI
        docs/                           # directory for documentation
            conf.py                     # documentation configuration
            index.rst                   # main documentation file
            requirements.txt            # list of packages required to compile the documentation
            requirements.rtd.txt        # list of packages required to compile the documentation; used by Read the Docs
            _build/html/                # directory where compiled documentation is saved
            _static                     # optional for static files such as .css and .js files needed for the documentation
        examples/                       # (optional) directory for examples of how to use the code
        LICENSE                         # license file
        MANIFEST.in                     # list of files that should be distributed with the package
        README.md                       # Read me file; displayed by GitHub
        requirements.txt                # list of required packages
        requirements.optional.txt       # list of optional requirements
        setup.cfg                       # options for the installation script
        setup.py                        # installation script
        .circleci/                      # directory for CircleCI configuration
            config.yml                  # CircleCI configuration
            requirements.txt            # list of locations of requirements not in PyPI; for details see `Karr Lab build utilities<https://docs.karrlab.org/karr_lab_build_utils/master/0.0.13/tutorial_developers.html>_`
            downstream_dependencies.yml # List of downstream dependencies in YAML format
        .gitignore                      # list of file paths and extensions that Git should ignore
        .readthedocs.yml                # Read the Docs configuration

    *Note: the name of the source code directory should be the same as that of the repository*

* Separate code which is useful on its own, distinct from the project, into their own packages and repositories
