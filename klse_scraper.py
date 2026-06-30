"""
KLSE Screener scraper - gets ALL Bursa Malaysia stocks.
Covers Main Market, ACE Market, and LEAP Market.
"""

import requests
import urllib3
from bs4 import BeautifulSoup
import time

urllib3.disable_warnings()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

BASE_URL = "https://www.klsescreener.com/v2/screener/quote_results"


def fetch_all_stocks_by_volume(market: str = "all", top_n: int = 100) -> list:
    """
    Fetch stocks from klsescreener.com sorted by volume.

    Args:
        market: "MAIN", "ACE", "LEAP", or "all"
        top_n: Number of stocks to return

    Returns:
        List of stock dicts with: code, name, price, change, change_pct, volume, category
    """
    params = {
        "type": "stock",
        "board": "all",
        "sector": "all",
        "market": market if market != "all" else "",
        "sort": "Volume",
        "order": "desc",
        "page": "1",
        "perpage": str(top_n),
    }

    try:
        r = requests.get(BASE_URL, params=params, headers=HEADERS, verify=False, timeout=20)

        if r.status_code != 200:
            print(f"  klsescreener returned status {r.status_code}")
            return []

        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table")

        if not table:
            return []

        rows = table.find_all("tr")
        stocks = []

        for row in rows[1:]:  # Skip header
            cells = row.find_all("td")
            if len(cells) < 7:
                continue

            name = cells[0].get_text(strip=True)
            code = cells[1].get_text(strip=True)
            category = cells[2].get_text(strip=True)
            price_text = cells[3].get_text(strip=True)
            change_text = cells[4].get_text(strip=True)
            change_pct_text = cells[5].get_text(strip=True)
            volume_text = cells[7].get_text(strip=True) if len(cells) > 7 else "0"

            # Parse values
            try:
                price = float(price_text) if price_text else 0
            except ValueError:
                price = 0

            try:
                change = float(change_text) if change_text else 0
            except ValueError:
                change = 0

            try:
                change_pct = float(change_pct_text.replace("%", "")) if change_pct_text else 0
            except ValueError:
                change_pct = 0

            try:
                volume = int(volume_text.replace(",", "")) if volume_text else 0
            except ValueError:
                volume = 0

            # Clean name (remove [s] suffix)
            name = name.replace("[s]", "").replace("[c]", "").strip()

            # Determine market type from category
            market_type = "MAIN"
            if "ACE" in category or "Ace" in category:
                market_type = "ACE"
            elif "LEAP" in category or "Leap" in category:
                market_type = "LEAP"

            if volume > 0:
                stocks.append({
                    "code": code,
                    "symbol": f"{code}.KL",
                    "name": name,
                    "price": price,
                    "change": change,
                    "change_pct": change_pct,
                    "volume": volume,
                    "market": market_type,
                    "category": category[:40],
                })

        return stocks

    except Exception as e:
        print(f"  Error scraping klsescreener: {e}")
        return []


def get_all_stock_symbols(top_n: int = 200) -> dict:
    """
    Get a dict of {symbol: name} for top stocks by volume.
    Used by divergence scanner.
    """
    stocks = fetch_all_stocks_by_volume(market="all", top_n=top_n)
    return {s["symbol"]: s["name"] for s in stocks}
