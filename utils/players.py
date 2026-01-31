import requests
import pandas as pd
import os

from constants.players import TROUT16
from bs4 import BeautifulSoup
from time import sleep

def name_search(player_name):
    print(f'Searching for {player_name.title()} on baseball-reference.com')
    # find player link on baseball-reference.com, base on player name
    split_name = player_name.split(' ')
    first_name = split_name[0].lower()
    last_name = split_name[1].lower()
    last_name_first_initial = last_name[0].lower()
    url = f'https://www.baseball-reference.com/players/{last_name_first_initial}'
    try:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
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
    # Get Player stats from CSV
    # if file exists, get the player stats from the CSV
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
    print(f'Getting stats for {player_name}')
    # Get Player stats from https://www.baseball-reference.com
    # https://www.baseball-reference.com/players/gl.fcgi?id=troutmi01&t=b&year=2013
    split_name = player_name.split(' ')
    first_name = split_name[0].lower()
    last_name = split_name[1].lower()

    # Get the player stats from CSV
    player = _get_from_csv(player_name, year)
    if player is not None:
        return player

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
