# API Reference — `monte_carlo.cli`

Module: `src/monte_carlo/cli.py`

CLI entry point and simulation driver functions.

---

## Functions

### `simulate_inning(player)`

Simulates a single baseball inning for the given player.

Repeatedly calls `player.simulate_ab()` until 3 outs are recorded.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `player` | `Player` | An instantiated `Player` object |

**Returns:** `int` — Total runs scored in the inning (≥ 0).

**Example:**

```python
from monte_carlo.classes.Player import Player
from monte_carlo.constants.players import TROUT16
from monte_carlo.cli import simulate_inning

player = Player(**TROUT16)
runs = simulate_inning(player)
print(runs)  # e.g., 1
```

---

### `simulate_game(player)`

Simulates a complete 9-inning baseball game for the given player.

Calls `simulate_inning()` nine times and sums the results.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `player` | `Player` | An instantiated `Player` object |

**Returns:** `int` — Total runs scored across all 9 innings.

**Example:**

```python
from monte_carlo.classes.Player import Player
from monte_carlo.constants.players import TROUT16
from monte_carlo.cli import simulate_game

player = Player(**TROUT16)
runs = simulate_game(player)
print(runs)  # e.g., 7
```

---

### `main()`

CLI entry point registered as the `monte-carlo` console script.

Parses command-line arguments, retrieves player statistics, runs simulations, and prints the results.

**CLI Arguments:**

| Flag | Short | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--count` | `-c` | int | `1000` | Number of game simulations to run |
| `--player` | `-p` | str | `'Mike Trout'` | Player name (case-insensitive) |
| `--year` | `-y` | str | `'2016'` | Season year |
| `--verbose` | `-v` | flag | `False` | Print per-game run output |

**Raises:** `Exception` if the player is not found in cache or on baseball-reference.com.

**Side effects:** Calls `player.runs_created(average_runs)` to store the result, then prints the player summary via `str(player)`.

**Example:**

```bash
monte-carlo -c 500 -p 'David Ortiz' -y 2015
```
