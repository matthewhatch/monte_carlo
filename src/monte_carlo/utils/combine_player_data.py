"""Merge per-year player CSV files into a single combined file.

Reads all files matching ``data/players_*.csv``, adds a ``year`` column
derived from each filename, and writes the combined data to
``data/players_all.csv``.

Usage::

    python src/monte_carlo/utils/combine_player_data.py
"""

import os
import glob
import pandas as pd

files = glob.glob('data/players_*.csv')
df = pd.concat([pd.read_csv(f).assign(year=f.split('.')[0].split('_')[-1]) for f in files], ignore_index=True)
df.to_csv('data/players_all.csv', index=False)