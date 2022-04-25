import requests
import csv
import os
import datetime
import pandas as pd

from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import fantasywidget
from datetime import date
from Player import Player

def nba_schedule(season='2021', save_path='csv_files'):


    ''' This function loads the nba teams and schedule for a given 
        year. It does nothing if the year has already been loaded.'''
    
    # Fetch data
    response = requests.get(
        'https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/' + season 
        + '/league/00_full_schedule.json')
    data = response.json()

    

    # Write data to file specified by save_path and save_file, if it 
    # exists then return
    save_path = save_path + '/' + season
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print(f'Directory {save_path} was created.\n\n')
    else:
        return

    file = open(save_path + '/nba_schedule.csv', 'w')
    file.write('Date,GameID, Away, Home\n') # headers

    # Write schedule from json
    for month in range(len(data['lscd'])):  #lscd: league schedule
        for game in range(len(data['lscd'][month]['mscd']['g'])):  # mscd: month schedule
            date = data['lscd'][month]['mscd']['g'][game]['gdte']
            game_id = data['lscd'][month]['mscd']['g'][game]['gid']
            away_team = data['lscd'][month]['mscd']['g'][game]['v']['ta']
            home_team = data['lscd'][month]['mscd']['g'][game]['h']['ta']
            file.writelines(f'{date},{game_id},{away_team},{home_team}\n')
    
    file.close()

    fieldnames = ['id','full_name','abbreviation','nickname','city','state','year_founded']
    nba_teams = teams.get_teams()

    # write nba team data
    with open(save_path + '/nba_team.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(nba_teams)


def first_game(season='2021'):

    ''' This function returns the first game of an nba season'''


    # create data if not existing yet
    read_dir = 'csv_files/' + season
    if not os.path.exists(read_dir):
        nba_schedule(season)
    
    # read data
    read_path = read_dir + '/nba_schedule.csv'
    raw_data = csv.reader(open(read_path))
    start_month = '12'
    start_date = '31'
    end_month = '01'
    end_date = '01'

    # get smallest date and largest date
    for data in raw_data:
        curr_date = data[0].split('-')
        if (curr_date[0] == season):
            if (int(curr_date[1]) < int(start_month)):
                start_month = curr_date[1]
                start_date = 31
                if (int(curr_date[2]) < int(start_date)):
                    start_date = curr_date[2]     
            elif int(curr_date[1]) == start_month:
                if int(curr_date[2]) < int(start_date):
                    start_date = curr_date[2]
        elif (curr_date[0] == str(int(season) + 1)):
            if (int(curr_date[1]) > int(end_month)):
                end_month = curr_date[1]
                end_date = '01'
                if (int(curr_date[2]) > int(end_date)):
                    end_date = curr_date[2]

    
    start = season + '-' + start_month + '-' + start_date
    season = str(int(season) + 1)
    end = season + '-' + end_month + '-' + end_date


    return start,end
    

def check_date(date,season='2021'):
    ''' Checks when file has last been updated '''

    update_dir = 'csv_files/' + season
    update_file = update_dir + '/update_data.csv'

    # load season if not existing
    if not os.path.exists(update_dir):
        nba_schedule(season)

    # check if file exists
    if not os.path.exists(update_file):

        start,end = first_game(season)

        dictionary = {'start': start, 'end': end, 'update': date}
        field_names = ['start', 'end', 'update']

        with open(update_file, 'w') as file:
            writer = csv.DictWriter(file,fieldnames=field_names)
            writer.writeheader()
            writer.writerow(dictionary)

            return 1  # return 0 since no update data

    # Checks if date today matches with last update
    raw_data = next(csv.DictReader(open(update_file)))

    if raw_data['update'] == date:
        return 0  # does not need to be updated 
    else:
        field_names = ['start', 'end','update']
        raw_data['update'] = date

        with open(update_file, 'w') as file:
            writer = csv.DictWriter(file,fieldnames=field_names)
            writer.writeheader()
            writer.writerow(raw_data)

        return 1 # needs to be updated


def get_nba_raw_data(start,end,season='2021'):
    ''' Loads data between a given date range '''

    raw_data = fantasywidget.FantasyWidget(
                date_from_nullable = start, 
                date_to_nullable = end)
    
    headers = raw_data.get_dict()['resultSets'][0]['headers']
    raw_data = raw_data.get_dict()['resultSets'][0]['rowSet']
    write_path = 'csv_files/' + season + '/fantasy_nba_raw_data.csv'

    with open(write_path, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(raw_data)

def earlier_date(end, update):
    ''' This function compares two dates and returns the earlier date'''

    end_comp = end.split('-')
    update_comp = update.split('-')

    if (int(update_comp[0]) > int(end_comp[0])):  #return end if the date that it is 
        return end                                #being updated on is after season's end
    elif(int(update_comp[0]) == int(end_comp[0])):
        if (int(update_comp[1]) > int(end_comp[1])):
            return end
        elif (int(update_comp[1]) == int(end_comp[1])):
            if (int(update[comp[2]]) < int(end_comp[2])):
                return end

    return update


def n_days(date,days):
    ''' This function returns the date thirty days back '''
    date = date.split('-')
    date = datetime.datetime(int(date[0]),int(date[1]),int(date[2]))

    thirty = date + datetime.timedelta(days)

    return thirty.strftime("%Y-%m-%d")

def load_players(season='2021'):
    players = {}
    read_path = 'csv_files/' + season + '/fantasy_nba_raw_data.csv'

    i = 0
    
    with open(read_path) as csv_file:
        raw_data = csv.reader(csv_file)
        for player_data in raw_data:
            if (i == 0):
                i += 1
                continue
            elif (player_data):
                player = Player(player_data)
                players[player_data[1]] = player

    return players


def get_games_for_week(start_date, days=6, season='2021'):
    ''' This function gets the number of NBA games each team plays
        per week'''
    end_date = n_days(start_date,days)
    team_data = {}

    week = pd.date_range(start = start_date, end = end_date)
    week = [str(date.date()) for date in week]

    with open('csv_files/' + season + '/nba_schedule.csv','r') as csv_file:
            
        schedule = csv.reader(csv_file)

        for game in schedule:
            if game[0] in week:
                team_data[game[2]] = team_data.get(game[2],0) + 1
                team_data[game[3]] = team_data.get(game[3],0) + 1
    
    return team_data


def weekly_nba_data(start_date = '2022-04-10', days=6, season ='2021'):
    end_date = n_days(start_date,days)

    weekly_data = {}

    week = pd.date_range(start = start_date, end = end_date)

    for date in week:
        key = str(date.date())
        weekly_data[key] = {}

    with open('csv_files/' + season + '/nba_schedule.csv', 'r') as csv_file:
        schedule = csv.reader(csv_file)

        for game in schedule:
            if (game[0] == key):
                away_team = game[2]
                home_team = game[3]
                weekly_data[key][away_team] = []
                weekly_data[key][home_team] = []
        
    for date in weekly_data:
        for team in weekly_data[date]:
            weekly_data[date][team] = team_data(team)

    return weekly_data

    


    
