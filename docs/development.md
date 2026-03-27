# Development

## Setting Up the Development Environment

```bash
git clone git@github.com:matthewhatch/monte_carlo.git
cd monte_carlo

python -m venv env
source env/bin/activate    # macOS / Linux
# env\Scripts\activate     # Windows

pip install -e .
```

---

## Running the Test Suite

Tests use Python's built-in `unittest` framework.

```bash
# Discover and run all tests with verbose output
python -m unittest discover -s tests -p "test_*.py" -v
```

### Test Modules

| File | What it covers |
|------|---------------|
| `test_cli.py` | `simulate_inning`, `simulate_game`, CLI argument parsing |
| `test_player_integration.py` | Full `Player` instantiation and `simulate_ab` integration |
| `test_data_utils.py` | CSV lookup and player data utilities |
| `test_error.py` | `error()` event function |
| `test_free_pass.py` | `free_pass()` event (walks + HBP) |
| `test_ground_out.py` | `ground_out()` and `gidp()` events |
| `test_long_double.py` | `long_double()` event |
| `test_long_single.py` | `long_single()` event |
| `test_medium_single.py` | `medium_single()` event |
| `test_short_double.py` | `short_double()` event |
| `test_short_single.py` | `short_single()` event |
| `test_strike_out.py` | `strike_out()` event |

---

## Generating Test Data

The CI/CD pipeline requires test data without web scraping. Generate it from the built-in `TROUT16` constant:

```bash
python setup_test_data.py
```

This writes `data/players_2016.csv`. Commit this file if you need it checked into the repo for other contributors.

---

## GitHub Actions CI/CD

The project includes a GitHub Actions workflow (`.github/`) that:

1. **Caches Poetry dependencies** for faster builds.
2. **Generates test data** via `setup_test_data.py` (no web scraping required).
3. **Runs the full test suite** with `python -m unittest discover`.
4. **Executes a sample simulation** to verify end-to-end functionality.

### CI Environment Flag

The `CI` environment variable is set automatically by GitHub Actions. The `get_stats` utility checks for this flag and raises an exception instead of attempting web scraping:

```python
IS_CI = os.getenv('CI') is not None
```

This ensures deterministic, fast, and network-free CI runs.

---

## Project Dependencies

Managed with [Poetry](https://python-poetry.org/). See `pyproject.toml` for the full dependency list.

| Package | Purpose |
|---------|---------|
| `numpy` | Probabilistic outcome sampling (`numpy.random.choice`) |
| `pandas` | CSV I/O and player data manipulation |
| `beautifulsoup4` | HTML parsing for web scraper |
| `requests` | HTTP client for baseball-reference.com scraper |
| `tqdm` | Progress bar for simulation loop |

To add a dependency:

```bash
poetry add <package>
```

To install all dependencies:

```bash
poetry install
```

---

## Contributing

1. Fork the repository and create a feature branch.
2. Make your changes with tests.
3. Run `python -m unittest discover -s tests -p "test_*.py" -v` and ensure all tests pass.
4. Submit a pull request with a clear description of the change.
