Writing Python code
===================

Installing Python
-----------------
Execute the following command to install Python, the pip Python package manager, the Sublime text editor, and the PyCharm integrated development environment (IDE) ::

    apt-get install \
        mysql-server \
        python \
        python3 \
        python-pip \
        python3-pip \
        ipython \
        ipython3

    pip install \
        cement \
        Flask

    sudo add-apt-repository ppa:webupd8team/sublime-text-3
    sudo apt-get update
    sudo apt-get install sublime-text-installer

    mv ~/Downloads/pycharm-community-2017.1.tar.gz /opt/
    tar -xzf pycharm-community-2017.1.tar.gz
    cd pycharm-community-2017.1
    ./pycharm.sh

Open Sublime and edit the following settings

* Preferences >> Key Bindings::

    [
        { "keys": ["ctrl+shift+r"], "command": "unbound"}
    ]
            
* Preferences >> Package control >> Install package >> AutoPEP8
* Preferences >> Package settings >> AutoPep8 >> Settings-User::

    [{"keys": ["ctrl+shift+r"], "command": "auto_pep8", "args": {"preview": false}}]

Open PyCharm and set the following settings to configure Pycharm

    * File >> Settings >> Tools >> Python Integrated Tools >> Default test runner: set to py.test
    * Run >> Edit configurations >> Defaults >> Python tests >> py.test: add additional arguments "--capture=no"
    * Run >> Edit configurations >> Defaults >> Python tests >> Nosetests: add additional arguments "--nocapture"


Helpful code editors
--------------------
Below are several recommended programs for editing Python code

* Text editors

    * `Atom <https://atom.io/>`_
    * `Notepad++ <https://notepad-plus-plus.org/>`_
    * `Sublime <https://www.sublimetext.com>`_

* Integrated development environments (IDEs)
    * `Canopy <https://www.enthought.com/products/canopy/>`_: tailored for science
    * `PyCharm <https://www.jetbrains.com/pycharm/>`_: good support for testing and general development
    * `Spyder <http://pythonhosted.org/spyder/>`_: tailored for science


An introduction to Python
-------------------------
There are numerous introductory Python tutorials

* `Learn Python <https://www.codecademy.com/learn/python>`_
* `Intro to Python for Data Science <https://www.datacamp.com/tracks/python-developer>`_
* `Learn Python the hard way <https://learnpythonthehardway.org/book>`_

Several important concepts to learn include

* Variables

    * Booleans, integers, floats, string
    * Dictionaries, lists, sets, tuples

* For and while loops
* Context managers
* Functions

    * Required and optional arguments
    * Returns    

* Classes

    * Key principles: abstraction, encapsulation, inheritance, polymorphism
    * Getters, setters

* Modules
* Importing
* Decorators
* Raising and handling exceptions and warnings
* Printing to the command line and prompting for input including formatting text
* Reading and writing to/from files


Comparison between Python and MATLAB
------------------------------------
Several websites have nice summaries of the advantages of Python over MATLAB

* `Python vs Matlab <http://www.pyzo.org/python_vs_matlab.html>`_
* `A Python Primer for Matlab Users <http://bastibe.de/2013-01-20-a-python-primer-for-matlab-users.html>`_
* `NumPy for Matlab users <https://docs.scipy.org/doc/numpy-dev/user/numpy-for-matlab-users.html>`_


How to structure Python code
----------------------------
There are several good resources on how to effectively structure Python code, including common

* `Python 3 Patterns, Recipes and Idioms <http://python-3-patterns-idioms-test.readthedocs.io/en/latest/index.html>`_
* Python Design Patterns: `Video <https://www.youtube.com/watch?v=4KZx8bATBFs&t=2434s>`_, `Slides <http://www.aleax.it/gdd_pydp.pdf>`_
* How To Design A Good API and Why it Matters: `Video <https://www.youtube.com/watch?v=aAb7hSCtvGw>`_, `Slides <http://zoomq.dn.qbox.me/ZQCollection/presentations/Howto-Design-a-Good-API_Why%20it%20Matters.pdf>`_


