An introduction to Python
=========================
The goal of this tutorial is to introduce the fundamentals of Python. This tutorial assumes familiarity with at least one other object-oriented programming language such as Java, MATLAB, or Perl.

For a more elementary introduction to Python for individuals with little or no programming experience, we recommend the following five websites. The first four of the websites provide interactive coding exercises.

* `Codecademy: Learn Python <https://www.codecademy.com/learn/python>`_
* `DataCamp: Intro to Python for Data Science <https://www.datacamp.com/tracks/python-developer>`_
* `Dataquest: Python Programming <https://www.dataquest.io/subject/learning-python>`_
* `Rosalind: Python problems <http://rosalind.info/problems/list-view/?location=python-village>`_
* `Learn Python the hard way <https://learnpythonthehardway.org/book>`_


Key concepts
------------
This tutorial will teach you how to use the following Python elements

* Core language features

    * Core builtin data types
    * Variables
    * Operators
    * Boolean statements
    * Loops
    * Context managers
    * Functions
    * Classes
    * Modules
    * Decorators

* Copying variables
* String formatting
* Printing to standard out
* Numerical computing with ``NumPy``
* Plotting graphs with ``matplotlib``
* Reading and writing to/from text, csv, and Excel files
* Exceptions and warnings


Installing Python and Python development tools
----------------------------------------------
To get started using Python, we recommend installing Python 3, the `pip package manager <https://pip.pypa.io>`_, the `Sublime text editor <https://www.sublimetext.com/>`_, and the `ipython interactive shell <https://ipython.org>`_. See our :ref:`installation instructions <software_development_tools_installation>` for more information.


Data types
----------

Scalars
^^^^^^^
Python provides several classes to represent Booleans (``bool``), integers (``int``), floats (``float``), and strings (``str``). The following code instantiates Python Booleans, integers, floats, and strings::

    True       # a instance of `bool`
    False      # another instance of `bool`
    1          # an instance of `int`
    1.0        # an instance of `float`
    'a string' # an instance of `str`


Lists, tuples, sets, and dictionaries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Python also provides several classes to represent lists (``list`` and ``tuple``), sets (``set``), and hashes (``dict``). The following code creates Python lists, sets, and hashes::

    [1, 2, 3]        # a `list`
    (1, 2, 3)        # a `tuple`
    set([1, 2, 3])   # a `set`
    {'a': 1, 'b': 2} # a `dict`

Lists and tuples can both represent ordered series of values. The major difference between lists and tuples is that lists are mutable (elements can be added and removed), whereas tuples are immutable (elements cannot be added or removed). In addition, tuples can be unpacked as illustrated below.

The individual elements of a list, tuple, or dictionary can be accessed as illustrated below::

    list_var = [1, 2, 3]
    list_var[0] # get the first element
    list_var[-1] # get the last element
    list_var[1:3] # get a subset of the list containing second and third elements

    tuple_var = (1, 2, 3)
    tuple_var[0] # get the first element
    tuple_var[-1] # get the last element
    tuple_var[1:3] # get a subset of the list containing second and third elements
    a, b, c = tuple_var # unpack the tuple into the values of a, b, and c

    dict_var = {'a': 1, 'b': 2}
    dict_var['a'] # get the value of the 'a' key


Variables
---------
The ``=`` operator can be used to create or set the value of a variable as illustrated below::

    my_var = [1, 2, 3]
    my_var = 'a' # reassign my_var to a string

Note, Python variables do not have to be declared and are not typed.


Boolean statements
------------------
As illustrated below, Boolean statements can be created using a variety of comparison operators (``==``, ``>=``, ``<=``, etc.) and binary operators (``and``, ``or``, ``not``)::

    x and y
    x or y
    x >= 1 and x <= 2
    x == 1.0


If statements
-------------
If/else statements can be implemented as illustrated below::

    if {statement}:
        ...
    else:
        ...

