"""
crypto_data.py - Obtains cryptocurrency data

Author: J.F. Imbet <juan.imbet@dauphine.psl.eu>

Date: May 30, 2021

Version: 0.1.1

Usage:
    python crypto_data.py [options]

Options:
    --verbose   Prints detailed progress information.

Description:
    This program downloads historical data for cryptocurrencies from CoinMarketCap and saves it as Parquet files.

Requirements:
    - Python 3.9 or higher
    - pandas
    - numpy
    - requests
    - tqdm
    - beautifulsoup4

Example usage:
    python crypto_data.py --verbose
"""
#%%
import os
import time
import datetime
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import pandas as pd 
import argparse
import logging
logging.basicConfig(level=logging.INFO)

def timing_minutes(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Execution time: {round((end - start) / 60, 2)} minutes")
        return result
    return wrapper

PATH_TO_DATA = os.environ['PATH_TO_DATA']
# copy paste a path here if you don't have the environment variable set
# PATH_TO_DATA = 'path/to/data'




@timing_minutes
def download_all_crypto(verbose=False, max_coins = 100):
    # Get the maximum page ID
    base_url = "https://coinmarketcap.com/coins/"
    response = requests.get(base_url)
    soup = bs(response.text, 'html.parser')
    pages = soup.find_all('li', {'class': 'page'})
    last = int(pages[-1].find('a').text)

    # Build a dictionary of available currencies
    info = {}
    for k in tqdm(range(1, last + 1), desc="Exploring pages", disable=not verbose):
        url = f"{base_url}?page={k}"
        r = requests.get(url)
        soup = bs(r.text, 'html.parser')
        rows = soup.find_all('table')[0].find_all('tbody')[0].find_all('tr')

        for row in rows:
            url_ = row.find_all('a')[0]['href']
            info[url_[12:-1]] = url_

    # Download historical data for each currency
    base_url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical"
    before = int(time.mktime(datetime.date(2010,1,1).timetuple()))
    today = int(time.time())

    # keep only the first max_coins
    info = {k: v for i, (k, v) in enumerate(info.items()) if i < max_coins}

    failed = 0
    for id, symbol in tqdm(info.items(), desc="Downloading data", disable=not verbose):
        url = f"{base_url}?id={id}&convertId=2781&timeStart={before}&timeEnd={today}"
        r = requests.get(url)
        result = r.json()
        try:
            df = pd.DataFrame()
            name = result['data']['name']
            for row in result['data']['quotes']:
                temp = row['quote']
                temp = {k: [temp[k]] for k in temp.keys()}
                temp['name'] = [name]
                temp['symbol'] = [symbol]
                df = pd.concat([df, pd.DataFrame.from_dict(temp)])

            df.to_parquet(os.path.join(PATH_TO_DATA, f"crypto/{symbol}.parquet"))
        except:
            failed += 1
        
    print(f"{failed} - currencies not found")

#%%
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Obtains cryptocurrency data')
    parser.add_argument('--verbose', action='store_true', help='Prints detailed progress information.')
    args = parser.parse_args()

    # display where the data will be saved
    logging.info("Running crypto_data.py")
    logging.info(f"Data will be saved in {PATH_TO_DATA}")

    download_all_crypto(args.verbose)
    