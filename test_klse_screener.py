import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

url = "https://www.klsescreener.com/v2/screener/quote_results"
params = {
    "type": "stock",
    "board": "all",
    "sector": "all",
    "market": "MAIN",
    "sort": "Volume",
    "order": "desc",
    "page": "1",
    "perpage": "10",
}

r = requests.get(url, params=params, headers=headers, verify=False, timeout=15)
print(f"Status: {r.status_code}, Length: {len(r.text)}")

soup = BeautifulSoup(r.text, "html.parser")
table = soup.find("table")

if table:
    rows = table.find_all("tr")
    print(f"Found {len(rows)} rows")
    for row in rows[:12]:
        cells = row.find_all(["td", "th"])
        text = [c.get_text(strip=True) for c in cells[:8]]
        if text:
            print("  | ".join(text[:8]))
else:
    # Try finding divs or other structures
    print("No table found, checking structure...")
    divs = soup.find_all("div", class_="row")
    print(f"Found {len(divs)} row divs")
    # Print first meaningful content
    for tag in soup.find_all(["td", "a"], limit=20):
        t = tag.get_text(strip=True)
        if t and len(t) < 50:
            print(f"  {tag.name}: {t}")
