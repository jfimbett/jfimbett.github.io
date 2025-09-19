import requests
from bs4 import BeautifulSoup
import re

def get_numeric_fraction(url):
    # Set headers to mimic a browser request
    headers = {
        'User-Agent': 'My Company Name (your.email@example.com)',  # SEC requires identification
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'www.sec.gov'
    }

    # Fetch the 10-K filing with headers
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    content = response.text

    # Extract documents from the SEC filing
    documents = re.findall(r'<DOCUMENT>(.*?)</DOCUMENT>', content, re.DOTALL)
    
    # Find the 10-K document
    tenk_text = ""
    for doc in documents:
        # Check document type
        type_match = re.search(r'<TYPE>(.*?)\n', doc)
        if type_match and type_match.group(1).strip() in ['10-K', '10-K/A']:
            # Extract text content
            text_match = re.search(r'<TEXT>(.*?)</TEXT>', doc, re.DOTALL)
            if text_match:
                text_content = text_match.group(1)
                # Remove HTML tags
                soup = BeautifulSoup(text_content, 'html.parser')
                tenk_text = soup.get_text()
                break
    
    if not tenk_text:
        raise ValueError("Could not find 10-K text in the document")
    
    # Calculate character statistics
    total_chars = len(tenk_text)
    numeric_chars = sum(c.isdigit() for c in tenk_text)
    return numeric_chars / total_chars

# Example usage
if __name__ == "__main__":
    # Example URL (Apple's 2023 10-K filing)
    sec_url = "https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/0000320193-23-000106.txt"
    
    try:
        fraction = get_numeric_fraction(sec_url)
        print(f"Fraction of numeric characters: {fraction:.4%}")
    except Exception as e:
        print(f"Error: {e}")