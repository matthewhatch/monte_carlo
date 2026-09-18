# Data

## Overview

Player statistics are stored locally as CSV files in the `data/` directory. The simulator checks this cache first before attempting to scrape the web. This design makes the tool fast for repeated queries and CI/CD-safe.

---

## CSV Format

Each file is named `data/players_{year}.csv` (e.g., `data/players_2016.csv`).

### Columns

| Column | Type | Description |
|--------|------|-------------|
| `name` | str | Player's full name (lowercase, e.g., `mike trout`) |
| `plate_appearences` | int | Total plate appearances in the season |
| `at_bats` | int | Official at-bats |
| `errors` | int | Reached-on-error events |
| `outs` | int | Outs recorded (AB − hits − Ks − errors) |
| `strike_outs` | int | Strikeouts |
| `walks` | int | Base on balls |
| `hbp` | int | Hit by pitch |
| `singles` | int | Singles (hits − 2B − 3B − HR) |
| `doubles` | int | Doubles |
| `triples` | int | Triples |
| `home_runs` | int | Home runs |

### Example Row

```csv
name,plate_appearences,at_bats,errors,outs,strike_outs,walks,hbp,singles,doubles,triples,home_runs
mike trout,681,554,10,234,137,118,11,107,32,5,29
```

---

## Supported Years

CSV data is currently available (or can be generated) for:

- 2002–2005
- 2015–2018

> Any year available on baseball-reference.com can be scraped and cached.

---

## Generating Test Data from Constants

For CI/CD environments (or offline use), generate CSV data from the built-in `TROUT16` constant without any web scraping:

```bash
python setup_test_data.py
```

This creates `data/players_2016.csv` with Mike Trout's 2016 statistics. See [`constants/players.py`](api/constants.md) for the source values.

---

## Web Scraping

When a player is not found in the local cache and the environment is **not** CI (checked via the `CI` environment variable), the utility automatically scrapes [baseball-reference.com](https://www.baseball-reference.com).

### Process

1. **Name search** — `name_search(player_name)` visits `baseball-reference.com/players/{last_initial}` and finds the player's profile link.
2. **Stats fetch** — Fetches the player's game log page and parses the `<tfoot>` (season totals row) using BeautifulSoup.
3. **Stat derivation** — Computed values:
   - `singles = hits − doubles − triples − home_runs`
   - `errors = (PA − AB) − (sac_flies + sac_hits + HBP + BB)` if non-zero
   - `outs = AB − singles − doubles − triples − HR − strikeouts − errors`
4. **Cache write** — Results are appended to `data/players_{year}.csv` so the scraper is not needed again.

### Rate Limiting

If baseball-reference.com returns HTTP 429 (Too Many Requests), the scraper reads the `Retry-After` header, waits the indicated number of seconds plus 10, then retries automatically.

---

## Combining Per-Year CSV Files

To merge all per-year CSV files into a single file with a `year` column:

```bash
python -c "
import glob, pandas as pd
files = glob.glob('data/players_*.csv')
df = pd.concat([pd.read_csv(f).assign(year=f.split('.')[0].split('_')[-1]) for f in files])
df.to_csv('data/players_all.csv', index=False)
"
```

Or use the included utility script:

```bash
python src/monte_carlo/utils/combine_player_data.py
```

Output: `data/players_all.csv`
