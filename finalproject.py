#!/usr/bin/python

"""
 * Name: Joshua Bih
 * Email: jbih2@nd.edu
 * File Name: finalproject.py
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

import os
import sys
import pprint

from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import leaguegamefinder, playercareerstats
from nba_api.live.nba.endpoints import scoreboard

import pandas as pd
from datetime import datetime, timezone
from dateutil import parser

def usage(exit_code=0):
    progname = os.path.basename(sys.argv[0])
    print(f'''Usage: {progname} [-a ALPHABET -c CORES -l LENGTH -p PATH -s HASHES]
    -a ALPHABET Alphabet to use in permutations
    -c CORES    CPU Cores to use
    -l LENGTH   Length of permutations
    -p PREFIX   Prefix for all permutations
    -s HASHES   Path of hashes file''')
    sys.exit(exit_code)

def main():
    # The player ID can be changed to find whoever you want
    career = playercareerstats.PlayerCareerStats(player_id='203076')
    print(career.get_data_frames()[1])



    ## From here to the for loop is to find the upcoming games for the day
    f = "{gameId}: {awayTeam} vs. {homeTeam} @ {gameTimeLTZ}" 

    ## Can modify this so that you iterate tbrough all the days for the week instead of just 1 day
    board = scoreboard.ScoreBoard()
    print("ScoreBoardDate: " + board.score_board_date)

    ## Can change this data type into json, data frames, normalized versions, or raw response
    games = board.games.get_dict()
    for game in games:
        gameTimeLTZ = parser.parse(game["gameTimeUTC"]).replace(tzinfo=timezone.utc).astimezone(tz=None)
        print(f.format(gameId=game['gameId'], awayTeam=game['awayTeam']['teamName'], homeTeam=game['homeTeam']['teamName'], gameTimeLTZ=gameTimeLTZ))



    ### This gets the team information for a given team
    nba_teams = teams.get_teams()
    
    ### Select the dictionary for the Celtics, which contains their team ID
    celtics = [team for team in nba_teams if team['abbreviation'] == 'BOS'][0]
    celtics_id = celtics['id']

    ### Query for games where the Celtics were playing
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=celtics_id)

    ### The first DataFrame of those returned is what we want.
    print(gamefinder.get_data_frames()[0])



    # Parse command line arguments  
    """
    if len(sys.argv) ...:
        usage(3)

    arguments = sys.argv[1:]

    while (len(arguments) and arguments[0].startswith('-')):
        argument = arguments.pop(0)
        
        if argument == "-h":
            usage(0)

        elif argument == "-s":

        elif argument == "-n":

        elif argument == "-o":

        elif argument == "-t":

        else:
            usage(4)
    """


# Main Execution

if __name__ == '__main__':
    main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
