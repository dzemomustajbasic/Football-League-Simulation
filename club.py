import time

class Club():

    def __init__(self, name, manager, stadium, founded):
        self.name = name
        self.stadium = stadium
        self.coach = manager
        self.founded = founded
        self.team = []
        self.number_of_played_matches = 0
        self.points = 0
        self.number_of_wins = 0
        self.number_of_losses = 0
        self.number_of_draws = 0
        self.number_of_scored_goals = 0
        self.number_of_conceded_goals = 0
        print(f"\n{name} was founded in {founded}, they play at {stadium}, and their manager is {manager}.")

    def add_new_player(self, player):
        player.club = self.name
        self.team.append(player)

    def add_match(self, scored, conceded, lineup):
        for player in lineup:
            if player.position == "goalkeeper" and conceded == 0:
                player.cleansheets += 1

        self.number_of_played_matches += 1
        self.number_of_scored_goals += scored
        self.number_of_conceded_goals += conceded

        if scored > conceded:
            self.points += 3
            self.number_of_wins += 1
        elif scored < conceded:
            self.number_of_losses += 1
        else:
            self.points += 1
            self.number_of_draws += 1        

    def list_players(self):
        for player in self.team:
            print(f"\n{player.name}")
    
    def get_stadium_name(self):
        return self.stadium

    
                   

    
   