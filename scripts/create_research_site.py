#%%
import requests
from bs4 import BeautifulSoup

# List of SSRN URLs to scrape
urls = ['https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4422754',
        'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3719169',
        'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4557679',
        'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3622433',
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

#% mentions in the press or other info
# the paper that finishes in 4422754 has a mention here
# https://www.ft.com/content/adb0ca9e-010b-4861-a2b5-ec0e30916956#comments-anchor
# add some extra text below the abstract saying "Featured in"
# and then add the link to the FT article

for paper in papers:
    if paper['url'] == 'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4422754':
        paper['abstract'] += f"""
        <p><b>Media mentions:</b> 
        <ul>
            <li><a href='https://www.ft.com/content/adb0ca9e-010b-4861-a2b5-ec0e30916956#comments-anchor'>A hat-trick of genuinely interesting papers relevant to the banking mess. FT 2023 </a></li>
            <li><a href='https://www.ft.com/content/a60e543d-c950-4ebb-8da9-d6b0b359ad7b'>Wake up to the dangers of digital bank runs. FT 2023 </a></li>
            <li><a href='https://www.nytimes.com/2023/04/21/business/dealbook/buzzfeed-news-shuts-down.html'>A social-media-powered bank run. The New York Times DEALBOOK 2023 </a></li>
            <li><a href="https://money.com/twitter-svb-collapse-study/">Study Finds Twitter Chatter Fueled SVB Collapse — and Other Banks Are at Risk. Money 2023</a></li>
            <li><a href="https://www.cnbc.com/2023/04/24/social-media-raises-bank-run-risk-fueled-svbs-collapse-paper-says.html">Social media raises bank run risk, fueled Silicon Valley Bank’s collapse, paper says. CNBC 2023</a></li>
            <li><a href="https://www.axios.com/2023/04/24/twitter-svb-bank-run"> Twitter fueled run on Silicon Valley Bank, new paper finds. Axios 2023</a></li>
            <li><a href="https://fortune.com/2023/04/24/twitter-financial-system-risk-silicon-valley-bank-run-study/">Twitter poses a risk to the financial system and helped fuel the SVB run, says first major study to investigate the topic. Fortune 2023</a></li> 
            <li><a href="https://www.technewsworld.com/story/social-media-fueled-the-run-on-silicon-valley-bank-study-178230.html">Social Media Fueled the Run on Silicon Valley Bank: Study. TECHNEWSWORLD 2023</a></li>
            <li><a href="https://www.nasdaq.com/articles/did-tweets-help-crash-silicon-valley-bank-paper-shows-new-social-media-risks">Did Tweets Help Crash Silicon Valley Bank? Paper Shows New Social Media Risks. Kiplinger 2023 </a></li>
            <li><a href="https://www.wsj.com/articles/silicon-valley-bank-run-twitter-59061759"> The Surprising Risk That Turbocharged a $142 Billion Bank Run. WSJ 2023 </a></li>
            <li><a href="https://www.brookings.edu/2023/04/27/hutchins-roundup-bank-runs-and-social-media-rising-wages-and-inflation-and-more/">Hutchins Roundup: Bank runs and social media, rising wages and inflation, and more. Brookings 2023</a></li>
            <li><a href="https://archive.ph/2023.05.07-050116/https://www.americanbanker.com/news/twitter-helped-kill-silicon-valley-bank-are-other-banks-at-risk">Twitter helped kill Silicon Valley Bank. Are other banks at risk? American Banker 2023</a></li> 
            <li><a href="https://cincodias.elpais.com/mercados-financieros/2023-05-12/twitter-un-motor-que-azuzo-el-miedo-financiero-y-precipito-la-caida-de-silicon-valley-bank.html"> Twitter, un motor que azuzó el miedo financiero y precipitó la caída de Silicon Valley Bank. Cinco días El Pais, 2023</a></li>
            <li><a href="https://www.lavanguardia.com/economia/20230514/8963234/panico-empresa-hablan-redes-sociales.html">Pánico en la empresa: hablan las redes sociales. La Vanguardia 2023</a></li>
        </ul>
        <b>Mentions by regulators:</b> 
        <ul>
            <li><a href="https://dfpi.ca.gov/wp-content/uploads/sites/337/2023/05/Review-of-DFPIs-Oversight-and-Regulation-of-Silicon-Valley-Bank.pdf"> Review of DFPI's Oversight and Regulation of Silicon Valley Bank. Department of FInancial Protection and Innovation DFPI. May 2023 </a></li>
            <li><a href="https://repositorio.banrep.gov.co/bitstream/handle/20.500.12134/10638/reporte-estabilidad-financiera-primer-semestre-2023.pdf?sequence=1"> Reporte de Estabilidad Financiera. Banco de la Republica de Colombia (2023) </a></li>
        </ul>
        </p>
        """

    if paper['url'] == 'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3719169':
        paper['abstract'] += f"""
        <p><b>Summary:</b> 
        <ul>
            <li><a href='https://focus.bse.eu/tweeting-for-money-impact-on-money-flows-when-mutual-funds-tweet/'>Tweeting for Money: Impact on Money Flows When Mutual Funds Tweet. BSE Focus 2023 </a></li>
            <li><a href='https://www.upf.edu/en/web/e-noticies/home/-/asset_publisher/wEpPxsVRD6Vt/content/id/262764917/maximized#.Y3tjxXbMKUm'>Asset management companies use social media to persuade investors, according to a study. Focus UPF 2022 </a></li>
        </ul>
        </p>
        """

#%
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

    if paper['url'] == 'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4422754':
        papers_html += f"<h3><a href='{paper['url']}'>{paper['title']}</a></h3><h4>R&R at the Journal of Financial Economics</h4><p>{', '.join(paper['authors'])}</p><p style='text-align: justify;'>{paper['abstract']}</p>"
    else:
        papers_html += f"<h3><a href='{paper['url']}'>{paper['title']}</a></h3><p>{', '.join(paper['authors'])}</p><p style='text-align: justify;'>{paper['abstract']}</p>"

    # add some space between papers
    papers_html += "<br>"

# Read existing HTML file
with open('../index2.html', 'r') as f:
    html = f.read()

# Insert generated HTML after placeholder comment
html = html.replace('<!-- INSERT PAPERS HERE -->', papers_html)

# Write updated HTML back to file
# encode to utf-8 to avoid issues with accents
with open('../index.html', 'w', encoding='utf-8') as f:
    f.write(html)
# %%
