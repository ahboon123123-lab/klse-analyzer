# Homily Chart - Reconstructed Indicator Formulas

> **IMPORTANT DISCLAIMER**: These formulas are *reconstructed approximations* based on:
> 1. The HTML documentation found in the APK (`res/raw/`)
> 2. Known Chinese technical analysis indicator patterns
> 3. Standard quantitative finance algorithms that match the described behavior
>
> The actual proprietary formulas are locked inside the 360 Jiagu-encrypted Java code.
> These reconstructions aim to replicate the described behavior, not claim to be exact copies.

---

## 1. MCD — 六彩神龙 (Multicolor Dragon) — Chip Distribution Model

### Concept
Tracks the distribution of market "chips" (shares held) across three categories:
- **Floating Chips** (浮动筹码) — Yellow — Recently traded, high liquidity
- **Profitable Chips** (获利盘) — Red — Shares held at a profit (bought below current price)  
- **Locked Chips** (套牢盘) — Green — Shares held at a loss (bought above current price)

Plus three average lines: Pink (Floating avg), Purple (Profitable avg), Blue (Locked avg)

### Reconstructed Formula (TDX/通达信 style pseudocode)

```
{=== Parameters ===}
N := 30;          {Lookback period for chip distribution}
M := 10;          {Average line period}

{=== Core Calculation ===}
{Estimate cost distribution using turnover-weighted price}
COST_CENTER := SMA((HIGH + LOW + CLOSE) / 3, N, 1);
TURNOVER_RATE := VOL / CAPITAL * 100;  {Daily turnover %}

{=== Profitable Chips: shares bought below current price ===}
{Approximation: ratio of volume accumulated at prices below current close}
PROFITABLE := SUM(IF(CLOSE > REF(COST_CENTER, 1), VOL, 0), N) / SUM(VOL, N) * 100;

{=== Locked Chips: shares bought above current price ===}
LOCKED := SUM(IF(CLOSE < REF(COST_CENTER, 1), VOL, 0), N) / SUM(VOL, N) * 100;

{=== Floating Chips: recent short-term traded volume ===}
FLOATING := TURNOVER_RATE * N / 100 * 
            (1 - ABS(CLOSE - COST_CENTER) / COST_CENTER);

{=== Normalize to 100% ===}
TOTAL := PROFITABLE + LOCKED + FLOATING;
PROFITABLE_PCT := PROFITABLE / TOTAL * 100;
LOCKED_PCT := LOCKED / TOTAL * 100;
FLOATING_PCT := FLOATING / TOTAL * 100;

{=== Average Lines ===}
FLOATING_AVG := MA(FLOATING_PCT, M);    {Pink line}
PROFITABLE_AVG := MA(PROFITABLE_PCT, M); {Purple line - INVERTED}
LOCKED_AVG := MA(LOCKED_PCT, M);         {Blue line - INVERTED}

{Note: Purple and Blue lines are "designed conversely" per documentation}
{This means they are plotted as (100 - value) or negative for visual clarity}
PURPLE_LINE := 100 - PROFITABLE_AVG;  {Inverted for bull/bear visual}
BLUE_LINE := 100 - LOCKED_AVG;        {Inverted for bull/bear visual}
```

### Alternative Implementation (More Precise Chip Model)

```python
import numpy as np

def multicolor_dragon(close, high, low, volume, capital, N=30, M=10):
    """
    Multicolor Dragon (六彩神龙) - Chip Distribution Indicator
    
    Parameters:
    - close, high, low, volume: OHLCV price arrays
    - capital: total shares outstanding
    - N: lookback period (default 30)
    - M: average line period (default 10)
    """
    n_bars = len(close)
    profitable = np.zeros(n_bars)
    locked = np.zeros(n_bars)
    floating = np.zeros(n_bars)
    
    for i in range(N, n_bars):
        total_vol = np.sum(volume[i-N:i])
        if total_vol == 0:
            continue
            
        # Estimate chip distribution over lookback
        vol_below = 0  # Volume traded at prices below current
        vol_above = 0  # Volume traded at prices above current
        vol_near = 0   # Volume traded near current price
        
        for j in range(i-N, i):
            avg_price = (high[j] + low[j] + close[j]) / 3
            # Decay factor: more recent volume has more weight
            decay = (j - (i-N) + 1) / N
            weighted_vol = volume[j] * decay
            
            if avg_price < close[i] * 0.97:  # Below current (profitable)
                vol_below += weighted_vol
            elif avg_price > close[i] * 1.03:  # Above current (locked)
                vol_above += weighted_vol
            else:  # Near current price (floating)
                vol_near += weighted_vol
        
        total_weighted = vol_below + vol_above + vol_near
        if total_weighted > 0:
            profitable[i] = vol_below / total_weighted * 100
            locked[i] = vol_above / total_weighted * 100
            floating[i] = vol_near / total_weighted * 100
    
    # Average lines
    profitable_avg = pd_ema(profitable, M)  # Purple line
    locked_avg = pd_ema(locked, M)          # Blue line  
    floating_avg = pd_ema(floating, M)      # Pink line
    
    return {
        'profitable': profitable,       # Red area
        'locked': locked,               # Green area
        'floating': floating,           # Yellow area
        'profitable_avg': profitable_avg,  # Purple line (inverted display)
        'locked_avg': locked_avg,          # Blue line (inverted display)
        'floating_avg': floating_avg,      # Pink line
    }
```

