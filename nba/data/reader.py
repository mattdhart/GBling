# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
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
