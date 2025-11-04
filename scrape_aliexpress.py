import requests
from bs4 import BeautifulSoup
from datetime import datetime
import hashlib
import time

# Pull "newest" search results for a query (very simple MVP)
def scrape_search(query="gadgets", pages=1):
    results = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    for p in range(1, pages+1):
        url = f"https://www.aliexpress.com/wholesale?SearchText={query}&page={p}"
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            continue
        soup = BeautifulSoup(r.text, "html.parser")

        # AliExpress HTML changes often; these selectors are best-effort.
        items = soup.select(".manhattan--container--1lP57Ag") or soup.select(".list-item")
        for it in items[:30]:
            a = it.find("a", href=True)
            title = it.get_text(separator=" ", strip=True)[:200]
            href = a["href"] if a else ""
            if href and href.startswith("/"):
                href = "https://www.aliexpress.com" + href

            uid = hashlib.md5((title + (href or "")).encode()).hexdigest()[:12]
            results.append({
                "id": uid,
                "source": "aliexpress",
                "title": title,
                "url": href,
                "image": "",
                "first_seen": datetime.utcnow().isoformat(),
                "views": 0,
                "favorites": 0,
                "orders": 0
            })
        time.sleep(1.2)
    return results

if __name__ == "__main__":
    items = scrape_search("gadgets", pages=1)
    for i in items[:5]:
        print(i)
