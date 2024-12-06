#%%
import pandas as pd
import numpy as np
import requests 
import openai
import os
import time
from tqdm import tqdm
# Function to retrieve valuation details
import yfinance as yf
# Specify the environment variable name
api_key_var_name = "OPENAI_API_KEY"

# Check if the environment variable is set
assert api_key_var_name in os.environ, f"Environment variable {api_key_var_name} not found."

client = openai.OpenAI(
            api_key = os.environ.get('OPENAI_API_KEY')
        )
url = 'https://raw.githubusercontent.com/nmapx/revolut-stocks-list/refs/heads/master/LIST.md'
r = requests.get(url)
data = r.text

# keep only rows with |
data = data.split('\n')
data = [x for x in data if '|' in x]

# elements look like this '| RKT   | Rocket Companies 
tickers = [x.split('|')[1].strip() for x in data]
names = [x.split('|')[2].strip() for x in data]

# to df 
df = pd.DataFrame({'ticker': tickers, 'name': names})
# remove if ticker is not caps
df = df[df.ticker.str.isupper()]

# %%
import json
def get_stock_elements():
    ticker = 'AAPL'
    stock = yf.Ticker(ticker)
    dirs = dir(stock)
    # remove dunders 
    elements = [d for d in dirs if not d.startswith('__')]
    # remove if starts with one _
    elements = [d for d in elements if not d.startswith('_')]

    implement_elements = []
    implement_functions = []
    for element in elements:
        try:
            time.sleep(0.3)
            getattr(stock, element)

            # if it is a function add to the functions list
            if callable(getattr(stock, element)):
                implement_functions.append(element)
            else:
                implement_elements.append(element)
        except:
            continue

    # store in json 
    elements = {'implemented_elements': implement_elements, 'implemented_functions': implement_functions}
    return elements

elements = get_stock_elements()
# %%
def get_stock_element(ticker, element):
    stock = yf.Ticker(ticker)
    # element is an attribute
    response =  getattr(stock, element)
    # The return type must be a string, dict, list, tuple with headers or status,
    # convert accordingly to json 

    if isinstance(response, dict) or isinstance(response, list) or isinstance(response, tuple):
        return {"data": response}

    # if its a dataframe convert to json 
    if hasattr(response, 'to_dict'):

        # if index is 0, 1, ... do not transpose
        if not (response.index[0] in range(len(response.index))):
            response = response.T

            # reset index 
            response = response.reset_index()
            
        # go column by column and if not string, or number (e.g. timestamp) convert to string
        for col in response.columns:
            if not response[col].dtype in ['int64', 'float64', 'object']:
                response[col] = response[col].astype(str)

        to_return = response.to_dict(orient='list')

        # if keys are timestamps convert to string
        to_return = {str(k): v for k, v in to_return.items()}

        # if values are timestamp, convert to string 
        for k, v in to_return.items():
            if isinstance(v[0], pd.Timestamp):
                to_return[k] = [str(val) for val in v]
        return json.dumps({"data": to_return})
        
    
    # if its a string return as is
    if isinstance(response, str):
        return {"data": response}
    
    # if its smt else convert it to text first 
    return {"data": str(response)}
# %%
# test
def retrieve_all_data(ticker, im_elements):
    to_return = {}
    for element in tqdm(im_elements):
        try:
            to_return[element] = get_stock_element(ticker, element)
        except Exception as e:
            pass
    return to_return



# %%
def recommendation(ticker):
    client = openai.OpenAI(
            api_key = os.environ.get('OPENAI_API_KEY')
        )

    all_data = retrieve_all_data(ticker, elements['implemented_elements']) 

    chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Based on the following output create a json object ONLY with the relevant information required to decide whether one should invest or not in {ticker}. Here is the info:
                    {all_data}

                    ONLY RETURN A JSON STRING!
                    """,
                }
            ],
            model="gpt-4o",
        )

    code_text = chat_completion.choices[0].message.content

    if code_text is None:
        return 

    code_text = code_text.replace('```json', '').replace('```', '')
    # replace \n 
    code_text = code_text.replace('\\n', '')
    # to json
    code_text = json.loads(code_text)

    stock = yf.Ticker(ticker)

    try:
        news = stock.get_news()
    except:
        news = 'No news available'
    
    chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Based on the following financial information, and news about a company, should I invest in {ticker}? Give me a recommendation, justify it and give me a confidence level from 1 to 5. Assume that I do not own any of the stocks. 
                    Return something like this:
                    {{
                        "recommendation": "buy",
                        "justification": "The company is in a good position to grow",
                        "confidence": 4
                    }}

                    Here is the information:

                    {code_text}

                    Here are the news:
                    {news}

                    ONLY RETURN A JSON STRING!
                    """,
                }
            ],
            model="gpt-4o",
        )
    
    recommendation = chat_completion.choices[0].message.content

    if recommendation is None:
        return

    recommendation = recommendation.replace('```json', '').replace('```', '')
    # replace \n
    recommendation = recommendation.replace('\\n', '')
    # to json
    recommendation = json.loads(recommendation)

    return recommendation

def get_all_recommendations():
    recommendations = {}
    for ticker, name in tqdm(zip(df.ticker, df.name)):
        recommendations[ticker] = recommendation(ticker)
        recommendations[ticker]['name'] = name
    
    # to json 
    with open('recommendations.json', 'w') as f:
        json.dump(recommendations, f)

    return recommendations

recommendations = get_all_recommendations()

print(recommendations)
    
    



# %%
