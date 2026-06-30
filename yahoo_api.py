"""
Direct Yahoo Finance API client.

Uses the v8 chart API directly to bypass yfinance rate limiting issues.
Also uses the screener API to get Most Active stocks by region.
"""

import requests
import urllib3
import pandas as pd
from datetime import datetime, timedelta
import time

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Yahoo Finance API endpoints
CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
SCREENER_URL = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved"

# Headers to mimic browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}


def fetch_most_active_malaysia(count: int = 50) -> list:
    """
    Fetch Most Active stocks for Malaysia using Yahoo Finance screener API.
    This matches the data shown on Yahoo Finance "Most Actives" page.

    Uses cookie/crumb authentication like the website does.

    Args:
        count: Number of stocks to return

    Returns:
        List of dicts with stock data, sorted by volume descending
    """
    try:
        # Create authenticated session
        s = requests.Session()
        s.verify = False
        s.headers.update(HEADERS)

        # Step 1: Get cookie from Yahoo
        s.get("https://fc.yahoo.com", timeout=10, allow_redirects=True)

        # Step 2: Get crumb token
        r2 = s.get("https://query2.finance.yahoo.com/v1/test/getcrumb", timeout=10)
        crumb = r2.text.strip()

        if not crumb:
            print("  Failed to get crumb token")
            return []

        # Step 3: Query screener with crumb
        url = "https://query2.finance.yahoo.com/v1/finance/screener"
        payload = {
            "offset": 0,
            "size": count,
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

        resp = s.post(url, json=payload, params={"crumb": crumb}, timeout=15)

        if resp.status_code == 200:
            data = resp.json()
            quotes = data.get("finance", {}).get("result", [{}])[0].get("quotes", [])
            return quotes
        else:
            print(f"  Screener returned status {resp.status_code}")

    except Exception as e:
        print(f"  Screener API error: {e}")

    return []


def fetch_most_active_weekly(count: int = 50) -> list:
    """
    Fetch stocks sorted by average volume (3 month) for weekly view.
    Uses the same screener API but sorts by 3-month avg volume.
    """
    try:
        s = requests.Session()
        s.verify = False
        s.headers.update(HEADERS)

        s.get("https://fc.yahoo.com", timeout=10, allow_redirects=True)
        r2 = s.get("https://query2.finance.yahoo.com/v1/test/getcrumb", timeout=10)
        crumb = r2.text.strip()

        if not crumb:
            return []

        url = "https://query2.finance.yahoo.com/v1/finance/screener"
        payload = {
            "offset": 0,
            "size": count,
            "sortField": "avgdailyvol3m",
            "sortType": "DESC",
            "quoteType": "EQUITY",
            "query": {
                "operator": "AND",
                "operands": [
                    {"operator": "EQ", "operands": ["region", "my"]},
                ],
            },
        }

        resp = s.post(url, json=payload, params={"crumb": crumb}, timeout=15)

        if resp.status_code == 200:
            data = resp.json()
            quotes = data.get("finance", {}).get("result", [{}])[0].get("quotes", [])
            return quotes

    except Exception as e:
        print(f"  Screener API error: {e}")

    return []


def fetch_chart_data(symbol: str, period: str = "5d", interval: str = "1d") -> dict:
    """
    Fetch stock data directly from Yahoo Finance chart API.

    Args:
        symbol: Stock symbol (e.g., '1155.KL')
        period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        interval: 1d, 1wk, 1mo

    Returns:
        Dict with price/volume data or empty dict on failure
    """
    url = CHART_URL.format(symbol=symbol)
    params = {
        "range": period,
        "interval": interval,
        "includePrePost": "false",
        "events": "div,splits",
    }

    try:
        resp = requests.get(url, params=params, headers=HEADERS, verify=False, timeout=10)

        if resp.status_code == 429:
            # Rate limited - wait and retry once
            time.sleep(2)
            resp = requests.get(url, params=params, headers=HEADERS, verify=False, timeout=10)

        if resp.status_code != 200:
            return {}

        data = resp.json()
        result = data.get("chart", {}).get("result", [])

        if not result:
            return {}

        return result[0]

    except Exception as e:
        return {}


def get_stock_quote(symbol: str) -> dict:
    """
    Get latest quote data for a single stock.

    Returns dict with: close, volume, high, low, open, prev_close, change_pct
    """
    raw = fetch_chart_data(symbol, period="5d", interval="1d")

    if not raw:
        return {}

    try:
        meta = raw.get("meta", {})
        indicators = raw.get("indicators", {})
        quotes = indicators.get("quote", [{}])[0]

        # Get the latest day's data
        closes = quotes.get("close", [])
        volumes = quotes.get("volume", [])
        highs = quotes.get("high", [])
        lows = quotes.get("low", [])
        opens = quotes.get("open", [])

        if not closes or not volumes:
            return {}

        # Find last valid data point
        for i in range(len(closes) - 1, -1, -1):
            if closes[i] is not None and volumes[i] is not None and volumes[i] > 0:
                close = closes[i]
                volume = volumes[i]
                high = highs[i] if highs[i] is not None else close
                low = lows[i] if lows[i] is not None else close
                open_price = opens[i] if opens[i] is not None else close

                # Calculate change from previous close
                prev_close = meta.get("chartPreviousClose", meta.get("previousClose", 0))
                if prev_close and prev_close > 0:
                    change_pct = ((close - prev_close) / prev_close) * 100
                elif open_price > 0:
                    change_pct = ((close - open_price) / open_price) * 100
                else:
                    change_pct = 0

                return {
                    "close": round(close, 4),
                    "volume": int(volume),
                    "high": round(high, 4),
                    "low": round(low, 4),
                    "open": round(open_price, 4),
                    "prev_close": round(prev_close, 4) if prev_close else 0,
                    "change_pct": round(change_pct, 2),
                    "currency": meta.get("currency", "MYR"),
                    "exchange": meta.get("exchangeName", "KLS"),
                }

        return {}

    except (KeyError, IndexError, TypeError):
        return {}


def get_stock_history(symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    """
    Get historical data as a pandas DataFrame.

    Args:
        symbol: Stock symbol (e.g., '1155.KL')
        period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max
        interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo

    Returns:
        DataFrame with Date index and OHLCV columns
    """
    raw = fetch_chart_data(symbol, period=period, interval=interval)

    if not raw:
        return pd.DataFrame()

    try:
        timestamps = raw.get("timestamp", [])
        indicators = raw.get("indicators", {})
        quotes = indicators.get("quote", [{}])[0]

        if not timestamps:
            return pd.DataFrame()

        df = pd.DataFrame({
            "Date": pd.to_datetime(timestamps, unit="s"),
            "Open": quotes.get("open", []),
            "High": quotes.get("high", []),
            "Low": quotes.get("low", []),
            "Close": quotes.get("close", []),
            "Volume": quotes.get("volume", []),
        })

        df = df.set_index("Date")
        df = df.dropna(subset=["Close", "Volume"])
        df["Volume"] = df["Volume"].astype(int)

        return df

    except (KeyError, IndexError, TypeError):
        return pd.DataFrame()


def get_multiple_quotes(symbols: list, delay: float = 0.2) -> list:
    """
    Get quotes for multiple stocks with rate limiting.

    Args:
        symbols: List of stock symbols
        delay: Delay between requests in seconds

    Returns:
        List of quote dicts (with 'symbol' key added)
    """
    results = []

    for i, symbol in enumerate(symbols):
        quote = get_stock_quote(symbol)
        if quote:
            quote["symbol"] = symbol
            results.append(quote)

        # Rate limiting
        if delay > 0 and i < len(symbols) - 1:
            time.sleep(delay)

    return results
