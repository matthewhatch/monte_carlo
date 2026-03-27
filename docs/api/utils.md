# API Reference — `monte_carlo.utils`

## Module: `monte_carlo.utils.players`

`src/monte_carlo/utils/players.py`

Player data retrieval pipeline: checks local CSV cache first, then falls back to web scraping baseball-reference.com.

---

### `get_stats(player_name, year)`

Primary entry point for retrieving a player's season statistics.

Checks the local CSV cache (`data/players_{year}.csv`) first. If not found and the environment is not CI, scrapes baseball-reference.com and caches the result.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `player_name` | str | Full player name, **lowercase** (e.g., `'mike trout'`) |
| `year` | str | Four-digit season year (e.g., `'2016'`) |

**Returns:** `dict | None` — Stats dictionary with these keys:

```python
{
    "plate_appearences": int,
    "at_bats": int,
    "errors": int,
    "outs": int,
    "strike_outs": int,
    "walks": int,
    "hbp": int,
    "singles": int,
    "doubles": int,
    "triples": int,
    "home_runs": int
}
```

Returns `None` if the player is not found and scraping is unavailable.

**Raises:**
- `Exception` if in CI environment and player not in cache.
- `Exception` if player not found on baseball-reference.com.
- Re-raises scraping exceptions on parse failure.

**Example:**

```python
from monte_carlo.utils.players import get_stats

stats = get_stats('mike trout', '2016')
print(stats['home_runs'])  # 29
```

---

### `_get_from_csv(player_name, year)`

Private helper. Reads `data/players_{year}.csv` and returns the row matching `player_name`.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `player_name` | str | Lowercase player name |
| `year` | str | Season year |

**Returns:** `dict | None` — Stats dict (without `name` column) if found; `None` if the file doesn't exist or the player isn't in it.

---

### `name_search(player_name)`

Searches baseball-reference.com for a player's unique profile ID.

Visits `https://www.baseball-reference.com/players/{last_initial}` and finds the matching anchor tag.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `player_name` | str | Lowercase full name (e.g., `'mike trout'`) |

**Returns:** `str | None` — The player's baseball-reference ID (e.g., `'troutmi01'`); `None` if not found.

**Raises:** Re-raises any network or parsing exceptions.

---

### `create_csv_from_constant(player_name, year, stats_dict)`

Creates or appends to a CSV file from a stats dictionary (no web scraping needed).

Useful for generating test/CI data from the pre-defined player constants.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `player_name` | str | Lowercase player name (added as `name` column) |
| `year` | str | Season year (used in filename `data/players_{year}.csv`) |
| `stats_dict` | dict | Stats dictionary matching the CSV column schema |

**Side effects:** Creates `data/players_{year}.csv` if it doesn't exist; otherwise appends a row.

**Example:**

```python
from monte_carlo.utils.players import create_csv_from_constant
from monte_carlo.constants.players import TROUT16

create_csv_from_constant('mike trout', '2016', TROUT16)
# Created data/players_2016.csv
```

---

## Module: `monte_carlo.utils.combine_player_data`

`src/monte_carlo/utils/combine_player_data.py`

Script that merges all per-year CSV files into a single combined file.

### Usage

```bash
python src/monte_carlo/utils/combine_player_data.py
```

**Reads:** All files matching `data/players_*.csv`

**Writes:** `data/players_all.csv` with an added `year` column derived from the filename.

### Output schema

All columns from the per-year CSVs plus:

| Column | Type | Description |
|--------|------|-------------|
| `year` | str | Season year extracted from the source filename |
