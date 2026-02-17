import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Tor proxy (make sure Tor is running on your system)
TOR_PROXIES = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def fetch_page(url):
    """Fetch page content. Use Tor for .onion URLs."""
    try:
        if url.endswith(".onion"):
            response = requests.get(url, proxies=TOR_PROXIES, timeout=15)
        else:
            response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"[!] Failed to fetch {url}: {e}")
        return None

def parse_page(url, keywords):
    """Scrape page for keywords and return results with sentiment"""
    html = fetch_page(url)
    results = []
    if html:
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        for keyword in keywords:
            if keyword.lower() in text.lower():
                sentiment_score = analyzer.polarity_scores(text)["compound"]
                if sentiment_score >= 0.05:
                    sentiment = "Positive"
                elif sentiment_score <= -0.05:
                    sentiment = "Negative"
                else:
                    sentiment = "Neutral"
                snippet = " ".join(text.split()[:50])
                results.append({
                    "url": url,
                    "keyword": keyword,
                    "snippet": snippet,
                    "sentiment": sentiment
                })
    return results
