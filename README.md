Overview
========
This project is designed to provide a scaffolding for, and a solution to generating basketball gambling predictions. It includes tools to download source data for games (basketball-reference) and odds (oddshark), tools to parse that data and insert it into an SQLite database, and also some sample algorithms for processing that data.

Installation
============
Use pip!

How to Pull Data
================
Generally this is a few step process that breaks down as such:

1. Use the schedule files (pulled from nba.com) in the data folder. These have been santized a bit to make sure team names are consistent across years (looking at you Charlotte).
2. Use the create_urls script to pull odds and box score data and dump them to disk.
3. Use the create_records script to parse those and insert them into our DB.

How to Make Predictions
=======================
Again, this step breakd down into a few steps

1. Use the create_models script to create predictive models and write them to disk

