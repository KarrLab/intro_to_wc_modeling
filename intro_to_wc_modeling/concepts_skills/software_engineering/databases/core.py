""" Relational database tutorial

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-06-08
:Copyright: 2017, Karr Lab
:License: MIT
"""

import os
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm


####################################
# Define the schema for the database
####################################

Base = sqlalchemy.ext.declarative.declarative_base()
# :obj:`Base`: base model for local sqlite database

specie_reaction = sqlalchemy.Table(
    'specie_reaction', Base.metadata,
    sqlalchemy.Column('specie__id', sqlalchemy.Integer, sqlalchemy.ForeignKey('specie._id'), index=True),
    sqlalchemy.Column('reaction__id', sqlalchemy.Integer, sqlalchemy.ForeignKey('reaction._id'), index=True),
)
# :obj:`sqlalchemy.Table`: Specie:Reaction \many-to-many association table


class Organism(Base):
    """ Represents an organism

    Attributes:
        ncbi_id (:obj:`int`): NCBI id
        name (:obj:`str`): name
    """
    __tablename__ = 'organism'

    _id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
    ncbi_id = sqlalchemy.Column(sqlalchemy.Integer(), index=True, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String(), unique=True)


class Compartment(Base):
    """ Represents an compartment

    Attributes:
        name (:obj:`str`): name
    """

    __tablename__ = 'compartment'

    _id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String())
    organism_id = sqlalchemy.Column(sqlalchemy.Integer(), sqlalchemy.ForeignKey('organism._id'), index=True)
    organism = sqlalchemy.orm.relationship('Organism',
                                           foreign_keys=[organism_id],
                                           backref=sqlalchemy.orm.backref('compartments', cascade="all, delete-orphan"))


class Specie(Base):
    """ Represents a species

    Attributes:
        name (:obj:`str`): name
    """
    __tablename__ = 'specie'

    _id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String())
    compartment_id = sqlalchemy.Column(sqlalchemy.Integer(), sqlalchemy.ForeignKey('compartment._id'), index=True)
    compartment = sqlalchemy.orm.relationship('Compartment',
                                              foreign_keys=[compartment_id],
                                              backref=sqlalchemy.orm.backref('species', cascade="all, delete-orphan"))


class Reaction(Base):
    """ Represents a reaction

    Attributes:
        name (:obj:`str`): name
    """
    __tablename__ = 'reaction'

    _id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String())
    species = sqlalchemy.orm.relationship('Specie',
                                          secondary=specie_reaction,
                                          backref=sqlalchemy.orm.backref('reactions', cascade="all, delete-orphan", single_parent=True))


def create_database():
    DATABASE_FILENAME = os.path.join(os.path.dirname(__file__), 'core.sqlite')
    # :obj:`str`: path to store database

    engine = sqlalchemy.create_engine('sqlite:///' + DATABASE_FILENAME)
    # :obj:`sqlalchemy.engine.Engine`: database engine

    # create the database
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    return engine


def create_session(engine):
    session = sqlalchemy.orm.sessionmaker(bind=engine)()
    # :obj:`sqlalchemy.orm.session.Session`: sqlalchemy session

    return session


def insert_records(session):
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


def query_database(session):
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
        .filter(Organism.ncbi_id == 9606) \
        .first()

    # using joining to select a subset based on reaction names
    homo_sapiens = session.query(Organism) \
        .join(Compartment, Organism.compartments) \
        .join(Specie, Compartment.species) \
        .join(Reaction, Specie.reactions) \
        .filter(Reaction.name == 'atp_hydrolysis') \
        .first()

    # get the number of species per organism
    homo_sapiens = session.query(Organism, sqlalchemy.func.count(Organism._id)) \
        .join(Compartment, Organism.compartments) \
        .join(Specie, Compartment.species) \
        .group_by(Organism._id) \
        .all()


def edit_database(session):
    # edit the name of Homo sapiens to "H. sapiens"
    homo_sapiens = session.query(Organism) \
        .filter(Organism.ncbi_id == 9606) \
        .first()
    homo_sapiens.name = 'H. sapiens'
    session.commit()

    # delete H. sapiens
    session.query(Organism) \
        .filter(Organism.ncbi_id == 9606) \
        .delete()
    session.commit()

    # delete E. coli
    e_coli = session.query(Organism) \
        .filter(Organism.ncbi_id == 562) \
        .first()
    session.delete(e_coli)
    session.commit()


def main():
    engine = create_database()
    session = create_session(engine)
    insert_records(session)
    query_database(session)
    edit_database(session)
