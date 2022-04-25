#!/usr/bin/env python3

def give_suggestions():
    update_status = dataloader.check_date(date,season=season) # return 1 if update needed

    update_dir = 'csv_files/' + season
    update_file = update_dir + '/update_data.csv'
    update_data = next(csv.DictReader(open(update_file)))

"""
 * Name: Joshua Bih, Marco Tan, Tram Trinh, Chris Capone
 * Email: jbih2@nd.edu, mtan3@nd.edu, htrinh@nd.edu, ccapone@nd.edu
 * File Name: main.py
 * Date Created: 4/7/2022
 * File Contents: This file contains the main code for the final project
"""

""" For help in understanding the nba_api, here are some links:
https://github.com/swar/nba_api
https://github.com/swar/nba_api/blob/master/docs/table_of_contents.md
https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/examples.md
https://github.com/swar/nba_api/blob/master/docs/examples/Basics.ipynb
https://github.com/swar/nba_api/blob/master/docs/examples/Finding%20Games.ipynb
https://github.com/swar/nba_api/blob/master/docs/examples/LiveData.ipynb
https://github.com/swar/nba_api/blob/master/docs/examples/PlayByPlay.ipynb
https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/static/players.md
https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/static/teams.md
"""
# imports
import os
import sys
import pprint
import pandas as pd
import csv
import tkinter

from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import leaguegamefinder, playercareerstats
from nba_api.live.nba.endpoints import scoreboard

from datetime import datetime, timezone
from dateutil import parser

# classes
sys.path.insert(0, 'class/')
from Player import Player
from League import League
from Team import Team

# functions
sys.path.insert(0, 'functions/')
import dataloader

if __name__ == "__main__":
    season = '2021'
    # check if year matches
    dataloader.nba_schedule(season=season)  # will do nothing if schedule has been loaded



    date = '2022-03-20'
    update_status = dataloader.check_date(date,season=season) # return 1 if update needed
    

    update_dir = 'csv_files/' + season
    update_file = update_dir + '/update_data.csv'
    update_data = next(csv.DictReader(open(update_file)))

    thirty = dataloader.n_days(date,-30)

    if update_status:
        #date = dataloader.earlier_date(update_data['end'],update_data['update'])
        #thirty = dataloader.n_days(date,-30)

        dataloader.get_nba_raw_data(thirty,date,season=season)
    
    # load players and game schedules
    game_index = dataloader.get_games_for_week(date)
    players = dataloader.load_players()

    my_league = League(date,game_index,players=players,capacity=5)
    teams = ["fudruckers","destroyers", "jolly rogers", "trees"] 

    for team in teams:
        my_league.add_team(team)

    # team rosters
    fud = ["Nikola Jokic", "DeMar DeRozan", "Domantas Sabonis", "Donovan Mitchell", "Terry Rozier"]
    des = ["Kevin Durant", "Joel Embiid", "Rudy Gobert", "Jayson Tatum", "Bam Adebayo"]
    jol = ["Luka Doncic","Kyrie Irving", "Trae Young", "Devin Booker", "Pascal Siakam"]
    tre = ["Jrue Holiday", "James Harden", "Giannis Antetokounmpo","Nikola Vucevic","Dejounte Murray"]

    # predict future points
    my_league.predict()

    # add players to teams
    for name in fud:
        my_league.player_add(name,"fudruckers")

    for name in tre:
        my_league.player_add(name,"trees")
    
    for name in des:
        my_league.player_add(name,"destroyers")

    for name in jol:
        my_league.player_add(name,"jolly rogers")
    
    # list teams and their rosters
    my_league.list_teams()

    # list free agents
    my_league.free_agent_list()


    # get tuples of priority queues
    compare = my_league.teams["fudruckers"].list_predictions(silent=1)
    agents = my_league.free_agent_list(silent=1)

    # make suggestions to the player
    print('\n' + "Based on your lineup and the available free agents, the following moves are recommended:")
    optimized = 0
    iter = 0
    while optimized < 1 and iter < my_league.capacity:
        if agents[iter][1] > compare[iter][1]:
            print(f" - You should add {agents[iter][0]} ({agents[iter][1]}) and drop {compare[iter][0]} ({compare[iter][1]})")
            iter = iter + 1
        else:
            optimized = 1 
