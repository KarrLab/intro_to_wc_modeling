Distributing Python software with GitHub, PyPI, Docker Hub, and Read The Docs
=============================================================================

The goal of this tutorial is to teach you how to distribute software with GitHub, PyPI, and Read the Docs. `GitHub <https://github.com>`_ is a code repository that can be used to distribute source code. `PyPI <https://pypi.python.org>`_ is a repository for Python software that makes it easy for users to use pip to install your software. `Docker Hub <https://hub.docker.com>`_ is a repository for Docker containers that makes it easy to distribute entire virtual machines that have your all of your software installed and fully configured. `Read The Docs <https://readthedocs.org>`_ is a repository for documentation that can be use to easily distribute documentation to end users and external developers.


Required packages
---------------------------
Execute the following commands to install the packages required for this tutorial::

  apt-get install pandoc
  pip install \
      pypandoc \
      setuptools \
      twine \
      wheel


Prepare your package for distribution
-------------------------------------

Annotate the version number of your package in ``_version.py`` and ``__init__.py``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Save the following to the ``_version.py`` file of your package, e.g. ``/path/to/intro_to_wc_modeling/intro_to_wc_modeling/_version.py``::

  __version__ = '0.0.1'y

Save the following to the ``__init__.py`` file of your package, e.g. ``/path/to/package/intro_to_wc_modeling/__init__.py``::

  import pkg_resources

  from ._version.py import __version__
  # :obj:`str`: version


Create a ``README.md`` file with an overview of the package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Save a brief description of the package to ``/path/to/package/README.md``. GitHub will display the content of this file on the landing page for the repository. For example::

  # intro_to_wc_modeling

  The goal of this tutorial is to teach you how to test and document Python code.


Create a file ``requirements.txt`` which lists the required dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The following example illustrates how to use ``/path/to/package/requirements.txt`` to specify requirements including how to specify package sources, how to specify version dependencies, and how to specify required options.::

  numpy
  scipy<=1.2
  matplotlib==2.3[option]
  git+https://github.com/KarrLab/obj_tables.git#egg=obj_tables

Packages that should be installed from PyPI should be listed by their names. Packages that should be installed from GitHub should be listed by their GitHub URL.

Version dependencies can be specified with '<', '>', '<=', '>=', and '='.

Required options can be specified by post-pending option names to each dependency.

Similarly, ``docs/requirements.txt`` and ``tests/requirements.txt`` can be used to specify packages required for testing and documentation.

In addition, ``.circleci/requirements.txt``  and ``docs/requirements.rtd.txt`` can be used to specify the locations of packages that are not in PyPI for CircleCI and Read the Docs.

Create a file ``requirements.optional.txt`` which lists the dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Optional dependencies can be listed in ``/path/to/package/requirements.optional.txt`` according this syntax:

  [option]
  dependency_1
  dependency_2
  ...

These optional dependencies can be installed by post-pending the option name(s) during pip and setup.py commands, e.g.::

  pip install package_name[option_name]


Create a license file
^^^^^^^^^^^^^^^^^^^^^
Save the following to `/path/to/package/LICENSE`::

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


Create a setup configuration file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Create a setup configuration file by following this example and saving it to ``/path/to/package/setup.cfg``::

  [bdist_wheel]
  universal = 1

  [coverage:run]
  source =
      intro_to_wc_modeling

  [sphinx-apidocs]
  packages =
      intro_to_wc_modeling


Create a ``MANIFEST.in`` file which describes additional files that should be packaged with your Python code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For example, save the following to ``/path/to/package/MANIFEST.in``::

  # documentation
  include README.rst

  # license
  include LICENSE

  # requirements
  include requirements.txt
  include requirements.optional.txt


Create a setup script
^^^^^^^^^^^^^^^^^^^^^
You can use the ``setuptools`` package to build a install script for your package. Simply edit this template and save it to ``/path/to/intro_to_wc_modeling/setup.py``::

  import setuptools
  try:
      import pkg_utils
  except ImportError:
      import subprocess
      import sys
      subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "pkg_utils"])
      import pkg_utils
  import os

  name = 'intro_to_wc_modeling'
  dirname = os.path.dirname(__file__)

  # get package metadata
  md = pkg_utils.get_package_metadata(dirname, name)

  # install package
  setup(
      name=name,
      version=md.version,

      description='Python tutorial',
      long_description=md.long_description,

      # The project's main homepage.
      url='https://github.com/KarrLab/' + name,
      download_url='https://github.com/KarrLab/' + name,

      author='Jonathan Karr',
      author_email='jonrkarr@gmail.com',

      license='MIT',

      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
      ],

      keywords='python, tutorial',

      # packages not prepared yet
      packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
      entry_points={
          'console_scripts': [
              'intro-to-wc-modeling = intro_to_wc_modeling.__main__:main',
          ],
      },

      install_requires=md.install_requires,
      extras_require=md.extras_require,
      tests_require=md.tests_require,
      dependency_links=md.dependency_links.
  )

