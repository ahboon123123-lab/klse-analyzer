"""
Divergence Scanner - Finds stocks with potential DE (Deviation Expert) divergence.

Divergence types detected:
1. Bullish Divergence: Price making lower lows, but DE making higher lows (reversal up)
2. Bearish Divergence: Price making higher highs, but DE making lower highs (reversal down)
3. DE Crossover: DE crossing from negative to positive (buy signal)
4. DE Crossunder: DE crossing from positive to negative (sell signal)
"""

from yahoo_api import fetch_chart_data
import time


def calculate_de(closes: list) -> list:
    """Calculate Deviation Expert (EMA5 - EMA20) values."""
    if len(closes) < 20:
        return []

    # EMA calculation
    def ema(data, period):
        result = [data[0]]
        multiplier = 2 / (period + 1)
        for i in range(1, len(data)):
            val = (data[i] * multiplier) + (result[-1] * (1 - multiplier))
            result.append(val)
        return result

    ema5 = ema(closes, 5)
    ema20 = ema(closes, 20)
    de_values = [e5 - e20 for e5, e20 in zip(ema5, ema20)]
    return de_values


def calculate_macd(closes: list) -> tuple:
    """
    Calculate MACD values.
    Returns (macd_line, signal_line, histogram)
    """
    if len(closes) < 26:
        return [], [], []

    def ema(data, period):
        result = [data[0]]
        multiplier = 2 / (period + 1)
        for i in range(1, len(data)):
            val = (data[i] * multiplier) + (result[-1] * (1 - multiplier))
            result.append(val)
        return result

    ema12 = ema(closes, 12)
    ema26 = ema(closes, 26)
    macd_line = [e12 - e26 for e12, e26 in zip(ema12, ema26)]
    signal_line = ema(macd_line, 9)
    histogram = [m - s for m, s in zip(macd_line, signal_line)]

    return macd_line, signal_line, histogram