### Trading Rules (from documentation)
1. Price rising + Profitable stays high + Floating/Locked low → Hold (strong uptrend)
2. Price falling + Profitable shrinking + Locked growing → Bearish, stay out
3. Floating increases at highs + Locked appears → Top warning
4. After decline, Floating expands at lows again → Bottom signal

---

## 2. MCD-X — 六彩游龙 (Multicolor DragonX) — Capital Flow Model

### Concept
Tracks capital flow direction by categorizing money into:
- **Floating Capital** (流动资金) — Yellow — Daily trading money
- **Profitable Capital** (盈利资金) — Red — Money in profitable positions
- **Loss Capital** (亏损资金) — Green — Money in losing positions

### Reconstructed Formula

```
{=== Parameters ===}
N := 20;       {Period}
M := 5;        {Smoothing}

{=== Capital Flow Classification ===}
{Average transaction price}
AVG_PRICE := AMOUNT / VOL;

{Daily floating capital = today's turnover amount}
FLOATING_CAPITAL := AMOUNT;

{Profitable capital = cumulative volume at prices below current * current price}
PROFIT_RATIO := (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N));
PROFITABLE_CAPITAL := EMA(AMOUNT * PROFIT_RATIO, M);

{Loss capital = cumulative volume at prices above current * current price}
LOSS_RATIO := (HHV(HIGH, N) - CLOSE) / (HHV(HIGH, N) - LLV(LOW, N));
LOSS_CAPITAL := EMA(AMOUNT * LOSS_RATIO, M);

{=== Display (suggested: daily/weekly/monthly) ===}
YELLOW := EMA(FLOATING_CAPITAL, M);     {Floating - Yellow}
RED := EMA(PROFITABLE_CAPITAL, M);       {Profitable - Red}
GREEN := EMA(LOSS_CAPITAL, M);           {Loss - Green}
```

### Trading Rules
1. Yellow (Floating Capital) — High liquidity daily trading flow
2. Red growing → Bulls dominate, hold; Red weakening → Price turning point, reduce
3. Green growing → Bears dominate, stay in cash

---

## 3. QSW — 趋势王 (Trend Expert)

### Concept
A trend-following indicator that combines price momentum with volume weighting.
Based on the "Ultimate Kit" placement alongside MCD and BLW, it's likely a
volume-weighted trend strength oscillator.

### Reconstructed Formula

```
{=== Parameters ===}
SHORT := 5;     {Short period}
MID := 13;      {Medium period}
LONG := 34;     {Long period}
SIGNAL := 5;    {Signal line period}

{=== Volume-Weighted Price ===}
VWP := (CLOSE * VOL + HIGH * VOL + LOW * VOL) / (3 * VOL);
{Simplified: VWAP-like weighted price}
WEIGHTED_CLOSE := (2 * CLOSE + HIGH + LOW) / 4;

{=== Trend Strength Calculation ===}
{Fast trend line}
FAST := EMA(WEIGHTED_CLOSE, SHORT);

{Medium trend line - incorporates volume momentum}
VOL_FACTOR := VOL / MA(VOL, MID);
MEDIUM := EMA(WEIGHTED_CLOSE * (1 + (VOL_FACTOR - 1) * 0.1), MID);

{Slow trend line}
SLOW := EMA(WEIGHTED_CLOSE, LONG);

{=== Trend Expert Value ===}
{Difference between fast and slow, normalized}
QSW_RAW := (FAST - SLOW) / SLOW * 100;
QSW := EMA(QSW_RAW, SIGNAL);
QSW_SIGNAL := EMA(QSW, SIGNAL);

{=== Buy/Sell Signals ===}
BUY := CROSS(QSW, QSW_SIGNAL) AND QSW < 0;   {Golden cross in oversold}
SELL := CROSS(QSW_SIGNAL, QSW) AND QSW > 0;   {Dead cross in overbought}

{=== Trend Direction ===}
TREND_UP := QSW > QSW_SIGNAL AND QSW > 0;
TREND_DOWN := QSW < QSW_SIGNAL AND QSW < 0;
```

### Alternative: Slope-Based Trend Model

```python
import numpy as np
from scipy.signal import savgol_filter

def trend_expert_qsw(close, high, low, volume, 
                      short=5, mid=13, long=34, signal=5):
    """
    QSW (趋势王) - Trend Expert Indicator
    
    Combines price trend slope with volume confirmation
    """
    # Weighted price
    wp = (2 * close + high + low) / 4
    
    # EMA calculations
    fast_ema = ema(wp, short)
    mid_ema = ema(wp, mid)
    slow_ema = ema(wp, long)
    
    # Trend slope (rate of change of EMA)
    fast_slope = np.gradient(fast_ema)
    slow_slope = np.gradient(slow_ema)
    
    # Volume momentum factor
    vol_ma = sma(volume, mid)
    vol_ratio = volume / vol_ma
    
    # QSW = Volume-weighted trend momentum
    trend_momentum = (fast_ema - slow_ema) / slow_ema * 100
    qsw = ema(trend_momentum * np.sqrt(vol_ratio), signal)
    qsw_signal = ema(qsw, signal)
    
    # Histogram
    histogram = qsw - qsw_signal
    
    return {
        'qsw': qsw,
        'signal': qsw_signal,
        'histogram': histogram,
        'buy': (np.diff(np.sign(histogram)) > 0) & (qsw[1:] < 0),
        'sell': (np.diff(np.sign(histogram)) < 0) & (qsw[1:] > 0),
    }
```

