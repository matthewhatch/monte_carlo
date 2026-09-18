# API Reference — `monte_carlo.classes.Player`

Module: `src/monte_carlo/classes/Player.py`

The `Player` class models a single batter's probability distribution over plate appearance outcomes and drives the at-bat simulation.

---

## Class `Player`

### Constructor

```python
Player(
    plate_appearences,
    at_bats,
    errors,
    outs,
    strike_outs,
    walks,
    hbp,
    singles,
    doubles,
    triples,
    home_runs
)
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `plate_appearences` | int | Total plate appearances in the season |
| `at_bats` | int | Official at-bats |
| `errors` | int | Times reached on error |
| `outs` | int | Outs recorded (not including strikeouts) |
| `strike_outs` | int | Strikeouts |
| `walks` | int | Base on balls |
| `hbp` | int | Hit by pitch |
| `singles` | int | Singles |
| `doubles` | int | Doubles |
| `triples` | int | Triples |
| `home_runs` | int | Home runs |

Each raw count is stored alongside a derived probability attribute (`p_<stat>`) computed as `count / plate_appearences`.

**Example:**

```python
from monte_carlo.classes.Player import Player
from monte_carlo.constants.players import TROUT16

player = Player(**TROUT16)
print(player.p_home_run)  # 0.0426...
```

---

### Methods

#### `normalize_probabilites(probabilities)`

Normalizes a list of probabilities so they sum to exactly 1.0.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `probabilities` | list[float] | Raw probability values |

**Returns:** `list[float]` — Normalized probabilities.

> Called internally before each `numpy.random.choice` call to guard against floating-point drift.

---

#### `simulate_ab(current_state)`

Simulates a single plate appearance and updates the game state.

Draws an outcome from the player's probability distribution, then delegates to the appropriate event function in `events.py`.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `current_state` | list[int] | `[outs, runner_1st, runner_2nd, runner_3rd]` |

**Returns:** `tuple[list[int], int]` — `(new_state, runs_scored)`

- `new_state`: Updated `[outs, runner_1st, runner_2nd, runner_3rd]`
- `runs_scored`: Number of runs scored on this plate appearance

**Possible outcomes and their event functions:**

| Outcome | Handler |
|---------|---------|
| `HOME_RUN` | `events.home_run()` |
| `TRIPLE` | `events.triple()` |
| `DOUBLE` | `events.double()` |
| `SINGLE` | `events.single()` |
| `BB` or `HBP` | `events.free_pass()` |
| `ERROR` | `events.error()` |
| `K` | `events.strike_out()` |
| `OUT` | `events.out_in_play()` |

**Example:**

```python
state = [0, 0, 0, 0]  # 0 outs, bases empty
new_state, runs = player.simulate_ab(state)
print(new_state, runs)  # e.g., [0, 1, 0, 0], 0  (single, runner on 1st)
```

---

#### `runs_created(rc)`

Stores the computed Runs Created value on the player instance.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `rc` | float \| None | Average runs per game from simulation; pass `None` to read the current value |

**Returns:** The stored `runs_created` value if `rc` is `None`; otherwise `None` (sets the value).

---

#### `__str__()`

Returns a formatted string representation of the player's raw statistics (probability columns are excluded).

Uses `pandas.DataFrame` for tabular formatting.

**Returns:** `str` — A single-row table with all non-probability stat columns.

**Example:**

```python
print(player)
#  plate_appearences  at_bats  errors  outs  ...  runs_created
#               681      554      10   234  ...          7.32
```
