from nba import config
from nba.model.games import Base
from sqlalchemy import create_engine as ce
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import ClauseElement


def create_engine(location=None):
    if location is None:
        location = "sqlite:///{0}".format(config.DATABASE_LOCATION)
    return ce(location)


def create_session(engine=None):
    if engine is None:
        engine = create_engine()
    return sessionmaker(bind=engine)()


def create_all(engine=None):
    if engine is None:
        engine = create_engine()
    Base.metadata.create_all(engine) 


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        params = dict((k, v) for k,v in kwargs.iteritems() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance
