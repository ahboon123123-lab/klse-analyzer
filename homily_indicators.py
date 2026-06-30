"""
Homily Chart Indicators - Reconstructed from INDICATOR_FORMULAS.md

Contains:
1. MCD-X (六彩游龙) - Capital Flow Model
2. QSW (趋势王) - Trend Expert
3. BLW (背离王) - Divergence Expert
4. Homily Rainbow (弘历彩虹) - Multi-Line Trend System
5. Homily Position (弘历进出) - Price-Volume Resistance
"""

import numpy as np
import pandas as pd


def ema(data, period):
    """Exponential Moving Average."""
    result = np.zeros(len(data))
    multiplier = 2.0 / (period + 1)
    result[0] = data[0]
    for i in range(1, len(data)):
        result[i] = (data[i] - result[i - 1]) * multiplier + result[i - 1]
    return result


def sma(data, period):
    """Simple Moving Average."""
    result = np.zeros(len(data))
    for i in range(period - 1, len(data)):
        result[i] = np.mean(data[i - period + 1:i + 1])
    return result


def atr(high, low, close, period=14):
    """Average True Range."""
    n = len(close)
    tr = np.zeros(n)
    for i in range(1, n):
        tr[i] = max(high[i] - low[i],
                    abs(high[i] - close[i - 1]),
                    abs(low[i] - close[i - 1]))
    return ema(tr, period)


# ============================================================
# MCD-X (六彩游龙) - Capital Flow Model
# ============================================================

def calculate_mcdx(close, high, low, volume, N=20, M=5):
    """
    MCD-X Capital Flow Model.

    Classifies money flow by position profitability using price range normalization.

    Returns dict with: floating_capital, profitable_capital, loss_capital
    """
    n = len(close)
    if n < N + 1:
        return None

    # Price range normalization
    floating = np.zeros(n)
    profitable = np.zeros(n)
    loss = np.zeros(n)

    for i in range(N, n):
        period_high = np.max(high[i - N:i + 1])
        period_low = np.min(low[i - N:i + 1])
        price_range = period_high - period_low

        if price_range == 0:
            floating[i] = 33.3
            profitable[i] = 33.3
            loss[i] = 33.3
            continue

        # Profit ratio: how far above the low
        profit_ratio = (close[i] - period_low) / price_range
        # Loss ratio: how far below the high
        loss_ratio = (period_high - close[i]) / price_range

        # Amount (price * volume proxy)
        amount = close[i] * volume[i]

        profitable[i] = profit_ratio * 100
        loss[i] = loss_ratio * 100
        floating[i] = 100 - profitable[i] - loss[i]
        # Ensure no negative
        floating[i] = max(0, floating[i])

    # Smooth with EMA
    profitable_smooth = ema(profitable, M)
    loss_smooth = ema(loss, M)
    floating_smooth = ema(floating, M)

    return {
        "profitable": profitable_smooth,  # Red
        "loss": loss_smooth,              # Green
        "floating": floating_smooth,      # Yellow
    }


# ============================================================
# QSW (趋势王) - Trend Expert
# ============================================================

def calculate_qsw(close, high, low, volume, short=5, mid=13, long=34, signal=5):
    """
    QSW (趋势王) - Volume-weighted EMA crossover trend system.

    Similar to MACD but with volume momentum as a multiplier.

    Returns dict with: qsw, signal_line, histogram, trend
    """
    n = len(close)
    if n < long + signal:
        return None

    # Weighted price
    wp = (2 * close + high + low) / 4.0

    # Volume factor
    vol_ma = sma(volume, mid)
    vol_ratio = np.ones(n)
    for i in range(mid, n):
        if vol_ma[i] > 0:
            vol_ratio[i] = volume[i] / vol_ma[i]

    # EMA lines
    fast_ema = ema(wp, short)
    slow_ema = ema(wp, long)

    # Trend momentum (normalized)
    trend_momentum = np.zeros(n)
    for i in range(long, n):
        if slow_ema[i] > 0:
            trend_momentum[i] = (fast_ema[i] - slow_ema[i]) / slow_ema[i] * 100

    # Apply volume weight
    vol_weighted = trend_momentum * np.sqrt(np.clip(vol_ratio, 0.1, 3.0))

    # QSW line and signal
    qsw_line = ema(vol_weighted, signal)
    qsw_signal = ema(qsw_line, signal)
    histogram = qsw_line - qsw_signal

    # Trend classification
    trend = []
    for i in range(n):
        if qsw_line[i] > qsw_signal[i] and qsw_line[i] > 0:
            trend.append("Strong Up")
        elif qsw_line[i] > qsw_signal[i]:
            trend.append("Recovering")
        elif qsw_line[i] < qsw_signal[i] and qsw_line[i] < 0:
            trend.append("Strong Down")
        else:
            trend.append("Weakening")

    return {
        "qsw": qsw_line,
        "signal": qsw_signal,
        "histogram": histogram,
        "trend": trend,
    }


