#%%
import requests
from bs4 import BeautifulSoup as bs

url = 'https://coinmarketcap.com/'
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
assert response.status_code == 200, 'Failed to fetch page'

#%%

soup = bs(response.content, 'html.parser')

# get all tr tags
table = soup.find_all('tr')

# %%
information = []
for i, row in enumerate(table):
    # get all td tags
    columns = row.find_all('td')
    if not columns:
        continue
    # get the name of the cryptocurrency
    name = columns[2].text
    # get the price of the cryptocurrency
    price = columns[3].text
    # get the market cap of the cryptocurrency
    market_cap = columns[6].text
    # get the volume of the cryptocurrency
    volume = columns[7].text
    # get the circulating supply of the cryptocurrency
    circulating_supply = columns[5].text
    # get the change of the cryptocurrency
    change = columns[8].text
    information.append({
        'Name': name,
        'Price': price,
        'Market Cap': market_cap,
        'Volume': volume,
        'Circulating Supply': circulating_supply,
        'Change': change
    })

# %%
