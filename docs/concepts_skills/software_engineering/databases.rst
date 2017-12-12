Using databases with SQLAlchemy and SQLite
-----------------------------------------------
Databases are useful tools for organizing and quickly searching large datasets. Relational databases are the most common type of databases. Relational databases are based around schemas or structured definitions of the types of your data and the relationships among your data. These structured definitions facilitate fast searching of large datasets. However, these schemas can also make it cumbersome to represent multiple types of data with different structures. To overcome this limitation, several Python package provide support for editing or migrating schemas. Recently, there has been significant progress in the development of No-SQL databases which do not have fixed schemas.

Database engines are the software programs which implement SQL and No-SQL databases. Several popular SQL database engines include MySQL, Oracle, and SQLite. Several popular No-SQL database engines include CouchBase, CouchDB, and MongoDB.

SQL (Structured Query Language) is the language used to describe relational database schemas and how to insert and retrieve data to/from them. Each relational database engine uses it own variant of SQL, but the SQL languages used by MySQL, Oracle, SQLite and most other popular relational database engines are very similar.

Most of the popular database engines have their own Python interfaces. In addition, there are several Python packages such as SQLAlchemy which abstract away many of the details the individual database engines and enable Python developers to use database with little direct interaction with SQL. These packages make it easy to map between Python objects and rows in relational database tables and between attributes of those objects and columns of those tables. Thus, the packages often referred to as object-relational mappers.

This tutorial will teach you how to use SQLAlchemy to build a SQLite database to represent of single-cell organisms and their components (compartments, species, and reactions). First, we will build a `schema` that can describe cells. Second, we will build the database. Third, we will populate the database with data. Finally, we will query the database.


Define the Python object model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In order to represent organisms, compartments, species, and reactions, we must create four Python classes. These classes should inherit from ``sqlalchemy.ext.declarative.declarative_base()`` so that SQLAlchemy can map them onto SQLite tables and each class should define a ``__tablename__`` class attribute to tell SQLAchemy which table each class should be mapped onto. First, these classes should define their instance attributes and how each instance attribute should be mapped onto a column in the relational database (i.e. their type in the database). In the example below, we have created ``name`` and ``ncbi_id`` instance attributes. Furthermore, to ensure we only create once Organism instance per organism, we have declared that the ncbi_id attributes must be unique (i.e. no two objects can have the same ncbi_id).::

    import sqlalchemy
    import sqlalchemy.ext.declarative
    import sqlalchemy.orm

    Base = sqlalchemy.ext.declarative.declarative_base()
    # :obj:`Base`: base model for local sqlite database

    class Organism(Base):
        __tablename__ = 'organism'

        ncbi_id = sqlalchemy.Column(sqlalchemy.Integer(), unique=True)
        name = sqlalchemy.Column(sqlalchemy.String(), unique=True)


    class Compartment(Base):
        __tablename__ = 'compartment'

        name = sqlalchemy.Column(sqlalchemy.String())


    class Specie(Base):
        __tablename__ = 'specie'

        name = sqlalchemy.Column(sqlalchemy.String())


    class Reaction(Base):
        __tablename__ = 'reaction'

        name = sqlalchemy.Column(sqlalchemy.String())


Define the relationships between the classes
""""""""""""""""""""""""""""""""""""""""""""
Once we have defined all of the classes that we need to represent organisms, compartments, species, and reactions, we can define how these classes are related to each other by defining relationship attributes and foreign keys. Foreign keys are columns that represent pointers to rows in other tables. Relationship attributes tell SQLAchemy how to map foreign keys between rows in tables onto references between Python objects. In order to define foreign keys, we must also define primary keys that for each table that the foreign keys can be related to. This can be done by adding ``_id`` attributes to each Python class.

There are four possible types of relationships between Python objects/relational table rows

* One-to-one relationships
* One-to-many relationships
* Many-to-one relationships
* Many-to-many relationships

The first three types of relationships can be defined by adding additional foreign key columns to tables. To define a many-to-many relationship, we must create an additional association table which contains foreign keys to both tables that we would like to relate.

