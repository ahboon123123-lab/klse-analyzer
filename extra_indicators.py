"""
Extra Technical Indicators - Batch Enhancement

Contains:
- KDJ (popular Chinese TA oscillator)
- OBV (On-Balance Volume)
- Ichimoku Cloud
- Support/Resistance levels
- Fibonacci Retracement
- Market Mood (breadth indicator)
"""

import numpy as np


def calculate_kdj(high, low, close, n=9, m1=3, m2=3):
    """
    KDJ Indicator (随机指标).
    Popular in Chinese/Asian markets. Similar to Stochastic but with J line.
    
    K = smoothed %K
    D = smoothed K
    J = 3*K - 2*D (amplified divergence)
    
    J > 100 = overbought, J < 0 = oversold
    Golden cross (K crosses above D) = Buy
    """
    length = len(close)
    rsv = np.zeros(length)
    k = np.zeros(length)
    d = np.zeros(length)
    j = np.zeros(length)

    k[0] = 50
    d[0] = 50

    for i in range(n - 1, length):
        lowest = np.min(low[i - n + 1:i + 1])
        highest = np.max(high[i - n + 1:i + 1])
        if highest != lowest:
            rsv[i] = (close[i] - lowest) / (highest - lowest) * 100
        else:
            rsv[i] = 50

        k[i] = (m1 - 1) / m1 * k[i - 1] + 1 / m1 * rsv[i]
        d[i] = (m2 - 1) / m2 * d[i - 1] + 1 / m2 * k[i]
        j[i] = 3 * k[i] - 2 * d[i]

    return k, d, j


def calculate_obv(close, volume):
    """
    On-Balance Volume (OBV).
    Cumulative volume: adds volume on up days, subtracts on down days.
    Rising OBV = accumulation, Falling OBV = distribution.
    """
    n = len(close)
    obv = np.zeros(n)

    for i in range(1, n):
        if close[i] > close[i - 1]:
            obv[i] = obv[i - 1] + volume[i]
        elif close[i] < close[i - 1]:
            obv[i] = obv[i - 1] - volume[i]
        else:
            obv[i] = obv[i - 1]

    return obv


def calculate_ichimoku(high, low, close, tenkan=9, kijun=26, senkou_b=52):
    """
    Ichimoku Cloud (一目均衡表).
    
    - Tenkan-sen (Conversion): (9-high + 9-low) / 2
    - Kijun-sen (Base): (26-high + 26-low) / 2
    - Senkou Span A: (Tenkan + Kijun) / 2, shifted 26 forward
    - Senkou Span B: (52-high + 52-low) / 2, shifted 26 forward
    - Cloud: area between Span A and B
    """
    n = len(close)
    tenkan_sen = np.zeros(n)
    kijun_sen = np.zeros(n)
    senkou_a = np.zeros(n)
    senkou_b_line = np.zeros(n)

    for i in range(tenkan - 1, n):
        tenkan_sen[i] = (np.max(high[i - tenkan + 1:i + 1]) + np.min(low[i - tenkan + 1:i + 1])) / 2

    for i in range(kijun - 1, n):
        kijun_sen[i] = (np.max(high[i - kijun + 1:i + 1]) + np.min(low[i - kijun + 1:i + 1])) / 2

    for i in range(senkou_b - 1, n):
        senkou_b_line[i] = (np.max(high[i - senkou_b + 1:i + 1]) + np.min(low[i - senkou_b + 1:i + 1])) / 2

    # Senkou A = midpoint of Tenkan and Kijun (shifted 26 forward in display)
    for i in range(kijun - 1, n):
        senkou_a[i] = (tenkan_sen[i] + kijun_sen[i]) / 2

    return {
        "tenkan": tenkan_sen,
        "kijun": kijun_sen,
        "senkou_a": senkou_a,
        "senkou_b": senkou_b_line,
    }


