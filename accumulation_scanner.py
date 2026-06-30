"""
Accumulation Scanner — Finds stocks with slowly increasing volume + price uptrend.

Pattern: Institutional accumulation before breakout
- Volume increasing steadily (not spike) over 30 days
- Price trending up gradually (not volatile jumps)
- Low volatility relative to the move (quiet accumulation)

Scoring:
- Volume slope (positive = accumulating)
- Price slope (positive = uptrend)
- Smoothness (low volatility relative to move = quiet accumulation)
- Volume consistency (steady increase, not erratic)
"""

import numpy as np
from yahoo_api import fetch_chart_data
import time


def analyze_accumulation(symbol: str, name: str = "", days: int = 30) -> dict:
    """
    Analyze a stock for accumulation pattern.

    Returns dict with score and metrics, or None if no data.
    """
    raw = fetch_chart_data(symbol, period="3mo", interval="1d")
    if not raw:
        return None

    try:
        indicators = raw.get("indicators", {})
        quotes = indicators.get("quote", [{}])[0]
        closes = quotes.get("close", [])
        volumes = quotes.get("volume", [])

        # Filter valid data
        valid = [(c, v) for c, v in zip(closes, volumes)
                 if c is not None and v is not None and v > 0]

        if len(valid) < days:
            return None

        # Use last N days
        recent = valid[-days:]
        prices = np.array([p for p, _ in recent])
        vols = np.array([v for _, v in recent], dtype=float)

        # === 1. Volume Slope (is volume increasing?) ===
        x = np.arange(days)
        vol_slope, vol_intercept = np.polyfit(x, vols, 1)
        vol_slope_pct = vol_slope / np.mean(vols) * 100  # % increase per day

        # === 2. Price Slope (is price trending up?) ===
        price_slope, price_intercept = np.polyfit(x, prices, 1)
        price_change_pct = (prices[-1] - prices[0]) / prices[0] * 100

        # === 3. Price Smoothness (low volatility = quiet accumulation) ===
        daily_returns = np.diff(prices) / prices[:-1]
        volatility = np.std(daily_returns) * 100
        # Smoothness = price change / volatility (high = smooth trend)
        smoothness = abs(price_change_pct) / (volatility * np.sqrt(days) + 0.01)

        # === 4. Volume Consistency (R² of volume trend) ===
        vol_predicted = vol_slope * x + vol_intercept
        ss_res = np.sum((vols - vol_predicted) ** 2)
        ss_tot = np.sum((vols - np.mean(vols)) ** 2)
        vol_r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        # === 5. Recent volume vs early volume ===
        early_avg_vol = np.mean(vols[:days // 3])
        recent_avg_vol = np.mean(vols[-days // 3:])
        vol_growth = (recent_avg_vol - early_avg_vol) / (early_avg_vol + 1) * 100

        # === ACCUMULATION SCORE ===
        score = 0

        # Volume increasing (max 40 points)
        if vol_slope_pct > 0:
            score += min(vol_slope_pct * 10, 40)

        # Price trending up (max 30 points)
        if price_change_pct > 0:
            score += min(price_change_pct * 3, 30)

        # Smooth trend (max 20 points)
        score += min(smoothness * 10, 20)

        # Volume consistency (max 10 points)
        if vol_r_squared > 0:
            score += vol_r_squared * 10

        # Penalties
        if price_change_pct < 0:
            score -= 20  # Price going down
        if vol_slope_pct < 0:
            score -= 15  # Volume decreasing
        if volatility > 5:
            score -= 10  # Too volatile (not quiet)

        # Only return if it looks like accumulation
        if score < 15:
            return None

        # Determine stage
        if vol_growth > 50 and price_change_pct > 10:
            stage = "Late Accumulation (near breakout)"
        elif vol_growth > 20 and price_change_pct > 3:
            stage = "Active Accumulation"
        elif vol_growth > 0 and price_change_pct > 0:
            stage = "Early Accumulation"
        else:
            stage = "Possible Accumulation"

        return {
            "symbol": symbol,
            "name": name,
            "price": round(float(prices[-1]), 4),
            "score": round(score, 1),
            "stage": stage,
            "price_change_30d": round(price_change_pct, 2),
            "vol_growth_pct": round(vol_growth, 1),
            "vol_slope_pct": round(vol_slope_pct, 3),
            "smoothness": round(smoothness, 2),
            "volatility": round(volatility, 2),
            "vol_consistency": round(vol_r_squared * 100, 1),
            "avg_volume": int(np.mean(vols)),
        }

    except (KeyError, IndexError, TypeError, ValueError):
        return None


def scan_accumulation(symbols_dict: dict, max_stocks: int = 80, days: int = 30) -> list:
    """
    Scan stocks for accumulation pattern.

    Returns list sorted by accumulation score (highest first).
    """
    results = []
    symbols = list(symbols_dict.items())[:max_stocks]

    for i, (symbol, name) in enumerate(symbols):
        result = analyze_accumulation(symbol, name, days=days)
        if result:
            results.append(result)

        # Rate limiting
        if (i + 1) % 5 == 0:
            time.sleep(0.5)
        else:
            time.sleep(0.2)

    # Sort by score (highest first)
    results.sort(key=lambda x: -x["score"])

    return results
