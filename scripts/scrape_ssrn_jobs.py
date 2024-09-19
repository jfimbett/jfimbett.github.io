#%%
import requests
url = "https://www.ssrn.com/index.cfm/en/janda/job-openings/?jobsNet=203"

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

assert response.status_code == 200
# %%
# get all p with class job-title-link
from bs4 import BeautifulSoup as bs

soup = bs(response.content, 'html.parser')
job_titles = soup.find_all('p', class_='job-title-link')
job_dates  = soup.find_all('span', class_='job-date')
job_org_name = soup.find_all('p', class_='job-org-name')
job_location   = soup.find_all('p', class_='location')
    

# %%
# asser tthey are all the same length 
assert len(job_titles) == len(job_dates) == len(job_org_name) == len(job_location)
# %%
# zip them together, create a dictionary for each one, and add the href in the <a> inside job-title-link
jobs = [{'title': title.text, 'date': date.text, 'org_name': org_name.text, 'location': location.text, 'href': title.find('a')['href']} for title, date, org_name, location in zip(job_titles, job_dates, job_org_name, job_location)]
# %%
