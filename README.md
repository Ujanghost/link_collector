# Web Scraping and URL Collection with Python

This Python script fetches URLs from specified web sources and saves them to a CSV file. It uses the `requests` library to make HTTP requests, `BeautifulSoup` from the `bs4` library to parse HTML content, and `pandas` to handle data and save it to a CSV file.

## Requirements

Ensure you have the following libraries installed:

```sh
pip install requests beautifulsoup4 pandas
```

## Code Explanation

### Import Libraries

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
```

- `requests`: For making HTTP requests to fetch web pages.
- `BeautifulSoup`: For parsing HTML content.
- `pandas`: For handling data and saving it to a CSV file.

### Function: `fetch_urls_from_source`

```python
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
```

- **Parameters**:
  - `url`: The URL of the web page to fetch.
  - `tag`: The HTML tag to search for (e.g., 'a' for anchor tags).
  - `attribute`: The attribute of the tag to extract (e.g., 'href' for hyperlinks).
  - `base_url` (optional): The base URL to use for relative links.

- **Functionality**:
  - Sends an HTTP GET request to the specified URL.
  - Parses the HTML content of the page using BeautifulSoup.
  - Finds all specified tags with the given attribute.
  - Constructs full URLs if `base_url` is provided and appends them to the `urls` list.
  - Handles exceptions by printing an error message if the request fails.

### Function: `collect_urls`

```python
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
```

- **Functionality**:
  - Defines a list of sources, each with a URL, tag, attribute, and optional base URL.
  - Iterates over the sources, fetching URLs from each source using `fetch_urls_from_source`.
  - Collects all URLs in the `all_urls` list.
  - Returns the collected URLs.

### Function: `save_urls_to_csv`

```python
def save_urls_to_csv(urls, filename):
    df = pd.DataFrame(urls, columns=["URL"])
    df.to_csv(filename, index=False)
```

- **Parameters**:
  - `urls`: A list of URLs to save.
  - `filename`: The name of the CSV file to save the URLs to.

- **Functionality**:
  - Creates a Pandas DataFrame from the list of URLs.
  - Saves the DataFrame to a CSV file without the index.

### Main Script

```python
# Collect URLs and save to CSV
urls = collect_urls()
save_urls_to_csv(urls, 'collected_urls.csv')

print("URLs collected and saved to collected_urls.csv")
```

- Collects URLs from the specified sources.
- Saves the collected URLs to a CSV file named `collected_urls.csv`.
- Prints a confirmation message.

## Usage

1. Ensure the required libraries are installed.
2. Run the script.
3. The script will collect URLs from the specified web sources and save them to `collected_urls.csv`.

This script is easily extensible. To add more sources, simply include additional dictionaries in the `sources` list with the appropriate URL, tag, attribute, and base URL if needed.
