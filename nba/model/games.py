from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, Date, Float, Integer, String, ForeignKey


Base = declarative_base()


class Team(Base):
    __tablename__ = 'team'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    abbr = Column(String)


class Game(Base):
    id = Column(Integer, primary_key=True)
    home = Column(ForeignKey('team.id'))
    away = Column(ForeignKey('team.id'))
    played = Boolean()
    date = Date()


class GameFeature(Base):
    id = Column(Integer, primary_key=True)
    team = Column(ForeignKey('team.id'))
    game = Column(ForeignKey('game.id'))
    fg = Column(Integer)  # Field Goals made
    fga = Column(Integer)  # Field Goals attempted
    fgp = Column(Float)  # Field goal percentage
    3p = Column(Integer)  # 3 pointers made
    3pa = Column(Integer)  # 3 pointers attempted
    3pp = Column(Float)  # 3 pointers percentage
    ft = Column(Integer)  # Free Throws made
    fta = Column(Integer)  # Free Throws attempted
    ftp = Column(Float)  # Free throws %
    orb = Column(Integer)  # Offensive Rebounds
    drb = Column(Integer)  # Defensive Rebounds
    trb = Column(Integer)  # Total Rebounds
    ast = Column(Integer)  # Assists
    stl = Column(Integer)  # Steals
    blk = Column(Integer)  # Blocks
    tov = Column(Integer)  # Turnovers
    pf = Column(Integer)  # Personal Fouls
    tsp = Column(Float)  # True Shooting Percentage
    efgp = Column(Float)  # Effective Field Goal Percentage
    3par = Column(Float)  # 3 Point attempt rate
    ftr = Column(Float)  # FT attempt rate
    orbp = Column(Float)  # Offensive Rebound Percentage
    drbp = Column(Float)  # Defensive Rebound Percentage
    trpb = Column(Float)  # Total Rebound Percentage
    astp = Column(Float)  # Assist rate percentage
    stlp = Column(Float)  # Steal rate percentage
    blkp = Column(Float)  # Block rate percentage
    tovp = Column(Float)  # Turn over rate percentage
    ortg = Column(Float)  # Offensive Rating
    drtg = Column(Float)  # Defensive Rating
    ftfga = Column(Float)  # Ft/FGA Rating
    pace = Column(Float)  # PACE
