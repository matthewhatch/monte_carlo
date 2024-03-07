# Monte Carlo Simulation:
# Rules:
# Based on Players Stats, we can determine the probability of each outcome
import argparse
from Player import Player

def simulate_inning(player):
    runs = 0
    state = [0,0,0,0] # tracks outs and runners on 1st, 2nd, 3rd
    while state[0] < 3:
        state, runs_scored = player.simulate_ab(state)
        runs = runs + runs_scored
    
    return runs

def simulate_game(player):
    runs = 0
    for _ in range(0,9):
        results = simulate_inning(player)
        runs = runs + results
    return runs

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', '-c', type=int, default=1000)
    args = parser.parse_args()

    simulations = args.count
    total_runs = 0
    trout = Player(681, 554, 10, 234, 137, 118, 11, 107, 32, 5, 29)

    for _ in range(0, simulations):
        runs_scored = simulate_game(trout)
        total_runs = total_runs + runs_scored
    
    average_runs = total_runs / simulations
    print(average_runs)

