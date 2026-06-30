"""
Rainbow Crossover Scanner — Finds stocks where Homily Rainbow lines converge
and Green(13) crosses from bottom to top.

Pattern: All 5 EMA lines (Red 3, Yellow 7, Green 13, Blue 21, White 55) converge,
then Green breaks upward through the cluster — bullish breakout signal.

Signals detected:
1. Green crossing above White from below (strongest: fastest crosses slowest)
2. Green crossing above Blue from below
3. All lines converging (tight cluster = about to explode)
4. Rainbow starting to fan out upward after convergence
"""

import numpy as np
from yahoo_api import fetch_chart_data
from homily_indicators import ema, sma
import time


def calculate_rainbow_lines(close, high, low, volume):
    """Calculate the 5 rainbow EMA lines."""
    vwp = (2 * close + high + low) / 4.0

    # Volume weight
    vol_ma = sma(volume, 20)
    vol_weight = np.ones(len(close))
    for i in range(20, len(close)):
        if vol_ma[i] > 0:
            vol_weight[i] = volume[i] / vol_ma[i]
    vol_weight_smooth = ema(vol_weight, 5)

    red = ema(vwp, 3)       # Fastest
    yellow = ema(vwp, 7)
    green = ema(vwp * vol_weight_smooth, 13)  # Volume-weighted
    blue = ema(vwp, 21)
    white = ema(vwp, 55)    # Slowest

    return red, yellow, green, blue, white


def detect_rainbow_crossover(symbol: str, name: str = "") -> dict:
    """
    Detect Rainbow crossover pattern for a stock.

    Looks for:
    - Lines converging (tight spread)
    - Green crossing above Blue/White from below
    - Rainbow starting to fan out upward

    Returns dict with signal info, or None if no signal.
    """
    raw = fetch_chart_data(symbol, period="6mo", interval="1d")
    if not raw:
        return None

    try:
        indicators = raw.get("indicators", {})
        quotes = indicators.get("quote", [{}])[0]
        closes = quotes.get("close", [])
        highs = quotes.get("high", [])
        lows = quotes.get("low", [])
        volumes = quotes.get("volume", [])

        # Filter valid
        valid = [(c, h, l, v) for c, h, l, v in zip(closes, highs, lows, volumes)
                 if c is not None and h is not None and l is not None and v is not None and v > 0]

        if len(valid) < 60:
            return None

        close = np.array([d[0] for d in valid])
        high = np.array([d[1] for d in valid])
        low = np.array([d[2] for d in valid])
        volume = np.array([d[3] for d in valid], dtype=float)

        red, yellow, green, blue, white = calculate_rainbow_lines(close, high, low, volume)

        n = len(close)
        signals = []
        score = 0

        # Check last 5 days for crossover
        for i in range(max(n - 5, 55), n):
            # Green crosses above White (strongest signal)
            if i > 0 and green[i] > white[i] and green[i - 1] <= white[i - 1]:
                signals.append("Green↑White (Strong)")
                score += 40

            # Green crosses above Blue
            if i > 0 and green[i] > blue[i] and green[i - 1] <= blue[i - 1]:
                signals.append("Green↑Blue")
                score += 30

            # Red crosses above White
            if i > 0 and red[i] > white[i] and red[i - 1] <= white[i - 1]:
                signals.append("Red↑White")
                score += 20

            # Yellow crosses above Blue
            if i > 0 and yellow[i] > blue[i] and yellow[i - 1] <= blue[i - 1]:
                signals.append("Yellow↑Blue")
                score += 15

        # Check convergence (all lines within 3% of each other)
        last_spread = (max(red[-1], yellow[-1], green[-1], blue[-1], white[-1]) -
                       min(red[-1], yellow[-1], green[-1], blue[-1], white[-1]))
        spread_pct = last_spread / close[-1] * 100

        if spread_pct < 2:
            signals.append("Tight Convergence")
            score += 25
        elif spread_pct < 4:
            signals.append("Converging")
            score += 10

        # Check if rainbow is fanning out upward (Red > Yellow > Green > Blue > White)
        if red[-1] > yellow[-1] > green[-1] > blue[-1] > white[-1]:
            signals.append("Rainbow Up ↑")
            score += 20
        elif red[-1] > yellow[-1] > green[-1] > blue[-1]:
            signals.append("Partial Rainbow Up")
            score += 10

        # Green above White currently (trend confirmed)
        if green[-1] > white[-1] and green[-2] > white[-2]:
            score += 10

        # Price above all lines (bullish)
        if close[-1] > max(red[-1], yellow[-1], green[-1], blue[-1], white[-1]):
            signals.append("Price above all MAs")
            score += 15

        if not signals or score < 20:
            return None

        # Recent price change
        price_5d = (close[-1] - close[-6]) / close[-6] * 100 if n > 6 else 0
        price_20d = (close[-1] - close[-21]) / close[-21] * 100 if n > 21 else 0

        # Volume trend (last 30 days)
        vol_30 = volume[-30:] if n >= 30 else volume
        vol_x = np.arange(len(vol_30))
        vol_slope, _ = np.polyfit(vol_x, vol_30, 1)
        vol_slope_pct = vol_slope / np.mean(vol_30) * 100
        early_vol = np.mean(vol_30[:10])
        recent_vol = np.mean(vol_30[-10:])
        vol_growth = (recent_vol - early_vol) / (early_vol + 1) * 100

        # Bonus for volume increasing
        if vol_growth > 20:
            score += 15
            signals.append(f"Vol↑ +{vol_growth:.0f}%")
        elif vol_growth > 5:
            score += 5

        return {
            "symbol": symbol,
            "name": name,
            "price": round(float(close[-1]), 4),
            "score": round(score, 1),
            "signals": signals,
            "spread_pct": round(spread_pct, 2),
            "price_5d": round(price_5d, 2),
            "price_20d": round(price_20d, 2),
            "vol_growth": round(vol_growth, 1),
            "green_vs_white": round((green[-1] - white[-1]) / white[-1] * 100, 3),
            "trend": "Rainbow Up" if red[-1] > yellow[-1] > green[-1] > blue[-1] > white[-1] else
                     "Converging" if spread_pct < 3 else "Mixed",
        }

    except (KeyError, IndexError, TypeError, ValueError):
        return None


def scan_rainbow_crossover(symbols_dict: dict, max_stocks: int = 80) -> list:
    """Scan stocks for Rainbow crossover pattern."""
    results = []
    symbols = list(symbols_dict.items())[:max_stocks]

    for i, (symbol, name) in enumerate(symbols):
        result = detect_rainbow_crossover(symbol, name)
        if result:
            results.append(result)

        if (i + 1) % 5 == 0:
            time.sleep(0.5)
        else:
            time.sleep(0.2)

    results.sort(key=lambda x: -x["score"])
    return results
