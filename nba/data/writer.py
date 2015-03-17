from dateutil.parser import parse
from nba.model import get_or_create
from nba.model.games import Game, GameFeature, Odds, Team
from nba.model.utils import oddsshark_city_lookup, team_abbr_lookup


def get_city_from_teamname(teamname):
    return teamname[:teamname.rfind(' ')]


def team_writer(team_name, session):
    team = get_or_create(session, Team, name=team_name)
    team.abbr = team_abbr_lookup.get(team_name)
    team.city = get_city_from_teamname(team_name)
    session.add(team)
    return team


def game_writer(game, session):
    if not all(k in game for k in ('date', 'home', 'away')):
        print "Not all keys present"
        return
    try:
        home_team_str = game['home']
        away_team_str = game['away']
        game_date = parse(game['date']).date()

        home_team = team_writer(home_team_str, session)
        away_team = team_writer(away_team_str, session)

        saved_game = get_or_create(
            session,
            Game,
            home=home_team,
            away=away_team,
            date=game_date)
        session.add(saved_game)
    except ValueError:
        print "ValueError on insert, may be ok (header row)"
        return


def odds_writer(odds, session):
    """
    Writes the odds as produced by nba.data.reader.parse_file_for_odds
    """
    game_date = parse(odds['date']).date()
    if odds['spread'] == 'Ev':
        spread = 0
    else:
        spread = float(odds['spread'])
    outotal = float(odds['outotal'])

    if odds['opponent'].startswith('@'):
        home = oddsshark_city_lookup[odds['opponent'][2:]]
        visitor = odds['team']
        home_game = True
    else:
        visitor = oddsshark_city_lookup[odds['opponent'][3:]]
        home = odds['team']
        home_game = False
    # Always put the spread in terms of the home team
    if home_game:
        spread *= -1.0

    home_team = session.query(Team).filter_by(name=home).first()
    away_team = session.query(Team).filter_by(name=visitor).first()

    if home_team is None or away_team is None:
        raise ValueError("Team is null")

    game = session.query(Game).filter_by(
        home=home_team,
        away=away_team,
        date=game_date).first()
    if game is None:
        raise ValueError(
            "Unknown game. {0} vs {1} on {2}".format(
                home_team.name,
                away_team.name,
                game_date))
    odds = get_or_create(session, Odds, spread=spread, overunder=outotal)
    session.add(odds)
    game.odds = odds


def box_score_writer(box, session):
    game, team = session.query(Game, Team).\
        filter(Game.home_id == Team.id).\
        filter(Team.name == box['home_team']).\
        filter(Game.date == box['date']).\
        first()
    if game is None:
        raise Exception("Could not find game for team: {0} and date: {1}".format(box['home_team'], box['date']))

    if game.home_features is None:
        home_dict = {key[5:]: val for key, val in box['features'].iteritems() if key.startswith('home')}
        home_features = GameFeature(**home_dict)
        session.add(home_features)
        game.home_features = home_features

    if game.away_features is None:
        away_dict = {key[5:]: val for key, val in box['features'].iteritems() if key.startswith('away')}
        away_features = GameFeature(**away_dict)
        session.add(away_features)
        game.away_features = away_features
