import random
import time
import numpy as np

class Match():

    def __init__(self, home_team, away_team):

        self.home_team = home_team
        self.away_team = away_team
        self.formation_list = ["433", "442", "343", "352"]
        self.home_lineup = self.get_lineup(home_team.team, random.choice(self.formation_list))
        self.away_lineup = self.get_lineup(away_team.team, random.choice(self.formation_list))
        self.home_goals = 0
        self.away_goals = 0
        self.yellow_cards = []
        self.red_cards = []
        self.scorers = []

    def get_lineup(self, team, formation):  # Returns a list of 11 players (Player object) who are starters in the match.

        for player in team:
            if player.suspended == False:
                goalkeepers = [player for player in team if player.position == "goalkeeper"]
                defenders = [player for player in team if player.position == "defence"]
                midfielders = [player for player in team if player.position == "midfield"]
                forwards = [player for player in team if player.position == "offence"]

        lineup = random.sample(goalkeepers, 1) + random.sample(defenders, int(formation[0])) + random.sample(midfielders, int(formation[1])) + random.sample(forwards, int(formation[2]))

        return lineup

    def goal(self):
        pass
            
    def yellow_card(self):
        pass
        
    def red_card(self):
        pass 
        
    def play_match(self):

        print(f"\nThe match between {self.home_team.name} and {self.away_team.name} at {self.home_team.stadium} is about to start!")
        print(f"\nThe home team coach {self.home_team.coach} has chosen the following lineup:\n")

        time.sleep(1)

        for player in self.home_lineup:
            print(player.name)
            player.appearances += 1
        print(f"\nThe away team coach {self.away_team.coach} has chosen the following lineup:\n")

        time.sleep(1)

        for player in self.away_lineup:
            print(player.name)
            player.appearances += 1

        time.sleep(1)    

        print("\nThe match has started!")     

        for minute in range(1, 91):

            event = Event(self)
            action = event.event()
            action[0](action[1], minute)
            time.sleep(1)
            if minute == 45:
                print(f"\nThe first half has ended with the score: {self.home_team.name} : {self.away_team.name} {self.home_goals} : {self.away_goals}")
                print("\n15-minute break!")
                print("\nThe second half has started!")

    def match_report(self):

        self.home_team.add_match(self.home_goals, self.away_goals, self.home_lineup)
        self.away_team.add_match(self.away_goals, self.home_goals, self.away_lineup)

        print(f"\nThe match has ended. {self.home_team.name} : {self.away_team.name} {self.home_goals} : {self.away_goals}")

        if len(self.scorers) > 0:
            print(f"\nGoals scored by: \n")
            for player in self.scorers:
                print(f"{player.name}")

        if len(self.yellow_cards) > 0:
            print(f"\nYellow cards received by:\n")
            for player in self.yellow_cards:
                print(f"{player.name}")     

HOME = 0.55
AWAY = 0.45
CORNER_GOAL = 0.05
PENALTY_GOAL = 0.80
FREE_KICK_GOAL = 0.10
GOALKEEPER_GOAL = 0.01
DEFENDER_GOAL = 0.15
MIDFIELDER_GOAL = 0.30
FORWARD_GOAL = 0.54
GOALKEEPER_YELLOW_CARD = 0.05
DEFENDER_YELLOW_CARD = 0.45
MIDFIELDER_YELLOW_CARD = 0.30
FORWARD_YELLOW_CARD = 0.20
GOALKEEPER_RED_CARD = 0.10
DEFENDER_RED_CARD = 0.35
MIDFIELDER_RED_CARD = 0.30
FORWARD_RED_CARD = 0.25

class Event():

    def __init__(self, match):
        self.event_list = [self.goal, self.corner, self.foul, self.penalty, self.no_event]
        self.event_probs = [0.03, 0.20, 0.30, 0.01, 0.46]
        self.match = match

    def event(self):

        choice = np.random.choice(self.event_list, p=self.event_probs)
        team = np.random.choice([self.match.home_team, self.match.away_team], p=[0.5, 0.5])
        if team == self.match.home_team:
            return (choice, self.match.home_lineup)
        else:
            return (choice, self.match.away_lineup)

    def goal(self, team, minute):
        team = (self.match.home_team, self.match.away_team)
        choice = np.random.choice(team, p=[HOME, AWAY])
        if choice == self.match.home_team:
            lineup = self.match.home_lineup
            self.match.home_goals += 1
        else:
            lineup = self.match.away_lineup
            self.match.away_goals += 1  
        position = np.random.choice(["goalkeeper", "defence", "midfield", "offence"], p=[GOALKEEPER_GOAL, DEFENDER_GOAL, MIDFIELDER_GOAL, FORWARD_GOAL])
        player = random.choice([player for player in lineup if player.position == position])
        player.goals += 1
        self.match.scorers.append(player)
        print(f"\n{minute}' - GOAL! {self.match.home_team.name} : {self.match.away_team.name} {self.match.home_goals} : {self.match.away_goals}\nGoal scored by {player.name}")
        
        
    def corner(self, team, minute):

        choice = np.random.choice([self.goal, False], p=[CORNER_GOAL, 1 - CORNER_GOAL])
        print(f"\n{minute}' - Corner for {team[0].club}!")
        if choice == False:
            pass
        else:
            choice(team, minute)

    def penalty(self, team, minute):
        print(f"\n{minute}' - Penalty for {team[0].club}")
        choice = np.random.choice([self.goal, False], p=[PENALTY_GOAL, 1 - PENALTY_GOAL])
        if choice == False:
            print("Incredible, they missed the penalty!")
        else:
            choice(team, minute)

    def foul(self, team, minute):

        foul_types = [self.yellow_card, self.red_card, "regular"]
        foul_types_probs = [0.15, 0.02, 0.83]
        choice = np.random.choice(foul_types, p=foul_types_probs)
        if choice == "regular":
            print(f"{team[0].club} committed a foul!")
        else:
            return choice(team, minute)

    def yellow_card(self, team, minute):
        position = np.random.choice(["goalkeeper", "defence", "midfield", "offence"], p=[GOALKEEPER_YELLOW_CARD, DEFENDER_YELLOW_CARD, MIDFIELDER_YELLOW_CARD, FORWARD_YELLOW_CARD])
        player = random.choice([player for player in team if player.position == position])
        player.yellow_cards += 1
        self.match.yellow_cards.append(player)
        print(f"\n{minute}' - {player.name}[{player.club}] received a yellow card!")

    def red_card(self, team, minute):
        position = np.random.choice(["goalkeeper", "defence", "midfield", "offence"], p=[GOALKEEPER_RED_CARD, DEFENDER_RED_CARD, MIDFIELDER_RED_CARD, FORWARD_RED_CARD])
        player = random.choice([player for player in team if player.position == position])
        player.red_cards += 1
        self.match.red_cards.append(player)
        print(f"\n{minute}' - {player.name}[{player.club}] received a red card! {player.club} is now down a player!")
    
    def no_event(self, team, minute):
        pass




    