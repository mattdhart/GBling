# -*- coding: utf8 -*-
from datetime import date
from nba.model.utils import oddsshark_team_id_lookup
from sqlalchemy import Boolean, Column, Date, Float, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


NOP_TO_NOH_DATE = date(2013, 10, 29)


Base = declarative_base()


class Team(Base):

    """
    Represents an NBA team
    """
    __tablename__ = 'team'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    abbr = Column(String)
    city = Column(String)

    def get_odds_url(self, year):
        return "http://www.oddsshark.com/stats/gamelog/basketball/nba/{0}/{1}".format(oddsshark_team_id_lookup.get(self.name), year)


class GameFeature(Base):

    """
    Represents the statistics associated with a game or range of games.
    """
    __tablename__ = 'game_feature'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    score = Column(Integer)  # Final score of team
    fg = Column(Integer)  # Field Goals made
    fga = Column(Integer)  # Field Goals attempted
    fgp = Column(Float)  # Field goal percentage
    threep = Column(Integer)  # three pointers made
    threepa = Column(Integer)  # three pointers attempted
    threepp = Column(Float)  # three pointers percentage
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
    threepar = Column(Float)  # three Point attempt rate
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
    b2b = Column(Boolean)  # Was it a back to back?


class Odds(Base):
    __tablename__ = 'odds'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    spread = Column(Float)
    overunder = Column(Float)


class Game(Base):

    """
    Represents a game with keys to the teams and features
    """
    __tablename__ = 'game'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    home_id = Column(ForeignKey('team.id'))
    home = relationship("Team", backref=backref("game_home", order_by=id), foreign_keys=[home_id])
    home_features_id = Column(ForeignKey('game_feature.id'))
    home_features = relationship("GameFeature", backref=backref("game_home_features", order_by=id), foreign_keys=[home_features_id])
    away_id = Column(ForeignKey('team.id'))
    away = relationship("Team", backref=backref("game_away", order_by=id), foreign_keys=[away_id])
    away_features_id = Column(ForeignKey('game_feature.id'))
    away_features = relationship("GameFeature", backref=backref("game_away_features", order_by=id), foreign_keys=[away_features_id])
    date = Column(Date)
    odds_id = Column(ForeignKey('odds.id'))
    odds = relationship("Odds", backref=backref("game", order_by=id))

    def get_br_url(self):
        """Returns the URL for the basketball-reference.com box scores"""
        if self.home.abbr == 'NOP' and self.date < NOP_TO_NOH_DATE:
            abbr = 'NOH'
        else:
            abbr = self.home.abbr
        return "http://www.basketball-reference.com/boxscores/{0}{1}{2}0{3}.html".format(self.date.year, str(self.date.month).zfill(2), str(self.date.day).zfill(2), abbr)


class Rollup(Base):

    """
    Contains rollup data for a set of features betweeen an inclusive
    range of games.
    """
    __tablename__ = "game_rollup"
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    team_id = Column(ForeignKey('team.id'))
    team = relationship("Team", backref=backref("game_rollup", order_by=id))
    start_id = Column(ForeignKey('game.id'))
    start = relationship("Game", backref=backref("game_rollup_start", order_by=id), foreign_keys=[start_id])
    end_id = Column(ForeignKey('game.id'))
    end = relationship("Game", backref=backref("game_rollup_end", order_by=id), foreign_keys=[end_id])
    features_id = Column(ForeignKey('game_feature.id'))
    features = relationship("GameFeature", backref=backref("game_rollup", order_by=id))
