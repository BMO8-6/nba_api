from Player import Player
import operator 
class Team:
    '''Fantasy Team with players on it'''


    def __init__(self,team_id,team_name):
        self.team_id = team_id
        self.team_name = team_name
        self.players = {}
        self.order = []

    def add_player(self, Player): # add player
        Player.fantasy_add(self.team_id)
        self.players[Player.name] = Player

    def drop_player(self,name): # drop player
        self.players[name].fantasy_drop()
        self.players.pop(name,None)
    
    def list_predictions(self,silent=0): # lists players and predictions
        self.sort_players()

        return_list = []

        for name in self.order:
            if silent == 0:
                print(f'{self.players[name].name} : {self.players[name].fantasy_predicted:0.2f}')
            return_list.append((self.players[name].name,self.players[name].fantasy_predicted))
        
        self.order = []

        return return_list

    def list_players(self): # lists teams and their players in sorted order
        print(f'{self.team_name}:\n')

        return_list = self.list_predictions()
        
        print("")

        return return_list
    
    def sort_players(self): # sorts players in reverse order
        for player in sorted(self.players.values(), key= operator.attrgetter('fantasy_predicted')):
            self.order.append(player.name)

