# Installation

## Requirements

- Python 3.11 or later
- Dependencies (installed automatically): `numpy`, `pandas`, `beautifulsoup4`, `requests`, `tqdm`

---

## Option 1 — pip (recommended for users)

```bash
pip install monte-carlo
```

---

## Option 2 — From Source (recommended for development)

```bash
# Clone the repository
git clone git@github.com:matthewhatch/monte_carlo.git
cd monte_carlo

# Create and activate a virtual environment
python -m venv env
source env/bin/activate       # macOS / Linux
# env\Scripts\activate        # Windows

# Install in editable mode (changes to source are reflected immediately)
pip install -e .
```

---

## Option 3 — Directly from GitHub

Install the latest version from the `main` branch without cloning:

```bash
pip install git+https://github.com/matthewhatch/monte_carlo.git
```

Install from a specific branch:

```bash
pip install git+https://github.com/matthewhatch/monte_carlo.git@feature/module
```

Install in editable mode from GitHub:

```bash
pip install -e git+https://github.com/matthewhatch/monte_carlo.git#egg=monte-carlo
```

---

## Option 4 — Poetry

Add to an existing Poetry project:

```bash
poetry add git+https://github.com/matthewhatch/monte_carlo.git
```

Or declare it in `pyproject.toml`:

```toml
[tool.poetry.dependencies]
monte-carlo = {git = "https://github.com/matthewhatch/monte_carlo.git", branch = "main"}
```

Then run:

```bash
poetry install
```

---

## Option 5 — requirements.txt

```
monte-carlo @ git+https://github.com/matthewhatch/monte_carlo.git
```

Then:

```bash
pip install -r requirements.txt
```

---

## Verifying the Installation

```bash
monte-carlo --help
```

Expected output:

```
usage: monte-carlo [-h] [--count COUNT] [--verbose] [--player PLAYER] [--year YEAR]

Monte Carlo Simulator for MLB player performance
...
```