Use the ``entry_points`` argument to specify the location(s) of command line programs that should be created. Use the ``install_requires`` argument to list any dependencies. Use the ``tests_require`` argument to specify any additional packages needed to run the tests.

See `The Hitchhiker's Guide to Packaging <http://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/quickstart.html>`_ for a more detailed explanation of the arguments to setup.

You can test the install script by running it locally::

  pip install -e .


Distributing source code with GitHub
------------------------------------
GitHub can be used to distribute source code simply by changing the public/private setting of a repository. The versions of key revisions should be marked using Git tags as illustrated below. See :numref:`code_revisioning` for more information about using Git and GitHub.::

  git add <path>
  git commit -m "<message>"
  git tag 0.0.8
  git push --tags


Distributing Python packages with PyPI
--------------------------------------
Follow the steps below to distribute your code via PyPI.

#. Create an account at `https://pypi.python.org <https://pypi.python.org>`_
#. Save your login information to ``~/.pypirc``::

    [distutils]
    index-servers =
        pypi

    [pypi]
    repository: https://upload.pypi.org/legacy/
    username: <username>
    password: <password>

#. Convert your ``README.md`` file to ``.rst`` format::

    pandoc --from=markdown --to=rst --output=README.rst README.md

#. Compile your package for source code and binary distribution::

    python2 setup.py sdist bdist_wheel
    python3 setup.py sdist bdist_wheel

#. Upload your package to PyPI::

    twine upload dist/*


There are also several online tutorials with more information about how to upload packages to PyPI

* `How to submit a package to PyPI <http://peterdowns.com/posts/first-time-with-pypi.html>`_
* `Python Packaging User Guide <https://packaging.python.org/distributing/#uploading-your-project-to-pypi>`_
* `Uploading to PyPI <https://tom-christie.github.io/articles/pypi/>`_


Distributing containers with Docker Hub
---------------------------------------
Docker Hub can be used to distribute virtual machines simply by changing the public/private setting of a repository. See :ref:`How to build a Ubuntu Linux image with Docker` for more information about using Docker and Docker Hub.


Distributing documentation with Read The Docs
---------------------------------------------
After you have configured Sphinx, committed your code to GitHub, and made your repository public, follow these instructions to configure Read The Docs to compile the documentation for your code upon each push to GitHub. Note, your configuration must follow the Sphinx configuration template in ``karr_lab_build_utils`` for Read The Docs to properly compile your documentation. Note also, Read The Docs can only be used to compile and distribute documentation for public GitHub repositories.

#. Create an account at `https://readthedocs.org <https://readthedocs.org>`_
#. Log into Read The Docs
#. Click the "Import a repository" button
#. Select the repository that you wish to distribute
#. Create the project
#. Use the "Settings" and "Advanced Settings" panels to edit the settings for the project.

    * Set the homepage and tags
    * Set the requirements file to ``docs/requirements.rtd.txt``
    * Set the Python configuration file to ``docs/conf.py``
    * Set the Python interpreter to ``CPython 3.x``

#. Optionally, use YAML files to configure the conda environment used to build the documentation within Read the Docs. This is helpful for documenting packages that depend on OS packages. The default Read the Docs conda environment cannot install OS packages, but some of these dependencies can be obtained from conda.:

    * Add the following to ``/path/to/package/.readthedocs.yml``::

        python:
           version: 3
           setup_py_install: true
        requirements_file: docs/requirements.rtd.txt
        conda:
            file: docs/conda.environment.yml

    * Add the following to ``/path/to/package/docs/conda.environment.yml``::

        name: <package>-docs
        channels:
          - conda-forge
          - defaults
        dependencies:
          - cython
          - pip
          - python
          - sphinx
          - pip:
            - configparser
            - sphinx_rtd_theme
            - robpol86-sphinxcontrib-googleanalytics
            - sphinxcontrib-bibtex
            - sphinxcontrib-spelling

#. Add your email in the "Notifications panel" so that you receive notifications documentation compilation errors
#. Check for errors

  * Navigate to "Builds"
  * Click on the latest build
  * Browse the tabs for errors and warnings