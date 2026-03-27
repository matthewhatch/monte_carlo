"""Player data retrieval utilities.

Provides a two-stage lookup pipeline:

1. Check the local CSV cache at ``data/players_{year}.csv``.
2. If not found and not running in a CI/CD environment, scrape
   `baseball-reference.com <https://www.baseball-reference.com>`_ and cache
   the result for future use.

Set the ``CI`` environment variable to any non-empty value to disable web
scraping (GitHub Actions sets this automatically).
"""

import requests
import pandas as pd
import os

from ..constants.players import TROUT16
from bs4 import BeautifulSoup
from time import sleep

# Check if running in CI/CD environment
IS_CI = os.getenv('CI') is not None

def create_csv_from_constant(player_name, year, stats_dict):
    """Create or append to a per-year CSV from a stats dictionary.

    Useful for generating test/CI data from the pre-defined player constants
    without any web scraping.

    Args:
        player_name (str): Lowercase player name (e.g. ``'mike trout'``).
            Added as the ``name`` column.
        year (str): Four-digit season year used in the filename
            ``data/players_{year}.csv``.
        stats_dict (dict): Stats dictionary matching the CSV column schema.

    Side effects:
        Creates ``data/players_{year}.csv`` if it does not exist; otherwise
        appends a row without writing the header again.
    """
    stats_dict['name'] = player_name.lower()
    columns_order = ['name'] + [col for col in stats_dict if col != 'name']
    df = pd.DataFrame(stats_dict, index=[0])[columns_order]
    
    csv_path = f'data/players_{year}.csv'
    if not os.path.isfile(csv_path):
        df.to_csv(csv_path, index=False)
        print(f'Created {csv_path}')
    else:
        df.to_csv(csv_path, mode='a', header=False, index=False)
        print(f'Appended to {csv_path}')

def name_search(player_name):
    """Search baseball-reference.com for a player's unique profile ID.

    Visits ``https://www.baseball-reference.com/players/{last_initial}`` and
    finds the anchor tag matching the player's full name.

    Args:
        player_name (str): Lowercase full player name (e.g. ``'mike trout'``).

    Returns:
        str | None: The player's baseball-reference ID (e.g. ``'troutmi01'``);
        ``None`` if the player is not found on the page.

    Raises:
        Exception: Re-raises any network or parsing exception encountered
            during the HTTP request.
    """
    # find player link on baseball-reference.com, base on player name
    split_name = player_name.split(' ')
    first_name = split_name[0].lower()
    last_name = split_name[1].lower()
    last_name_first_initial = last_name[0].lower()
    url = f'https://www.baseball-reference.com/players/{last_name_first_initial}'
    try:
        print(f'Getting page from {url}')
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        print(f'Page status code: {page.status_code}')
        soup = BeautifulSoup(page.content, 'html.parser')
        player = soup.find('a', text=player_name.title())
    except Exception as e:
        raise e

    if player is not None:
        print(f'Found {player_name} on baseball-reference.com')
        href = player['href']
        player_id = href.split('/')[3].split('.')[0]
        return player_id
    return None

def _get_from_csv(player_name, year):
    """Read player stats from the local CSV cache.

    Args:
        player_name (str): Lowercase player name.
        year (str): Four-digit season year.

    Returns:
        dict | None: Stats dictionary (without the ``name`` column) if the
        player is found; ``None`` if the file does not exist or the player
        is not present.
    """
    if os.path.isfile(f'data/players_{year}.csv'):
        df = pd.read_csv(f'data/players_{year}.csv')
        player = df[(df['name'] == player_name.lower())]
        if player.empty:
            return None
        else:
            # remove name column
            print(f'Getting stats for {player_name} from CSV')
            player = player.drop(columns=['name'])

            return player.to_dict(orient='records')[0]
    else:
        return None

