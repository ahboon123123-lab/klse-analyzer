"""
Buy/Sell Signal Engine — Combines all indicators into a clear verdict.

Scoring system:
- Each indicator votes: +1 (Buy), -1 (Sell), 0 (Neutral)
- Weighted by reliability in volatile markets
- Final score determines: STRONG BUY / BUY / HOLD / SELL / STRONG SELL
- Confidence % based on how many indicators agree

Designed for volatile markets: emphasizes momentum reversal + volume confirmation.
"""

from yahoo_api import get_stock_history
from analyzer import StockAnalyzer
import numpy as np


# Indicator weights (higher = more trusted in volatile markets)
WEIGHTS = {
    "RSI": 1.5,           # Good for overbought/oversold in volatile markets
    "MACD": 1.5,          # Trend + momentum crossover
    "Parabolic_SAR": 1.0, # Trend following
    "Stochastic": 1.2,    # Short-term reversal
    "Williams_R": 1.0,    # Overbought/oversold
    "CCI": 1.0,           # Extreme moves
    "ADX": 0.8,           # Trend strength (less useful for timing)
    "Momentum": 1.2,      # Direct price momentum
    "DE": 1.5,            # Deviation Expert (EMA5-EMA20 fund flow)
    "L3_Banker": 1.3,     # Institutional behavior
    "MCDX": 1.0,          # Chip distribution
    "QSW": 1.5,           # Volume-weighted trend
    "Rainbow": 1.2,       # Multi-timeframe alignment
    "Position": 1.5,      # Life line signals (★Increase/★StopLoss)
    "Banker_Holding": 1.0, # Institutional position
    "Banker_Control": 0.8, # Float control
    "BLW_Divergence": 2.0, # Divergence (very reliable in volatile markets)
}