---

## 4. BLW — 背离王 (Deviation/Divergence Expert)

### Concept
Automatically detects price-indicator divergences. A divergence occurs when:
- **Bullish divergence**: Price makes lower low, but indicator makes higher low
- **Bearish divergence**: Price makes higher high, but indicator makes lower high

The "Deviation Expert" likely uses multiple oscillators (RSI, MACD histogram)
to detect divergences automatically and score their reliability.

### Reconstructed Formula

```
{=== Parameters ===}
RSI_PERIOD := 14;
MACD_SHORT := 12;
MACD_LONG := 26;
MACD_SIGNAL := 9;
LOOKBACK := 60;      {Bars to look back for divergence}
PIVOT_BARS := 5;     {Bars left/right for pivot detection}

{=== Oscillator Calculations ===}
RSI_VAL := RSI(CLOSE, RSI_PERIOD);
DIF := EMA(CLOSE, MACD_SHORT) - EMA(CLOSE, MACD_LONG);
DEA := EMA(DIF, MACD_SIGNAL);
MACD_HIST := (DIF - DEA) * 2;

{=== Pivot Point Detection ===}
{Find local highs and lows in price and indicator}
PRICE_HIGH_PIVOT := HIGH = HHV(HIGH, PIVOT_BARS * 2 + 1);
PRICE_LOW_PIVOT := LOW = LLV(LOW, PIVOT_BARS * 2 + 1);
RSI_HIGH_PIVOT := RSI_VAL = HHV(RSI_VAL, PIVOT_BARS * 2 + 1);
RSI_LOW_PIVOT := RSI_VAL = LLV(RSI_VAL, PIVOT_BARS * 2 + 1);

{=== Bearish Divergence (Top Divergence) ===}
{Price makes higher high BUT RSI makes lower high}
BEAR_DIV := HIGH > REF(HHV(HIGH, LOOKBACK), PIVOT_BARS) 
            AND RSI_VAL < REF(HHV(RSI_VAL, LOOKBACK), PIVOT_BARS)
            AND RSI_VAL > 60;

{=== Bullish Divergence (Bottom Divergence) ===}
{Price makes lower low BUT RSI makes higher low}
BULL_DIV := LOW < REF(LLV(LOW, LOOKBACK), PIVOT_BARS)
            AND RSI_VAL > REF(LLV(RSI_VAL, LOOKBACK), PIVOT_BARS)
            AND RSI_VAL < 40;

{=== Composite Divergence Score ===}
{Combine RSI + MACD divergence for stronger signal}
MACD_BEAR := HIGH > REF(HHV(HIGH, LOOKBACK), PIVOT_BARS)
             AND MACD_HIST < REF(HHV(MACD_HIST, LOOKBACK), PIVOT_BARS);
MACD_BULL := LOW < REF(LLV(LOW, LOOKBACK), PIVOT_BARS)
             AND MACD_HIST > REF(LLV(MACD_HIST, LOOKBACK), PIVOT_BARS);

{Combined signal strength}
BEARISH_SIGNAL := BEAR_DIV + MACD_BEAR;  {0, 1, or 2}
BULLISH_SIGNAL := BULL_DIV + MACD_BULL;  {0, 1, or 2}
```

### Python Implementation

```python
import numpy as np

def divergence_expert_blw(close, high, low, volume,
                           rsi_period=14, macd_short=12, macd_long=26,
                           macd_signal=9, lookback=60, pivot_bars=5):
    """
    BLW (背离王) - Divergence Expert Indicator
    
    Detects bullish and bearish divergences between price and oscillators.
    """
    n = len(close)
    
    # Calculate RSI
    rsi = calculate_rsi(close, rsi_period)
    
    # Calculate MACD
    dif = ema(close, macd_short) - ema(close, macd_long)
    dea = ema(dif, macd_signal)
    macd_hist = (dif - dea) * 2
    
    # Find pivot highs and lows
    price_highs = find_pivots(high, pivot_bars, 'high')
    price_lows = find_pivots(low, pivot_bars, 'low')
    rsi_highs = find_pivots(rsi, pivot_bars, 'high')
    rsi_lows = find_pivots(rsi, pivot_bars, 'low')
    
    bullish_div = np.zeros(n)
    bearish_div = np.zeros(n)
    
    for i in range(lookback, n):
        # Check for bearish divergence
        # Price higher high + RSI lower high
        recent_price_highs = [j for j in price_highs if i-lookback <= j <= i]
        recent_rsi_highs = [j for j in rsi_highs if i-lookback <= j <= i]
        
        if len(recent_price_highs) >= 2:
            p1, p2 = recent_price_highs[-2], recent_price_highs[-1]
            if high[p2] > high[p1] and rsi[p2] < rsi[p1]:
                bearish_div[p2] = 1
                if macd_hist[p2] < macd_hist[p1]:
                    bearish_div[p2] = 2  # Double confirmed
        
        # Check for bullish divergence
        # Price lower low + RSI higher low
        recent_price_lows = [j for j in price_lows if i-lookback <= j <= i]
        recent_rsi_lows = [j for j in rsi_lows if i-lookback <= j <= i]
        
        if len(recent_price_lows) >= 2:
            p1, p2 = recent_price_lows[-2], recent_price_lows[-1]
            if low[p2] < low[p1] and rsi[p2] > rsi[p1]:
                bullish_div[p2] = 1
                if macd_hist[p2] > macd_hist[p1]:
                    bullish_div[p2] = 2  # Double confirmed
    
    return {
        'rsi': rsi,
        'macd_hist': macd_hist,
        'bullish_divergence': bullish_div,   # 1=RSI div, 2=RSI+MACD div
        'bearish_divergence': bearish_div,   # 1=RSI div, 2=RSI+MACD div
    }


def find_pivots(data, left_bars, pivot_type):
    """Find pivot highs or lows"""
    pivots = []
    for i in range(left_bars, len(data) - left_bars):
        if pivot_type == 'high':
            if data[i] == max(data[i-left_bars:i+left_bars+1]):
                pivots.append(i)
        else:
            if data[i] == min(data[i-left_bars:i+left_bars+1]):
                pivots.append(i)
    return pivots


def calculate_rsi(close, period=14):
    """Standard RSI calculation"""
    n = len(close)
    rsi = np.zeros(n)
    gains = np.zeros(n)
    losses = np.zeros(n)
    
    for i in range(1, n):
        change = close[i] - close[i-1]
        if change > 0:
            gains[i] = change
        else:
            losses[i] = abs(change)
    
    avg_gain = np.zeros(n)
    avg_loss = np.zeros(n)
    
    # Initial SMA
    avg_gain[period] = np.mean(gains[1:period+1])
    avg_loss[period] = np.mean(losses[1:period+1])
    
    # Smoothed (Wilder's method)
    for i in range(period+1, n):
        avg_gain[i] = (avg_gain[i-1] * (period-1) + gains[i]) / period
        avg_loss[i] = (avg_loss[i-1] * (period-1) + losses[i]) / period
    
    for i in range(period, n):
        if avg_loss[i] == 0:
            rsi[i] = 100
        else:
            rs = avg_gain[i] / avg_loss[i]
            rsi[i] = 100 - (100 / (1 + rs))
    
    return rsi
```