def get_stats(player_name, year):
    """Retrieve a player's seasonal statistics.

    Checks the local CSV cache first.  If not found and the environment is not
    CI, scrapes baseball-reference.com, caches the result, and returns it.

    Args:
        player_name (str): Lowercase full player name (e.g. ``'mike trout'``).
        year (str): Four-digit season year (e.g. ``'2016'``).

    Returns:
        dict | None: Stats dictionary with keys:
        ``plate_appearences``, ``at_bats``, ``errors``, ``outs``,
        ``strike_outs``, ``walks``, ``hbp``, ``singles``, ``doubles``,
        ``triples``, ``home_runs``.  Returns ``None`` if the player is not
        found and scraping is unavailable.

    Raises:
        Exception: If running in CI and the player is not in the local cache.
        Exception: If the player is not found on baseball-reference.com.
        Exception: Re-raises scraping/parsing exceptions on failure.
    """
    # https://www.baseball-reference.com/players/gl.fcgi?id=troutmi01&t=b&year=2013
    split_name = player_name.split(' ')
    first_name = split_name[0].lower()
    last_name = split_name[1].lower()

    # Get the player stats from CSV
    player = _get_from_csv(player_name, year)
    if player is not None:
        return player

    # Skip web scraping in CI/CD environments
    if IS_CI:
        raise Exception(f'Player {player_name.title()} not found in cached data for {year}. Web scraping is disabled in CI/CD environments.')

    print(f'{player_name.title()} not cached for {year}, let the scraping begin')
    # if the player is not in the CSV, get the stats from the website
    player_link = name_search(player_name)
    if player_link is None:
        raise Exception(f'Player {player_name.title()} not found on baseball-reference.com')
        return None
    else:
        url = f'https://www.baseball-reference.com/players/gl.fcgi?id={player_link}&t=b&year={year}'

    print(f'Getting stats from {url}')
    
    # Get the page, randomize the user agent
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    if page.status_code == 429:
        print('Error: 429 - Too Many Requests')
        # wait based on Retry-After header
        retry_after = page.headers['Retry-After']
        print(f'Retrying after {str(retry_after)} seconds')

        sleep(int(int(retry_after) + 10))
        return get_stats(player_name, year)
    else:
        soup = BeautifulSoup(page.content, 'html.parser')
        
        try:
             # Get tfoot tag
            tfoot = soup.find('tfoot')

            # Get plate appearences using data-stat attribute
            plate_appearences = tfoot.find('td', {'data-stat': 'b_pa'}).text
            at_bats = tfoot.find('td', {'data-stat': 'b_ab'}).text
            # errors = tfoot.find('td', {'data-stat': 'ROE'}).text
            strike_outs = tfoot.find('td', {'data-stat': 'b_so'}).text
            walks = tfoot.find('td', {'data-stat': 'b_bb'}).text
            hbp = tfoot.find('td', {'data-stat': 'b_hbp'}).text
            sac_flies = tfoot.find('td', {'data-stat': 'b_sf'}).text
            sac_hits = tfoot.find('td', {'data-stat': 'b_sh'}).text
            hits = tfoot.find('td', {'data-stat': 'b_h'}).text
            doubles = tfoot.find('td', {'data-stat': 'b_doubles'}).text
            triples = tfoot.find('td', {'data-stat': 'b_triples'}).text
            home_runs = tfoot.find('td', {'data-stat': 'b_hr'}).text

            # calculate singles
            singles = int(hits) - int(doubles) - int(triples) - int(home_runs)

            # calculate errors
            ab_pa_diff = int(plate_appearences) - int(at_bats)
            sac_hbp_bb_total = int(sac_flies) + int(sac_hits) + int(hbp) + int(walks)
            if ab_pa_diff != sac_hbp_bb_total:
                errors = ab_pa_diff - sac_hbp_bb_total
            else:
                errors = 0

            # calculate outs, based on AB - Singles - Doubles - Triples - Home Runs - Strike Outs - Errors
            outs = int(at_bats) - int(singles) - int(doubles) - int(triples) - int(home_runs) - int(strike_outs) - int(errors)
            
            results = {
                "plate_appearences": int(plate_appearences),
                "at_bats": int(at_bats),
                "errors": int(errors),
                "outs": outs,
                "strike_outs": int(strike_outs),
                "walks":  int(walks),
                "hbp": int(hbp),
                "singles": int(singles),
                "doubles": int(doubles),
                "triples": int(triples),
                "home_runs": int(home_runs)
            }

            # append line to csv with data in the order of the columns, adding the name first
            results['name'] = player_name.lower()

            # Ensure 'name' is the first column
            columns_order = ['name'] + [col for col in results if col != 'name']
            df = pd.DataFrame(results, index=[0])[columns_order]

            # file does not exist, create it
            if not os.path.isfile(f'data/players_{year}.csv'):
                df.to_csv(f'data/players_{year}.csv', index=False)
            else:
                # file exists, append without writing the header
                df.to_csv(f'data/players_{year}.csv', mode='a', header=False, index=False)

            # remove name from results
            results.pop('name')
            return results
        
        except Exception as e:
            print(f'Error getting stats for {player_name.title()}: {e}')
            print(f'Data for {player_name.title()} not found for {year}')
            raise e
            return None