The ``elif`` directive can be used to achieve a similar behavior to the switch directives of other languages::

    if {statement_1}:
        ...
    elif {statement_2}:
        ...
    else:
        ...


Loops
-----
Python provides a for loop which can be used to iterate over ranges of values, lists, tuples, sets, dictionaries, and matrices as illustrated below. Note, the code that should be executed with the for loop must be nested underneath the loop definition and indented.::

    # iterate from 0 .. iter_max
    for iter in range(iter_max):
        ...

    # iterate over the values of a list, tuple, set, or matrix
    list_var = [...]
    for value in list_var:
        ...

    # iterate over the keys in a dictionary
    dict_var = {...}

    for key in dict_var:
        ...

    for key in dict_var.keys():
        ...

    # iterate over the values in a dictionary
    for value in dict_var.values():
        ...

    # use tuple unpacking to iterate over the keys and values in a dictionary
    for key, value in dict_var.items():
        ...

While loops can be implemented as illustrated below::

    while {statement}:
        ...

The ``continue`` directive can be used to advance to the next iteration of a loop and the ``break`` directive can be used to exit a loop.


Functions
---------
Python functions can be defined and evaluated as illustrated below::

    # define a function with one required and one optional argument
    def my_func(required_arg_1, optional_arg_2=default_value):
        ...
        return return_val # return the value return_val

    return_val_1 = my_func(value_1)
    return_val_2 = my_func(value_1, arg_2=value_2)

Inline `lambda` functions can also be defined as illustrated below::

    my_func = lambda required_arg_1: ...


Classes
-------
Python classes can be defined and objects can be instantiated as illustrated below. Note, ``self`` is the name typically used to refer to the class instance.::

    # create a class with one attribute
    class MyClass(object):

        # the method called when an instance of the class is constructed
        def __init__(self, required_arg_1, optional_arg_2=default_value):
            self.attribute_1 = ... # define the attributes of the class
            ...

        def my_method(self, required_arg_1, optional_arg_2=default_value):
            return self.attribute_1 # access the attribute of the class

    my_instance = MyClass(value_1) # create an instance of the class
    my_instance.attribute_1 # get the value of attribute_1
    my_instance.attribute_1 = value_2 # set the value of attribute_1
    value_4 = my_instance.my_method(value_3) # evaluate the method of the class

Note, all Python class attributes are public. The ``_`` prefix is often used to indicate attributes that should be treated as protected and the ``__`` prefix is often used to indicate attributes that should be treated as private.

Subclasses can be created as illustrated below::

    class MySecondClass(MyClass):

        def __init__(self, required_arg_1):
            super(MySecondClass, self).__init__(required_arg_1) # call the constructor for the parent class
            ...

Modules
-------
Python programs can be organized into multiple `modules` by splitting the code into multiple directories and/or files. In order for Python to recognize a directory as a module, the directory must contain a file with the name ``__init__.py``. This file can be blank. For example, the following file structure will create two modules, each with three sub-modules::

    /path/to/project/
        module_1/
            __init__.py
            sub_module_1a.py
            sub_module_1b.py
            sub_module_1c.py
        module_2/
            __init__.py
            sub_module_2a.py
            sub_module_2b.py
            sub_module_2c.py

The ``import`` directive can be used to access code from other modules. For example, the following code fragment could be used within ``sub_module_2a.py`` to access code from the other modules

    import module_1.sub_module_1a
    module_1.sub_module_1a.my_func(...)
    module_1.sub_module_1a.MyClass(...)

    from module_1 import sub_module_1b
    sub_module_1b.my_func(...)
    sub_module_1b.MyClass(...)

    from module_1 import sub_module_1b as s1c
    s1c.my_func(...)
    s1c.MyClass(...)

    from . import sub_module_2b
    sub_module_2b.my_func(...)
    sub_module_2b.MyClass(...)