---

## 5. Homily Rainbow (弘历彩虹) — Multi-Line Trend System

### Concept
A 5-color moving average system incorporating volume and time:
- **Red line** — Fastest (short-term)
- **Yellow line** — Fast (short-medium)
- **Green line** — Medium (trading auxiliary)
- **Blue line** — Medium-slow (mid-long term)
- **White line** — Slowest (long-term)

### Reconstructed Formula

```
{=== Parameters ===}
P1 := 3;      {Red - fastest}
P2 := 7;      {Yellow - fast}
P3 := 13;     {Green - auxiliary}
P4 := 21;     {Blue - medium-slow}
P5 := 55;     {White - slowest}

{=== Volume-Weighted Price ===}
VWP := (CLOSE * 2 + HIGH + LOW) / 4;

{=== Volume Factor (time-weighted) ===}
VOL_MA := MA(VOL, 20);
VOL_WEIGHT := EMA(VOL / VOL_MA, 5);

{=== Rainbow Lines (Volume-Time Weighted EMAs) ===}
RED_LINE := EMA(VWP, P1);                          {Fastest}
YELLOW_LINE := EMA(VWP, P2);                       {Fast}
GREEN_LINE := EMA(VWP * VOL_WEIGHT, P3);           {Auxiliary with vol}
BLUE_LINE := EMA(VWP, P4);                         {Medium-slow}
WHITE_LINE := EMA(VWP, P5);                        {Slowest}

{=== Value Center (价值中枢) ===}
{When lines converge, this is the value center}
VALUE_CENTER := (RED_LINE + YELLOW_LINE + GREEN_LINE + BLUE_LINE + WHITE_LINE) / 5;

{=== Trend Signals ===}
{Rainbow diverging upward = buy}
RAINBOW_UP := RED_LINE > YELLOW_LINE 
              AND YELLOW_LINE > GREEN_LINE 
              AND GREEN_LINE > BLUE_LINE 
              AND BLUE_LINE > WHITE_LINE;

{Rainbow diverging downward = sell}
RAINBOW_DOWN := RED_LINE < YELLOW_LINE 
                AND YELLOW_LINE < GREEN_LINE 
                AND GREEN_LINE < BLUE_LINE 
                AND BLUE_LINE < WHITE_LINE;

{Lines converging = consolidation, wait}
CONVERGING := ABS(RED_LINE - WHITE_LINE) / WHITE_LINE < 0.02;
```

### Trading Rules (from documentation)
1. Rainbow UP + Price pulls back to Yellow → Medium-short buy signal
2. Rainbow DOWN + Price rebounds to Yellow → Medium-short sell signal
3. Rainbow UP + Price pulls back to Blue/White → Mid-long term buy
4. Rainbow DOWN + Price rebounds to Blue/White → Mid-long term sell
5. Yellow line concentrating + sideways → Wait for direction
6. Yellow + White concentrating + long sideways → Only short-term trades

---

## 6. Homily Position (弘历进出) — Price-Volume Resistance

### Concept
Predicts price direction by analyzing price-volume relationships.
Features a "life line" (生命线) and resonance bands (共振带).
Generates "★Increase" and "★Stop Loss" signals.

### Reconstructed Formula

