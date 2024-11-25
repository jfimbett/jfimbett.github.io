#%%
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import pandas as pd

url = "https://danielfeau.com/en/sales/paris-and%20exclusive-western-susburbs"

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}) 
assert response.status_code == 200, 'Failed to fetch page'

# For exploration, but let's use the html in file page_source.html 
# we will do this because the website has a lot of JS that is executed after the requets, making it invisible to the library. 
with open('page_source.html', 'r') as file:
    content = file.read()


soup = bs(content, 'html.parser')

# %%
# get all li with class property initial 
properties = soup.find_all('li', {'class': 'property initial'})

def retrieve_data_property(element):
    property_dict = {}

    # Extract image URL and alt text
    image_tag = element.find_all('img')
    if len(image_tag) > 0:
        image_tag = image_tag[0]
        property_dict['image_url'] = image_tag['src']
        property_dict['image_alt'] = image_tag['alt']

    # Extract property description
    property_desc_tag = element.find_all('h2')
    if len(property_desc_tag) > 0:
        property_desc_tag = property_desc_tag[0]
        property_dict['description'] = property_desc_tag.find_all('div')[0].text.strip()

    # Extract price
    price_tag = element.find_all('span', class_='price')
    if len(price_tag) > 0:
        price_tag = price_tag[0].text.strip()
        property_dict['price'] = price_tag
    

    # Extract property type, size, rooms, and bedrooms
    h3_tags = element.find_all('h3')
    if len(h3_tags) > 0:
        h3_tags = h3_tags[0].find_all('span')
        property_dict['type'] = h3_tags[0].text.strip()
        property_dict['size'] = h3_tags[1].text.strip()
        property_dict['rooms'] = h3_tags[2].text.strip()
        property_dict['bedrooms'] = h3_tags[3].text.strip()

    # Extract reference and additional comment
    comment_tag = element.find_all('p', class_='comment')
    if len(comment_tag) > 0:
        comment_tag = comment_tag[0]

        property_dict['reference'] = comment_tag.find_all('span', class_='reference')[0].text.strip()
        property_dict['comment'] = comment_tag.text.strip()

    # Extract property link
    link_tag = element.find_all('a', class_='allLink')
    if len(link_tag) > 0:
        property_dict['property_link'] = link_tag[0]['href']

    # dictionary to pandas row 
    return pd.DataFrame.from_dict(property_dict, orient='index').T


# test 
retrieve_data_property(properties[-1])
# %%
df = pd.DataFrame()
for i, property in tqdm(enumerate(properties), desc='Extracting data', total=len(properties)):
    df = pd.concat([df, retrieve_data_property(property)], ignore_index=True)


# save to csv
df.to_csv('properties.csv', index=False)
# %%
