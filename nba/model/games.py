from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, Column, Date, Integer, String, ForeignKey


Base = declarative_base()


class Team(Base):
    __tablename__ = 'team'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    abbr = Column(String)


class Game(Base):
    home = Column(ForeignKey('team.id'))
    away = Column(ForeignKey('team.id'))
    home_score = Column(Integer)
    away_score = Column(Integer)
    played = Boolean()
    date = Date()


def create_engine():
    pass


def create_session(engine=None):
    if engine is None:
        engine = create_engine()
    return sessionmaker(bind=engine)