# ============================================================
# BLW (背离王) - Divergence Expert
# ============================================================

def calculate_blw(close, high, low, rsi_period=14, lookback=60, pivot_bars=5):
    """
    BLW (背离王) - Multi-oscillator divergence detection.

    Scans RSI and MACD for pivot-based divergences.

    Returns dict with: bullish_div, bearish_div, rsi, score
    """
    n = len(close)
    if n < lookback:
        return None

    # RSI
    rsi = np.zeros(n)
    gains = np.zeros(n)
    losses = np.zeros(n)
    for i in range(1, n):
        change = close[i] - close[i - 1]
        if change > 0:
            gains[i] = change
        else:
            losses[i] = abs(change)

    avg_gain = np.zeros(n)
    avg_loss = np.zeros(n)
    if n > rsi_period:
        avg_gain[rsi_period] = np.mean(gains[1:rsi_period + 1])
        avg_loss[rsi_period] = np.mean(losses[1:rsi_period + 1])
        for i in range(rsi_period + 1, n):
            avg_gain[i] = (avg_gain[i - 1] * (rsi_period - 1) + gains[i]) / rsi_period
            avg_loss[i] = (avg_loss[i - 1] * (rsi_period - 1) + losses[i]) / rsi_period
        for i in range(rsi_period, n):
            if avg_loss[i] == 0:
                rsi[i] = 100
            else:
                rsi[i] = 100 - (100 / (1 + avg_gain[i] / avg_loss[i]))

    # MACD histogram
    ema12 = ema(close, 12)
    ema26 = ema(close, 26)
    dif = ema12 - ema26
    dea = ema(dif, 9)
    macd_hist = (dif - dea) * 2

    # Find pivot points
    def find_pivots(data, bars, ptype):
        pivots = []
        for i in range(bars, len(data) - bars):
            window = data[i - bars:i + bars + 1]
            if ptype == "high" and data[i] == np.max(window):
                pivots.append(i)
            elif ptype == "low" and data[i] == np.min(window):
                pivots.append(i)
        return pivots

    price_highs = find_pivots(high, pivot_bars, "high")
    price_lows = find_pivots(low, pivot_bars, "low")

    bullish_div = np.zeros(n)
    bearish_div = np.zeros(n)

    # Check bearish divergence (price higher high, RSI lower high)
    for i in range(len(price_highs) - 1):
        p1, p2 = price_highs[i], price_highs[i + 1]
        if p2 - p1 < 5 or p2 >= n:
            continue
        if high[p2] > high[p1] and rsi[p2] < rsi[p1] and rsi[p2] > 50:
            bearish_div[p2] = 1
            if macd_hist[p2] < macd_hist[p1]:
                bearish_div[p2] = 2  # Double confirmed

    # Check bullish divergence (price lower low, RSI higher low)
    for i in range(len(price_lows) - 1):
        p1, p2 = price_lows[i], price_lows[i + 1]
        if p2 - p1 < 5 or p2 >= n:
            continue
        if low[p2] < low[p1] and rsi[p2] > rsi[p1] and rsi[p2] < 50:
            bullish_div[p2] = 1
            if macd_hist[p2] > macd_hist[p1]:
                bullish_div[p2] = 2  # Double confirmed

    return {
        "bullish_div": bullish_div,
        "bearish_div": bearish_div,
        "rsi": rsi,
        "macd_hist": macd_hist,
    }


# ============================================================
# Homily Rainbow (弘历彩虹) - 5-Color Trend System
# ============================================================