```
{=== Parameters ===}
LIFE_N := 13;    {Life line period}
BAND_N := 21;    {Resonance band period}
SIGNAL_N := 5;   {Signal sensitivity}

{=== Life Line (Volume-Weighted Moving Average) ===}
{Core: VWMA that considers price-volume relationship anomalies}
VWMA_BASE := SUM(CLOSE * VOL, LIFE_N) / SUM(VOL, LIFE_N);
LIFE_LINE := EMA(VWMA_BASE, SIGNAL_N);

{=== Price-Volume Resistance Index ===}
{When price rises faster than volume supports → resistance increases}
PRICE_CHG := (CLOSE - REF(CLOSE, 1)) / REF(CLOSE, 1) * 100;
VOL_CHG := (VOL - REF(VOL, 1)) / REF(VOL, 1) * 100;
RESISTANCE := EMA(PRICE_CHG - VOL_CHG * 0.5, SIGNAL_N);

{=== Resonance Bands ===}
ATR_VAL := ATR(BAND_N);
UPPER_BAND := LIFE_LINE + ATR_VAL * 1.5;
LOWER_BAND := LIFE_LINE - ATR_VAL * 1.5;

{=== Direction ===}
LIFE_UP := LIFE_LINE > REF(LIFE_LINE, 1);   {Life line turning up}
LIFE_DOWN := LIFE_LINE < REF(LIFE_LINE, 1); {Life line turning down}

{=== Signals ===}
{★Increase: Life line up + price crosses above life line}
INCREASE := LIFE_UP AND CROSS(CLOSE, LIFE_LINE) 
            AND RESISTANCE > 0;

{★Stop Loss: Life line down + price crosses below life line}
STOP_LOSS := LIFE_DOWN AND CROSS(LIFE_LINE, CLOSE)
             AND RESISTANCE < 0;

{=== Holding Rules ===}
{Hold stock: price above upper band in uptrend}
HOLD_STOCK := CLOSE > UPPER_BAND AND LIFE_UP;

{Hold cash: price below lower band in downtrend}
HOLD_CASH := CLOSE < LOWER_BAND AND LIFE_DOWN;
```

---

## Helper Functions

```python
def ema(data, period):
    """Exponential Moving Average"""
    result = np.zeros(len(data))
    multiplier = 2.0 / (period + 1)
    result[0] = data[0]
    for i in range(1, len(data)):
        result[i] = (data[i] - result[i-1]) * multiplier + result[i-1]
    return result

def sma(data, period):
    """Simple Moving Average"""
    result = np.zeros(len(data))
    for i in range(period-1, len(data)):
        result[i] = np.mean(data[i-period+1:i+1])
    return result

def atr(high, low, close, period=14):
    """Average True Range"""
    n = len(close)
    tr = np.zeros(n)
    for i in range(1, n):
        tr[i] = max(high[i] - low[i],
                    abs(high[i] - close[i-1]),
                    abs(low[i] - close[i-1]))
    return ema(tr, period)
```

---

## How to Validate These Reconstructions

1. **Get actual indicator output**: Use the Homily Chart app on sample stocks and screenshot the indicator values
2. **Compare with reconstruction**: Run the formulas above on the same stock data
3. **Adjust parameters**: Tune N, M, period values until output matches
4. **For exact formulas**: Unpack the 360 Jiagu protection using Frida/FART/BlackDex on a rooted device, then decompile the extracted DEX with jadx

## Unpacking Guide (360 Jiagu)

To extract the actual Java source code:

1. Install the APK on a **rooted Android emulator** (API 28/29 recommended)
2. Use **BlackDex** (no root needed) or **Frida + dex-dumper** script:
   ```bash
   frida -U -f com.hlzzb.xjp -l dex_dump.js --no-pause
   ```
3. The dumped DEX files will contain classes like:
   - `com.homilychart.indicator.*`
   - `com.homilychart.server.main.util.*`
4. Decompile with **jadx**:
   ```bash
   jadx -d output/ classes_dumped.dex
   ```
5. Search for indicator calculation classes (likely using standard patterns like EMA/SMA with custom parameters)


---

## 7. Banker Hunter (庄家猎手) — Chart Label Indicators

These labels appear on the chart as overlay data, primarily in the "Banker Hunter" (庄家猎手) module. They track institutional (banker/庄家) vs retail (散户) behavior.

---

### 7a. profitLine → 获利线 (Profit Line)

**Concept**: Shows the price level at which a specific percentage of holders are in profit. Uses the `COST()` function which estimates the price distribution of historical accumulation.

```
{=== Profit Line (获利线) ===}
{COST(X) = the price at which X% of chips are below (profitable)}
{WINNER(P) = the percentage of chips below price P}

{Profit Line: the price below which ~80% of holders are profitable}
获利线: COST(80);

{Alternative: Volume-weighted average cost of profitable positions}
{All shares bought below current price, weighted by volume}
PROFITABLE_COST := SUM(IF(CLOSE > REF(CLOSE,1), AMOUNT, 0), 60) / 
                   SUM(IF(CLOSE > REF(CLOSE,1), VOL, 0), 60);

{Simplified approximation without COST/WINNER functions:}
PROFIT_LINE := EMA((HIGH + LOW + CLOSE * 2) / 4, 30) * 
               (1 - (1 - WINNER_APPROX) * 0.1);

{Where WINNER_APPROX estimates profit ratio:}
WINNER_APPROX := (CLOSE - LLV(LOW, 60)) / (HHV(HIGH, 60) - LLV(LOW, 60));
```