The ``cascade`` argument to ``sqlalchemy.orm.relationship`` tells SQLAlchemy whether or not related objects should be deleted when their parents are deleted.::

    specie_reaction = sqlalchemy.Table(
        'specie_reaction', Base.metadata,
        sqlalchemy.Column('specie__id', sqlalchemy.Integer, sqlalchemy.ForeignKey('specie._id')),
        sqlalchemy.Column('reaction__id', sqlalchemy.Integer, sqlalchemy.ForeignKey('reaction._id')),
    )
    # :obj:`sqlalchemy.Table`: Specie:Reaction \many-to-many association table


    class Organism(Base):
        __tablename__ = 'organism'

        _id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
        ncbi_id = sqlalchemy.Column(sqlalchemy.Integer(), unique=True)
        name = sqlalchemy.Column(sqlalchemy.String(), unique=True)


    class Compartment(Base):
        __tablename__ = 'compartment'

        _id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
        name = sqlalchemy.Column(sqlalchemy.String())
        organism_id = sqlalchemy.Column(sqlalchemy.Integer(), sqlalchemy.ForeignKey('organism._id'))
        organism = sqlalchemy.orm.relationship('Organism',
                                               foreign_keys=[organism_id],
                                               backref=sqlalchemy.orm.backref('compartments', cascade="all, delete-orphan"))


    class Specie(Base):
        __tablename__ = 'specie'

        _id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
        name = sqlalchemy.Column(sqlalchemy.String())
        compartment_id = sqlalchemy.Column(sqlalchemy.Integer(), sqlalchemy.ForeignKey('compartment._id'))
        compartment = sqlalchemy.orm.relationship('Compartment',
                                                  foreign_keys=[compartment_id],
                                                  backref=sqlalchemy.orm.backref('species', cascade="all, delete-orphan"))


    class Reaction(Base):
        __tablename__ = 'reaction'

        _id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
        name = sqlalchemy.Column(sqlalchemy.String())
        species = sqlalchemy.orm.relationship('Specie',
                                              secondary=specie_reaction,
                                              backref=sqlalchemy.orm.backref('reactions', cascade="all, delete-orphan", single_parent=True))


Optimizing the schema
^^^^^^^^^^^^^^^^^^^^^
To speed up the querying of the database, we can instruct SQLlite to build index tables, or pre-sorted copies of the primary tables that can be used to quickly find rows using a binary search rather than having to iterate over every row in a table. This can be done by setting the ``index`` argument to each column constructor to ``True``::

    specie_reaction = sqlalchemy.Table(
        'specie_reaction', Base.metadata,
        sqlalchemy.Column('specie__id', sqlalchemy.Integer, sqlalchemy.ForeignKey('specie._id'), index=True),
        sqlalchemy.Column('reaction__id', sqlalchemy.Integer, sqlalchemy.ForeignKey('reaction._id'), index=True),
    )
    # :obj:`sqlalchemy.Table`: Specie:Reaction \many-to-many association table


    class Organism(Base):
        __tablename__ = 'organism'

        _id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
        ncbi_id = sqlalchemy.Column(sqlalchemy.Integer(), index=True, unique=True)
        name = sqlalchemy.Column(sqlalchemy.String(), unique=True)


    class Compartment(Base):
        __tablename__ = 'compartment'

        _id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
        name = sqlalchemy.Column(sqlalchemy.String())
        organism_id = sqlalchemy.Column(sqlalchemy.Integer(), sqlalchemy.ForeignKey('organism._id'), index=True)
        organism = sqlalchemy.orm.relationship('Organism',
                                               foreign_keys=[organism_id],
                                               backref=sqlalchemy.orm.backref('compartments', cascade="all, delete-orphan"))


    class Specie(Base):
        __tablename__ = 'specie'

        _id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
        name = sqlalchemy.Column(sqlalchemy.String())
        compartment_id = sqlalchemy.Column(sqlalchemy.Integer(), sqlalchemy.ForeignKey('compartment._id'), index=True)
        compartment = sqlalchemy.orm.relationship('Compartment',
                                                  foreign_keys=[compartment_id],
                                                  backref=sqlalchemy.orm.backref('species', cascade="all, delete-orphan"))


    class Reaction(Base):
        __tablename__ = 'reaction'

        _id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
        name = sqlalchemy.Column(sqlalchemy.String())
        species = sqlalchemy.orm.relationship('Specie',
                                              secondary=specie_reaction,
                                              backref=sqlalchemy.orm.backref('reactions', cascade="all, delete-orphan", single_parent=True))


Create the database
^^^^^^^^^^^^^^^^^^^
Once we have defined the Python data model, we can use SQLAlchemy to generate the database::

    DATABASE_FILENAME = 'test.sqlite'
    # :obj:`str`: path to store the database

    engine = sqlalchemy.create_engine('sqlite:///' + DATABASE_FILENAME)
    # :obj:`sqlalchemy.engine.Engine`: database engine

    # create the database
    Base.metadata.create_all(engine)

We can use the sqlite3 lite command lite utility to inspect the schema of the database that SQLAchemy generated.::

    sqlite3 test.sqlite .schema


Insert records into the database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
We can insert records into the database by (1) creating a "session" on the database, (2) instantiating instances of the Organism, Compartment, Specie, and Reaction classes, (3) adding those instances to the session, and (4) "committing" the session. A session is an in-memory copy of the database which can be used to query and make changes to the database. However, the changes are not saved to the database (and therefore not accessible to other sessions) until they are committed.

