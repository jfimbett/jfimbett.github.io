#%%
import numpy as np
import pandas as pd
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import re
# Util functions
# %%
def get_content(x, soup):
    try:
         return soup.find("meta", {"name" : x})["content"]
    except:
        return ""

def print_authors(x):
    text = ""
    for (i, author) in enumerate(x):
        if i>0:
            text = text + " and "+author
        else:
            text = author
    return text

def trim_name(x):
    return re.sub('[^a-zA-Z]+', '', x.lower())

def last_names(x):
    text = ""
    for (i, author) in enumerate(x):
        ln = trim_name(author.split(',')[0])
        if i>0:
            text = text + "&"+ln
        else:
            text = ln

    return text.replace(" ", "")

def last_clean(x):
    return x.replace("&", "\&")

def get_bibtex(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    # To get the data
    each_author = [s["content"] for s in soup.find_all("meta", {"name" : "citation_author"})]
    citation_title              = get_content("citation_title", soup)
    citation_authors            = get_content("citation_authors", soup)
    citation_date               = get_content("citation_date", soup)
    citation_year               = get_content("citation_year", soup)
    citation_publication_date   = get_content("citation_publication_date", soup)
    citation_publisher          = ""
    publisher                   = get_content("citation_publisher", soup)
    if publisher=="":
        publisher               = get_content("citation_technical_report_institution", soup)
    
    citation_journal_title      = get_content("citation_journal_title", soup)
    citation_issue              = get_content("citation_issue", soup)
    citation_firstpage          = get_content("citation_firstpage", soup)
    citation_lastpage           = get_content("citation_lastpage", soup)
    is_edited                   = get_content("is_edited", soup)
    series                      = get_content("series", soup)
    keywords                    = get_content("key_words", soup)
    paper_url                   = get_content("citation_abstract_html_url", soup)
    abstract                    = get_content("citation_abstract", soup)
    volume                      = get_content("citation_volume", soup)
    number                      = get_content("wp_number", soup)
    page_start                  = get_content("citation_firstpage", soup)
    page_end                    = get_content("citation_lastpage", soup)
    edition                     = get_content("book_edition", soup)
    book_title                  = get_content("book_title", soup)
    book_editor                 = get_content("book_editor", soup)
    chapter                     = get_content("chapter", soup)
    type_ref                    = get_content("redif-type", soup)

    #Small changes after testing
    # i) avoid the & character

    if type_ref == "article":
        handle = f"""
                    @ARTICLE{{{last_names(each_author)+citation_year},
                    title = {{ {last_clean(citation_title)} }},
                    author = {{ {last_clean(print_authors(each_author))} }},
                    year = {{ {last_clean(citation_year)} }},
                    journal = {{ {last_clean(citation_journal_title)} }},
                    volume = {{ {last_clean(volume)} }},
                    number = {{ {last_clean(series)} }},
                    pages = {{ {page_start}-{page_end} }},
                    abstract = {{ {last_clean(abstract)} }},
                    url = {{ {paper_url} }}
                    }}
                """


        return handle
    else:
        return ""



base_url = "https://econpapers.repec.org/"
page     = requests.get(base_url+"article/")
soup     = BeautifulSoup(page.content, 'html.parser')
# %%
urls = soup.find_all('div', {'class' : 'issuelinks'})[0].find_all('a')
article_urls = []
t = tqdm(urls)
for url in t:
    page = requests.get(base_url+url['href'])
    soup = BeautifulSoup(page.content, 'html.parser')
    t.set_description(f"Getting repec url form subpage {url} ")
    t.refresh()
    dts = soup.find('div', {'class':'bodytext'}).find_all('dt')

    for dt in dts:
        try:
            article_urls.append(dt.find_all('a')[0]['href'])
        except:
            pass
# %%
article_urls=['article/blajfinan', 'article/eeejfinec']
# %%
journal_articles = []
for article_url in article_urls:
    url  = base_url+article_url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # How many default pages we need to iterate?
    to_it= soup.find_all('div', {'class' : 'issuelinks'})[0].find_all('a')[-1]['href'][7:-4]

    # Get current volume
    # %%
    sub_urls =[]
    for i in range(int(to_it)+1):
        n = i if i>0 else ""
        sub_urls.append(f"{url}/default{n}.htm")
    
    # Links, other volumes

    # %%
    
    for sub_url in tqdm(sub_urls):
        page = requests.get(sub_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        dls = soup.find_all('dl')
        for dl in dls:
            as_dl = dl.find_all('a')
            for a in as_dl:
                journal_articles.append(f"{url}/{a['href']}")

citations = []
for link in tqdm(journal_articles):
    citations.append(get_bibtex(link))

# %%
# Create a bibtex file
with open('test_bibtex.bib', 'w',encoding="utf-8") as f:
    for b in citations:
        f.write(b+"\n")
# %%
# For some tests
papers = [c.split(",")[0].replace(" ","")[10:] for c in citations if c!='']
# %%
command = "\\cite{" + ','.join(papers) +"}"
# %%
with open('command.tex', 'w', encoding="utf-8") as f:
    f.write(command)
# %%
