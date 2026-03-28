# API Reference — `monte_carlo.constants`

---

## Module: `monte_carlo.constants.events`

`src/monte_carlo/constants/events.py`

String constants representing all plate appearance outcome types used throughout the simulation. Imported with `from .constants.events import *`.

### Primary Outcome Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `HOME_RUN` | `'HOME_RUN'` | Home run |
| `TRIPLE` | `'TRIPLE'` | Triple |
| `DOUBLE` | `'DOUBLE'` | Double |
| `SINGLE` | `'SINGLE'` | Single |
| `BB` | `'WALK'` | Base on balls (walk) |
| `HBP` | `'HBP'` | Hit by pitch |
| `K` | `'STRIKE_OUT'` | Strikeout |
| `OUT` | `'OUT'` | Out in play (ground, line, or fly) |
| `ERROR` | `'ERROR'` | Reached on error |

### Single Sub-type Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `SHORT_SINGLE` | `'SHORT_SINGLE'` | Batter and runners advance 1 base |
| `MEDIUM_SINGLE` | `'MEDIUM_SINGLE'` | Runners on 2nd/3rd score; batter to 1st |
| `LONG_SINGLE` | `'LONG_SINGLE'` | Runners on 2nd/3rd score; runner on 1st to 3rd |

### Double Sub-type Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `SHORT_DOUBLE` | `'SHORT_DOUBLE'` | Batter to 2nd; runner on 1st to 3rd; others score |
| `LONG_DOUBLE` | `'LONG_DOUBLE'` | Batter to 2nd; all runners score |

### Out Sub-type Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `GROUND_OUT` | `'GROUND_OUT'` | Ground ball out |
| `LINE_OUT` | `'LINE_OUT'` | Line drive out |
| `FLY_OUT` | `'FLY_OUT'` | Fly ball out |
| `GIDP` | `'GIDP'` | Ground into double play |
| `SHORT_FLY` | `'SHORT_FLY'` | Short fly — no runner advancement |
| `MEDIUM_FLY` | `'MEDIUM_FLY'` | Medium fly — sac fly possible |
| `LONG_FLY` | `'LONG_FLY'` | Long fly — sac fly + runner advancement |

---

## Module: `monte_carlo.constants.players`

`src/monte_carlo/constants/players.py`

Pre-defined player stat dictionaries for use without CSV files or web scraping. Used by `setup_test_data.py` and in tests.

### `TROUT16`

Mike Trout's 2016 season statistics.

```python
TROUT16 = {
    "plate_appearences": 681,
    "at_bats": 554,
    "errors": 10,
    "outs": 234,
    "strike_outs": 137,
    "walks": 118,
    "hbp": 11,
    "singles": 107,
    "doubles": 32,
    "triples": 5,
    "home_runs": 29
}
```

**Usage:**

```python
from monte_carlo.constants.players import TROUT16
from monte_carlo.classes.Player import Player

player = Player(**TROUT16)
```

> To add a new player constant, append a new dict following the same schema. All values must be integers and `plate_appearences` must be non-zero.
