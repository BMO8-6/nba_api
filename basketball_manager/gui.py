#!/usr/bin/env python3

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

from tkinter import *
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkcalendar import Calendar

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

global date
global game_index 
global players 

players = {}



# functions
sys.path.insert(0, 'functions/')
import dataloader

if __name__ == "__main__":

    def get_player_data():
        date = date_str.get().split('/') # 0 month 1 day 2 year
        date[2] = '20' + date[2]
        date = datetime(int(date[2]),int(date[0]),int(date[1]))

        date = date.strftime("%Y-%m-%d")

        update_status = dataloader.check_date(date,season=season) # return 1 if update needed
        
        update_dir = 'csv_files/' + season
        update_file = update_dir + '/update_data.csv'
        update_data = next(csv.DictReader(open(update_file)))

        thirty = dataloader.n_days(date,-30)

        if update_status:
            dataloader.get_nba_raw_data(thirty,date,season=season)

        game_index = dataloader.get_games_for_week(date)
        print("Games this week: ")
        print(game_index)
        players = dataloader.load_players()
        available = players

        global my_league
        
        my_league = League(date,game_index,players=players,capacity=5)
        my_league.predict()

        
        teams = ["Your Team","destroyers", "jolly rogers", "trees"] 

        for team in teams:
            my_league.add_team(team)

        des = ["Kevin Durant", "Joel Embiid", "Rudy Gobert", "Jayson Tatum", "Bam Adebayo"]
        jol = ["Luka Doncic","Kyrie Irving", "Trae Young", "Devin Booker", "Pascal Siakam"]
        tre = ["Jrue Holiday", "James Harden", "Giannis Antetokounmpo","Nikola Vucevic","Dejounte Murray"]

        for name in tre:
            my_league.player_add(name,"trees")
            available.pop(name,'None')

        for name in des:
            my_league.player_add(name,"destroyers")
            available.pop(name,'None')

        for name in jol:
            my_league.player_add(name,"jolly rogers")
            available.pop(name,'None')
        
        for name in list(available.keys()):
            player_entry.insert(END,name)

    def add_player():
        name = player_entry.get(player_entry.curselection())
        my_league.player_add(name,"Your Team",silent=0)
        print()
        print("Current Roster:")
        my_league.teams["Your Team"].list_predictions()

    def make_predictions():
        os.system('clear')
        my_league.list_teams()

        # list free agents
        my_league.free_agent_list()


        # get tuples of priority queues
        total, compare = my_league.teams["Your Team"].list_predictions(silent=1)
        agents = my_league.free_agent_list(silent=1)

        # make suggestions to the player
        print('\n' + "Based on your lineup and the available free agents, the following moves are recommended:")
        optimized = 0
        iter = 0
        old = total
        while optimized < 1 and iter < my_league.capacity:
            if agents[iter][1] > compare[iter][1]:
                print(f" - You should add {agents[iter][0]} ({agents[iter][1]:0.2f}) and drop {compare[iter][0]} ({compare[iter][1]:0.2f})")
                total += (agents[iter][1] - compare[iter][1])
                iter = iter + 1
            else:
                optimized = 1 

        print(f"This brings your expected total from {old:0.2f} to {total:0.2f}")
            
    season = '2021'
    # check if year matches
    dataloader.nba_schedule(season=season)  # will do nothing if schedule has been loaded

    root = Tk()

    mainframe = ttk.Frame(root, padding = "5 5 12 12")
    mainframe.grid(column=0,row=0,sticky = (N,W,E,S))
    root.columnconfigure(0,weight=1)
    root.rowconfigure(0,weight=1)

#player_entry = ttk.Entry(mainframe, width=7, textvariable=player_add)
#player_entry.grid(column=2,row=1,sticky=(W,E))
    player_entry = Listbox(root)
    player_entry.grid(column=1,row=0)

    
    ttk.Button(mainframe, text = "Add Player", command=add_player).grid(column=0,row=1,sticky=W)
    ttk.Button(mainframe, text = "Predict", command = make_predictions).grid(column=0,row=0)
    ttk.Button(mainframe, text = "Start", command = get_player_data).grid(column=0,row=2)
    
    date_str = StringVar()
    cal = Calendar(root, selectmode='day',year=2022,month=3,day=21,textvariable=date_str)
    cal.grid(column=1,row=2)

    date = Label(root, textvariable = date_str).grid(column=1,row=2)

    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
    

    root.mainloop()



    # load players and game schedules

    # team rosters

    # predict future points
    

    
    # list teams and their rosters
