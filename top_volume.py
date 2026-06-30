"""
Top 50 KLSE Stocks by Daily/Weekly Volume

Fetches the most actively traded KLSE stocks using Yahoo Finance screener API.
This gives the same results as the Yahoo Finance "Most Actives" page.
"""

import pandas as pd
from datetime import datetime
from yahoo_api import (
    get_stock_quote,
    fetch_chart_data,
    fetch_most_active_malaysia,
    fetch_most_active_weekly,
)
import time


# Comprehensive list of KLSE stocks (symbol: name)
# Yahoo Finance uses .KL suffix for Bursa Malaysia stocks
KLSE_STOCKS = {
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
    "4715.KL": "Genting Malaysia",
    "5285.KL": "Sime Darby Plantation",
    "4677.KL": "YTL Corporation",
    "6742.KL": "YTL Power",
    "5168.KL": "Hartalega",
    "7113.KL": "Top Glove",
    "7153.KL": "Kossan Rubber",
    "5235.KL": "Supermax",
    "3816.KL": "MISC",
    "6033.KL": "Petronas Dagangan",
    "1961.KL": "IOI Corporation",
    "5014.KL": "Malaysia Airports",
    "4065.KL": "PPB Group",
    "1818.KL": "Bursa Malaysia",
    "5819.KL": "Hong Leong Financial",
    "8869.KL": "Press Metal",
    "5296.KL": "QL Resources",
    "3034.KL": "Hap Seng Consolidated",
    "5398.KL": "Gamuda",
    "5185.KL": "Dialog Group",
    "2291.KL": "Carlsberg Brewery",
    "4588.KL": "UMW Holdings",
    "6399.KL": "Sunway",
    "1066.KL": "RHB Bank",
    "5099.KL": "Capital A",
    "2488.KL": "SP Setia",
    "1015.KL": "AMMB Holdings",
    "6645.KL": "Inari Amertron",
    "0166.KL": "V.S. Industry",
    "7084.KL": "ViTrox",
    "0023.KL": "Datasonic",
    "7033.KL": "Pentamaster",
    "5218.KL": "Sapura Energy",
    "2836.KL": "CTOS Digital",
    "5148.KL": "UEM Sunrise",
    "3336.KL": "Sunway REIT",
    "5127.KL": "Pavilion REIT",
    "5106.KL": "IGB REIT",
    "5180.KL": "Sunway Construction",
    "0041.KL": "MyEG Services",
    "8583.KL": "Frontken",
    "1171.KL": "Sunway Berhad",
    "5020.KL": "Yinson Holdings",
    "0078.KL": "FGV Holdings",
    "5239.KL": "Duopharma Biotech",
    "7164.KL": "Karex",
    "2194.KL": "MMC Corporation",
    "5264.KL": "Aeon Credit",
    "5209.KL": "Gas Malaysia",
}


def get_top_volume_stocks(top_n: int = 50, period: str = "daily") -> pd.DataFrame:
    """
    Fetch most active KLSE stocks by volume using Yahoo Finance screener API.
    Returns the same data as Yahoo Finance "Most Actives" page.

    Args:
        top_n: Number of top stocks to return (default 50)
        period: "daily" for last trading day volume, "weekly" for avg 3-month volume

    Returns:
        DataFrame sorted by volume descending
    """
    print(f"Fetching {period} volume data from Yahoo Finance screener...")

    # Use screener API (same data as Yahoo Finance website)
    if period == "weekly":
        quotes = fetch_most_active_weekly(count=top_n)
    else:
        quotes = fetch_most_active_malaysia(count=top_n)

    if quotes:
        print(f"  Got {len(quotes)} stocks from Yahoo Finance screener")
        results = []
        for q in quotes:
            symbol = q.get("symbol", "")
            volume = q.get("regularMarketVolume", 0)
            close = q.get("regularMarketPrice", 0)
            high = q.get("regularMarketDayHigh", close)
            low = q.get("regularMarketDayLow", close)
            change_pct = q.get("regularMarketChangePercent", 0)
            name = q.get("shortName", q.get("longName", symbol))
            avg_vol_3m = q.get("averageDailyVolume3Month", 0)

            if period == "weekly":
                display_volume = avg_vol_3m if avg_vol_3m else volume
            else:
                display_volume = volume

            if display_volume and display_volume > 0:
                results.append({
                    "Symbol": symbol,
                    "Name": name[:25] if name else symbol,
                    "Close (RM)": round(float(close), 4) if close else 0,
                    "Volume": int(display_volume),
                    "High (RM)": round(float(high), 4) if high else 0,
                    "Low (RM)": round(float(low), 4) if low else 0,
                    "Change (%)": round(float(change_pct), 2) if change_pct else 0,
                })

        if results:
            df = pd.DataFrame(results)
            df = df.sort_values("Volume", ascending=False).reset_index(drop=True)
            df.index += 1
            return df.head(top_n)

    # Fallback: fetch individually from our stock list
    print("  Screener API unavailable, fetching individual stocks...")
    return _fetch_individual_stocks(top_n=top_n, period=period)