def calculate_rainbow(close, high, low, volume, p1=3, p2=7, p3=13, p4=21, p5=55):
    """
    Homily Rainbow - 5-period cascaded EMA system with volume weighting.

    Returns dict with: red, yellow, green, blue, white lines + trend signal
    """
    n = len(close)
    if n < p5 + 1:
        return None

    # Volume-weighted price
    vwp = (2 * close + high + low) / 4.0

    # Volume factor
    vol_ma = sma(volume, 20)
    vol_weight = np.ones(n)
    for i in range(20, n):
        if vol_ma[i] > 0:
            vol_weight[i] = volume[i] / vol_ma[i]
    vol_weight_smooth = ema(vol_weight, 5)

    # Rainbow lines
    red = ema(vwp, p1)
    yellow = ema(vwp, p2)
    green = ema(vwp * vol_weight_smooth, p3)
    blue = ema(vwp, p4)
    white = ema(vwp, p5)

    # Value center
    value_center = (red + yellow + green + blue + white) / 5.0

    # Trend signal
    trend = []
    for i in range(n):
        if red[i] > yellow[i] > green[i] > blue[i] > white[i]:
            trend.append("Rainbow Up")
        elif red[i] < yellow[i] < green[i] < blue[i] < white[i]:
            trend.append("Rainbow Down")
        elif abs(red[i] - white[i]) / (white[i] + 0.0001) < 0.02:
            trend.append("Converging")
        else:
            trend.append("Mixed")

    return {
        "red": red,
        "yellow": yellow,
        "green": green,
        "blue": blue,
        "white": white,
        "value_center": value_center,
        "trend": trend,
    }


# ============================================================
# Homily Position (弘历进出) - VWMA Life Line + ATR Bands
# ============================================================

def calculate_position(close, high, low, volume, life_n=13, band_n=21, signal_n=5):
    """
    Homily Position - VWMA "life line" with ATR resonance bands.

    Returns dict with: life_line, upper_band, lower_band, signals
    """
    n = len(close)
    if n < band_n + signal_n:
        return None

    # Life Line (VWMA)
    vwma = np.zeros(n)
    for i in range(life_n, n):
        vol_sum = np.sum(volume[i - life_n:i])
        if vol_sum > 0:
            vwma[i] = np.sum(close[i - life_n:i] * volume[i - life_n:i]) / vol_sum
        else:
            vwma[i] = close[i]

    life_line = ema(vwma, signal_n)

    # ATR for bands
    atr_val = atr(high, low, close, band_n)

    # Resonance bands
    upper_band = life_line + atr_val * 1.5
    lower_band = life_line - atr_val * 1.5

    # Signals
    signals = []
    for i in range(1, n):
        life_up = life_line[i] > life_line[i - 1]
        life_down = life_line[i] < life_line[i - 1]

        if life_up and close[i] > life_line[i] and close[i - 1] <= life_line[i - 1]:
            signals.append("★ Increase")
        elif life_down and close[i] < life_line[i] and close[i - 1] >= life_line[i - 1]:
            signals.append("★ Stop Loss")
        elif close[i] > upper_band[i] and life_up:
            signals.append("Hold Stock")
        elif close[i] < lower_band[i] and life_down:
            signals.append("Hold Cash")
        elif life_up:
            signals.append("Uptrend")
        elif life_down:
            signals.append("Downtrend")
        else:
            signals.append("Neutral")

    signals.insert(0, "Neutral")  # First bar

    return {
        "life_line": life_line,
        "upper_band": upper_band,
        "lower_band": lower_band,
        "signals": signals,
    }


# ============================================================
# Section 7: BANKER HUNTER (庄家猎手) Module
# ============================================================

def wilders_sma(data, period):
    """Wilder's smoothing (SMA in TDX style with weight=1)."""
    result = np.zeros(len(data))
    result[0] = data[0]
    for i in range(1, len(data)):
        result[i] = (result[i - 1] * (period - 1) + data[i]) / period
    return result


def calculate_profit_line(close, high, low, volume, period=60):
    """
    Profit Line (获利线/profitLine)
    Estimates the average cost basis of profitable positions.
    The price where ~80% of holders are profitable.
    """
    n = len(close)
    profit_line = np.zeros(n)

    for i in range(period, n):
        weights = []
        prices = []
        for j in range(i - period, i):
            avg_price = (high[j] + low[j] + close[j]) / 3.0
            if avg_price < close[i]:  # Profitable position
                weights.append(volume[j])
                prices.append(avg_price)

        if weights and sum(weights) > 0:
            profit_line[i] = np.average(prices, weights=weights)
        else:
            profit_line[i] = close[i]

    return profit_line


