from datetime import datetime

class Player():

    def __init__(self, name, age, position, nationality, club):
        self.name = name
        self.age = age
        self.position = position.lower()
        self.nationality = nationality
        self.club = club 
        self.goals = 0
        self.assists = 0
        self.yellow_cards = 0
        self.red_cards = 0
        self.appearances = 0
        self.suspended = False
        
    def check_suspension(self):
        if self.yellow_cards % 3 == 0 and self.yellow_cards > 0:
            self.suspended = True   

class Goalkeeper(Player):

    def __init__(self, name, age, position, nationality, club):
        super().__init__(name, age, position, nationality, club)
        self.goals_conceded = 0
        self.cleansheets = 0
