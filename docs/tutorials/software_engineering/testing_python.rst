Testing Python code with unittest, pytest, and Coverage
=======================================================

The goal of this tutorial to teach you how to effectively test and debug Python code.

`Unit testing <https://en.wikibooks.org/wiki/Introduction_to_Software_Engineering/Testing/Unit_Tests>`_ is a powerful methodology for testing and debugging code and ensuring that code works as intended. You can unit test your code by writing numerous tests of your code, each of which executes the code and assert that the expected result is produced. 

To use unit testing effectively, it is best to begin by writing tests of individual pieces of your code, debugging each individual piece until they all work, and then proceeding to write larger tests of larger assemblies of code. 

Collectively, your tests should cover or execute every line of your code. This line coverage can be assessed using the coverage and pytest-cov packages.


Required packages
---------------------------
Execute the following commands to install the packages required for this tutorial::
    
    apt-get install \
        python \
        python-pip
    pip install \
        capturer \
        cement \
        coverage \
        numpy \
        pytest \
        pytest-cov \


File naming and organization
-----------------------------
Our convention is to store tests within separate ``tests`` subdirectories within each repository. Any non-Python files which are needed for testing, can be organized in a ``fixtures`` subdirectory. The ``tests`` directory should also contain a ``requirements.txt`` file which lists all of the packages that are needed to run the tests.

Often it is helpful create one file for all of the tests for each source code file and to name this ``test_<source_filename>.py``.

Taken together, your test code should be organized as follows::

    /path/to/repo/
        tests/                              # directory for all of the test files
            <source_modulename>             # parallel directory structure to source code
                test_<source_filename>.py   # parallel filenames to source code
            fixtures/                       # files needed by the tests
            requirements.txt                # list of packages needed to run the tests


Writing tests
-----------------------
In the remainder of the tutorial, we will write tests for the code located in ``/path/to/this/repo/karr_lab_tutorials/software_engineering/unit_testing/`` to run a simple stochastic simulation.

#. Create a file for the tests, `tests/software_engineering/unit_testing/test_core.py`
#. Write a test file. For example::

    from karr_lab_tutorials.software_engineering.unit_testing import core
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

Each test method should begin within the prefix ``test_``

There are a large number of use assertions such as those below that can be used to verify that code produces the expected results. See the `unittest documentation <https://docs.python.org/2/library/unittest.html>`_ and the `numpy.testing documentation <https://docs.scipy.org/doc/numpy/reference/routines.testing.html>`_ for additional assertions.

* ``unittest.TestCase.assertEqual``
* ``unittest.TestCase.assertNotEqual``
* ``unittest.TestCase.assertTrue``
* ``unittest.TestCase.assertFalse``
* ``unittest.TestCase.assertIsInstance``
* ``unittest.TestCase.assertGreater``
* ``unittest.TestCase.assertLess``
* ``unittest.TestCase.assertAlmostEqual``
* ``unittest.TestCase.assertRaises``
* ``numpy.testing.assert_array_equal``
* ``numpy.testing.assert_array_almost_equal``

The ``setUp`` and ``tearDown`` methods can be used to organize the code that should be executed before and after each individual test. This is often useful for creating and removing temporary files. Similarly, the ``setUpClass`` and ``tearDownClass`` can be used to organize code that should be executed before and after the execution of all of the tests. This can be helpful to organizing computationally expensive operations that don't need to be executed multiple times.


Testing stochastic algorithms
-----------------------------
Stochastic codes should be validated by testing the statistical distribution of their output. Typically this is done with the 
following process

#. Run the code many times and keep a list of the outputs
#. Run a statistical test of the distribution of the outputs. At a minimum test the average of the distribution is
   close to the expected value. If possible, also test the variance of the distribution and higher-order moments of the
   distribution.


Testing standard output
-----------------------
The ``capturer`` package is helpful for collecting and testing stdout generated by code. This can be used to test standard output as shown in the example below::

    import capturer

    def test_stdout(self):
        with capturer.CaptureOutput() as captured:
            run_method()
            stdout = captured.get_text()
            self.assertEqual(stdout, expected)


Testing cement command line programs
--------------------------------------
Cement command line programs can be tested as illustrated below:

    from karr_lab_tutorials import __main__
    import capturer

    def test(self):
        # array of command line arguments, just as they would be supplied at the command line except
        # each should be an element of an array
        arv = ['value']

        with __main__.App(argv=argv) as app:
            with capturer.CaptureOutput() as captured:
                app.run()
                self.assertEqual(captured.get_text(), expected_value)

See [`tests/test_main.py`](tests/test_main.py) for an annotated example.


Testing for multiple version of Python
---------------------------------------
You should test your code on both major versions of Python. This can be done as follows::

    python2 -m pytest tests
    python3 -m pytest tests


Running your tests
------------------
You can use pytest as follows to run all or a subset of your tests::

    python -m pytest tests                                         # run all tests in a directory
    python -m pytest tests/test_core.py                            # run all tests in a file
    python -m pytest tests/test_core.py::TestSimulation            # run all tests in a class
    python -m pytest tests/test_core.py::TestSimulation::test_run  # run a specific test
    python -m pytest tests -k run                                  # run tests that contain `run` in their name
    python -m pytest tests -s                                      # use the `-s` option to display the stdout generated by the tests


Analyzing the coverage of your tests
------------------------------------

Test coverage can be analyzed as follows:

    python -m pytest --cov=karr_lab_tutorials tests


This prints a summary of the coverage to the console and saves the details to ``.coverage``.

The following can be used to generated a more detailed HTML coverage report. The report will be saved to ``htmlcov/``::

    coverage html

You can view the HTML report by opening ``file:///path/to/karr_lab_tutorials/htmlcov/index.html`` 
in your browser. Green indicates lines that were executed by the tests. Red indicates lines that 
were not executed. Large amounts of red lines means that more tests are needed. Ideally, code
would be tested to 100% coverage.


Additional tutorials 
--------------------
There are numerous additional tutorials on unit testing Python

* `Understanding Unit Testing <https://jeffknupp.com/blog/2013/12/09/improve-your-python-understanding-unit-testing/>`_
* `Testing Python Applications with Pytest <https://semaphoreci.com/community/tutorials/testing-python-applications-with-pytest>`_