def calculate_banker_cost(close, high, low, volume, period=120):
    """
    Banker Cost Line (庄家成本线/bankerCostLine)
    Estimates banker's average entry price using VWAP weighted by large-volume days.
    """
    n = len(close)
    cost_line = np.zeros(n)
    amount = close * volume  # Proxy for daily amount

    vol_ma20 = sma(volume, 20)

    for i in range(period, n):
        # Weight by large volume days (banker accumulation)
        big_amount = 0.0
        big_vol = 0.0
        normal_amount = 0.0
        normal_vol = 0.0

        for j in range(i - period, i):
            if volume[j] > vol_ma20[j] * 1.5:
                big_amount += amount[j]
                big_vol += volume[j]
            else:
                normal_amount += amount[j]
                normal_vol += volume[j]

        # Blend: 70% weight to large-volume days, 30% to normal
        total_amount = big_amount * 0.7 + normal_amount * 0.3
        total_vol = big_vol * 0.7 + normal_vol * 0.3

        if total_vol > 0:
            cost_line[i] = total_amount / total_vol
        else:
            cost_line[i] = close[i]

    return cost_line


def calculate_banker_control(close, volume, capital, period=30):
    """
    Banker Controlling Line (庄家控盘线/banker_controlling_line)
    Measures how tightly the banker controls the float.
    High value = low free float, banker dominates.
    """
    n = len(close)
    control = np.zeros(n)

    turnover = volume / (capital + 1) * 100  # Daily turnover %
    avg_turnover = sma(turnover, 20)

    for i in range(20, n):
        # Price stability
        if close[i - 1] > 0:
            price_change = abs(close[i] - close[i - 1]) / close[i - 1]
        else:
            price_change = 0
        stability = 1 - min(price_change * 10, 1)

        # Low turnover with stable price = high control
        if avg_turnover[i] > 0:
            turnover_ratio = 1 - min(turnover[i] / (avg_turnover[i] + 0.001), 2) / 2
        else:
            turnover_ratio = 0

        control[i] = max(0, turnover_ratio * stability * 100)

    return ema(control, period)


def calculate_banker_holding(close, open_price, volume, capital, period=120):
    """
    Banker Holding Position Line (庄家持仓线/banker_holding_position_line)
    Estimates institutional holding percentage.
    Large volume on up-days = accumulation, on down-days = distribution.
    """
    n = len(close)
    holding = np.zeros(n)

    vol_ma5 = sma(volume, 5)

    for i in range(period, n):
        accumulated = 0.0
        distributed = 0.0

        for j in range(i - period, i):
            if volume[j] > vol_ma5[j] * 1.5:
                if close[j] > open_price[j]:  # Up day = accumulation
                    accumulated += volume[j]
                else:  # Down day = distribution
                    distributed += volume[j]

        net = accumulated - distributed
        cap = capital[i] if hasattr(capital, '__len__') else capital
        if cap > 0:
            holding[i] = net / cap * 100

    # Smooth and bound
    holding_line = ema(np.clip(holding, 0, 100), 20)
    return holding_line


def calculate_wash_out(close, low, high, volume, period=34):
    """
    Wash Out / Shakeout Detection (洗盘/zlxp)
    Detects when banker deliberately shakes out weak holders.
    Price drops on declining volume without breaking support.
    """
    n = len(close)
    wash = np.zeros(n)

    # VAR method from TDX
    var1 = np.roll(low, 1)
    var1[0] = low[0]

    abs_diff = np.abs(low - var1)
    max_diff = np.maximum(low - var1, 0)

    sma_abs = wilders_sma(abs_diff, 13)
    sma_max = wilders_sma(max_diff, 13)

    var2 = np.where(sma_max > 0, sma_abs / sma_max * 4, 0)
    var3 = ema(var2, 13)

    # LLV(LOW, period)
    var4 = np.zeros(n)
    for i in range(period, n):
        var4[i] = np.min(low[i - period:i + 1])

    var5_raw = np.where(low <= var4, var3, 0)
    var5 = ema(var5_raw, 3)

    # Wash: var5 declining from peak
    for i in range(1, n):
        if var5[i] < var5[i - 1] and var5[i] > 0:
            wash[i] = var5[i]

    return wash


def calculate_banker_zlcc(close, high, low):
    """
    Banker Holding Display (庄家持仓/zlcc)
    Uses the V1-V4 EMA method for accumulation/distribution ratio.
    """
    n = len(close)

    v1 = (close * 2 + high + low) / 4 * 10
    v2 = ema(v1, 13) - ema(v1, 34)
    v3 = ema(v2, 5)
    v4 = 2 * (v2 - v3) * 5.5

    # Accumulation (V4 > 0) vs Distribution (V4 < 0)
    acc = ema(np.maximum(v4, 0), 30)
    dist = ema(np.maximum(-v4, 0), 30)

    # Banker holding %
    total = acc + dist
    zlcc = np.where(total > 0, acc / total * 100, 50)

    return zlcc
