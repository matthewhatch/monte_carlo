# Monte Carlo Simulation: Runs Created Calculator — Documentation

Welcome to the full documentation for the **monte-carlo** package, a probabilistic baseball game simulator that calculates *Runs Created* for any MLB player in any year.

---

## Quick Start

```bash
pip install monte-carlo
monte-carlo -c 1000 --player 'Mike Trout' --year 2016
```

---

## Contents

### Guides

| Page | Description |
|------|-------------|
| [Installation](installation.md) | All install methods: pip, Poetry, from source, from GitHub |
| [Usage](usage.md) | CLI examples, Python module usage, expected output |
| [Architecture](architecture.md) | How the simulation works — game state, probability model, baserunning logic |
| [Data](data.md) | CSV cache format, web scraping, CI/CD data strategy |
| [Development](development.md) | Running tests, contributing, GitHub Actions CI/CD |

### API Reference

| Module | Description |
|--------|-------------|
| [cli](api/cli.md) | `simulate_inning`, `simulate_game`, `main` — entry points and simulation drivers |
| [Player](api/player.md) | `Player` class — probability model, at-bat simulation, output formatting |
| [events](api/events.md) | All baseball event functions — hits, outs, walks, errors with baserunner logic |
| [utils](api/utils.md) | `get_stats`, CSV helpers, web scraper — player data retrieval pipeline |
| [constants](api/constants.md) | Event type strings and pre-defined player stat dictionaries |

---

## Project Overview

The simulator models a single batter facing an infinite number of opposing players (i.e., a lineup of one). Each plate appearance outcome is drawn probabilistically from the player's historical statistics. The simulator:

1. Draws a plate appearance outcome (single, strikeout, home run, etc.) based on the player's real statistical rates.
2. Advances baserunners according to detailed baserunning rules.
3. Accumulates runs over 9 innings.
4. Averages runs across all simulated games to produce the **Runs Created** estimate.

This approach is inspired by the methodology described in *Mathletics* by Wayne Winston.

---

## Repository Structure

```
monte_carlo/
├── src/monte_carlo/
│   ├── cli.py              # CLI entry point & simulation drivers
│   ├── events.py           # Baseball event & baserunning logic
│   ├── classes/
│   │   └── Player.py       # Player probability model
│   ├── constants/
│   │   ├── events.py       # Event type string constants
│   │   └── players.py      # Pre-defined player stat dictionaries
│   └── utils/
│       ├── players.py      # Player data retrieval (CSV + web scraping)
│       └── combine_player_data.py  # Merge per-year CSV files
├── tests/                  # Unit tests (unittest)
├── data/                   # Cached player stats (CSV, git-ignored per year)
├── docs/                   # This documentation
├── main.py                 # Thin CLI wrapper script
├── setup_test_data.py      # Generate test CSV from constants (CI-friendly)
└── pyproject.toml          # Poetry project config
```
