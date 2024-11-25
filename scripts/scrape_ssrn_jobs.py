#%%
import requests
import openai
import os
import json
import pandas as pd
from tqdm import tqdm
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
def ask_question_llm(url):
    # get the text from the url
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code != 200:
        return None
    soup = bs(response.content, 'html.parser')
    text = soup.get_text()

    client = openai.OpenAI(
        api_key = os.environ.get('OPENAI_API_KEY')
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""
                Based on the following job description, return in a dictionary (json string) the following information (do not return anything else):
                - place: The university or department
                - country: The country
                - city: The city
                - description: The job description
                - rec_letters: The number of recommendation letters required
                - where_rec: Where to send the recommendation letters
                - how_to_apply: How to apply
                - deadline: The deadline for the application
                - cover_letter: If a cover letter is required
                - cv: If a CV is required
                - papers: How many papers are required
                - teaching_eval: If teaching evaluations are required
                - research_statement: If a research statement is required  


                {text}             
                """,
            }
        ],
        model="gpt-4o",
    )

    response_ = chat_completion.choices[0].message.content
    # clean a bit, 
    # remove ```json and ```
    response_ = str(response_).replace('```json', '').replace('```', '')
    # remove \n
    response_ = response_.replace('\n', '')

    return response_
# %%
for i, job in tqdm(enumerate(jobs)):
    # job is a dictionary remember
    job_description = ask_question_llm(job['href'])
    # to json   
    try:
        job_description = json.loads(job_description) # type: ignore

        # add the job description to the job dictionary
        job.update(job_description)
    except:
        job['error'] = job_description

    jobs[i] = job

# to pandas 

df = pd.DataFrame(jobs)

df.to_csv('jobs_ssrn.csv', index=False)

# save to excel 
df.to_excel('jobs_ssrn.xlsx', index=False)