String formatting
-----------------
Strings can be formatted using the ``str.format`` method as illustrated below. This method can be used to substitute variables into strings using the ``{}`` placeholder::

    '{} {} {}'.format('first value', 2, 3.0)


Printing to the command line
----------------------------
The ``print`` method can be used to write to standard output::

    print('Message')


Reading and writing to/from files with ``csv`` and ``pyexcel``
--------------------------------------------------------------
The follow example illustrates how to read and write text files::

    # write content to a file
    file_handle = open('filename.txt', 'w')
    file_handle.write(content)
    file_handle.close()

    # write content to a file using a context manager
    with open('filename.txt', 'w') as file_handle:
        file_handle.write(content)

    # read content from a file using a context manager
    with open('filename.txt', 'r') as file_handle:
        content = file_handle.read()

The follow example illustrates how to read and write csv files::

    import csv

    # write a list of lists to a csv file
    with open('eggs.csv', 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        for row in rows:
            csv_writer.writerow(row)

    # write a list of dictionaries to a csv file with row headings
    with open('eggs.csv', 'r') as csvfile:
        csv_writer = csv.DictReader(csvfile, fieldnames)
        for row in rows:
            csv_writer.writerow(row)

    # read a csv file into a list of lists
    with open('eggs.csv', 'r') as csvfile:
        rows = csv.reader(csvfile)

    # read a csv file with row headings into a list of dictionaries
    with open('eggs.csv', 'r') as csvfile:
        rows = csv.DictReader(csvfile)


The following example illustrates how to reading and write Excel files using the ``pxexcel`` package::

    import pxexcel

    book = pxexcel.get_book(file_name="example.xlsx")
    book.save_as("another_file.xlsx")


Warnings and exceptions
-----------------------
Warnings can be issued and suppressed as illustrated below::

    import warnings
    warnings.warn('Warning message')

    warnings.simplefilter("ignore", warnings.UserWarning) # ignore a class of warnings

Custom warning categories can be created and used as illustrated below::

    class MyWarning(warnings.UserWarning):
        ...
    warnings.warn('Message', MyWarning)

Exceptions can be issued as illustrated below::

    raise Exception('Message')

Exceptions can be handled as illustrated below::

    try:
        ... # code which raises an exception
    except:
        ... # code to execute if the try block raises an exception

    try:
        ... # code which raises an exception
    except Exception as exception:
        ... # code to execute if the try block raises an exception and the exception is an instance of Exception

Custom exception classes can be defined and raised as illustrated below::

    class MyException(Exception):
        ...

    raise MyException(...)


Other Python languages features
-------------------------------
Python provides a variety of additional powerful language features

* Context managers: context managers can be used to automatically run code at the beginning and end of a nested below
* Copying: the ``copy.copy`` and ``copy.deepcopy`` methods can be used to make copies of variables
* Customizable operators: the methods executed by operators such as ``==``, ``>=``, and ``<=`` can be customized by overriding the ``__eq__``, ``__geq__``, and ``__leq__`` methods
* Decorators: decorators can be used to wrap the execution of a method. Examples of decorators include ``@classmethod``
* Getters and setters: Getters and setters can be implemented by defining methods and decorating them with the ``@property`` and ``@property.setter`` decorators


Exercises
---------

* Write a function which computes the volume of a spherical cell
* Write a function which uses if statements to return the type of a codon (start, stop, other)
* Write a class which represents RNA, with an attribute that stores the sequence of each transcript and a method which uses a dictionary to compute the amino acid sequence of the protein coded by the transcript
* Import the ``csv`` package and use it to read a comma-separated file with a header row into a list of dictionaries
* Use the ``print`` and ``format`` methods to write `Hello {your name}!` to standard out

See `intro_to_wc_modeling/software_engineering/python_introduction.py <https://github.com/KarrLab/intro_to_wc_modeling/tree/master/intro_to_wc_modeling/software_engineering/python_introduction.py>`_ for solutions to these exercises.
