#%%
import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.imdb.com/chart/top'
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
assert response.status_code == 200, 'Failed to fetch page'

soup = bs(response.content, 'html.parser')
movies = soup.find_all('div', class_='ipc-metadata-list-summary-item__tc')
for movie in movies:
    title = movie.find('a').text
    rating = movie.find('span').text
    print(f'{title}: {rating}')
# %%