```python
def profit_line(close, high, low, volume, period=60):
    """
    Profit Line (获利线)
    Estimates the average cost basis of profitable positions.
    
    Uses a simplified chip distribution model since COST/WINNER 
    are proprietary TDX functions.
    """
    n = len(close)
    profit_line = np.zeros(n)
    
    for i in range(period, n):
        # Estimate: weighted average of prices where current close > historical price
        # (positions that are currently profitable)
        weights = []
        prices = []
        for j in range(i-period, i):
            avg_price = (high[j] + low[j] + close[j]) / 3
            if avg_price < close[i]:  # This position is profitable
                weights.append(volume[j])
                prices.append(avg_price)
        
        if weights:
            profit_line[i] = np.average(prices, weights=weights)
        else:
            profit_line[i] = close[i]
    
    return profit_line
```

---

### 7b. bankerCostLine → 庄家成本线 (Banker Cost Line)

**Concept**: Estimates the average cost basis of the institutional "banker" (主力/庄家). Based on the assumption that large-volume accumulation at specific price levels reveals the banker's average entry price.

```
{=== Banker Cost Line (庄家成本线) ===}
{Core idea: Volume-weighted average price over accumulation period}

{Method 1: Exponential volume-weighted price}
V1 := (CLOSE * 2 + HIGH + LOW) / 4 * 10;
V2 := EMA(V1, 13) - EMA(V1, 34);
V3 := EMA(V2, 5);

{Banker cost is approximated as long-term VWAP}
庄家成本线 := SUM(AMOUNT, 120) / SUM(VOL, 120);

{Alternative: DMA-based cost estimation}
{Uses displaced moving average to estimate institutional accumulation price}
BANKER_COST := DMA(CLOSE, VOL / SUM(VOL, 60));

{Method 2: Weighted by large orders (big volume days)}
BIG_VOL := IF(VOL > MA(VOL, 20) * 1.5, VOL, 0);
BANKER_COST_ALT := SUM(CLOSE * BIG_VOL, 120) / SUM(BIG_VOL, 120);
```

```python
def banker_cost_line(close, high, low, volume, amount, period=120):
    """
    Banker Cost Line (庄家成本线)
    Estimates the average cost of institutional accumulation.
    
    Uses volume-weighted average price (VWAP) with emphasis on 
    high-volume accumulation days.
    """
    n = len(close)
    cost_line = np.zeros(n)
    
    vol_ma_20 = sma(volume, 20)
    
    for i in range(period, n):
        # Standard VWAP over period
        total_amount = np.sum(amount[i-period:i])
        total_vol = np.sum(volume[i-period:i])
        
        if total_vol > 0:
            cost_line[i] = total_amount / total_vol
        
        # Alternative: weight by large-volume days (banker accumulation)
        # big_vol_mask = volume[i-period:i] > vol_ma_20[i-period:i] * 1.5
        # if np.any(big_vol_mask):
        #     big_amounts = amount[i-period:i][big_vol_mask]
        #     big_vols = volume[i-period:i][big_vol_mask]
        #     cost_line[i] = np.sum(big_amounts) / np.sum(big_vols)
    
    return cost_line
```

---

### 7c. banker_controlling_line → 庄家控盘线 (Banker Controlling Line)

**Concept**: Measures the degree to which the banker controls (locks up) shares. A high value means the banker holds most of the float, reducing supply and enabling price manipulation.

```
{=== Banker Controlling Line (庄家控盘线) ===}
{Based on volume and price behavior analysis}
{When volume shrinks but price holds = banker controlling}

{Method: Inverse of free float activity}
TURNOVER := VOL / CAPITAL * 100;
AVG_TURNOVER := MA(TURNOVER, 20);

{Control degree: lower turnover with stable price = higher control}
PRICE_STABILITY := 1 - ABS(CLOSE - REF(CLOSE, 1)) / REF(CLOSE, 1);
CONTROL_RAW := (1 - TURNOVER / AVG_TURNOVER) * PRICE_STABILITY * 100;

庄家控盘线 := EMA(MAX(CONTROL_RAW, 0), 30);

{Alternative Method: Using chip concentration}
{If 80% of chips are within a narrow price band, banker controls}
CHIP_CONCENTRATION := (COST(90) - COST(10)) / CLOSE * 100;
CONTROL_DEGREE := 100 - CHIP_CONCENTRATION;  {Tighter = more control}

{Method 3: Volume anomaly detection}
VA1 := 100 - 3 * SMA((CLOSE - LLV(LOW, 75)) / 
       (HHV(HIGH, 75) - LLV(LOW, 75)) * 100, 20, 1) + 
       2 * SMA(SMA((CLOSE - LLV(LOW, 75)) / 
       (HHV(HIGH, 75) - LLV(LOW, 75)) * 100, 20, 1), 15, 1);

庄家控盘 := EMA(100 - VA1, 13);
```

```python
def banker_controlling_line(close, volume, capital, period=30):
    """
    Banker Controlling Line (庄家控盘线)
    Measures institutional control over the stock's float.
    
    High values = banker holds most shares, low free float
    """
    n = len(close)
    control = np.zeros(n)
    
    turnover = volume / capital * 100  # Daily turnover rate %
    avg_turnover = sma(turnover, 20)
    
    for i in range(20, n):
        # Price stability factor
        if close[i-1] > 0:
            price_change = abs(close[i] - close[i-1]) / close[i-1]
        else:
            price_change = 0
        stability = 1 - min(price_change * 10, 1)  # Cap at 1
        
        # Control = low turnover + stable price
        if avg_turnover[i] > 0:
            turnover_ratio = 1 - min(turnover[i] / avg_turnover[i], 2) / 2
        else:
            turnover_ratio = 0
        
        control[i] = turnover_ratio * stability * 100
    
    # Smooth with EMA
    control_line = ema(np.maximum(control, 0), period)
    
    return control_line
```

