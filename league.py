from club import Club
from player import Player, Goalkeeper
from tabulate import tabulate
from match import Match
import time
from abc import ABC, abstractmethod
from jsonparsing import league_list

class League(ABC):

    def __init__(self, name, number_of_clubs):
        self.name = name
        self.number_of_clubs = number_of_clubs
        self.clubs = []
        self.number_of_rounds = number_of_clubs * 2
        self.create_league(league_list)
           
    @abstractmethod
    def info(self):
        raise NotImplementedError("You need to implement this method in a subclass!")
    
    @classmethod
    def get_name(cls):
        return cls.__name__

    def create_league(self, league_list):
        raise NotImplementedError("You need to implement this method in a subclass!")    
    
    def add_new_club(self, club):
        self.clubs.append(club)
         
    def make_schedule(self) -> dict:
        schedule = {}
        copy = [club for club in self.clubs]
        for i in range((len(copy) - 1) * 2):
            matches_in_round = []
            for j in range(0, len(copy) // 2):
                if i < len(copy) - 1:
                    match = (copy[j], copy[-(j + 1)])
                    matches_in_round.append(match)
                else:
                    match = (copy[-(j + 1)], copy[j])
                    matches_in_round.append(match)   
            schedule[i + 1] = matches_in_round
            copy = [copy[0]] + [copy[-1]] + copy[1:-1]  
        return schedule 
    
    def play_next_round(self, round_number, schedule) -> dict:
        current_round = schedule[round_number]
        print(f"\nIn round {round_number} of {self.name}, the matches are: \n")
        for i in range(self.number_of_clubs // 2):
                print(f"{current_round[i][0].name} vs {current_round[i][1].name}")   
        return current_round      
       
    def simulate_season(self):
        time.sleep(2)
        clubs = {club.name : club for club in self.clubs}
        schedule = self.make_schedule()
        for i in range(self.number_of_rounds):
            report = []
            current_round = self.play_next_round(i + 1, schedule)
            for match in current_round:
                for team in match:
                    game = Match(clubs[match[0].name], clubs[match[1].name])
                    game.play_match()
                    game.match_report()
                    report.append(game)
                    break
            self.post_round_report(report, i + 1)    
            self.print_table()
            self.get_top_scorers()  

    def print_table(self):
        time.sleep(2)
        print(f"\nStandings of {self.name} after {self.clubs[0].number_of_played_matches} rounds:\n")
        time.sleep(2)
        table = []
        i = 1
        for club in self.clubs:
            club_table = [club.name, club.number_of_played_matches, club.points, club.number_of_wins, club.number_of_draws, club.number_of_losses, club.number_of_scored_goals, club.number_of_conceded_goals, club.number_of_scored_goals - club.number_of_conceded_goals]
            table.append(club_table)
            i += 1
        # Sort the list by points column
        sorted_table = sorted(table, key=lambda points : points[2], reverse=True)
        # Add position column 1-12 after sorting
        i = 1
        for lst in sorted_table:
            lst.insert(0, i)
            i += 1     

        columns = ["Pos", "Club Name", "MP", "Points", "W", "D", "L", "GF", "GA", "GD"]
        # Create a table sorted by 'Points' column    
        tabulate_table = tabulate(sorted_table, headers=columns, tablefmt="fancy_grid")

        print(tabulate_table) 

    def post_round_report(self, report, round_number):
        #time.sleep(2)
        print(f"\nRound {round_number} of {self.name} is completed, and these are the results:\n")
        #time.sleep(1)
        for match in report:
            time.sleep(1)
            print(f"{match.home.name} : {match.away.name} {match.home_goals} : {match.away_goals}")

    def get_top_scorers(self):
        table = []
        time.sleep(2)
        print(f"\nTop scorers list after {self.clubs[0].number_of_played_matches} rounds: \n")
        time.sleep(2)
        for club in self.clubs:
            for player in club.team:
                if player.goals > 0:
                    scorers_list = [player.name, player.position, player.club, player.goals]
                    table.append(scorers_list)   

        columns = ["Name", "Position", "Club", "Goals"]
        sorted_table = sorted(table, key=lambda goals : goals[3], reverse=True)                  
        print(tabulate(sorted_table, headers=columns))

    def get_top_assistants(self):
        table = []
        print(f"\nTop assistants list after {self.clubs[0].number_of_played_matches} rounds: \n")
        for club in self.clubs:
            for player in club.team:
                    if player.assists > 0:
                        assistants_list = [player.name, player.position, player.club, player.assists]
                        table.append(assistants_list)   

        columns = ["Name", "Position", "Club", "Assists"]
        sorted_table = sorted(table, key=lambda assists : assists[3], reverse=True)                  
        print(tabulate(sorted_table, headers=columns))            
    
class PremierLeague(League):

    def __init__(self):
        super().__init__("English Premier League", 20)
        self.info()

    def info(self):
        print("\nWelcome to the simulation of the English Premier League!")

    def create_league(self, league_list):
        for club in league_list[0]:
            #time.sleep(1)
            new_club = Club(club["name"], club["manager"], club["stadium"], club["founded"])
            for name, details in club["roster"].items():
                if details["position"] == "Goalkeeper":
                    new_player = Goalkeeper(name, details["dateOfBirth"], details["position"], details["nationality"], club["name"])
                else:
                    new_player = Player(name, details["dateOfBirth"], details["position"], details["nationality"], club["name"])
                new_club.add_new_player(new_player)
            self.add_new_club(new_club)    
        print("\nLeague successfully created!")           

class Bundesliga(League):

    def __init__(self):
        super().__init__("Bundesliga", 18)
        self.info()

    def info(self):
        print("\nWelcome to the simulation of the German Bundesliga!") 

    def create_league(self, league_list):
        for club in league_list[1]:
            time.sleep(1)
            new_club = Club(club["name"], club["manager"], club["stadium"], club["founded"])
            for name, details in club["roster"].items():
                if details["position"] == "Goalkeeper":
                    new_player = Goalkeeper(name, details["dateOfBirth"], details["position"], details["nationality"], club["name"])
                else:
                    new_player = Player(name, details["dateOfBirth"], details["position"], details["nationality"], club["name"])
                new_club.add_new_player(new_player)
            self.add_new_club(new_club)    
        print("\nLeague successfully created!")              

class LaLiga(League):

    def __init__(self):
        super().__init__("Primera Division", 20)
        self.info()

    def info(self):
        print("\nWelcome to the simulation of the Spanish La Liga!")

    def create_league(self, league_list):
        for club in league_list[3]:
            time.sleep(1)
            new_club = Club(club["name"], club["manager"], club["stadium"], club["founded"])
            for name, details in club["roster"].items():
                if details["position"] == "Goalkeeper":
                    new_player = Goalkeeper(name, details["dateOfBirth"], details["position"], details["nationality"], club["name"])
                else:
                    new_player = Player(name, details["dateOfBirth"], details["position"], details["nationality"], club["name"])
                new_club.add_new_player(new_player)
            self.add_new_club(new_club)    
        print("\nLeague successfully created!")       

class Ligue1(League):

    def __init__(self):
        super().__init__("Ligue 1", 18)
        self.info()

    def info(self):
        print("\nWelcome to the simulation of the French Ligue 1!")

    def create_league(self, league_list):
        for club in league_list[4]:
            time.sleep(1)
            new_club = Club(club["name"], club["manager"], club["stadium"], club["founded"])
            for name, details in club["roster"].items():
                if details["position"] == "Goalkeeper":
                    new_player = Goalkeeper(name, details["dateOfBirth"], details["position"], details["nationality"], club["name"])
                else:
                    new_player = Player(name, details["dateOfBirth"], details["position"], details["nationality"], club["name"])
                new_club.add_new_player(new_player)
            self.add_new_club(new_club)    
        print("\nLeague successfully created!")       
        

class SerieA(League):
    
    def __init__(self):
        super().__init__("Serie A", 20)
        self.info()

    def info(self):
        print("\nWelcome to the simulation of the Italian Serie A!")

    def create_league(self, league_list):
        for club in league_list[2]:
            time.sleep(1)
            new_club = Club(club["name"], club["manager"], club["stadium"], club["founded"])
            for name, details in club["roster"].items():
                if details["position"] == "Goalkeeper":
                    new_player = Goalkeeper(name, details["dateOfBirth"], details["position"], details["nationality"], club["name"])
                else:
                    new_player = Player(name, details["dateOfBirth"], details["position"], details["nationality"], club["name"])
                new_club.add_new_player(new_player)
            self.add_new_club(new_club)    
        print("\nLeague successfully created!") 

                                 







