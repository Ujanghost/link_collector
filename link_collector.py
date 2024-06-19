import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_urls_from_source(url, tag, attribute, base_url=None):
    urls = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all(tag, href=True):
            href = link.get(attribute)
            if base_url and not href.startswith("http"):
                href = f"{base_url}{href}"
            urls.append(href)
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
    return urls

def collect_urls():
    sources = [
        {"url": "https://www.bbc.com", "tag": "a", "attribute": "href", "base_url": "https://www.bbc.com"},
        {"url": "https://www.cnn.com", "tag": "a", "attribute": "href", "base_url": "https://www.cnn.com"},
        {"url": "https://www.techcrunch.com", "tag": "a", "attribute": "href"},
        {"url": "https://www.nytimes.com", "tag": "a", "attribute": "href"},
        # Add more sources as needed
    ]

    all_urls = []
    for source in sources:
        urls = fetch_urls_from_source(source["url"], source["tag"], source["attribute"], source.get("base_url"))
        all_urls.extend(urls)

    return all_urls

def save_urls_to_csv(urls, filename):
    df = pd.DataFrame(urls, columns=["URL"])
    df.to_csv(filename, index=False)

# Collect URLs and save to CSV
urls = collect_urls()
save_urls_to_csv(urls, 'collected_urls.csv')

print("URLs collected and saved to collected_urls.csv")
