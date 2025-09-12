from monitor_config import TARGET_URLS
from db import init_db, log_entry
from scraper import fetch_site_content, scan_for_keywords
from alert import send_email_alert, send_discord_alert

def main():
    init_db()
    for url in TARGET_URLS:
        print(f"[+] Scanning {url}")
        content = fetch_site_content(url)
        if not content:
            continue
        findings = scan_for_keywords(url, content)
        for keyword, snippet, sentiment in findings:
            print(f"[!] Found '{keyword}' on {url} | Sentiment: {sentiment}")
            log_entry(url, keyword, snippet, sentiment)
            message = f"Keyword '{keyword}' found on {url}.\nSentiment: {sentiment}\nSnippet: {snippet[:200]}"
            send_discord_alert(message)
            send_email_alert("Dark Web Alert", message)

if __name__ == '__main__':
    main()
    
