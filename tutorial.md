The goal of this tutorial is to teach you how to test and document Python code.

# Install requirements

* Linux packages
  ```
  apt-get install \
      git \                                    # repository manager
      meld \                                   # graphical differencing tool
      libgnome-keyring-dev \                   # password manager
      python \                                 # programming language
      python-pip                               # python package manager
  ```
* Python packages
  ```
  pip install \
      setuptools                               # utility for distributing python packages

  pip install \
      capturer \                               # capture stdout
      configparse \                            # configuration file parser
      cement \                                 # framework for building command line programs
      codeclimate-test-reporter \              # tool to upload coverage reports to Code Climate
      coverage \                               # coverage tool
      coveralls \                              # tool to upload coverage reports to coveralls
      ipython \                                # interactive python shell
      pytest \                                 # test runner
      pytest-cov \                             # pytest plugin for coverage
      robpol86-sphinxcontrib-googleanalytics \ # sphinx support for google analytics 
      six \                                    # utilities for python 2/3 compatibility
      sphinx \                                 # documentation generator
      sphinx-rtd-theme                         # sphinx HTML theme
  ```
        
# Create repository

1. Create a GitHub account
2. Sign into GitHub
3. Add a repository at [https://github.com/new](https://github.com/new)

   *Note: package names should be in "lower_camel_case"*

4. Clone the new repository to your computer
  ```
  cd ~/Documents
  git clone https://github.com/KarrLab/python_tutorial.git
  ```

# Setup the directory structure within the repository
```
cd ~/Documents/python_tutorial
mkdir python_tutorial             # to hold source code
touch python_tutorial/__init__.py # each directory with code must contain an `__init__.py` file
mkdir python_tutorial/data        # directory to hold any data files needed by the code
```

*Note: the name of the source code directory should be the same as that of the repository*

# Write some code

See [`python_tutorial/core.py`](python_tutorial/core.py) for an annotated example.

## Making command line utilities

[`cement`](https://builtoncement.com) can be used to easily build command line utilities.

See [`python_tutorial/__main__.py`](python_tutorial/__main__.py) for a simple example. See
`https://github.com/KarrLab/kinetic_datanator/blob/master/kinetic_datanator/__main__.py`
for a more extensive example with nested controllers.

# Write tests to make sure the code works

## Create a directory structure for the tests
```
cd ~/Documents/python_tutorial
mkdir tests                    # directory to hold tests; the canonical name is `tests`
touch tests/requirements.txt   # list of required packages to run the tests
mkdir tests/fixtures           # directory to hold any files needed for the tests
```

## Write one or more tests

1. Create a file for the tests, e.g. `tests/test_core.py`. The file should start with the prefix `test_'. The directory
   structure for the tests should generally parallel that of the source code.
2. Write a test file. For example: 
  ```
  from python_tutorial import core
  import unittest

  class TestSimulation(unittest.TestCase):
      class NewClass():
          pass

      @classmethod
      def setUpClass(cls):
          """ Code to execute before all of the tests. For example, this can be used to create temporary
          files.
          """
          pass

      @classmethod
      def tearDownClass(cls):
          """ Code to execute after all of the tests. For example, this can be used to clean up temporary
          files.
          """
          pass

      def setUp(self):
          """ Code to execute before each test. """
          pass

      def tearDown(self):
          """ Code to execute after each test. """
          pass

      def test_run(self):
          self.NewClass

          # run code
          sim = core.Simulation()
          hist = sim.run(time_max=10)

          # check the result
          self.assertEqual(hist.times[0], 0.)
  ```
  
  The goal of testing is to make sure that your code works as intended. Thus, each test should should (1) run some code and 
  (2) check (or "assert") its results to make sure the code functions as intended. Collectively, all of your tests should
  validate the results of every line of your code. This can be assessed using coverage analysis. See below for more
  information.

  Generally, it it helpful to start by testing small pieces of code such as individual methods and then work
  your way up to testing entire classes and packages. This is done by creating multiple test methods, each
  which start with the prefix `test_`.

  There are a large number of use assertions such as those below. See the [`unittest` documentation](https://docs.python.org/2/library/unittest.html)
  and the [`numpy.testing` documentation](https://docs.scipy.org/doc/numpy/reference/routines.testing.html) for additional assertions.

  * `unittest.TestCase.assertEqual`
  * `unittest.TestCase.assertNotEqual`
  * `unittest.TestCase.assertTrue`
  * `unittest.TestCase.assertFalse`
  * `unittest.TestCase.assertIsInstance`
  * `unittest.TestCase.assertGreater`
  * `unittest.TestCase.assertLess`
  * `unittest.TestCase.assertAlmostEqual`
  * `unittest.TestCase.assertRaises`
  * `numpy.testing.assert_array_equal`
  * `numpy.testing.assert_array_almost_equal`
 
  See [`tests/test_core.py`](tests/test_core.py) for an annotated example.

## Run the tests
You can use pytest to run all or a subset of the tests
```
python -m pytest tests                                         # run all tests in a directory
python -m pytest tests/test_core.py                            # run all tests in a file
python -m pytest tests/test_core.py::TestSimulation            # run all tests in a class
python -m pytest tests/test_core.py::TestSimulation::test_run  # run a specific test
python -m pytest tests -k run                                  # run tests that contain `run` in their name
python -m pytest tests -s                                      # use the `-s` option to display the stdout generated by the tests
```

## Testing stochastic algorithms
Stochastic codes should be validated by testing the statistical distribution of their output. Typically this is done with the 
following process:

1. Run the code many times and keep a list of the outputs
2. Run a statistical test of the distribution of the outputs. At a minimum test the average of the distribution is
   close to the expected value. If possible, also test the variance of the distribution and higher-order moments of the
   distribution.

## Testing for multiple version of python
We are aiming to support both the latest versions of Python 2 and 3. Therefore, you should test your code on both versions.
```
python2 -m pytest tests
python3 -m pytest tests
```

*Note: The `six` package provides several helpful utilities for writing code that works on both Python 2 and 3 with very little extra
effort.*

## Testing stdout generated by code
The `capturer` package is helpful for collecting and testing stdout generated by code. For example:
```
import capturer

def test_stdout(self):
    with capturer.CaptureOutput() as captured:
        run_method()
        stdout = captured.get_text()
        self.assertEqual(stdout, expected)
```

## Testing `cement` command line programs

Cement command line programs can be tested as illustrated below:
```
from python_tutorial import __main__
import capturer

def test(self):
    # array of command line arguments, just as they would be supplied at the command line except
    # each should be an element of an array
    arv = ['value']

    with __main__.App(argv=argv) as app:
        with capturer.CaptureOutput() as captured:
            app.run()
            self.assertEqual(captured.get_text(), expected_value)
```

See [`tests/test_main.py`](tests/test_main.py) for an annotated example.

## Analyze the coverage of the tests
Test coverage can be analyzed as follows:
```
python -m pytest --cov=python_tutorial tests
```

This prints a summary of the coverage to the console and saves the details to `.coverage`.

The following can be used to generated a more detailed HTML coverage report. The report
will be saved to `htmlcov`. 
```
coverage html
```

You can view the HTML report by opening `file:///path/to/python_tutorial/htmlcov/index.html` 
in your browser. Green indicates lines that were executed by the tests. Red indicates lines that 
were not executed. Large amounts of red lines means that more tests are needed. Ideally, code
would be tested to 100% coverage.

# Document the code

## Create a directory for the top-level documentation
```
cd ~/Documents/python_tutorial
mkdir docs                  # directory to hold documentation; the canonical name is `docs`
touch docs/requirements.txt # list of required packages to compile the documentation
mkdir examples              # directory to hold examples
```

## Use `sphinx-quickstart` to create a documentation configuration file `docs/conf.py`
```
sphinx-quickstart
  # root path: docs
  # Project name: python_tutorial
  # Author name(s): Jonathan Karr
  # Do you want to use the epub builder: n
  # autodoc: automatically insert docstrings from modules: y
  # Create Makefile?: n
  # Create Windows command file? n
```

## Customize the documentation configuration
Add the following to the top of `docs/conf.py`
```
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import python_tutorial
```

Enable these additional packages
```
'sphinx.ext.napoleon',
'sphinxcontrib.googleanalytics',
```

Add napolean options
```
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
```

Set the version and release
```
version = python_tutorial.__version__
release = version
```

Set the theme
```
import sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_show_sphinx = False
html_show_sourcelink = False
html_show_copyright = True
```

Set the Google Analytics id
```
googleanalytics_id = 'UA-86340737-1'
```

Add the following to run sphinx-apidoc within ReadTheDocs on sphinx-build. Place the
following at the bottom of `docs/conf.py`.
```
from configparser import ConfigParser
from sphinx import apidoc

def run_apidoc(app):
    this_dir = os.path.dirname(__file__)
    parser = ConfigParser()
    parser.read(os.path.join(this_dir, '..', 'setup.cfg'))
    packages = parser.get('sphinx-apidocs', 'packages').strip().split('\n')
    for package in packages:
        apidoc.main(argv=['sphinx-apidoc', '-f', '-o', os.path.join(this_dir, 'source'), os.path.join(this_dir, '..', package)])

def setup(app):
    app.connect('builder-inited', run_apidoc)
```

Save the following to `setup.cfg`
```
[metadata]
long_description = file: README.rst

[bdist_wheel]
universal = 1

[coverage:run]
source = 
    python_tutorial

[sphinx-apidocs]
packages = 
    python_tutorial
```

Append this line to the `.. toctree::` section of `docs/index.rst`
```
source/modules.rst
```

Save the following to the `__init__.py` file of your package, e.g. `python_tutorial/__init__.py`
```
__version__ = '0.0.1'
```

## Document each class, method, and attribute
Use the `napoleon` style below to document each class, method, and attribute

See [`python_tutorial/core.py`](python_tutorial/core.py) for an annotated example.

### Classes
```
class Class():
    """ Description

    Attributes:
        name (:obj:`core.Simulation`): description
    """

    ...
```

### Methods
```
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
```

## Create top-level documentation

Add top-level documentation to `docs/index.rst` in the reStructuredText markup language. See the 
[reStructuredText primer](http://www.sphinx-doc.org/en/stable/rest.html#rst-primer) for a brief tutorial 
about the reStructuredText markup language.

## Compile the documentation
Run the following to compile the documentation.
```
sphinx-build docs docs/_build/html 
```

Sphinx will print out any errors in the your documentation. These must be fixed to properly generate
the documentation.

The documenation can be viewed by opening `docs/_build/html/index.html` in your browser.

# Package the code

## Set the version number

Save the following to the `__init__.py` file of your package, e.g. `python_tutorial/__init__.py`
```
__version__ = '0.0.1'
```

## Create a file which lists the required packages

Save a list of required packages to `requirements.txt`. The following illustrates
how to specify packages for PyPI or GitHub and how specify specific package versions.
```
numpy
scipy<=1.2
matplotlib==2.3
git+https://github.com/KarrLab/obj_model.git#egg=obj_model
```

Save lists of required packages for testing and documenation to `docs/requirements.txt`
and `tests/requirements.txt`.

## Create a readme file with an overview of the package

Save a brief description of the package to `README.md`. GitHub will display the content of this
file on the landing page for the repository. For example:

```
# python_tutorial

The goal of this tutorial is to teach you how to test and document Python code.
```

## Create a license file

Save the following to `LICENSE`
```
The MIT License (MIT)

Copyright (c) <Year> Karr Lab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Create a setup configuration file

Save the following to `setup.cfg`
```
[metadata]
long_description = file: README.rst

[bdist_wheel]
universal = 1

[coverage:run]
source = 
    python_tutorial

[sphinx-apidocs]
packages = 
    python_tutorial
```

## Create a `MANIFEST.in` file which describes additional files that should be packaged with Python code

Save the following to `MANIFEST.in`
```
# license
include LICENSE

# requirements
include requirements.txt

# documentation
include README.rst
```

## Create a setup script
Create a `setup.py`. See [`setup.py`](setup.py) for an example.

## Test the setup

Install the package locally with the `-e` option:
```
pip install -e .
```

## Push code to GitHub

1. Configure git
  ```
  git config --global user.name "John Doe"
  git config --global user.email johndoe@example.com

  cd /usr/share/doc/git/contrib/credential/gnome-keyring
  sudo make
  git config --global credential.helper /usr/share/doc/git/contrib/credential/gnome-keyring/git-credential-gnome-keyring
  ```

  Add the following to ~/.gitconfig
  ```
  [diff]
    tool = meld
  [difftool]
      prompt = false
  [difftool "meld"]
      cmd = meld "$LOCAL" "$REMOTE"
  ```
2. Review your changes
  ```
  git diff /path/to/file
  git difftool /path/to/file
  ```
3. Commit the changes to the code to your local Git repository
  ```
  git commit -a -m "<Description of the changes to the code>"  
  ```
4. Pull recent changes from other developers
  ```
  git pull
  ```
5. Merge any conflicts by editing the conflicting files
6. Push the changes to the central repository at GitHub
  ```
  git push
  ```
## Push code to PyPI

1. Convert readme to .rst format
2. Todo

# Integrate with cloud-based development tools (CircleCI, Code Climate, Read The Docs, tests.karrlab.org)

## CircleCI
1. Log into [CircleCI](https://circleci.com)
2. Click on the `Projects` tab
3. Click the `Add a project` button
4. Click the `Build` button for the selected repository
5. Add environment variables for the Code Climate, Coveralls, and Karr Lab server password
  * CODECLIMATE_REPO_TOKEN 
  * COVERALLS_REPO_TOKEN
  * TEST_SERVER_TOKEN: jxdLhmaPkakbrdTs5MRgKD7p
6. Create a configation file to instruct CircleCI what to do
  
   See [`.circleci/config.yml`](.circleci/config.yml) for an example. See the [CircleCI documentation](https://circleci.com/docs/2.0/)
   for more information.

If you push a commit which breaks the tests, you are responsible for fixing the problem or notifying
whoever else you think is response. It is important to fix the problem quickly while its fresh in 
memory and so you don't suffer from test failure fatigure.

## Coveralls
1. Log into [Coveralls](https://coveralls.io)
2. Click the "Add repos" button
3. Turn the selected the repository on
4. To push coverage data to Coveralls,
   1. Copy the `repo_token`
   2. Create an environment variable in the corresponding CircleCI build with the key = `COVERALLS_REPO_TOKEN`
      and the value = the value of the `repo_token`

## Code Climate
1. Log into [Code Climate](https://codeclimate.com/dashboard)
2. Click one of the "Add a repository" links
3. Select the desired repository
4. To view the analysis, return to your dashboard and select the package from the dashboard
5. To push coverage data to Code Climate
   1. Open the settings for the package
   2. Navigate to the 'Test Coverage' settings
   3. Copy the `Test reporter ID`
   4. Create an environment variable in the corresponding CircleCI build with the key = `CODECLIMATE_REPO_TOKEN`
      and the value = the value of the `Test reporter ID`

## Read The Docs
1. Log into [Read The Docs](https://readthedocs.org)
2. Click the `Import a repository` button
3. Select the repository
4. Create the project
5. Edit the settings
  * Advanced settings
    * Requirements file: docs/requirements.txt
  * Notifications
    * Add email
6. Check for errors
  * Navigate to builds
  * Click on the latest build
  * Browse the tabs for errors

## code.karrlab.org
1. SSH into code.karrlab.org
2. Add a repository configuration file to /home/karrlab_code/code.karrlab.org/repo/<repo-name>.json
3. Copy the syntax from the other files in that directory

## Add badgets to `README.md`
Add the following to the top of `README.md`
```
<!-- [![PyPI package](https://img.shields.io/pypi/v/python_tutorial.svg)](https://pypi.python.org/pypi/python_tutorial) -->
[![Documentation](https://readthedocs.org/projects/karrlab_python_tutorial/badge/?version=latest)](http://karrlab_python_tutorial.readthedocs.org)
[![Test results](https://circleci.com/gh/KarrLab/python_tutorial.svg?style=shield)](https://circleci.com/gh/KarrLab/python_tutorial)
[![Test coverage](https://coveralls.io/repos/github/KarrLab/python_tutorial/badge.svg)](https://coveralls.io/github/KarrLab/python_tutorial)
[![Code analysis](https://codeclimate.com/github/KarrLab/python_tutorial/badges/gpa.svg)](https://codeclimate.com/github/KarrLab/python_tutorial)
[![License](https://img.shields.io/github/license/KarrLab/python_tutorial.svg)](LICENSE)
![Analytics](https://ga-beacon.appspot.com/UA-86759801-1/python_tutorial/README.md?pixel)
```

# Build a custom virtual machine for CircleCI

See 
* [Docker](https://www.docker.com)
* [Docker Hub](https://hub.docker.com)
* [http://private.karrlab.org/wiki/index.php?title=Docker_installation_and_setup_instructions](http://private.karrlab.org/wiki/index.php?title=Docker_installation_and_setup_instructions)
* [https://github.com/KarrLab/karr_lab_docker_images](https://github.com/KarrLab/karr_lab_docker_images)