def calculate_support_resistance(high, low, close, lookback=60, num_levels=3):
    """
    Support and Resistance levels.
    Uses pivot points and volume-price clustering.
    """
    n = len(close)
    if n < lookback:
        return [], []

    recent_high = high[-lookback:]
    recent_low = low[-lookback:]
    recent_close = close[-lookback:]

    # Find pivot highs and lows
    pivot_highs = []
    pivot_lows = []
    window = 5

    for i in range(window, lookback - window):
        if recent_high[i] == np.max(recent_high[i - window:i + window + 1]):
            pivot_highs.append(recent_high[i])
        if recent_low[i] == np.min(recent_low[i - window:i + window + 1]):
            pivot_lows.append(recent_low[i])

    # Cluster nearby levels (within 2%)
    def cluster_levels(levels, threshold=0.02):
        if not levels:
            return []
        levels = sorted(levels)
        clusters = []
        current_cluster = [levels[0]]
        for i in range(1, len(levels)):
            if (levels[i] - current_cluster[0]) / current_cluster[0] < threshold:
                current_cluster.append(levels[i])
            else:
                clusters.append(np.mean(current_cluster))
                current_cluster = [levels[i]]
        clusters.append(np.mean(current_cluster))
        return clusters

    resistance = cluster_levels(pivot_highs)[-num_levels:] if pivot_highs else []
    support = cluster_levels(pivot_lows)[:num_levels] if pivot_lows else []

    return support, resistance


def calculate_fibonacci(high, low, close, lookback=60):
    """
    Fibonacci Retracement levels.
    Based on the most recent significant swing.
    """
    n = len(close)
    if n < lookback:
        return {}

    # Find the highest high and lowest low in lookback
    recent_high = np.max(high[-lookback:])
    recent_low = np.min(low[-lookback:])
    diff = recent_high - recent_low

    # Determine if uptrend or downtrend
    if close[-1] > (recent_high + recent_low) / 2:
        # Uptrend: retracements from high
        return {
            "trend": "up",
            "high": round(float(recent_high), 4),
            "low": round(float(recent_low), 4),
            "fib_0": round(float(recent_high), 4),
            "fib_236": round(float(recent_high - diff * 0.236), 4),
            "fib_382": round(float(recent_high - diff * 0.382), 4),
            "fib_500": round(float(recent_high - diff * 0.500), 4),
            "fib_618": round(float(recent_high - diff * 0.618), 4),
            "fib_786": round(float(recent_high - diff * 0.786), 4),
            "fib_100": round(float(recent_low), 4),
        }
    else:
        # Downtrend: retracements from low
        return {
            "trend": "down",
            "high": round(float(recent_high), 4),
            "low": round(float(recent_low), 4),
            "fib_0": round(float(recent_low), 4),
            "fib_236": round(float(recent_low + diff * 0.236), 4),
            "fib_382": round(float(recent_low + diff * 0.382), 4),
            "fib_500": round(float(recent_low + diff * 0.500), 4),
            "fib_618": round(float(recent_low + diff * 0.618), 4),
            "fib_786": round(float(recent_low + diff * 0.786), 4),
            "fib_100": round(float(recent_high), 4),
        }


def calculate_market_mood(advances, declines, unchanged, volume_up, volume_down):
    """
    Market Mood / Breadth indicator.
    
    Combines advance/decline ratio with volume flow.
    Score: -100 (extreme fear) to +100 (extreme greed)
    """
    total = advances + declines + unchanged
    if total == 0:
        return 0, "Neutral"

    # Advance/Decline ratio
    ad_ratio = (advances - declines) / total * 100

    # Volume flow
    total_vol = volume_up + volume_down
    vol_ratio = (volume_up - volume_down) / total_vol * 100 if total_vol > 0 else 0

    # Combined mood score
    mood_score = ad_ratio * 0.6 + vol_ratio * 0.4

    # Classification
    if mood_score > 50:
        mood = "Extreme Greed"
    elif mood_score > 20:
        mood = "Greed"
    elif mood_score > -20:
        mood = "Neutral"
    elif mood_score > -50:
        mood = "Fear"
    else:
        mood = "Extreme Fear"

    return round(mood_score, 1), mood
