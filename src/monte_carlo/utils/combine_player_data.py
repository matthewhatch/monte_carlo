import os
import glob
import pandas as pd

files = glob.glob('data/players_*.csv')
df = pd.concat([pd.read_csv(f).assign(year=f.split('.')[0].split('_')[-1]) for f in files], ignore_index=True)
df.to_csv('data/players_all.csv', index=False)