def detect_divergence(symbol: str, name: str = "") -> dict:
    """
    Analyze a stock for DE and MACD divergence signals.

    Returns dict with signal info or None if no signal.
    """
    raw = fetch_chart_data(symbol, period="3mo", interval="1d")
    if not raw:
        return None

    try:
        indicators = raw.get("indicators", {})
        quotes = indicators.get("quote", [{}])[0]
        closes = quotes.get("close", [])
        highs = quotes.get("high", [])
        lows = quotes.get("low", [])
        meta = raw.get("meta", {})

        # Filter None values
        valid_data = [(c, h, l) for c, h, l in zip(closes, highs, lows)
                      if c is not None and h is not None and l is not None]

        if len(valid_data) < 30:
            return None

        closes = [d[0] for d in valid_data]
        highs = [d[1] for d in valid_data]
        lows = [d[2] for d in valid_data]

        de_values = calculate_de(closes)
        macd_line, signal_line, histogram = calculate_macd(closes)

        if len(de_values) < 30:
            return None

        # Get recent values (last 20 days for analysis)
        recent_de = de_values[-20:]
        recent_closes = closes[-20:]
        recent_lows = lows[-20:]
        recent_highs = highs[-20:]

        last_price = closes[-1]
        last_de = de_values[-1]
        prev_de = de_values[-2]

        signals = []

        # ============ DE SIGNALS ============

        # --- DE Crossover (negative to positive) ---
        if prev_de <= 0 and last_de > 0:
            signals.append("DE_BULLISH_CROSS")

        # --- DE Crossunder (positive to negative) ---
        if prev_de >= 0 and last_de < 0:
            signals.append("DE_BEARISH_CROSS")

        # --- DE Bullish Divergence ---
        price_lows_first = min(recent_lows[:10])
        price_lows_last = min(recent_lows[10:])
        de_lows_first = min(recent_de[:10])
        de_lows_last = min(recent_de[10:])

        if price_lows_last < price_lows_first and de_lows_last > de_lows_first:
            signals.append("DE_BULLISH_DIVERGENCE")

        # --- DE Bearish Divergence ---
        price_highs_first = max(recent_highs[:10])
        price_highs_last = max(recent_highs[10:])
        de_highs_first = max(recent_de[:10])
        de_highs_last = max(recent_de[10:])

        if price_highs_last > price_highs_first and de_highs_last < de_highs_first:
            signals.append("DE_BEARISH_DIVERGENCE")

        # --- DE Recovery ---
        if last_de < 0 and last_de > prev_de and de_values[-3] > de_values[-4]:
            signals.append("DE_RECOVERY")

        # --- DE Strong Bull ---
        if last_de > 0 and last_de > prev_de > de_values[-3]:
            signals.append("DE_STRONG_BULL")

        # ============ MACD SIGNALS ============

        if len(macd_line) >= 20 and len(histogram) >= 20:
            recent_macd = macd_line[-20:]
            recent_hist = histogram[-20:]
            last_macd = macd_line[-1]
            prev_macd = macd_line[-2]
            last_signal = signal_line[-1]
            prev_signal = signal_line[-2]
            last_hist = histogram[-1]
            prev_hist = histogram[-2]

            # --- MACD Crossover (bullish) ---
            if prev_macd <= prev_signal and last_macd > last_signal:
                signals.append("MACD_BULLISH_CROSS")

            # --- MACD Crossunder (bearish) ---
            if prev_macd >= prev_signal and last_macd < last_signal:
                signals.append("MACD_BEARISH_CROSS")

            # --- MACD Bullish Divergence ---
            # Price lower lows, MACD higher lows
            macd_lows_first = min(recent_macd[:10])
            macd_lows_last = min(recent_macd[10:])

            if price_lows_last < price_lows_first and macd_lows_last > macd_lows_first:
                signals.append("MACD_BULLISH_DIVERGENCE")

            # --- MACD Bearish Divergence ---
            # Price higher highs, MACD lower highs
            macd_highs_first = max(recent_macd[:10])
            macd_highs_last = max(recent_macd[10:])

            if price_highs_last > price_highs_first and macd_highs_last < macd_highs_first:
                signals.append("MACD_BEARISH_DIVERGENCE")

            # --- MACD Histogram reversal (turning positive from negative) ---
            if prev_hist <= 0 and last_hist > 0:
                signals.append("MACD_HIST_BULLISH")

            # --- MACD Histogram turning negative ---
            if prev_hist >= 0 and last_hist < 0:
                signals.append("MACD_HIST_BEARISH")

        if not signals:
            return None

        # Determine overall signal direction
        bullish_signals = [s for s in signals if "BULLISH" in s or "RECOVERY" in s or "STRONG_BULL" in s]
        bearish_signals = [s for s in signals if "BEARISH" in s]

        if len(bullish_signals) > len(bearish_signals):
            direction = "BULLISH"
        elif len(bearish_signals) > len(bullish_signals):
            direction = "BEARISH"
        elif bullish_signals:
            direction = "BULLISH"
        else:
            direction = "BEARISH"

        return {
            "symbol": symbol,
            "name": name,
            "price": round(last_price, 4),
            "de_value": round(last_de, 4),
            "de_prev": round(prev_de, 4),
            "macd_value": round(macd_line[-1], 4) if macd_line else 0,
            "direction": direction,
            "signals": signals,
            "signal_count": len(signals),
            "signal_text": " + ".join(signals),
        }

    except (KeyError, IndexError, TypeError, ValueError):
        return None


def scan_top_stocks(symbols_dict: dict, max_stocks: int = 50) -> list:
    """
    Scan a list of stocks for DE divergence signals.

    Args:
        symbols_dict: Dict of {symbol: name}
        max_stocks: Max stocks to scan

    Returns:
        List of stocks with divergence signals, sorted by strength
    """
    results = []
    symbols = list(symbols_dict.items())[:max_stocks]

    for i, (symbol, name) in enumerate(symbols):
        signal = detect_divergence(symbol, name)
        if signal:
            results.append(signal)

        # Rate limiting
        if (i + 1) % 5 == 0:
            time.sleep(0.5)
        else:
            time.sleep(0.2)

    # Sort: most signals first, then bullish before bearish
    results.sort(key=lambda x: (-x["signal_count"], 0 if x["direction"] == "BULLISH" else 1))

    return results
