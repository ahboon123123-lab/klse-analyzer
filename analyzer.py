"""
Stock analysis module with technical indicators and performance metrics.
"""

import pandas as pd
import numpy as np
from homily_indicators import (
    calculate_mcdx as calc_mcdx_flow, calculate_qsw, calculate_blw,
    calculate_rainbow, calculate_position,
    calculate_profit_line, calculate_banker_cost, calculate_banker_control,
    calculate_banker_holding, calculate_wash_out, calculate_banker_zlcc
)


class StockAnalyzer:
    """Analyze stock data with technical indicators and metrics."""

    def __init__(self, df: pd.DataFrame, symbol: str = ""):
        self.df = df.copy()
        self.symbol = symbol
        self._calculate_indicators()

    def _calculate_indicators(self):
        """Calculate all technical indicators."""
        self._calculate_moving_averages()
        self._calculate_rsi()
        self._calculate_macd()
        self._calculate_bollinger_bands()
        self._calculate_daily_returns()

    def _calculate_moving_averages(self):
        """Calculate Simple and Exponential Moving Averages."""
        self.df["SMA_20"] = self.df["Close"].rolling(window=20).mean()
        self.df["SMA_50"] = self.df["Close"].rolling(window=50).mean()
        self.df["SMA_200"] = self.df["Close"].rolling(window=200).mean()
        self.df["EMA_12"] = self.df["Close"].ewm(span=12, adjust=False).mean()
        self.df["EMA_26"] = self.df["Close"].ewm(span=26, adjust=False).mean()

    def _calculate_rsi(self, period: int = 14):
        """Calculate Relative Strength Index."""
        delta = self.df["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        self.df["RSI"] = 100 - (100 / (1 + rs))

    def _calculate_macd(self):
        """Calculate MACD (Moving Average Convergence Divergence)."""
        self.df["MACD"] = self.df["EMA_12"] - self.df["EMA_26"]
        self.df["MACD_Signal"] = self.df["MACD"].ewm(span=9, adjust=False).mean()
        self.df["MACD_Histogram"] = self.df["MACD"] - self.df["MACD_Signal"]

    def _calculate_bollinger_bands(self, period: int = 20):
        """Calculate Bollinger Bands."""
        sma = self.df["Close"].rolling(window=period).mean()
        std = self.df["Close"].rolling(window=period).std()
        self.df["BB_Upper"] = sma + (std * 2)
        self.df["BB_Middle"] = sma
        self.df["BB_Lower"] = sma - (std * 2)

    def _calculate_daily_returns(self):
        """Calculate daily returns."""
        self.df["Daily_Return"] = self.df["Close"].pct_change()
        self.df["Cumulative_Return"] = (1 + self.df["Daily_Return"]).cumprod() - 1

    def _calculate_deviation(self, period: int = 20):
        """
        Calculate Standard Deviation and Price Deviation indicators.

        - StdDev: Rolling standard deviation of close price (volatility measure)
        - Price Deviation %: How far price is from its SMA as a percentage
        - Z-Score: Number of standard deviations price is from its mean
        """
        sma = self.df["Close"].rolling(window=period).mean()
        std = self.df["Close"].rolling(window=period).std()

        # Standard Deviation (raw volatility)
        self.df["StdDev_20"] = std

        # Price Deviation % from SMA
        self.df["Price_Dev_Pct"] = ((self.df["Close"] - sma) / sma) * 100

        # Z-Score: how many std devs price is from mean
        self.df["Z_Score"] = (self.df["Close"] - sma) / std

        # Deviation bands (1, 2, 3 standard deviations)
        self.df["Dev_Upper_1"] = sma + (std * 1)
        self.df["Dev_Upper_2"] = sma + (std * 2)
        self.df["Dev_Upper_3"] = sma + (std * 3)
        self.df["Dev_Lower_1"] = sma - (std * 1)
        self.df["Dev_Lower_2"] = sma - (std * 2)
        self.df["Dev_Lower_3"] = sma - (std * 3)

    def _calculate_homily(self):
        """
        Calculate Homily Chart indicators (True Trend Circles + Deviation Expert).

        True Trend Circles:
        - Uses Parabolic SAR to determine trend direction
        - RED circle: Open Position Day (1st bar of uptrend)
        - BLUE circle: Stable Hold Position Day (continuing uptrend)
        - YELLOW circle: Close/Cash State Day (downtrend)

        Deviation Expert (DE):
        - EMA(5) - EMA(20) = fund flow divergence
        - Positive = Inflow beating Outflow (Red histogram)
        - Negative = Outflow beating Inflow (Green histogram)
        """
        close = self.df["Close"]
        high = self.df["High"]
        low = self.df["Low"]

        # --- Parabolic SAR calculation ---
        sar_values = self._calculate_parabolic_sar(
            high.values, low.values, close.values,
            start=0.02, increment=0.02, maximum=0.20
        )
        self.df["Homily_SAR"] = sar_values

        # Determine trend state
        is_uptrend = close > self.df["Homily_SAR"]
        was_uptrend = is_uptrend.shift(1).fillna(False)

        # Color matrix
        # RED: first bar of uptrend (buy trigger)
        # BLUE: continuing uptrend (hold)
        # YELLOW: downtrend (cash/sell)
        conditions = []
        for i in range(len(self.df)):
            if is_uptrend.iloc[i] and (i == 0 or not was_uptrend.iloc[i]):
                conditions.append("red")  # Buy trigger
            elif is_uptrend.iloc[i] and was_uptrend.iloc[i]:
                conditions.append("blue")  # Hold
            else:
                conditions.append("yellow")  # Cash state
        self.df["Homily_Color"] = conditions

        # --- Deviation Expert (DE) ---
        de_fast_ema = close.ewm(span=5, adjust=False).mean()
        de_slow_ema = close.ewm(span=20, adjust=False).mean()
        self.df["DE_Value"] = de_fast_ema - de_slow_ema
        self.df["DE_Color"] = self.df["DE_Value"].apply(lambda x: "red" if x > 0 else "green")

    @staticmethod
    def _calculate_parabolic_sar(high, low, close, start=0.02, increment=0.02, maximum=0.20):
        """Calculate Parabolic SAR values."""
        length = len(close)
        sar = np.zeros(length)
        af = start
        uptrend = True
        ep = high[0]
        sar[0] = low[0]

        for i in range(1, length):
            if uptrend:
                sar[i] = sar[i - 1] + af * (ep - sar[i - 1])
                sar[i] = min(sar[i], low[i - 1])
                if i >= 2:
                    sar[i] = min(sar[i], low[i - 2])

                if high[i] > ep:
                    ep = high[i]
                    af = min(af + increment, maximum)

                if low[i] < sar[i]:
                    uptrend = False
                    sar[i] = ep
                    ep = low[i]
                    af = start
            else:
                sar[i] = sar[i - 1] + af * (ep - sar[i - 1])
                sar[i] = max(sar[i], high[i - 1])
                if i >= 2:
                    sar[i] = max(sar[i], high[i - 2])

                if low[i] < ep:
                    ep = low[i]
                    af = min(af + increment, maximum)

                if high[i] > sar[i]:
                    uptrend = True
                    sar[i] = ep
                    ep = high[i]
                    af = start

        return sar

    def _calculate_indicators(self):
        """Calculate all technical indicators."""
        self._calculate_moving_averages()
        self._calculate_rsi()
        self._calculate_macd()
        self._calculate_bollinger_bands()
        self._calculate_daily_returns()
        self._calculate_deviation()
        self._calculate_homily()
        self._calculate_extra_indicators()

    def _calculate_extra_indicators(self):
        """Calculate additional indicators: Stochastic, Williams %R, ADX, CCI, Momentum, L3 Banker, MCDX, etc."""
        close = self.df["Close"]
        high = self.df["High"]
        low = self.df["Low"]
        n = len(close)

        # --- L3 Banker Fund ---
        self._calculate_l3_banker()

        # --- MCDX Smart Money (Chip Distribution) ---
        self._calculate_mcdx()

        # --- QSW Trend Expert ---
        self._calculate_qsw()

        # --- BLW Divergence Expert ---
        self._calculate_blw()

        # --- Homily Rainbow ---
        self._calculate_rainbow()

        # --- Homily Position ---
        self._calculate_position()

        # --- Banker Hunter Module ---
        self._calculate_banker_hunter()

        # --- Momentum (10-period) ---
        self.df["Momentum"] = close - close.shift(10)

        # --- Stochastic %K and %D (14,3,3) ---
        low14 = low.rolling(14).min()
        high14 = high.rolling(14).max()
        self.df["Stoch_K"] = ((close - low14) / (high14 - low14)) * 100
        self.df["Stoch_D"] = self.df["Stoch_K"].rolling(3).mean()

        # --- Stochastic RSI ---
        rsi = self.df["RSI"]
        rsi14_min = rsi.rolling(14).min()
        rsi14_max = rsi.rolling(14).max()
        self.df["Stoch_RSI"] = ((rsi - rsi14_min) / (rsi14_max - rsi14_min)) * 100

        # --- Williams %R (14) ---
        self.df["Williams_R"] = ((high14 - close) / (high14 - low14)) * -100

        # --- CCI (Commodity Channel Index, 20) ---
        tp = (high + low + close) / 3
        sma_tp = tp.rolling(20).mean()
        mad = tp.rolling(20).apply(lambda x: np.mean(np.abs(x - x.mean())), raw=True)
        self.df["CCI"] = (tp - sma_tp) / (0.015 * mad)

        # --- ADX (14) ---
        self._calculate_adx(14)

        # --- Awesome Oscillator ---
        mid = (high + low) / 2
        self.df["AO"] = mid.rolling(5).mean() - mid.rolling(34).mean()

        # --- Ultimate Oscillator ---
        self._calculate_ultimate_oscillator()

    def _calculate_l3_banker(self):
        """
        Calculate L3 Banker Fund indicator.

        Based on blackcat1402's TradingView indicator:
        - Uses slope of close over 21 periods * 20 + close as artificial curve
        - Fast line: EMA(2) of the curve
        - Slow line: EMA(42) of the curve
        - Green = Bullish (fast > slow), Red = Bearish (fast < slow)
        - Yellow = First Green (swing start / entry signal)
        """
        close = self.df["Close"].values
        n = len(close)

        if n < 22:
            self.df["L3_Banker"] = np.nan
            self.df["L3_Banker_Signal"] = "Not enough data"
            return

        # Adapt periods based on data length
        slope_period = min(21, max(5, n // 4))
        slow_ema_period = min(42, max(10, n // 3))

        # Calculate slope over periods (linear regression slope)
        slope_values = np.zeros(n)
        for i in range(slope_period, n):
            y = close[i - slope_period:i]
            x = np.arange(slope_period)
            if len(y) == slope_period:
                slope_values[i] = np.polyfit(x, y, 1)[0]

        # Artificial curve: slope * 20 + close
        curve = slope_values * 20 + close

        # Fast line: EMA(2) of curve
        fast = pd.Series(curve).ewm(span=2, adjust=False).mean().values

        # Slow line: EMA(slow_ema_period) of curve
        slow = pd.Series(curve).ewm(span=slow_ema_period, adjust=False).mean().values

        # L3 Banker value (fast - slow normalized)
        banker_value = fast - slow
        self.df["L3_Banker"] = banker_value

        # Determine signal
        signals = []
        min_period = max(slope_period, slow_ema_period)
        for i in range(n):
            if i < min_period:
                signals.append("Not enough data")
            elif banker_value[i] > 0:
                if i > 0 and banker_value[i - 1] <= 0:
                    signals.append("First Green")  # Swing start (Yellow)
                else:
                    signals.append("Green")  # Bullish
            else:
                if i > 0 and banker_value[i - 1] > 0:
                    signals.append("First Red")  # Bearish start
                else:
                    signals.append("Red")  # Bearish

        self.df["L3_Banker_Signal"] = signals

    def _calculate_mcdx(self):
        """
        Calculate Multicolor Dragon (六彩神龙) - Chip Distribution Model.

        Tuned to match Homily app output:
        - FCHIPS (Red): Volume accumulated at prices SIGNIFICANTLY below current (>10% below)
        - LCHIPS (Green): Volume accumulated at prices SIGNIFICANTLY above current (>10% above)  
        - PCHIPS (Yellow): Everything else — recent turnover / floating chips

        Key insight from Homily screenshots: PCHIPS (yellow) dominates for actively traded stocks.
        The floating chip calculation emphasizes TURNOVER RATE not price position.
        """
        close = self.df["Close"].values
        high = self.df["High"].values
        low = self.df["Low"].values
        volume = self.df["Volume"].values
        n = len(close)

        N = min(30, max(10, n // 3))  # Lookback period
        M = min(10, max(3, N // 3))   # Average line period

        if n < N + 1:
            self.df["MCDX_Banker"] = np.nan
            self.df["MCDX_HotMoney"] = np.nan
            self.df["MCDX_Retail"] = np.nan
            self.df["MCDX_Signal"] = "Not enough data"
            return

        profitable = np.zeros(n)
        locked = np.zeros(n)
        floating = np.zeros(n)

        for i in range(N, n):
            total_vol = np.sum(volume[i - N:i])
            if total_vol == 0:
                floating[i] = 100
                continue

            # Cost center (turnover-weighted avg price)
            cost_center = 0
            for j in range(i - N, i):
                cost_center += ((high[j] + low[j] + close[j]) / 3.0) * volume[j]
            cost_center /= total_vol

            # Turnover rate factor: high turnover = more floating
            avg_vol = total_vol / N
            today_turnover = volume[i] / (avg_vol + 1)  # Relative turnover

            # Profitable: volume at prices significantly below current (deep profit)
            # Use 10% threshold (tuned from screenshots - wide threshold means less red)
            vol_below = 0.0
            vol_above = 0.0
            vol_float = 0.0

            for j in range(i - N, i):
                avg_price = (high[j] + low[j] + close[j]) / 3.0
                decay = (j - (i - N) + 1) / N  # Recent = more weight

                if avg_price < close[i] * 0.90:  # 10% below = deep profit
                    vol_below += volume[j] * decay
                elif avg_price > close[i] * 1.10:  # 10% above = deep loss
                    vol_above += volume[j] * decay
                else:  # Within 10% = floating
                    vol_float += volume[j] * decay

            total_weighted = vol_below + vol_above + vol_float
            if total_weighted > 0:
                profitable[i] = vol_below / total_weighted * 100
                locked[i] = vol_above / total_weighted * 100
                floating[i] = vol_float / total_weighted * 100

            # Apply turnover boost to floating (key Homily behavior):
            # High turnover stocks show more yellow
            turnover_boost = min(today_turnover * 0.3, 0.5)
            floating[i] = floating[i] * (1 + turnover_boost)

            # Re-normalize to 100%
            total = profitable[i] + locked[i] + floating[i]
            if total > 0:
                profitable[i] = profitable[i] / total * 100
                locked[i] = locked[i] / total * 100
                floating[i] = floating[i] / total * 100

        # Store
        self.df["MCDX_Banker"] = profitable     # Red (FCHIPS)
        self.df["MCDX_HotMoney"] = floating     # Yellow (PCHIPS)
        self.df["MCDX_Retail"] = locked         # Green (LCHIPS)

        # Average lines (EMA smoothed)
        self.df["MCDX_Profitable_Avg"] = pd.Series(profitable).ewm(span=M, adjust=False).mean()
        self.df["MCDX_Floating_Avg"] = pd.Series(floating).ewm(span=M, adjust=False).mean()
        self.df["MCDX_Locked_Avg"] = pd.Series(locked).ewm(span=M, adjust=False).mean()

        # Signal
        signals = []
        for i in range(n):
            if i < N:
                signals.append("Not enough data")
            elif profitable[i] > 50:
                signals.append("Hot Money")
            elif profitable[i] > 20:
                signals.append("Accumulation")
            elif locked[i] > 50:
                signals.append("Retail")
            else:
                signals.append("Neutral")
        self.df["MCDX_Signal"] = signals

    def _calculate_qsw(self):
        """Calculate QSW (趋势王) Trend Expert."""
        result = calculate_qsw(
            self.df["Close"].values, self.df["High"].values,
            self.df["Low"].values, self.df["Volume"].values.astype(float)
        )
        if result is None:
            self.df["QSW"] = np.nan
            self.df["QSW_Signal"] = np.nan
            self.df["QSW_Hist"] = np.nan
            self.df["QSW_Trend"] = "Not enough data"
        else:
            self.df["QSW"] = result["qsw"]
            self.df["QSW_Signal"] = result["signal"]
            self.df["QSW_Hist"] = result["histogram"]
            self.df["QSW_Trend"] = result["trend"]

    def _calculate_blw(self):
        """Calculate BLW (背离王) Divergence Expert."""
        result = calculate_blw(
            self.df["Close"].values, self.df["High"].values, self.df["Low"].values
        )
        if result is None:
            self.df["BLW_Bullish"] = 0
            self.df["BLW_Bearish"] = 0
        else:
            self.df["BLW_Bullish"] = result["bullish_div"]
            self.df["BLW_Bearish"] = result["bearish_div"]

    def _calculate_rainbow(self):
        """Calculate Homily Rainbow (弘历彩虹)."""
        result = calculate_rainbow(
            self.df["Close"].values, self.df["High"].values,
            self.df["Low"].values, self.df["Volume"].values.astype(float)
        )
        if result is None:
            self.df["Rainbow_Red"] = np.nan
            self.df["Rainbow_Yellow"] = np.nan
            self.df["Rainbow_Green"] = np.nan
            self.df["Rainbow_Blue"] = np.nan
            self.df["Rainbow_White"] = np.nan
            self.df["Rainbow_Trend"] = "Not enough data"
        else:
            self.df["Rainbow_Red"] = result["red"]
            self.df["Rainbow_Yellow"] = result["yellow"]
            self.df["Rainbow_Green"] = result["green"]
            self.df["Rainbow_Blue"] = result["blue"]
            self.df["Rainbow_White"] = result["white"]
            self.df["Rainbow_Trend"] = result["trend"]

    def _calculate_position(self):
        """Calculate Homily Position (弘历进出)."""
        result = calculate_position(
            self.df["Close"].values, self.df["High"].values,
            self.df["Low"].values, self.df["Volume"].values.astype(float)
        )
        if result is None:
            self.df["Position_Life"] = np.nan
            self.df["Position_Upper"] = np.nan
            self.df["Position_Lower"] = np.nan
            self.df["Position_Signal"] = "Not enough data"
        else:
            self.df["Position_Life"] = result["life_line"]
            self.df["Position_Upper"] = result["upper_band"]
            self.df["Position_Lower"] = result["lower_band"]
            self.df["Position_Signal"] = result["signals"]

    def _calculate_banker_hunter(self):
        """Calculate Banker Hunter (庄家猎手) module indicators."""
        close = self.df["Close"].values
        high = self.df["High"].values
        low = self.df["Low"].values
        volume = self.df["Volume"].values.astype(float)
        open_price = self.df["Open"].values if "Open" in self.df.columns else close
        n = len(close)

        # Use average volume as capital proxy (since we don't have shares outstanding)
        capital = np.mean(volume) * 50  # Rough estimate

        # Profit Line
        self.df["Profit_Line"] = calculate_profit_line(close, high, low, volume)

        # Banker Cost Line
        period = min(120, n - 1)
        self.df["Banker_Cost"] = calculate_banker_cost(close, high, low, volume, period=period)

        # Banker Control
        self.df["Banker_Control"] = calculate_banker_control(close, volume, capital)

        # Banker Holding (zlcc)
        self.df["Banker_Holding"] = calculate_banker_zlcc(close, high, low)

        # Wash Out Detection
        self.df["Wash_Out"] = calculate_wash_out(close, low, high, volume)

    def _calculate_adx(self, period=14):
        """Calculate ADX (Average Directional Index)."""
        high = self.df["High"]
        low = self.df["Low"]
        close = self.df["Close"]

        plus_dm = high.diff()
        minus_dm = -low.diff()
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm < 0] = 0

        # When +DM > -DM, keep +DM, else 0
        plus_dm_final = np.where((plus_dm > minus_dm), plus_dm, 0)
        minus_dm_final = np.where((minus_dm > plus_dm), minus_dm, 0)

        tr1 = high - low
        tr2 = abs(high - close.shift(1))
        tr3 = abs(low - close.shift(1))
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        atr = tr.rolling(period).mean()
        plus_di = 100 * pd.Series(plus_dm_final).rolling(period).mean() / atr
        minus_di = 100 * pd.Series(minus_dm_final).rolling(period).mean() / atr

        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        self.df["ADX"] = dx.rolling(period).mean()
        self.df["Plus_DI"] = plus_di
        self.df["Minus_DI"] = minus_di

    def _calculate_ultimate_oscillator(self):
        """Calculate Ultimate Oscillator (7, 14, 28)."""
        close = self.df["Close"]
        high = self.df["High"]
        low = self.df["Low"]

        prev_close = close.shift(1)
        bp = close - pd.concat([low, prev_close], axis=1).min(axis=1)
        tr = pd.concat([high, prev_close], axis=1).max(axis=1) - pd.concat([low, prev_close], axis=1).min(axis=1)

        avg7 = bp.rolling(7).sum() / tr.rolling(7).sum()
        avg14 = bp.rolling(14).sum() / tr.rolling(14).sum()
        avg28 = bp.rolling(28).sum() / tr.rolling(28).sum()

        self.df["UO"] = 100 * ((4 * avg7) + (2 * avg14) + avg28) / 7

    def get_signal_summary(self) -> list:
        """
        Get a pickastock-style signal summary for all indicators.
        Returns list of dicts: {name, value, signal}
        signal is one of: 'Buy', 'Sell', 'Neutral', 'Strong Buy', 'Strong Sell', 'Not enough data'
        """
        latest = self.df.iloc[-1]
        signals = []

        def safe(val):
            """Return None if NaN."""
            if val != val:  # NaN check
                return None
            return val

        # RSI
        rsi = safe(latest.get("RSI"))
        if rsi is not None:
            if rsi < 20: sig = "Strong Buy"
            elif rsi < 30: sig = "Buy"
            elif rsi > 80: sig = "Strong Sell"
            elif rsi > 70: sig = "Sell"
            else: sig = "Neutral"
            signals.append({"name": "RSI (14)", "value": round(rsi, 2), "signal": sig})
        else:
            signals.append({"name": "RSI (14)", "value": None, "signal": "Not enough data"})

        # MACD
        macd = safe(latest.get("MACD"))
        macd_sig = safe(latest.get("MACD_Signal"))
        if macd is not None and macd_sig is not None:
            sig = "Buy" if macd > macd_sig else "Sell"
            signals.append({"name": "MACD", "value": round(macd, 4), "signal": sig})
        else:
            signals.append({"name": "MACD", "value": None, "signal": "Not enough data"})

        # Parabolic SAR
        sar = safe(latest.get("Homily_SAR"))
        if sar is not None:
            sig = "Buy" if latest["Close"] > sar else "Sell"
            signals.append({"name": "Parabolic SAR", "value": round(sar, 4), "signal": sig})
        else:
            signals.append({"name": "Parabolic SAR", "value": None, "signal": "Not enough data"})

        # Momentum
        mom = safe(latest.get("Momentum"))
        if mom is not None:
            sig = "Buy" if mom > 0 else "Sell"
            signals.append({"name": "Momentum (10)", "value": round(mom, 4), "signal": sig})
        else:
            signals.append({"name": "Momentum (10)", "value": None, "signal": "Not enough data"})

        # Stochastic
        stoch_k = safe(latest.get("Stoch_K"))
        stoch_d = safe(latest.get("Stoch_D"))
        if stoch_k is not None and stoch_d is not None:
            if stoch_k < 20: sig = "Buy"
            elif stoch_k > 80: sig = "Sell"
            elif stoch_k > stoch_d: sig = "Buy"
            else: sig = "Neutral"
            signals.append({"name": "Stochastic (14,3)", "value": round(stoch_k, 2), "signal": sig})
        else:
            signals.append({"name": "Stochastic (14,3)", "value": None, "signal": "Not enough data"})

        # Stoch RSI
        stoch_rsi = safe(latest.get("Stoch_RSI"))
        if stoch_rsi is not None:
            if stoch_rsi < 20: sig = "Buy"
            elif stoch_rsi > 80: sig = "Sell"
            else: sig = "Neutral"
            signals.append({"name": "Stoch RSI", "value": round(stoch_rsi, 2), "signal": sig})
        else:
            signals.append({"name": "Stoch RSI", "value": None, "signal": "Not enough data"})

        # Williams %R
        wr = safe(latest.get("Williams_R"))
        if wr is not None:
            if wr < -80: sig = "Buy"
            elif wr > -20: sig = "Sell"
            else: sig = "Neutral"
            signals.append({"name": "Williams %R", "value": round(wr, 2), "signal": sig})
        else:
            signals.append({"name": "Williams %R", "value": None, "signal": "Not enough data"})

        # CCI
        cci = safe(latest.get("CCI"))
        if cci is not None:
            if cci < -100: sig = "Buy"
            elif cci > 100: sig = "Sell"
            else: sig = "Neutral"
            signals.append({"name": "CCI (20)", "value": round(cci, 2), "signal": sig})
        else:
            signals.append({"name": "CCI (20)", "value": None, "signal": "Not enough data"})

        # ADX
        adx = safe(latest.get("ADX"))
        plus_di = safe(latest.get("Plus_DI"))
        minus_di = safe(latest.get("Minus_DI"))
        if adx is not None and plus_di is not None and minus_di is not None:
            if adx > 25 and plus_di > minus_di: sig = "Buy"
            elif adx > 25 and minus_di > plus_di: sig = "Sell"
            else: sig = "Neutral"
            signals.append({"name": "ADX (14)", "value": round(adx, 2), "signal": sig})
        else:
            signals.append({"name": "ADX (14)", "value": None, "signal": "Not enough data"})

        # Awesome Oscillator
        ao = safe(latest.get("AO"))
        if ao is not None:
            sig = "Buy" if ao > 0 else "Sell"
            signals.append({"name": "Awesome Oscillator", "value": round(ao, 4), "signal": sig})
        else:
            signals.append({"name": "Awesome Oscillator", "value": None, "signal": "Not enough data"})

        # Ultimate Oscillator
        uo = safe(latest.get("UO"))
        if uo is not None:
            if uo < 30: sig = "Buy"
            elif uo > 70: sig = "Sell"
            else: sig = "Neutral"
            signals.append({"name": "Ultimate Oscillator", "value": round(uo, 2), "signal": sig})
        else:
            signals.append({"name": "Ultimate Oscillator", "value": None, "signal": "Not enough data"})

        # DE (Deviation Expert)
        de = safe(latest.get("DE_Value"))
        if de is not None:
            sig = "Buy" if de > 0 else "Sell"
            signals.append({"name": "Deviation Expert", "value": round(de, 4), "signal": sig})
        else:
            signals.append({"name": "Deviation Expert", "value": None, "signal": "Not enough data"})

        # L3 Banker
        l3 = safe(latest.get("L3_Banker"))
        l3_sig = latest.get("L3_Banker_Signal", "Not enough data")
        if l3 is not None and l3_sig != "Not enough data":
            if l3_sig == "First Green":
                sig = "Strong Buy"
            elif l3_sig == "Green":
                sig = "Buy"
            elif l3_sig == "First Red":
                sig = "Strong Sell"
            else:
                sig = "Sell"
            signals.append({"name": "L3 Banker", "value": round(l3, 4), "signal": f"{sig} ({l3_sig})"})
        else:
            signals.append({"name": "L3 Banker", "value": None, "signal": "Not enough data"})

        # MCDX Smart Money
        mcdx = safe(latest.get("MCDX_Banker"))
        mcdx_sig = latest.get("MCDX_Signal", "Not enough data")
        if mcdx is not None and mcdx_sig != "Not enough data":
            if mcdx_sig == "Hot Money":
                sig = "Strong Buy"
            elif mcdx_sig == "Accumulation":
                sig = "Buy"
            elif mcdx_sig == "Neutral":
                sig = "Neutral"
            else:
                sig = "Sell"
            signals.append({"name": "MCDX Smart Money", "value": round(mcdx, 2), "signal": f"{sig} ({mcdx_sig})"})
        else:
            signals.append({"name": "MCDX Smart Money", "value": None, "signal": "Not enough data"})

        # QSW Trend Expert
        qsw = safe(latest.get("QSW"))
        qsw_trend = latest.get("QSW_Trend", "Not enough data")
        if qsw is not None and qsw_trend != "Not enough data":
            if "Up" in qsw_trend:
                sig = "Buy"
            elif "Down" in qsw_trend:
                sig = "Sell"
            else:
                sig = "Neutral"
            signals.append({"name": "QSW Trend Expert", "value": round(qsw, 4), "signal": f"{sig} ({qsw_trend})"})
        else:
            signals.append({"name": "QSW Trend Expert", "value": None, "signal": "Not enough data"})

        # Homily Rainbow
        rainbow_trend = latest.get("Rainbow_Trend", "Not enough data")
        if rainbow_trend != "Not enough data":
            if rainbow_trend == "Rainbow Up":
                sig = "Strong Buy"
            elif rainbow_trend == "Rainbow Down":
                sig = "Strong Sell"
            elif rainbow_trend == "Converging":
                sig = "Neutral"
            else:
                sig = "Neutral"
            signals.append({"name": "Homily Rainbow", "value": None, "signal": f"{sig} ({rainbow_trend})"})
        else:
            signals.append({"name": "Homily Rainbow", "value": None, "signal": "Not enough data"})

        # Homily Position
        pos_sig = latest.get("Position_Signal", "Not enough data")
        if pos_sig != "Not enough data":
            if "Increase" in pos_sig:
                sig = "Strong Buy"
            elif "Stop Loss" in pos_sig:
                sig = "Strong Sell"
            elif "Hold Stock" in pos_sig:
                sig = "Buy"
            elif "Hold Cash" in pos_sig:
                sig = "Sell"
            elif "Uptrend" in pos_sig:
                sig = "Buy"
            elif "Downtrend" in pos_sig:
                sig = "Sell"
            else:
                sig = "Neutral"
            signals.append({"name": "Homily Position", "value": None, "signal": f"{sig} ({pos_sig})"})
        else:
            signals.append({"name": "Homily Position", "value": None, "signal": "Not enough data"})

        # Banker Holding (庄家持仓)
        banker_hold = safe(latest.get("Banker_Holding"))
        if banker_hold is not None:
            if banker_hold > 70:
                sig = "Strong Buy"
                desc = "High Control"
            elif banker_hold > 50:
                sig = "Buy"
                desc = "Accumulating"
            elif banker_hold < 30:
                sig = "Sell"
                desc = "Distributing"
            else:
                sig = "Neutral"
                desc = "Normal"
            signals.append({"name": "Banker Holding (庄家持仓)", "value": round(banker_hold, 1), "signal": f"{sig} ({desc})"})
        else:
            signals.append({"name": "Banker Holding (庄家持仓)", "value": None, "signal": "Not enough data"})

        # Banker Control (庄家控盘)
        control = safe(latest.get("Banker_Control"))
        if control is not None:
            if control > 60:
                sig = "Buy"
                desc = "Tight Control"
            elif control > 40:
                sig = "Neutral"
                desc = "Moderate"
            else:
                sig = "Sell"
                desc = "Weak Control"
            signals.append({"name": "Banker Control (庄家控盘)", "value": round(control, 1), "signal": f"{sig} ({desc})"})
        else:
            signals.append({"name": "Banker Control (庄家控盘)", "value": None, "signal": "Not enough data"})

        # Wash Out (洗盘)
        wash = safe(latest.get("Wash_Out"))
        if wash is not None and wash > 0:
            signals.append({"name": "Wash Out (洗盘)", "value": round(wash, 4), "signal": "Buy (Shakeout Detected)"})
        else:
            signals.append({"name": "Wash Out (洗盘)", "value": 0, "signal": "Neutral (No Shakeout)"})

        return signals
        """Print price summary statistics."""
        latest = self.df.iloc[-1]
        prev = self.df.iloc[-2] if len(self.df) > 1 else latest

        change = latest["Close"] - prev["Close"]
        change_pct = (change / prev["Close"]) * 100

        print(f"  Latest Close:  RM {latest['Close']:.4f}")
        print(f"  Daily Change:  RM {change:.4f} ({change_pct:+.2f}%)")
        print(f"  Day High:      RM {latest['High']:.4f}")
        print(f"  Day Low:       RM {latest['Low']:.4f}")
        print(f"  Volume:        {latest['Volume']:,.0f}")
        print(f"  52-Week High:  RM {self.df['High'].max():.4f}")
        print(f"  52-Week Low:   RM {self.df['Low'].min():.4f}")
        print(f"  Average Volume: {self.df['Volume'].mean():,.0f}")

    def print_technical_indicators(self):
        """Print latest technical indicator values."""
        latest = self.df.iloc[-1]

        print(f"  SMA 20:        RM {latest['SMA_20']:.4f}")
        print(f"  SMA 50:        RM {latest['SMA_50']:.4f}")

        if not np.isnan(latest["SMA_200"]):
            print(f"  SMA 200:       RM {latest['SMA_200']:.4f}")
        else:
            print(f"  SMA 200:       N/A (need more data)")

        print(f"  RSI (14):      {latest['RSI']:.2f}", end="")
        if latest["RSI"] > 70:
            print(" [OVERBOUGHT]")
        elif latest["RSI"] < 30:
            print(" [OVERSOLD]")
        else:
            print(" [NEUTRAL]")

        print(f"  MACD:          {latest['MACD']:.4f}")
        print(f"  MACD Signal:   {latest['MACD_Signal']:.4f}")

        # Trend signals
        print(f"\n  Trend Signals:")
        if latest["Close"] > latest["SMA_50"]:
            print(f"    Price > SMA50: BULLISH")
        else:
            print(f"    Price < SMA50: BEARISH")

        if latest["MACD"] > latest["MACD_Signal"]:
            print(f"    MACD > Signal: BULLISH")
        else:
            print(f"    MACD < Signal: BEARISH")

    def print_performance_metrics(self):
        """Print performance and risk metrics."""
        returns = self.df["Daily_Return"].dropna()

        total_return = self.df["Cumulative_Return"].iloc[-1] * 100
        annualized_return = ((1 + total_return / 100) ** (252 / len(returns)) - 1) * 100
        volatility = returns.std() * np.sqrt(252) * 100
        sharpe_ratio = (annualized_return / 100) / (volatility / 100) if volatility != 0 else 0

        # Maximum drawdown
        cumulative = (1 + returns).cumprod()
        rolling_max = cumulative.cummax()
        drawdown = (cumulative - rolling_max) / rolling_max
        max_drawdown = drawdown.min() * 100

        print(f"  Total Return:       {total_return:+.2f}%")
        print(f"  Annualized Return:  {annualized_return:+.2f}%")
        print(f"  Volatility (Annual): {volatility:.2f}%")
        print(f"  Sharpe Ratio:       {sharpe_ratio:.3f}")
        print(f"  Max Drawdown:       {max_drawdown:.2f}%")
        print(f"  Positive Days:      {(returns > 0).sum()} / {len(returns)} ({(returns > 0).mean() * 100:.1f}%)")
        print(f"  Best Day:           {returns.max() * 100:+.2f}%")
        print(f"  Worst Day:          {returns.min() * 100:+.2f}%")