def _fetch_individual_stocks(top_n: int = 50, period: str = "daily") -> pd.DataFrame:
    """Fallback: fetch stocks individually from hardcoded list."""
    results = []
    symbols = list(KLSE_STOCKS.keys())
    failed = 0

    for i, symbol in enumerate(symbols):
        try:
            if period == "weekly":
                raw = fetch_chart_data(symbol, period="5d", interval="1d")
                if raw:
                    indicators = raw.get("indicators", {})
                    quotes = indicators.get("quote", [{}])[0]
                    closes = quotes.get("close", [])
                    volumes = quotes.get("volume", [])
                    highs = quotes.get("high", [])
                    lows = quotes.get("low", [])
                    meta = raw.get("meta", {})

                    total_volume = sum(v for v in volumes if v is not None and v > 0)

                    last_close = None
                    week_high = 0
                    week_low = float("inf")

                    for j in range(len(closes) - 1, -1, -1):
                        if closes[j] is not None:
                            last_close = closes[j]
                            break

                    for h in highs:
                        if h is not None and h > week_high:
                            week_high = h
                    for l in lows:
                        if l is not None and l < week_low:
                            week_low = l

                    prev_close = meta.get("chartPreviousClose", 0)
                    change_pct = 0
                    if prev_close and prev_close > 0 and last_close:
                        change_pct = ((last_close - prev_close) / prev_close) * 100

                    if total_volume > 0 and last_close:
                        results.append({
                            "Symbol": symbol,
                            "Name": KLSE_STOCKS.get(symbol, "Unknown"),
                            "Close (RM)": round(last_close, 4),
                            "Volume": int(total_volume),
                            "High (RM)": round(week_high, 4),
                            "Low (RM)": round(week_low, 4) if week_low != float("inf") else 0,
                            "Change (%)": round(change_pct, 2),
                        })
                    else:
                        failed += 1
                else:
                    failed += 1
            else:
                quote = get_stock_quote(symbol)
                if quote and quote.get("volume", 0) > 0:
                    results.append({
                        "Symbol": symbol,
                        "Name": KLSE_STOCKS.get(symbol, "Unknown"),
                        "Close (RM)": quote["close"],
                        "Volume": quote["volume"],
                        "High (RM)": quote["high"],
                        "Low (RM)": quote["low"],
                        "Change (%)": quote["change_pct"],
                    })
                else:
                    failed += 1
        except Exception:
            failed += 1

        if (i + 1) % 10 == 0:
            print(f"  Processed {i + 1}/{len(symbols)} stocks...")
            time.sleep(0.3)
        else:
            time.sleep(0.15)

    print(f"\n  Done! Got data for {len(results)} stocks ({failed} failed)")

    if not results:
        return pd.DataFrame()

    df = pd.DataFrame(results)
    df = df.sort_values("Volume", ascending=False).reset_index(drop=True)
    df.index += 1
    return df.head(top_n)


def display_top_volume(df: pd.DataFrame):
    """Display the top volume stocks in a formatted table."""
    if df.empty:
        return

    print("\n" + "=" * 90)
    print(f"  TOP {len(df)} KLSE STOCKS BY DAILY VOLUME")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 90)
    print(f"{'Rank':<5}{'Symbol':<10}{'Name':<22}{'Close (RM)':<12}{'Volume':>15}{'Change %':>10}")
    print("-" * 90)

    for rank, row in df.iterrows():
        change_str = f"{row['Change (%)']:+.2f}%"
        volume_str = f"{row['Volume']:,.0f}"
        print(f"{rank:<5}{row['Symbol']:<10}{row['Name']:<22}{row['Close (RM)']:<12.4f}{volume_str:>15}{change_str:>10}")

    print("-" * 90)
    print(f"  Total Volume (Top {len(df)}): {df['Volume'].sum():,.0f}")
    print(f"  Average Volume: {df['Volume'].mean():,.0f}")
    print()


def save_to_csv(df: pd.DataFrame, filename: str = "output/top_volume.csv"):
    """Save results to CSV file."""
    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index_label="Rank")
    print(f"Results saved to {filename}")


def main():
    print("=" * 60)
    print("  KLSE TOP 50 STOCKS BY DAILY VOLUME")
    print("=" * 60)

    df = get_top_volume_stocks(top_n=50)

    if not df.empty:
        display_top_volume(df)
        save_to_csv(df)


if __name__ == "__main__":
    main()
