from Team import Team
from Player import Player
import operator

class League:
    '''League with Teams in it'''


    def __init__(self,date,games,players={},capacity=10):
        self.teams = {}
        self.players = players
        self.games = games
        self.capacity = capacity
        self.order = []
    
    def add_team(self,team_name):
        self.teams[team_name] = Team(len(self.teams)+1,team_name)

    def player_add(self, player_name, team_name):
        if player_name in self.players:
            if (self.players[player_name].fantasy_id == 0) and len(self.teams[team_name].players) <= self.capacity:
                self.teams[team_name].add_player(self.players[player_name])
                self.players[player_name].fantasy_id = self.teams[team_name].team_id
            else:
                print(f'{player_name} could not be added.')
        else:
            print(f"Error loading {player_name}")
    
    def player_drop(self, player_name, team_name):
        if (self.players[player_name].team_id == self.teams[team_name].team_id):
            self.teams[team_name].drop_player(player_name)
            self.players[player_name].fantasy_id = 0
        else:
            print(f'{player_name} is not on you team.')

    def list_teams(self):
        for team in self.teams:
            self.teams[team].list_players()

    def predict(self):
        for name in self.players:
            self.players[name].fantasy_predicted = self.players[name].fantasy_average*self.games[self.players[name].team]
    
    def print_order(self,team_name):
        self.teams[team_name].sort_players()
    
    def free_agent_list(self,silent=0):
        return_list = []
        for name in self.players:
            if self.players[name].fantasy_id == 0:
                if (len(self.order) <= self.capacity): # list is not filled yet
                    self.order.append(self.players[name])
                    self.order = list(sorted((self.order),key=operator.attrgetter('fantasy_predicted'),reverse=True))
                else:
                    if self.players[name].fantasy_predicted > self.order[-1].fantasy_predicted:
                        self.order.pop()
                        self.order.append(self.players[name])
                        self.order = list(sorted(self.order,key=operator.attrgetter('fantasy_predicted'),reverse=True))

        for i in self.order:
            if silent == 0:
                print(f'{i.name}: {i.fantasy_predicted:0.2f}')
            return_list = return_list + [(i.name,i.fantasy_predicted)] 
        
        self.order = []
        return return_list


        


