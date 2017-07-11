Structuring Python projects
===========================
We recommend using the following principles to organize Python projects:

* Use separate repositories for each project
* Store only one package in each repository
* Structure each package as outlined below following the recommendations provided by `The Hitchhiker's Guide To Python <http://python-guide-pt-br.readthedocs.io/en/latest/writing/structure/>`_:

    .. code-block :: text

        repository_name/      # source code directory
            __init__.py       # each source code directory must contain an ``__init__.py`` file
            data/             # directory for data files needed by the code
        tests/                # directory for test code
            requirements.txt  # list of packages required to run the tests; used by CircleCI
        docs/                 # directory for documentation
            conf.py           # documentation configuration
            index.rst         # main documentation file
            requirements.txt  # list of packages required to compile the documentation; used by Read the Docs
            _build/html/      # directory where compiled documentation is saved
        examples/             # (optional) directory for examples of how to use the code    
        LICENSE               # license file
        MANIFEST.in           # list of files that should be distributed with the package
        README.md             # Read me file; displayed by GitHub
        setup.cfg             # options for the installation script 
        setup.py              # installation script
        .circleci/            # directory for CircleCI configuration
            config.yml        # CircleCI configuration
        .gitignore            # list of file paths and extensions that Git should ignore

    *Note: the name of the source code directory should be the same as that of the repository*

* Separate code which is useful on its own, distinct from the project, into their own packages and repositories