def generate_signal(symbol: str, period: str = "6mo") -> dict:
    """
    Generate a comprehensive Buy/Sell signal for a stock.

    Returns:
    {
        "symbol": "1023.KL",
        "verdict": "BUY" | "SELL" | "HOLD" | "STRONG BUY" | "STRONG SELL",
        "score": float (-100 to +100),
        "confidence": float (0-100%),
        "reasons_buy": [...],
        "reasons_sell": [...],
        "indicators": {...},
        "risk_level": "LOW" | "MEDIUM" | "HIGH",
        "entry_price": float,
        "stop_loss": float,
        "target_price": float,
    }
    """
    if not symbol.endswith(".KL"):
        symbol += ".KL"

    df = get_stock_history(symbol, period=period)
    if df.empty or len(df) < 30:
        return {"error": f"Not enough data for {symbol}"}

    analyzer = StockAnalyzer(df, symbol)
    latest = analyzer.df.iloc[-1]
    prev = analyzer.df.iloc[-2] if len(analyzer.df) > 1 else latest

    votes = []  # List of (indicator_name, vote, weight, reason)

    # === RSI ===
    rsi = latest.get("RSI")
    if rsi == rsi:  # Not NaN
        if rsi < 25:
            votes.append(("RSI", +1, WEIGHTS["RSI"] * 1.5, f"RSI {rsi:.1f} — Deeply Oversold"))
        elif rsi < 35:
            votes.append(("RSI", +1, WEIGHTS["RSI"], f"RSI {rsi:.1f} — Oversold"))
        elif rsi > 75:
            votes.append(("RSI", -1, WEIGHTS["RSI"] * 1.5, f"RSI {rsi:.1f} — Deeply Overbought"))
        elif rsi > 65:
            votes.append(("RSI", -1, WEIGHTS["RSI"], f"RSI {rsi:.1f} — Overbought"))
        else:
            votes.append(("RSI", 0, WEIGHTS["RSI"] * 0.5, f"RSI {rsi:.1f} — Neutral"))

    # === MACD ===
    macd = latest.get("MACD")
    macd_sig = latest.get("MACD_Signal")
    prev_macd = prev.get("MACD")
    prev_macd_sig = prev.get("MACD_Signal")
    if macd == macd and macd_sig == macd_sig:
        if prev_macd <= prev_macd_sig and macd > macd_sig:
            votes.append(("MACD", +1, WEIGHTS["MACD"] * 1.5, "MACD Golden Cross ↑"))
        elif prev_macd >= prev_macd_sig and macd < macd_sig:
            votes.append(("MACD", -1, WEIGHTS["MACD"] * 1.5, "MACD Dead Cross ↓"))
        elif macd > macd_sig:
            votes.append(("MACD", +1, WEIGHTS["MACD"], "MACD above Signal"))
        else:
            votes.append(("MACD", -1, WEIGHTS["MACD"], "MACD below Signal"))

    # === Parabolic SAR (Homily) ===
    color = latest.get("Homily_Color")
    if color == "red":
        votes.append(("Parabolic_SAR", +1, WEIGHTS["Parabolic_SAR"] * 1.5, "SAR: Buy Trigger (1st day uptrend)"))
    elif color == "blue":
        votes.append(("Parabolic_SAR", +1, WEIGHTS["Parabolic_SAR"], "SAR: Hold (uptrend continues)"))
    elif color == "yellow":
        votes.append(("Parabolic_SAR", -1, WEIGHTS["Parabolic_SAR"], "SAR: Cash/Sell (downtrend)"))

    # === Stochastic ===
    stoch_k = latest.get("Stoch_K")
    if stoch_k == stoch_k:
        if stoch_k < 20:
            votes.append(("Stochastic", +1, WEIGHTS["Stochastic"], f"Stoch {stoch_k:.0f} — Oversold"))
        elif stoch_k > 80:
            votes.append(("Stochastic", -1, WEIGHTS["Stochastic"], f"Stoch {stoch_k:.0f} — Overbought"))
        else:
            votes.append(("Stochastic", 0, WEIGHTS["Stochastic"] * 0.3, f"Stoch {stoch_k:.0f} — Neutral"))

    # === Williams %R ===
    wr = latest.get("Williams_R")
    if wr == wr:
        if wr < -80:
            votes.append(("Williams_R", +1, WEIGHTS["Williams_R"], f"W%R {wr:.0f} — Oversold"))
        elif wr > -20:
            votes.append(("Williams_R", -1, WEIGHTS["Williams_R"], f"W%R {wr:.0f} — Overbought"))

    # === CCI ===
    cci = latest.get("CCI")
    if cci == cci:
        if cci < -150:
            votes.append(("CCI", +1, WEIGHTS["CCI"] * 1.3, f"CCI {cci:.0f} — Extreme Oversold"))
        elif cci < -100:
            votes.append(("CCI", +1, WEIGHTS["CCI"], f"CCI {cci:.0f} — Oversold"))
        elif cci > 150:
            votes.append(("CCI", -1, WEIGHTS["CCI"] * 1.3, f"CCI {cci:.0f} — Extreme Overbought"))
        elif cci > 100:
            votes.append(("CCI", -1, WEIGHTS["CCI"], f"CCI {cci:.0f} — Overbought"))

    # === Momentum ===
    mom = latest.get("Momentum")
    if mom == mom:
        if mom > 0:
            votes.append(("Momentum", +1, WEIGHTS["Momentum"], f"Momentum +{mom:.4f} — Positive"))
        else:
            votes.append(("Momentum", -1, WEIGHTS["Momentum"], f"Momentum {mom:.4f} — Negative"))

    # === ADX (Trend Strength) ===
    adx = latest.get("ADX")
    plus_di = latest.get("Plus_DI")
    minus_di = latest.get("Minus_DI")
    if adx == adx and plus_di == plus_di and minus_di == minus_di:
        if adx > 25 and plus_di > minus_di:
            votes.append(("ADX", +1, WEIGHTS["ADX"], f"ADX {adx:.0f} — Strong Uptrend"))
        elif adx > 25 and minus_di > plus_di:
            votes.append(("ADX", -1, WEIGHTS["ADX"], f"ADX {adx:.0f} — Strong Downtrend"))

    # === Deviation Expert (EMA5 - EMA20) ===
    de = latest.get("DE_Value")
    prev_de = prev.get("DE_Value")
    if de == de:
        if prev_de <= 0 and de > 0:
            votes.append(("DE", +1, WEIGHTS["DE"] * 1.5, "DE crossed positive — Fund Inflow ↑"))
        elif prev_de >= 0 and de < 0:
            votes.append(("DE", -1, WEIGHTS["DE"] * 1.5, "DE crossed negative — Fund Outflow ↓"))
        elif de > 0 and de > prev_de:
            votes.append(("DE", +1, WEIGHTS["DE"], "DE positive & rising"))
        elif de < 0 and de < prev_de:
            votes.append(("DE", -1, WEIGHTS["DE"], "DE negative & falling"))
        elif de > 0:
            votes.append(("DE", +1, WEIGHTS["DE"] * 0.5, "DE positive"))
        else:
            votes.append(("DE", -1, WEIGHTS["DE"] * 0.5, "DE negative"))

    # === L3 Banker ===
    l3_sig = latest.get("L3_Banker_Signal")
    if l3_sig == "First Green":
        votes.append(("L3_Banker", +1, WEIGHTS["L3_Banker"] * 1.5, "L3: First Green — Entry Signal"))
    elif l3_sig == "Green":
        votes.append(("L3_Banker", +1, WEIGHTS["L3_Banker"], "L3: Green — Bullish"))
    elif l3_sig == "First Red":
        votes.append(("L3_Banker", -1, WEIGHTS["L3_Banker"] * 1.5, "L3: First Red — Exit Warning"))
    elif l3_sig == "Red":
        votes.append(("L3_Banker", -1, WEIGHTS["L3_Banker"], "L3: Red — Bearish"))

    # === QSW Trend Expert ===
    qsw = latest.get("QSW")
    qsw_trend = latest.get("QSW_Trend")
    if qsw == qsw and qsw_trend != "Not enough data":
        if "Strong Up" in str(qsw_trend):
            votes.append(("QSW", +1, WEIGHTS["QSW"], "QSW: Strong Uptrend"))
        elif "Recovering" in str(qsw_trend):
            votes.append(("QSW", +1, WEIGHTS["QSW"] * 0.7, "QSW: Recovering"))
        elif "Strong Down" in str(qsw_trend):
            votes.append(("QSW", -1, WEIGHTS["QSW"], "QSW: Strong Downtrend"))
        elif "Weakening" in str(qsw_trend):
            votes.append(("QSW", -1, WEIGHTS["QSW"] * 0.7, "QSW: Weakening"))

    # === Homily Rainbow ===
    rainbow = latest.get("Rainbow_Trend")
    if rainbow != "Not enough data":
        if rainbow == "Rainbow Up":
            votes.append(("Rainbow", +1, WEIGHTS["Rainbow"], "Rainbow: All EMAs aligned UP"))
        elif rainbow == "Rainbow Down":
            votes.append(("Rainbow", -1, WEIGHTS["Rainbow"], "Rainbow: All EMAs aligned DOWN"))

    # === Homily Position ===
    pos = latest.get("Position_Signal")
    if pos != "Not enough data":
        if "Increase" in str(pos):
            votes.append(("Position", +1, WEIGHTS["Position"] * 1.5, "Position: ★Increase Signal"))
        elif "Stop Loss" in str(pos):
            votes.append(("Position", -1, WEIGHTS["Position"] * 1.5, "Position: ★Stop Loss Signal"))
        elif "Hold Stock" in str(pos):
            votes.append(("Position", +1, WEIGHTS["Position"], "Position: Hold Stock"))
        elif "Hold Cash" in str(pos):
            votes.append(("Position", -1, WEIGHTS["Position"], "Position: Hold Cash"))
        elif "Uptrend" in str(pos):
            votes.append(("Position", +1, WEIGHTS["Position"] * 0.5, "Position: Uptrend"))
        elif "Downtrend" in str(pos):
            votes.append(("Position", -1, WEIGHTS["Position"] * 0.5, "Position: Downtrend"))

    # === Banker Holding ===
    banker = latest.get("Banker_Holding")
    if banker == banker:
        if banker > 65:
            votes.append(("Banker_Holding", +1, WEIGHTS["Banker_Holding"], f"Banker Hold {banker:.0f}% — High"))
        elif banker < 35:
            votes.append(("Banker_Holding", -1, WEIGHTS["Banker_Holding"], f"Banker Hold {banker:.0f}% — Low"))

    # === BLW Divergence ===
    blw_bull = latest.get("BLW_Bullish", 0)
    blw_bear = latest.get("BLW_Bearish", 0)
    if blw_bull > 0:
        strength = "Double" if blw_bull >= 2 else "Single"
        votes.append(("BLW_Divergence", +1, WEIGHTS["BLW_Divergence"] * blw_bull,
                      f"BLW: Bullish Divergence ({strength})"))
    if blw_bear > 0:
        strength = "Double" if blw_bear >= 2 else "Single"
        votes.append(("BLW_Divergence", -1, WEIGHTS["BLW_Divergence"] * blw_bear,
                      f"BLW: Bearish Divergence ({strength})"))

    # === CALCULATE FINAL SCORE ===
    total_weight = sum(abs(w) for _, _, w, _ in votes)
    if total_weight == 0:
        return {"error": "No indicator data available"}

    weighted_score = sum(vote * weight for _, vote, weight, _ in votes)
    max_possible = total_weight
    score = (weighted_score / max_possible) * 100  # Normalize to -100 to +100

    # Confidence = how many indicators agree vs disagree
    buy_votes = sum(1 for _, v, _, _ in votes if v > 0)
    sell_votes = sum(1 for _, v, _, _ in votes if v < 0)
    neutral_votes = sum(1 for _, v, _, _ in votes if v == 0)
    total_votes = len(votes)
    agreement = max(buy_votes, sell_votes) / total_votes * 100 if total_votes > 0 else 0

    # Verdict
    if score >= 60:
        verdict = "STRONG BUY"
    elif score >= 25:
        verdict = "BUY"
    elif score <= -60:
        verdict = "STRONG SELL"
    elif score <= -25:
        verdict = "SELL"
    else:
        verdict = "HOLD"

    # Risk level (based on volatility)
    volatility = analyzer.df["Daily_Return"].std() * np.sqrt(252) * 100
    if volatility > 60:
        risk = "HIGH"
    elif volatility > 30:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    # Entry/Stop/Target
    close_price = float(latest["Close"])

    # ATR approximation for stop/target
    if len(analyzer.df) > 14:
        highs_14 = analyzer.df["High"].tail(14).values
        lows_14 = analyzer.df["Low"].tail(14).values
        atr_approx = float(np.mean(highs_14 - lows_14))
    else:
        atr_approx = close_price * 0.03

    stop_loss = round(close_price - atr_approx * 1.5, 4)
    target = round(close_price + atr_approx * 2.5, 4)

    reasons_buy = [r for _, v, _, r in votes if v > 0]
    reasons_sell = [r for _, v, _, r in votes if v < 0]

    return {
        "symbol": symbol,
        "price": round(close_price, 4),
        "verdict": verdict,
        "score": round(score, 1),
        "confidence": round(agreement, 1),
        "buy_count": buy_votes,
        "sell_count": sell_votes,
        "neutral_count": neutral_votes,
        "total_indicators": total_votes,
        "reasons_buy": reasons_buy,
        "reasons_sell": reasons_sell,
        "risk_level": risk,
        "volatility": round(volatility, 1),
        "entry_price": round(close_price, 4),
        "stop_loss": stop_loss,
        "target_price": target,
        "risk_reward": round((target - close_price) / (close_price - stop_loss), 2) if close_price > stop_loss else 0,
    }
