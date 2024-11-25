#%%
import requests
import openai
import os
import json
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
url = "https://econjobmarket.org/positions"

# identify the maximum number of pages

max_pages = input("How many pages do you want to scrape? ")
max_pages = int(max_pages)

base_url = "https://econjobmarket.org/positions?page="

url = base_url + '1'

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = bs(response.content, 'html.parser')

# all div with class panel
panels = soup.find_all('div', class_='panel panel-primary')