from dateutil.parser import parse
from nba.model import get_or_create
from nba.model.games import Game, Team
from nba.model.utils import team_abbr_lookup


def get_city_from_teamname(teamname):
    return teamname[:teamname.rfind(' ')]


def team_writer(team_name, session):
    team = get_or_create(session, Team, name=team_name)
    team.abbr = team_abbr_lookup.get(team_name) 
    team.city = get_city_from_teamname(team_name)
    session.add(team)
    return team


def game_writer(game, session):
    if not all (k in game for k in ('date', 'home', 'away')):
        return
    try:
        home_team_str = game['home']
        away_team_str = game['away']
        game_date = parse(game['date'])
        
        home_team = team_writer(home_team_str, session)
        away_team = team_writer(away_team_str, session)

        saved_game = Game(home=home_team.id, away=away_team.id, date=game_date)
        session.add(saved_game)
    except ValueError, e:
        print "Exception: ", e
        return
    
