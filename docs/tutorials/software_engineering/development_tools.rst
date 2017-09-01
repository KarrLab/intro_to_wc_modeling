Recommended development Python tools
====================================
Below are several recommended programs for developing Python code:

* Text editors

    * `Atom <https://atom.io/>`_
    * `Notepad++ <https://notepad-plus-plus.org/>`_
    * `Sublime <https://www.sublimetext.com>`_

* Interactive Python shells

    * `ipython <https://ipython.org>`_
    * `Jupyter <https://jupyter.org/>`_ notebooks

* Integrated development environments (IDEs) with debuggers

    * `Canopy <https://www.enthought.com/products/canopy/>`_: tailored for science
    * `PyCharm <https://www.jetbrains.com/pycharm/>`_: good support for testing and general development
    * `Spyder <http://pythonhosted.org/spyder/>`_: tailored for science

* Test runners

    * `nose <http://nose.readthedocs.io>`_
    * `pytest <https://docs.pytest.org>`_

* Test coverage tools

    * `coverage <https://coverage.readthedocs.io>`_

* Profilers
    
    * `cProfile <https://docs.python.org/2/library/profile.html#module-cProfile>`_
    * `line_profiler <https://github.com/rkern/line_profiler>`_
    * `memory_profiler <https://github.com/fabianp/memory_profiler>`_

* Documentation generation

    * `Sphinx <http://www.sphinx-doc.org>`_
    * `Napoleon sphinx extension <http://www.sphinx-doc.org/en/latest/ext/napoleon.html>`_

* Installing packages

    * `pip <https://pip.pypa.io>`_
    * `PyPI <http://pypi.python.org>`_

* Packaging code

    * `setuptools <https://packaging.python.org/>`_
    * `twine <https://packaging.python.org/>`_

.. _software_development_tools_installation:

Installation
------------

Python
^^^^^^
Execute the following command to install Python 2 and 3::

    apt-get install python python3


Pip package manager
^^^^^^^^^^^^^^^^^^^
Execute the following command to install the pip package manager::
    
    apt-get install python-pip python3-pip


ipython interactive shell
^^^^^^^^^^^^^^^^^^^^^^^^^
Execute the following command to install the ipython interactive shell::
    
    apt-get install ipython ipython3


Sublime code editor
^^^^^^^^^^^^^^^^^^^
Execute the following command to install the Sublime code editor::

    sudo add-apt-repository ppa:webupd8team/sublime-text-3
    sudo apt-get update
    sudo apt-get install sublime-text-installer

We also recommend editing the following settings:

* Preferences >> Key Bindings::

    [
        { "keys": ["ctrl+shift+r"], "command": "unbound"}
    ]
            
* Preferences >> Package control >> Install package >> AutoPEP8
* Preferences >> Package settings >> AutoPep8 >> Settings-User::

    [{"keys": ["ctrl+shift+r"], "command": "auto_pep8", "args": {"preview": false}}]


PyCharm IDE
^^^^^^^^^^^
Execute the following command to install the PyCharm IDE::

    mv ~/Downloads/pycharm-community-2017.1.tar.gz /opt/
        tar -xzf pycharm-community-2017.1.tar.gz
        cd pycharm-community-2017.1
        ./pycharm.sh

We also recommend editing the following settings:

    * File >> Settings >> Tools >> Python Integrated Tools >> Default test runner: set to py.test
    * Run >> Edit configurations >> Defaults >> Python tests >> py.test: add additional arguments "--capture=no"
    * Run >> Edit configurations >> Defaults >> Python tests >> Nosetests: add additional arguments "--nocapture"
