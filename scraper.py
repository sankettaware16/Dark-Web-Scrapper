import requests
from bs4 import BeautifulSoup
from monitor_config import KEYWORDS
from sentiment import analyze_sentiment

def fetch_site_content(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()
    except Exception as e:
        print(f"[!] Failed to fetch {url}: {e}")
        return None

def scan_for_keywords(url, content):
    results = []
    for keyword in KEYWORDS:
        if keyword.lower() in content.lower():
            snippet = content[content.lower().index(keyword.lower()):][:300]
            sentiment = analyze_sentiment(snippet)
            results.append((keyword, snippet, sentiment))
    return results
