# -*- coding: utf8 -*-
import csv


def game_generator(file_handle):
    csv_reader = csv.DictReader(file_handle, fieldnames=['date', 'box', 'away', 'away_score', 'home', 'home_score'], restkey="extra")
    for row in csv_reader:
        yield row


def game_reader(generator, writer):
    """
    Takes in an object that generates game information in a map format
    """
    for game in generator:
        writer(game)
