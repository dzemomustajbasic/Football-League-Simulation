import requests
from datetime import datetime
from player import Player
from club import Club

codes = ["PL", "BL1", "SA", "PD", "FL1"]

league_list = []

for code in codes:
    url = f"https://api.football-data.org/v4/competitions/{code}/teams/"
    headers = {
        "X-Auth-Token": "6ad751898e9343cd9702f76d82ac78fe"
    }
    response = requests.request("GET", url, headers=headers)
    data = response.json()

    league = []

    for team in data["teams"]:
        name = team["name"]
        manager = team["coach"]["name"]
        stadium = team["venue"]
        founded = team["founded"]
        players_dict = {player["name"]: player for player in team["squad"]}
        team_dict = {
            'name': name,
            'manager': manager,
            'stadium': stadium,
            'founded': founded,
            'roster': players_dict
        }
        league.append(team_dict)

    league_list.append(league)

""" 
A list of 5 elements where each element represents a new list consisting of dictionaries, where
each dictionary represents a new club. A club has 5 keys, the last of which is the roster key, whose value
is another dictionary representing each player.
"""










            
    



 





