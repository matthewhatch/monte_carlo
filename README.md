# Monte Carlo Simulation: Runs Created Calculator

A Monte Carlo simulation tool that calculates Runs Created (RC) for any Major League Baseball player in any year. The simulator uses historical player statistics to model plate appearance outcomes and runs scored across full games.

## Overview

This project is inspired by the book *Mathletics* and implements a probabilistic baseball game simulator. Based on a player's historical statistics (batting average, walk rate, home run rate, etc.), the simulator:

1. Runs multiple game simulations where each plate appearance outcome is determined probabilistically
2. Tracks baserunners and outs using game state logic
3. Calculates runs scored across 9 innings for each simulated game
4. Averages results across all simulations to estimate Runs Created

The simulator accounts for different types of hits (singles, doubles, triples, home runs) and various baserunning scenarios.

## Data

Player statistics are sourced from baseball-reference.com and cached locally in CSV files organized by year (2002-2005, 2015-2018).

## Setup

```bash
# Clone the repository
git clone git@github.com:matthewhatch/monte_carlo.git
cd monte_carlo

# Create virtual environment
python -m venv env

# Activate environment and install dependencies
source env/bin/activate
poetry install
```

## Usage

Run simulations for any player and year:

```bash
# Run 100 simulations for Mike Trout in 2016
python main.py -c 100 --player 'Mike Trout' --year 2016

# Run with verbose output
python main.py -c 1000 --player 'Babe Ruth' --year 2018 --verbose
```

### Command Line Arguments

- `-c, --count`: Number of simulations to run (default: 1000)
- `-p, --player`: Player name to simulate (default: 'Mike Trout')
- `-y, --year`: Year of statistics to use (default: '2016')
- `-v, --verbose`: Print output for each simulated game
