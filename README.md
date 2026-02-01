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

Player statistics are cached locally in CSV files organized by year (2002-2005, 2015-2018). The project can automatically generate test data from player constants, making it CI/CD friendly without requiring web scraping in pipelines.

## Installation

### From Source (Development)

```bash
# Clone the repository
git clone git@github.com:matthewhatch/monte_carlo.git
cd monte_carlo

# Create virtual environment
python -m venv env

# Activate environment
source env/bin/activate

# Install in editable mode
pip install -e .
```

### As a Package

```bash
pip install monte-carlo
```

### From GitHub

```bash
# Install from main branch
pip install git+https://github.com/matthewhatch/monte_carlo.git

# Install from a specific branch
pip install git+https://github.com/matthewhatch/monte_carlo.git@feature/module

# Install in editable mode (for development)
pip install -e git+https://github.com/matthewhatch/monte_carlo.git#egg=monte-carlo
```

Or add to your project's dependencies:

**requirements.txt:**
```
monte-carlo @ git+https://github.com/matthewhatch/monte_carlo.git
```

**pyproject.toml (Poetry):**
```toml
[tool.poetry.dependencies]
monte-carlo = {git = "https://github.com/matthewhatch/monte_carlo.git", branch = "main"}
```

## Usage

### Command Line

Use the `monte-carlo` command after installation:

```bash
# Run 100 simulations for Mike Trout in 2016
monte-carlo -c 100 --player 'Mike Trout' --year 2016

# Run with verbose output
monte-carlo -c 1000 --player 'Babe Ruth' --year 2018 --verbose

# Full example with all options
monte-carlo -c 500 -p 'David Ortiz' -y 2015 -v
```

Or use the wrapper script:

```bash
python main.py -c 100 --player 'Mike Trout' --year 2016
```

### Command Line Arguments

- `-c, --count`: Number of simulations to run (default: 1000)
- `-p, --player`: Player name to simulate (default: 'Mike Trout')
- `-y, --year`: Year of statistics to use (default: '2016')
- `-v, --verbose`: Print output for each simulated game

### Python Module

Import and use as a module:

```python
from monte_carlo.utils.players import get_stats
from monte_carlo.classes.Player import Player
from monte_carlo.cli import simulate_game, simulate_inning

# Get player stats
stats = get_stats('mike trout', '2016')

# Create player instance
player = Player(**stats)

# Run simulations
total_runs = sum(simulate_game(player) for _ in range(100))
average_runs = total_runs / 100
```

## Project Structure

```
monte_carlo/
├── src/monte_carlo/
│   ├── cli.py              # Command-line interface
│   ├── events.py           # Baseball event definitions
│   ├── classes/
│   │   └── Player.py       # Player simulation logic
│   ├── constants/
│   │   ├── events.py       # Event type constants
│   │   └── players.py      # Pre-defined player stats
│   └── utils/
│       └── players.py      # Player data utilities
├── tests/                  # Unit tests
├── data/                   # Cached player statistics (CSV)
├── main.py                 # CLI wrapper script
├── setup_test_data.py      # Generate test data from constants
├── pyproject.toml          # Poetry configuration
└── README.md              # This file
```

## Development

### Running Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Setting Up Test Data

Generate test data from player constants:

```bash
python setup_test_data.py
```

This creates CSV files from the `TROUT16` constant, useful for CI/CD environments without web scraping.

### CI/CD

The project includes GitHub Actions workflows that:
- Cache Poetry dependencies for faster builds
- Generate test data from constants (no web scraping)
- Run the full test suite
- Execute sample simulations

## Requirements

- Python 3.11+
- Dependencies: numpy, pandas, beautifulsoup4, requests, tqdm

## License

MIT
