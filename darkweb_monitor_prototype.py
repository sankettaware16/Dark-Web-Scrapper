import sqlite3
from scraper import parse_page
import db 
# Load SQLite DB
conn = sqlite3.connect("darkweb.db")
c = conn.cursor()

# Configuration (safe example URLs)
TARGET_URLS = [
   # "https://duckduckgo.com/",
    "http://torprojectorgn2qqx4tqv7obxqz6y5v5z3c6r6xqv5p7w4k6r4kqad.onion"  # Uncomment for real onion testing
]
KEYWORDS = ["duckduckgo", "search", "privacy"]

def log_entry(result):
    """Insert result into SQLite DB and print"""
    c.execute(
        "INSERT INTO logs (url, keyword, snippet, sentiment) VALUES (?, ?, ?, ?)",
        (result["url"], result["keyword"], result["snippet"], result["sentiment"])
    )
    conn.commit()
    print(f"[DB] Logged: {result['keyword']} | {result['sentiment']} | {result['url']}")

def main():
    print("[*] Dark Web Monitor (Prototype) Started")
    for url in TARGET_URLS:
        print(f"[+] Scanning {url}")
        results = parse_page(url, KEYWORDS)
        for res in results:
            log_entry(res)

if __name__ == "__main__":
    main()
