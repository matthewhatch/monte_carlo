"""CLI entry point for the monte-carlo simulator.

Provides simulation driver functions and the ``main`` console-script entry
point registered as ``monte-carlo`` in pyproject.toml.
"""

import argparse
from tqdm import tqdm
from .classes.Player import Player
from .utils.players import get_stats

def simulate_inning(player):
    """Simulate a single baseball inning for *player*.

    Repeatedly calls :meth:`Player.simulate_ab` until the inning ends (3 outs).

    Args:
        player (Player): An instantiated :class:`~monte_carlo.classes.Player.Player`
            object whose statistical rates drive the simulation.

    Returns:
        int: Total runs scored in the inning (>= 0).
    """
    runs = 0
    state = [0,0,0,0] # tracks outs and runners on 1st, 2nd, 3rd
    while state[0] < 3:
        state, runs_scored = player.simulate_ab(state)
        runs = runs + runs_scored
    
    return runs

def simulate_game(player):
    """Simulate a complete 9-inning baseball game for *player*.

    Calls :func:`simulate_inning` nine times and sums the results.

    Args:
        player (Player): An instantiated :class:`~monte_carlo.classes.Player.Player`
            object.

    Returns:
        int: Total runs scored across all 9 innings.
    """
    runs = 0
    for _ in range(0,9):
        inning_runs = simulate_inning(player)
        runs = runs + inning_runs
    return runs

def main():
    """Console-script entry point for the ``monte-carlo`` command.

    Parses command-line arguments, retrieves player statistics via
    :func:`~monte_carlo.utils.players.get_stats`, runs the requested number of
    full-game simulations, and prints the player's Runs Created estimate.

    CLI Arguments:
        --count / -c (int): Number of game simulations to run. Default: 1000.
        --player / -p (str): Player name (case-insensitive). Default: 'Mike Trout'.
        --year / -y (str): Season year for statistics. Default: '2016'.
        --verbose / -v (flag): Print per-game run totals when set.

    Raises:
        Exception: If the player is not found in the local CSV cache or on
            baseball-reference.com.
    """
    parser = argparse.ArgumentParser(prog='monte-carlo', description='Monte Carlo Simulator for MLB player performance')
    parser.add_argument('--count', '-c', type=int, default=1000)
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--player', '-p', type=str, default='Mike Trout')
    parser.add_argument('--year', '-y', type=str, default='2016')
    args = parser.parse_args()

    simulations = args.count
    total_runs = 0
   
    player_stats = get_stats(args.player.lower(), args.year)

    if player_stats is None:
        raise Exception(f'Player {args.player.title()} not found for {args.year}')  

    player = Player(**player_stats)
    for i in tqdm(range(1, simulations + 1)):
        runs_scored = simulate_game(player)
        total_runs = total_runs + runs_scored
        if args.verbose:
            print(f'Simulating game {i} - Runs: {runs_scored}')
    
    average_runs = total_runs / simulations
    player.runs_created(average_runs)
    print(str(player))

if __name__ == '__main__':
    main()
