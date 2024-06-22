from league import PremierLeague, Bundesliga, LaLiga, Ligue1, SerieA
import time

leagues = [PremierLeague, Bundesliga, Ligue1, LaLiga, SerieA]

print("\nWelcome to the simulation of the top 5 European leagues\n")

for i in range(5):
    time.sleep(0.5)
    print(f"{i + 1} - {leagues[i].get_name()}")
choice = int(input("\nPlease choose the league you want to simulate: (1-5) "))

simulate = leagues[choice - 1]()
simulate.simulate_season()












    

                                        







