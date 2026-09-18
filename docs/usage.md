# Usage

## Command Line Interface

After [installation](installation.md), use the `monte-carlo` command:

```bash
monte-carlo [OPTIONS]
```

### Options

| Flag | Short | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--count` | `-c` | int | `1000` | Number of full-game simulations to run |
| `--player` | `-p` | str | `'Mike Trout'` | Player name to look up (case-insensitive) |
| `--year` | `-y` | str | `'2016'` | Season year for statistics |
| `--verbose` | `-v` | flag | off | Print runs scored for each simulated game |

### Examples

```bash
# Run 1000 simulations for Mike Trout's 2016 season (default)
monte-carlo

# Run 100 simulations
monte-carlo -c 100 --player 'Mike Trout' --year 2016

# Use a different player and year
monte-carlo -c 500 --player 'David Ortiz' --year 2015

# Show per-game run output
monte-carlo -c 50 --player 'Babe Ruth' --year 2018 --verbose

# Short flags
monte-carlo -c 500 -p 'David Ortiz' -y 2015 -v
```

### Sample Output

```
Getting stats for mike trout
Getting stats for Mike Trout from CSV
100%|████████████████████| 1000/1000 [00:03<00:00, 310.45it/s]
 plate_appearences  at_bats  errors  outs  strike_outs  walks  hbp  singles  doubles  triples  home_runs  runs_created
               681      554      10   234          137    118   11      107       32        5         29          7.32
```

> **Note:** If the player is not found in the local CSV cache, the simulator will attempt to scrape stats from [baseball-reference.com](https://www.baseball-reference.com). Web scraping is disabled in CI/CD environments.

---

## Wrapper Script

Alternatively, run via the included wrapper script (no install needed):

```bash
python main.py -c 100 --player 'Mike Trout' --year 2016
```

---

## Python Module

Import and use the package programmatically:

```python
from monte_carlo.utils.players import get_stats
from monte_carlo.classes.Player import Player
from monte_carlo.cli import simulate_game, simulate_inning

# Retrieve player statistics (from CSV cache or web scraping)
stats = get_stats('mike trout', '2016')

# Instantiate a Player with the retrieved stats
player = Player(**stats)

# Simulate a single inning and get runs scored
inning_runs = simulate_inning(player)

# Simulate a full 9-inning game
game_runs = simulate_game(player)

# Run many simulations and compute average Runs Created
n = 1000
total = sum(simulate_game(player) for _ in range(n))
runs_created = total / n
print(f"Estimated Runs Created: {runs_created:.2f}")
```

### Using a Pre-defined Player Constant

No CSV or network access needed:

```python
from monte_carlo.classes.Player import Player
from monte_carlo.constants.players import TROUT16
from monte_carlo.cli import simulate_game

player = Player(**TROUT16)

n = 500
runs_created = sum(simulate_game(player) for _ in range(n)) / n
print(f"Estimated Runs Created: {runs_created:.2f}")
```

### Inspecting the Player Object

```python
from monte_carlo.classes.Player import Player
from monte_carlo.constants.players import TROUT16

player = Player(**TROUT16)
print(player)
# Prints a DataFrame-formatted table of raw stats (probability columns are hidden)
```
