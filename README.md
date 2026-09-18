# Monte Carlo Simulation: Runs Created Calculator

A probabilistic baseball game simulator that estimates **Runs Created** for any MLB player in any season.
Inspired by *Mathletics* by Wayne Winston.

## Quick Start

```bash
pip install monte-carlo
monte-carlo -c 1000 --player 'Mike Trout' --year 2016
```

## Documentation

📖 **[Full Documentation →](docs/index.md)**

| | |
|--|--|
| [Installation](docs/installation.md) | pip, Poetry, from source, from GitHub |
| [Usage](docs/usage.md) | CLI options, Python module examples |
| [Architecture](docs/architecture.md) | Simulation model, game state, probability design |
| [Data](docs/data.md) | CSV cache, web scraping, CI/CD strategy |
| [Development](docs/development.md) | Tests, contributing, GitHub Actions |
| [API Reference](docs/api/) | Full API docs for every module |

## Requirements

- Python 3.11+
- Dependencies: `numpy`, `pandas`, `beautifulsoup4`, `requests`, `tqdm`

## License

MIT