Note, SQLAlchemy automatically creates constructors for each class which have keyword arguments for each instance attribute.

Note, SQLAlchemy automatically adds add objects to sessions that are linked to other objects that have been explicitly added to the session.::

    session = sqlalchemy.orm.sessionmaker(bind=engine)()
    # :obj:`sqlalchemy.orm.session.Session`: sqlalchemy session

    # create homo sapiens organism with one reaction
    organism = Organism(ncbi_id=9606, name='Homo sapiens')
    session.add(organism)

    compartment = Compartment(name='cytosol')
    organism.compartments.append(compartment)

    atp = Specie(name='atp')
    compartment.species.append(atp)

    adp = Specie(name='adp')
    compartment.species.append(adp)

    pi = Specie(name='pi')
    compartment.species.append(pi)

    h2o = Specie(name='h2o')
    compartment.species.append(h2o)

    h = Specie(name='h')
    compartment.species.append(h)

    reaction = Reaction(name='atp_hydrolysis')
    reaction.species = [atp, adp, pi, h2o, h]


    # create E. colii organism with one reaction
    organism = Organism(ncbi_id=562, name='Escherichia coli')
    session.add(organism)

    compartment = Compartment(name='cytosol')
    organism.compartments.append(compartment)

    gtp = Specie(name='gtp')
    compartment.species.append(gtp)

    gdp = Specie(name='gdp')
    compartment.species.append(gdp)

    pi = Specie(name='pi')
    compartment.species.append(pi)

    h2o = Specie(name='h2o')
    compartment.species.append(h2o)

    h = Specie(name='h')
    compartment.species.append(h)

    reaction = Reaction(name='gtp_hydrolysis')
    reaction.species = [gtp, gdp, pi, h2o, h]


    # save the new objects to the database
    session.commit()


Querying the database
^^^^^^^^^^^^^^^^^^^^^
The following examples illustrate how to query the database::

    # get the number organisms
    organisms = session.query(Organism) \
        .count()

    # select all of the organisms
    organisms = session.query(Organism) \
        .all()

    # order the organisms by their names
    organisms = session.query(Organism) \
        .order_by(Organism.name) \
        .all()

    # order the organisms by their names in descending order
    organisms = session.query(Organism) \
        .order_by(Organism.name.desc()) \
        .all()

    # select only organism names
    organisms = session.query(Organism.name) \
        .all()

    # select a subset of the database
    homo_sapiens = session.query(Organism) \
        .filter(Organism.ncbi_id=9606) \
        .first()

    # using joining to select a subset based on reaction names
    homo_sapiens = session.query(Organism) \
        .join(Compartment, Organism.compartments) \
        .join(Specie, Compartment.species) \
        .join(Reaction, Specie.reactions) \
        .filter(Reaction.name='atp_hydrolysis') \
        .first()

    # get the number of species per organism
    homo_sapiens = session.query(Organism, sqlalchemy.func.count(Organism._id)) \
        .join(Compartment, Organism.compartments) \
        .join(Specie, Compartment.species) \
        .group_by(Organism._id) \
        .all()


Editing and removing records
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The following examples illustrate how to edit and remove records::

    # edit the name of Homo sapiens to "H. sapiens"
    homo_sapiens = session.query(Organism) \
        .filter(Organism.ncbi_id=9606) \
        .first()
    homo_sapiens.name = 'H. sapiens'
    session.commit()

    # delete H. sapiens
    session.query(Organism) \
        .filter(Organism.ncbi_id=9606) \
        .delete()
    session.commit()

    # delete E. coli
    e_coli = session.query(Organism) \
        .filter(Organism.ncbi_id=562) \
        .first()
    session.delete(e_coli)
    session.commit()

SQLAlchemy documentation
^^^^^^^^^^^^^^^^^^^^^^^^
See the `SQLAlchemy documentation <http://docs.sqlalchemy.org>`_ for additional information about building and querying databases with SQLAlchemy.

Additional tutorials
^^^^^^^^^^^^^^^^^^^^
There are several good tutorial on how to use SQLAlchemy and SQLite

* `Introductory Tutorial of Python's SQLAlchemy <http://pythoncentral.io/introductory-tutorial-python-sqlalchemy/>`_
* `SQLAlchemy ORM for Beginners <https://www.youtube.com/watch?v=51RpDZKShiw>`_
* `SQLAlchemy Object Relational Tutorial <http://docs.sqlalchemy.org/en/latest/orm/tutorial.html>`_

Advanced concepts
^^^^^^^^^^^^^^^^^

* Migrations
