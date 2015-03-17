# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
from dateutil.parser import parse
from nba.model.utils import abbr_team_lookup
import csv
import re
import requests
import time


CHUNK_SIZE = 1024
SLEEP_TIME = .5


def save_urls_to_file(urls, outputs):
    """
    Saves a list of urls to a list of output files, waiting in between each request
    """
    if len(urls) != len(outputs):
        raise Exception("Urls and output files must be same size")
    for url, output in zip(urls, outputs):
        save_url_to_file(url, output)
        time.sleep(SLEEP_TIME)


def save_url_to_file(url, output):
    """
    Saves a given url to a file as raw data
    """
    r = requests.get(url, stream=True)
    if not r.status_code == 200:
        raise Exception("Request returned status code: {0}".format(r.status_code))
    with open(output, 'wb') as fd:
        for chunk in r.iter_content(CHUNK_SIZE):
            fd.write(chunk)


def game_generator(file_handle):
    csv_reader = csv.DictReader(file_handle, fieldnames=['date', 'box', 'away', 'away_score', 'home', 'home_score'], restkey="extra")
    for row in csv_reader:
        yield row


def pipeline(generator, handler):
    """
    Calls function for each element in generator
    """
    map(handler, generator)


def get_teamname_from_odds_filename(filename):
    odds, team, dateext = re.split('_', filename)
    return abbr_team_lookup[team]


def parse_file_for_odds(fl):
    team = get_teamname_from_odds_filename(fl)
    headers = ['date', 'opponent', 'game', 'result', 'score', 'ats', 'spread', 'ou', 'outotal']
    contents = open(fl, 'r').read()
    soup = BeautifulSoup(contents)
    odds_rows = soup.find_all('tr', class_='sport_data')
    for odds_row in odds_rows:
        row_vals = [re.sub(r"\s+", " ", inner.get_text().strip()) for inner in odds_row.find_all('td')]
        row_dict = dict(zip(headers, row_vals))
        if len(row_dict['result']) == 0 or row_dict['game'] != 'REG':
            continue
        row_dict['team'] = team
        yield row_dict


def get_team_from_box_filename(filename):
    br, team, dateext = re.split('_', filename)
    date, ext = re.split(r'\.', dateext)
    team_name = abbr_team_lookup[team]
    date_val = parse(date).date()
    return team_name, team, date_val


def get_nth_value_from_table(table, n):
    return table.select('tfoot > tr > td:nth-of-type({0})'.format(n))[0].get_text()


def extract_basic(table, prefix=''):
    return {
        prefix + 'fg': get_nth_value_from_table(table, 3),
        prefix + 'fga': get_nth_value_from_table(table, 4),
        prefix + 'fgp': get_nth_value_from_table(table, 5),
        prefix + 'threep': get_nth_value_from_table(table, 6),
        prefix + 'threepa': get_nth_value_from_table(table, 7),
        prefix + 'threepp': get_nth_value_from_table(table, 8),
        prefix + 'ft': get_nth_value_from_table(table, 9),
        prefix + 'fta': get_nth_value_from_table(table, 10),
        prefix + 'ftp': get_nth_value_from_table(table, 11),
        prefix + 'orb': get_nth_value_from_table(table, 12),
        prefix + 'drb': get_nth_value_from_table(table, 13),
        prefix + 'trb': get_nth_value_from_table(table, 14),
        prefix + 'ast': get_nth_value_from_table(table, 15),
        prefix + 'stl': get_nth_value_from_table(table, 16),
        prefix + 'blk': get_nth_value_from_table(table, 17),
        prefix + 'tov': get_nth_value_from_table(table, 18),
        prefix + 'pf': get_nth_value_from_table(table, 19),
    }


def extract_advanced(table, prefix=''):
    return {
        prefix + 'tsp': get_nth_value_from_table(table, 3),
        prefix + 'efgp': get_nth_value_from_table(table, 4),
        prefix + 'threepar': get_nth_value_from_table(table, 5),
        prefix + 'ftr': get_nth_value_from_table(table, 6),
        prefix + 'orbp': get_nth_value_from_table(table, 7),
        prefix + 'drbp': get_nth_value_from_table(table, 8),
        prefix + 'trpb': get_nth_value_from_table(table, 9),
        prefix + 'astp': get_nth_value_from_table(table, 10),
        prefix + 'stlp': get_nth_value_from_table(table, 11),
        prefix + 'blkp': get_nth_value_from_table(table, 12),
        prefix + 'tovp': get_nth_value_from_table(table, 13),
        prefix + 'ortg': get_nth_value_from_table(table, 14),
        prefix + 'drtg': get_nth_value_from_table(table, 15),
    }


def extract_four_factors(table):
    return {
        'away_ftfga': table.select('tbody > tr:nth-of-type(1) > td:nth-of-type(6)')[0].get_text(),
        'away_pace': table.select('tbody > tr:nth-of-type(1) > td:nth-of-type(2)')[0].get_text(),
        'home_ftfga': table.select('tbody > tr:nth-of-type(2) > td:nth-of-type(6)')[0].get_text(),
        'home_pace': table.select('tbody > tr:nth-of-type(2) > td:nth-of-type(2)')[0].get_text(),
    }


def get_features(contents):
    # First find teh scores
    soup = BeautifulSoup(contents)
    away_score_string = soup.body.select('div#page_content > table > tr > td > div:nth-of-type(1) > div:nth-of-type(1) > table:nth-of-type(2) > tr > td > table > tr:nth-of-type(1) > td:nth-of-type(1) > span:nth-of-type(1)')[0].get_text()
    away_score = re.search(r"[ A-Za-z](\d+)", away_score_string).group(1)
    home_score_string = soup.body.select('div#page_content > table > tr > td > div:nth-of-type(1) > div:nth-of-type(1) > table:nth-of-type(2) > tr > td > table > tr:nth-of-type(1) > td:nth-of-type(2) > span:nth-of-type(1)')[0].get_text()
    home_score = re.search(r"[ A-Za-z](\d+)", home_score_string).group(1)

    # Find all of the tables we need to extract data from separately
    x, y, four_factors, away_basic, away_advanced, home_basic, home_advanced = soup.body.select('table.stats_table')
    home_basic = extract_basic(home_basic, 'home_')
    home_advanced = extract_advanced(home_advanced, 'home_')
    away_basic = extract_basic(away_basic, 'away_')
    away_advanced = extract_advanced(away_advanced, 'away_')
    four_factors = extract_four_factors(four_factors)

    # Add scores
    scores = {
        'away_score': away_score,
        'home_score': home_score,
    }
    return dict(scores.items() + home_basic.items() + home_advanced.items() + away_basic.items() + away_advanced.items() + four_factors.items())


def parse_file_for_box(fl):
    team, x, date = get_team_from_box_filename(fl)
    contents = open(fl, 'r').read()
    try:
        return {
            'home_team': team,
            'date': date,
            'features': get_features(contents)
        }
    except Exception, e:
        print "Problem reading {0}".format(fl)
        raise e
