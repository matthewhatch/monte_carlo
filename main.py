# Monte Carlo Simulation:
# Rules:
# Based on Players Stats, we can determine the probability of each outcome
import argparse
from classes.Player import Player
from constants.players import TROUT16
from tqdm import tqdm
from utils.players import get_stats

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
        inning_runs = simulate_inning(player)
        runs = runs + inning_runs
    return runs

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', '-c', type=int, default=1000)
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--player', '-p', type=str, default='Mike Trout')
    parser.add_argument('--year', '-y', type=str, default='2016')
    args = parser.parse_args()

    simulations = args.count
    total_runs = 0
   
    player_stats = get_stats(args.player.lower(), args.year)

    if player_stats is None:
        print(f'Player {args.player.title()} not found for {args.year}')
        exit(0)

    player = Player(**player_stats)
    for i in tqdm(range(1, simulations + 1)):
        runs_scored = simulate_game(player)
        total_runs = total_runs + runs_scored
        if args.verbose:
            print(f'Simulating game {i} - Runs: {runs_scored}')
    
    average_runs = total_runs / simulations
    player.runs_created(average_runs)
    print(str(player))