---

### 7d. banker_holding_position_line → 庄家持仓线 (Banker Holding Position Line)

**Concept**: Estimates the percentage of total shares held by the banker/institutions. Derived from analyzing volume patterns, turnover rates, and chip distribution.

```
{=== Banker Holding Position Line (庄家持仓线) ===}
{Estimates the % of shares held by institutions}

{Method: Based on trapped volume analysis}
{High-volume accumulation at lows = banker buying}
VAR1 := REF(LOW, 1);
VAR2 := SMA(ABS(LOW - VAR1), 13, 1) / SMA(MAX(LOW - VAR1, 0), 13, 1) * 4;
VAR3 := EMA(VAR2, 13);
VAR4 := LLV(LOW, 34);
VAR5 := EMA(IF(LOW <= VAR4, VAR3, 0), 3);

{Cumulative banker position estimate (0-100%)}
庄家持仓 := 100 - 100 * (HHV(HIGH, 34) - CLOSE) / (HHV(HIGH, 34) - LLV(LOW, 34));

{Alternative: Turnover-based accumulation model}
{Banker holding = 100% - retail holding - floating}
ACCUMULATED_VOL := SUM(IF(VOL > MA(VOL, 5) * 2 AND CLOSE > OPEN, VOL, 0), 120);
DISTRIBUTED_VOL := SUM(IF(VOL > MA(VOL, 5) * 2 AND CLOSE < OPEN, VOL, 0), 120);
NET_ACCUMULATION := ACCUMULATED_VOL - DISTRIBUTED_VOL;
庄家持仓线 := EMA(NET_ACCUMULATION / CAPITAL * 100, 20);
```

```python
def banker_holding_position(close, high, low, open_price, volume, capital, period=120):
    """
    Banker Holding Position Line (庄家持仓线)
    Estimates institutional holding percentage.
    
    Logic: Large volume on up-days = accumulation
           Large volume on down-days = distribution
    """
    n = len(close)
    holding = np.zeros(n)
    
    vol_ma5 = sma(volume, 5)
    
    for i in range(period, n):
        accumulated = 0
        distributed = 0
        
        for j in range(i-period, i):
            # Large volume day
            if volume[j] > vol_ma5[j] * 1.5:
                if close[j] > open_price[j]:  # Up day = accumulation
                    accumulated += volume[j]
                else:  # Down day = distribution
                    distributed += volume[j]
        
        net = accumulated - distributed
        if capital[i] > 0:
            holding[i] = net / capital[i] * 100
    
    # Smooth and bound to 0-100
    holding_line = ema(np.clip(holding, 0, 100), 20)
    
    return holding_line
```

---

### 7e. shcc → 散户持仓 (Retail Holding)

**Concept**: Estimates the percentage of shares held by retail investors. Inverse/complement of banker holding. Retail typically trades on high-volume days with small individual orders.

```
{=== Retail Holding (散户持仓) ===}
{Retail = 100% - Banker - Free Float}
{Retail traders are characterized by:}
{  - High frequency trading on volatile days}
{  - Small volume per transaction}
{  - Buying on up days, panic selling on down days}

{Method: Turnover-based estimation}
{Days with normal/low volume and high turnover = retail activity}
TOTAL_TURNOVER_60 := SUM(VOL, 60) / CAPITAL * 100;
BANKER_HOLDING := (上面的庄家持仓线);

散户持仓 := 100 - BANKER_HOLDING;

{Alternative: Using WINNER function approach}
{Retail tends to hold at loss longer (套牢) and sell at small profits}
RETAIL_TRAPPED := WINNER(CLOSE * 1.05) - WINNER(CLOSE * 0.85);
散户持仓_ALT := RETAIL_TRAPPED * 100;

{Simplified model}
散户持仓 := EMA(100 * (1 - VOL / (CAPITAL * MA(VOL/CAPITAL, 20))), 20);
```

```python
def retail_holding(close, volume, capital, banker_holding):
    """
    Retail Holding (散户持仓/shcc)
    Complement of banker holding.
    """
    # Simple: retail = 100% - banker
    # In practice also subtract institutional float and locked shares
    retail = 100 - banker_holding
    
    # Bound to reasonable range (retail typically 30-80%)
    retail = np.clip(retail, 0, 100)
    
    return retail
```

---

### 7f. zlcc → 庄家持仓 (Banker Holding)

**Concept**: Display label for the banker holding percentage. Same calculation as `banker_holding_position_line` but formatted as a percentage value for the info panel.

```
{=== Banker Holding Display (庄家持仓 - zlcc) ===}
{Same as banker_holding_position_line, formatted as %}

V1 := (CLOSE * 2 + HIGH + LOW) / 4 * 10;
V2 := EMA(V1, 13) - EMA(V1, 34);
V3 := EMA(V2, 5);
V4 := 2 * (V2 - V3) * 5.5;

{When V4 > 0 = banker accumulating, V4 < 0 = banker distributing}
庄家持仓 := EMA(IF(V4 > 0, V4, 0), 30) / 
            (EMA(IF(V4 > 0, V4, 0), 30) + EMA(IF(V4 < 0, ABS(V4), 0), 30)) * 100;
```

---

### 7g. zlxp → 洗盘 (Wash Out / Shakeout)

**Concept**: Detects when the banker is "washing" (shaking out) weak retail holders through deliberate price drops, before the next major up-move. Characterized by:
- Price drops on declining volume
- Quick recovery after the drop
- Banker holding doesn't decrease during the drop

