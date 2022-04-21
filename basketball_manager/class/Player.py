class Player:
    ''' Each nba player is represented by a player class '''

    def __init__(self, player_data):
        self.player_id = int(player_data[0])
        self.name = player_data[1]
        self.position = player_data[2]
        self.team_id = player_data[3]
        self.team = player_data[4]
        self.fantasy_average = float(player_data[8])
        self.pts = player_data[9]
        self.fantasy_id = 0
        self.fantasy_predicted = 0
    
    def fantasy_add(self, team_id): # add player to fantasy team
        self.fantasy_id = team_id
    
    def fantasy_drop(self): # reset player
        self.fantasy_id = 0
