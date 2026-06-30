"""
Data fetcher module for KLSE stocks using Yahoo Finance.

KLSE stocks use the '.KL' suffix on Yahoo Finance.
"""

import os
import ssl
import urllib3
import time

# Disable SSL verification globally (needed for corporate/restricted networks)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ["CURL_CA_BUNDLE"] = ""
os.environ["PYTHONHTTPSVERIFY"] = "0"
ssl._create_default_https_context = ssl._create_unverified_context

import yfinance as yf
import pandas as pd
import requests

# Session with SSL disabled
session = requests.Session()
session.verify = False


def get_popular_klse_stocks() -> dict:
    """Return a dictionary of popular KLSE stock symbols and names."""
    return {
        "1155.KL": "Maybank",
        "1023.KL": "CIMB Group",
        "5347.KL": "Tenaga Nasional",
        "3182.KL": "Genting",
        "1295.KL": "Public Bank",
        "6888.KL": "Axiata Group",
        "4707.KL": "Nestle Malaysia",
        "5681.KL": "Petronas Chemicals",
        "4863.KL": "Telekom Malaysia",
        "1082.KL": "Hong Leong Bank",
        "5225.KL": "IHH Healthcare",
        "4197.KL": "Sime Darby",
        "6012.KL": "Maxis",
        "2445.KL": "Kuala Lumpur Kepong",
        "5183.KL": "Petronas Gas",
    }


def fetch_stock_data(symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    """
    Fetch historical stock data from Yahoo Finance.

    Args:
        symbol: Stock symbol with .KL suffix (e.g., '1155.KL' for Maybank)
        period: Data period - 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        interval: Data interval - 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo

    Returns:
        DataFrame with OHLCV data
    """
    try:
        ticker = yf.Ticker(symbol, session=session)
        df = ticker.history(period=period, interval=interval)

        if df.empty:
            print(f"Warning: No data returned for {symbol}")
            return pd.DataFrame()

        # Clean up columns
        df.index.name = "Date"
        return df

    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()


def fetch_stock_info(symbol: str) -> dict:
    """
    Fetch current stock info using fast_info (more reliable, less rate-limited).

    Args:
        symbol: Stock symbol with .KL suffix

    Returns:
        Dictionary with stock info
    """
    try:
        ticker = yf.Ticker(symbol, session=session)
        info = ticker.fast_info
        return {
            "last_price": info.get("lastPrice", 0),
            "last_volume": info.get("lastVolume", 0),
            "day_high": info.get("dayHigh", 0),
            "day_low": info.get("dayLow", 0),
            "open": info.get("open", 0),
            "previous_close": info.get("previousClose", 0),
            "market_cap": info.get("marketCap", 0),
            "fifty_day_avg": info.get("fiftyDayAverage", 0),
            "two_hundred_day_avg": info.get("twoHundredDayAverage", 0),
            "year_high": info.get("yearHigh", 0),
            "year_low": info.get("yearLow", 0),
            "year_change": info.get("yearChange", 0),
            "ten_day_avg_volume": info.get("tenDayAverageVolume", 0),
            "three_month_avg_volume": info.get("threeMonthAverageVolume", 0),
        }
    except Exception as e:
        print(f"Error fetching info for {symbol}: {e}")
        return {}


def fetch_multiple_stocks(symbols: list, period: str = "1y") -> dict:
    """
    Fetch data for multiple KLSE stocks.

    Args:
        symbols: List of stock symbols
        period: Data period

    Returns:
        Dictionary mapping symbol to DataFrame
    """
    results = {}
    for symbol in symbols:
        print(f"  Fetching {symbol}...")
        df = fetch_stock_data(symbol, period=period)
        if not df.empty:
            results[symbol] = df
        time.sleep(0.5)  # Rate limit protection
    return results
