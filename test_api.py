import requests
import urllib3
import json

urllib3.disable_warnings()

s = requests.Session()
s.verify = False
s.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

# Step 1: Get cookie
r = s.get("https://fc.yahoo.com", timeout=10, allow_redirects=True)
print("Cookie status:", r.status_code)

# Step 2: Get crumb
r2 = s.get("https://query2.finance.yahoo.com/v1/test/getcrumb", timeout=10)
crumb = r2.text.strip()
print("Crumb:", crumb)

# Step 3: Query screener - NO volume filter to get all stocks
url = "https://query2.finance.yahoo.com/v1/finance/screener"
payload = {
    "offset": 0,
    "size": 10,
    "sortField": "dayvolume",
    "sortType": "DESC",
    "quoteType": "EQUITY",
    "query": {
        "operator": "AND",
        "operands": [
            {"operator": "EQ", "operands": ["region", "my"]},
        ],
    },
}

r3 = s.post(url, json=payload, params={"crumb": crumb}, timeout=15)
print("Screener status:", r3.status_code)

if r3.status_code == 200:
    data = r3.json()
    quotes = data.get("finance", {}).get("result", [{}])[0].get("quotes", [])
    print(f"\nGot {len(quotes)} stocks:\n")
    for i, q in enumerate(quotes):
        sym = q.get("symbol", "")
        name = q.get("shortName", "")
        vol = q.get("regularMarketVolume", 0)
        price = q.get("regularMarketPrice", 0)
        chg = q.get("regularMarketChangePercent", 0)
        print(f"  {i+1:>2}. {sym:<12} {name:<25} RM {price:>8.4f}  Vol: {vol:>12,}  Chg: {chg:+.2f}%")
else:
    print("Error:", r3.text[:300])