How to structure the files within a Python project
--------------------------------------------------
We are using the following convention to structure our Python source code repositories. This convention largely follows that recommended in `The Hitchhiker's Guide To Python <http://python-guide-pt-br.readthedocs.io/en/latest/writing/structure/>`_::

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


Using databases with SQLAlchemy and SQLite
-----------------------------------------------
Databases are useful tools for organizing and quickly searching large datasets. Relational databases are the most common type of databases. Relational databases are based around schemas or structured definitions of the types of your data and the relationships among your data. These structured definitions facilitate fast searching of large datasets. However, these schemas can also make it cumbersome to represent multiple types of data with different structures. To overcome this limitation, several Python package provide support for editing or migrating schemas. Recently, there has been significant progress in the development of No-SQL databases which do not have fixed schemas.

Database engines are the software programs which implement SQL and No-SQL databases. Several popular SQL database engines include MySQL, Oracle, and SQLite. Several popular No-SQL database engines include CouchBase, CouchDB, and MongoDB.

SQL (Structured Query Language) is the language used to describe relational database schemas and how to insert and retrieve data to/from them. Each relational database engine uses it own variant of SQL, but the SQL langauges used by MySQL, Oracle, SQLite and most other popular relational database engines are very similar.

Most of the popular database engines have their own Python interfaces. In addition, there are several Python packages such as SQLAlchemy which abstract away many of the details the individual database engines and enable Python developers to use database with little direct interaction with SQL.

There are several good tutorial on how to use SQLAlchemy and SQLite

* `Introductory Tutorial of Python's SQLAlchemy <http://pythoncentral.io/introductory-tutorial-python-sqlalchemy/>`_
* `SQLAlchemy ORM for Beginners <https://www.youtube.com/watch?v=51RpDZKShiw>`_
* `SQLAlchemy Object Relational Tutorial <http://docs.sqlalchemy.org/en/latest/orm/tutorial.html>`_


Building command line programs with Cement
------------------------------------------
`Cement <http://builtoncement.com>`_ is a useful package for easily building command line programs.

See the `Cement quickstart guide <http://builtoncement.com/2.10/dev/quickstart.html>`_ for an introduction to Cement.


Building web-based programs with Flask
--------------------------------------
`Flask <http://flask.pocoo.org>`_ is a useful package for building web-based programs.

There are several good Flask tutorials

* `Flask Tutorial <http://flask.pocoo.org/docs/0.12/tutorial/>`_
* `The Flask Mega-Tutorial <https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world>`_
* `Flask by Example <https://realpython.com/blog/python/flask-by-example-part-1-project-setup/>`_


Building code for Python 2 and 3
--------------------------------
Because Python 2.7 and 3 are similar, and because many people still use Python 2, we aim to write code that works on both Python 2 and 3. The ``six`` package provides several helpful utilities for writing code that works on both Python 2 and 3 with little extra effort.


Using the PyCharm debugger to debug code
----------------------------------------
Debuggers are useful tools for debugging code that can be are far more powerful than print statements or logging. Debbuggers allow users to interactively inspect Python programs during their execution. In particular, debuggers allow users to set breakpoints at which the Python interpret should halt its execution and enable the user to inspect the state of the program (value of each variable in the namespace and in all parent namespaces), run an arbitrary Python code (e.g. to print something out), step through the code (instruct the Python interpreter to execute one additional instructions of the program), and/or resume the program. Debuggers also allow users to set conditional breakpoints which can be used to halt the execution of a program when the value of a variable meets a specific condition. Together, debuggers make it easy to trace through programs and find errors.

Most IDEs include debuggers and there are debugger plugins for text editors such as Sublime. We recommend the PyCharm debugger. There are several tutorials on how to use PyCharm to debug code.

* `Debugging in Python (using PyCharm) <https://waterprogramming.wordpress.com/2015/09/10/debugging-in-python-using-pycharm/>`_
* `PyCharm Debugger Tutorial <https://confluence.jetbrains.com/display/PYH/Debugger>`_
* `Getting Started with PyCharm 6/8: Debugging <https://www.youtube.com/watch?v=QJtWxm12Eo0>`_
