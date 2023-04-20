#%%
import requests
from bs4 import BeautifulSoup

# List of SSRN URLs to scrape
urls = ['https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4422754',
        'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3622433',
        'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3719169',
        'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3711536']

# Empty list to store paper details
papers = []

# Loop through each URL and scrape paper details
for url in urls:
    # Make a GET request to the SSRN URL
    # but use headers
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        continue
    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract paper details from the HTML
    title = soup.find_all('h1')[0].text.strip()
    
    # get firs thte div with class authors authors-full-width
    authors = [author.text.strip() for author in soup.find_all('div', class_='authors authors-full-width')[0].find_all('h2')]
  
    abstract = soup.find_all('div', class_='abstract-text')[0].text.strip()

    # Add paper details to the list
    papers.append({
        'title': title,
        'authors': authors,
        'abstract': abstract,
        'url': url
    })

#%%
# generate HTML for papers, justify the abstract, include the url as a hyperlink in the title
# and bold the author Juan Felipe Imbet 

# first in the authors, bold Juan Felipe Imbet
for paper in papers:
    for i, author in enumerate(paper['authors']):
        if author == 'Juan Felipe Imbet':
            paper['authors'][i] = f'<b>{author}</b>'

# in the abstract, bold the word Abstract
for paper in papers:
    paper['abstract'] = paper['abstract'].replace('Abstract', '<b>Abstract:</b>')

papers_html = ""
for paper in papers:
    papers_html += f"<h3><a href='{paper['url']}'>{paper['title']}</a></h3><p>{', '.join(paper['authors'])}</p><p style='text-align: justify;'>{paper['abstract']}</p>"

# Read existing HTML file
with open('../research_base.html', 'r') as f:
    html = f.read()

# Insert generated HTML after placeholder comment
html = html.replace('<!-- INSERT PAPERS HERE -->', papers_html)

# Write updated HTML back to file
with open('../research.html', 'w') as f:
    f.write(html)

# %%
