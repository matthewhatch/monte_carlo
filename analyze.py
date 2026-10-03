import argparse
import duckdb
from src.monte_carlo.cli import main as mc

parser = argparse.ArgumentParser(description='Analyze player statistics from CSV files.')
parser.add_argument('--year', '-y', type=str, default='*', help='Season year for statistics. Default: *.')
parser.add_argument('--action', '-a', type=str, choices=['ingest', 'clean', 'get_all', 'drop'], required=True, help='Action to perform: ingest, clean, or get_all.')
args = parser.parse_args()
# read from data dir

# data = duckdb.read_csv(f'data/players_{args.year}.csv', filename=True).to_df()
# print(data.head())

def ingest():
    conn = duckdb.connect('data/players.db')

    conn.execute("""
        CREATE OR REPLACE TABLE telemetry_data AS 
            SELECT regexp_extract(filename, '\\d{4}', 0)::INTEGER AS year, 
            *,
            hash(concat_ws('||', *COLUMNS(*))) AS row_hash,
        FROM read_csv('data/*.csv', filename = true);
    """)

    df = conn.execute("SELECT * FROM telemetry_data").df()
    print(df)

    conn.close()

def clean():
    conn = duckdb.connect('data/players.db')

    conn.execute("""
        CREATE OR REPLACE TABLE cleaned_data AS
        SELECT * 
        FROM telemetry_data
        QUALIFY ROW_NUMBER() OVER (PARTITION BY row_hash ORDER BY year DESC) = 1;
    """)

    df = conn.execute("SELECT * FROM cleaned_data").df()
    print(df)

    conn.close()

def drop():
    conn = duckdb.connect('data/players.db')

    conn.execute("DROP TABLE IF EXISTS telemetry_data")
    conn.execute("DROP TABLE IF EXISTS cleaned_data")

    conn.close()

def get_all():
    conn = duckdb.connect('data/players.db')

    try:
        df = conn.execute("SELECT * FROM cleaned_data").df()
        print(df)
    except Exception as e:
        print(f"Error retrieving data: {e}")
    finally:
        print("Closing connection...")
        conn.close()

if args.action == 'ingest':
    ingest()
elif args.action == 'clean':
    clean()
elif args.action == 'get_all':
    get_all()
elif args.action == 'drop':
    drop()
else:
    print("Invalid action. Please choose 'ingest', 'clean', or 'get_all'.")