# -*- coding: utf8 -*-
import csv
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