```
{=== Wash Out Detection (洗盘 - zlxp) ===}

{Indicators of a wash-out:}
{1. Price drops but volume decreases (not genuine selling)}
{2. The drop doesn't break key support (banker protects position)}
{3. After shakeout, price recovers quickly}

VAR1 := REF(LOW, 1);
VAR2 := SMA(ABS(LOW - VAR1), 13, 1) / SMA(MAX(LOW - VAR1, 0), 13, 1) * 4;
VAR3 := EMA(VAR2, 13);
VAR4 := LLV(LOW, 34);
VAR5 := EMA(IF(LOW <= VAR4, VAR3, 0), 3);

{Wash out: VAR5 decreasing from peak (banker was buying, now shaking)}
洗盘 := IF(VAR5 < REF(VAR5, 1) AND VAR5 > 0, VAR5, 0);

{Alternative: Volume-price divergence method}
{Price dropping but with shrinking volume = wash, not real distribution}
PRICE_DROP := CLOSE < REF(CLOSE, 1) AND CLOSE < REF(CLOSE, 2);
VOL_SHRINK := VOL < MA(VOL, 5) * 0.7;
SUPPORT_HOLD := LOW > MA(CLOSE, 60) * 0.95;  {Doesn't break 60MA by much}
BANKER_STILL_IN := 庄家持仓线 > REF(庄家持仓线, 5) * 0.95;  {Holding stable}

洗盘_SIGNAL := PRICE_DROP AND VOL_SHRINK AND SUPPORT_HOLD AND BANKER_STILL_IN;

{Wash intensity (higher = more shakeout happening)}
WASH_INTENSITY := EMA(IF(洗盘_SIGNAL, 
                    ABS(CLOSE - REF(CLOSE, 1)) / REF(CLOSE, 1) * 100, 0), 5);
```

```python
def wash_out(close, low, high, volume, capital, period=34):
    """
    Wash Out / Shakeout Detection (洗盘/zlxp)
    
    Detects when a banker is deliberately shaking out weak holders
    before the next leg up.
    
    Signals:
    - Price drops on declining volume
    - Doesn't break major support
    - Banker holding remains stable
    """
    n = len(close)
    wash = np.zeros(n)
    
    # VAR method (from TDX formulas)
    var1 = np.roll(low, 1)  # REF(LOW, 1)
    var1[0] = low[0]
    
    abs_diff = np.abs(low - var1)
    max_diff = np.maximum(low - var1, 0)
    
    # SMA(ABS(LOW-VAR1), 13, 1) / SMA(MAX(LOW-VAR1, 0), 13, 1) * 4
    sma_abs = wilders_sma(abs_diff, 13)
    sma_max = wilders_sma(max_diff, 13)
    
    var2 = np.where(sma_max > 0, sma_abs / sma_max * 4, 0)
    var3 = ema(var2, 13)
    
    # LLV(LOW, 34) - lowest low in 34 bars
    var4 = np.zeros(n)
    for i in range(period, n):
        var4[i] = np.min(low[i-period:i+1])
    
    # EMA of var3 only when LOW touches new lows
    var5_raw = np.where(low <= var4, var3, 0)
    var5 = ema(var5_raw, 3)
    
    # Wash out: var5 declining from peak (accumulation phase ending -> shakeout)
    for i in range(1, n):
        if var5[i] < var5[i-1] and var5[i] > 0:
            wash[i] = var5[i]
    
    return wash


def wilders_sma(data, period):
    """Wilder's smoothing (SMA in TDX with weight=1)"""
    result = np.zeros(len(data))
    result[0] = data[0]
    for i in range(1, len(data)):
        result[i] = (result[i-1] * (period - 1) + data[i]) / period
    return result
```

---

### Summary Table: Banker Hunter Labels

| Label | Chinese | Formula Basis | What It Shows |
|-------|---------|---------------|---------------|
| profitLine | 获利线 | `COST(80)` / VWAP of profitable positions | Price where 80% holders are profitable |
| bankerCostLine | 庄家成本线 | Long-term VWAP weighted by large-volume days | Banker's average entry price |
| banker_controlling_line | 庄家控盘线 | Inverse turnover × price stability | How tightly banker controls the float |
| banker_holding_position_line | 庄家持仓线 | Net accumulation (big vol up-days minus big vol down-days) / capital | Banker's estimated holding % |
| shcc | 散户持仓 | `100% - banker_holding` | Retail investors' holding % |
| zlcc | 庄家持仓 | Same as banker_holding, formatted for display | Banker's holding % (info panel) |
| zlxp | 洗盘 | Volume-price divergence + support holding | Shakeout detection signal |

### Key TDX Functions Used

| Function | Description |
|----------|-------------|
| `COST(X)` | Price at which X% of chips are below (profitable) |
| `WINNER(P)` | % of total chips held below price P |
| `CAPITAL` | Total shares outstanding (流通股本) |
| `AMOUNT` | Daily trading amount (成交额 = price × volume) |
| `SMA(X, N, M)` | Smoothed MA: `(M*X + (N-M)*REF) / N` (Wilder's method) |
| `DMA(X, A)` | Dynamic Moving Average: `A*X + (1-A)*REF` |
| `EMA(X, N)` | Exponential Moving Average |
| `LLV(X, N)` | Lowest value of X in last N bars |
| `HHV(X, N)` | Highest value of X in last N bars |
