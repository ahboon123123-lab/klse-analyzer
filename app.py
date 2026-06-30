"""
KLSE Stock Analyzer - Web Interface
Run this and open http://localhost:5000 in your browser.
"""

from flask import Flask, render_template, jsonify, request
from top_volume import get_top_volume_stocks, KLSE_STOCKS
from yahoo_api import get_stock_history, get_stock_quote
from analyzer import StockAnalyzer
from divergence_scanner import scan_top_stocks, detect_divergence
from klse_scraper import fetch_all_stocks_by_volume, get_all_stock_symbols
from signal_engine import generate_signal
from accumulation_scanner import scan_accumulation
from rainbow_scanner import scan_rainbow_crossover

app = Flask(__name__)


@app.route("/")
def index():
    """Main page - Top 50 volume stocks."""
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    """Full dashboard page (similar to pickastock.info)."""
    return render_template("dashboard.html")


@app.route("/api/top-volume")
def api_top_volume():
    """API endpoint to fetch top volume stocks."""
    top_n = request.args.get("top", 50, type=int)
    period = request.args.get("period", "daily")  # "daily" or "weekly"
    df = get_top_volume_stocks(top_n=top_n, period=period)

    if df.empty:
        return jsonify({"error": "No data available", "stocks": []})

    stocks = df.to_dict(orient="records")
    return jsonify({
        "stocks": stocks,
        "total_volume": int(df["Volume"].sum()),
        "count": len(stocks),
        "period": period,
    })


@app.route("/stock/<symbol>")
def stock_page(symbol):
    """Individual stock analysis page."""
    if not symbol.endswith(".KL"):
        symbol = symbol + ".KL"
    return render_template("stock.html", symbol=symbol)


@app.route("/api/stock/<symbol>")
def api_stock_detail(symbol):
    """API endpoint for individual stock analysis."""
    # Ensure .KL suffix
    if not symbol.endswith(".KL"):
        symbol = symbol + ".KL"

    df = get_stock_history(symbol, period="1y")
    if df.empty:
        return jsonify({"error": f"No data for {symbol}"})

    analyzer = StockAnalyzer(df, symbol)
    latest = analyzer.df.iloc[-1]

    # Get Yahoo Finance info for fundamentals
    from yahoo_api import fetch_chart_data
    raw = fetch_chart_data(symbol, period="5d", interval="1d")
    meta = raw.get("meta", {}) if raw else {}

    # Calculate range data
    df_5d = analyzer.df.tail(5)
    df_4w = analyzer.df.tail(20)
    df_3m = analyzer.df.tail(63)

    # Build response
    data = {
        "symbol": symbol,
        "name": KLSE_STOCKS.get(symbol, meta.get("shortName", symbol)),
        "meta": {
            "exchange": meta.get("exchangeName", "KLS"),
            "currency": meta.get("currency", "MYR"),
            "instrument_type": meta.get("instrumentType", "EQUITY"),
        },
        "latest": {
            "open": round(float(latest["Open"]), 4) if latest["Open"] == latest["Open"] else None,
            "close": round(float(latest["Close"]), 4),
            "high": round(float(latest["High"]), 4),
            "low": round(float(latest["Low"]), 4),
            "volume": int(latest["Volume"]),
            "sma_20": round(float(latest["SMA_20"]), 4) if latest["SMA_20"] == latest["SMA_20"] else None,
            "sma_50": round(float(latest["SMA_50"]), 4) if latest["SMA_50"] == latest["SMA_50"] else None,
            "sma_200": round(float(latest["SMA_200"]), 4) if latest["SMA_200"] == latest["SMA_200"] else None,
            "rsi": round(float(latest["RSI"]), 2) if latest["RSI"] == latest["RSI"] else None,
            "macd": round(float(latest["MACD"]), 4) if latest["MACD"] == latest["MACD"] else None,
            "macd_signal": round(float(latest["MACD_Signal"]), 4) if latest["MACD_Signal"] == latest["MACD_Signal"] else None,
        },
        "ranges": {
            "day": {"low": round(float(latest["Low"]), 4), "high": round(float(latest["High"]), 4)},
            "5day": {"low": round(float(df_5d["Low"].min()), 4), "high": round(float(df_5d["High"].max()), 4)},
            "4week": {"low": round(float(df_4w["Low"].min()), 4), "high": round(float(df_4w["High"].max()), 4)},
            "3month": {"low": round(float(df_3m["Low"].min()), 4), "high": round(float(df_3m["High"].max()), 4)},
            "1year": {"low": round(float(analyzer.df["Low"].min()), 4), "high": round(float(analyzer.df["High"].max()), 4)},
        },
        "deviation": {
            "std_dev": round(float(latest["StdDev_20"]), 4) if latest["StdDev_20"] == latest["StdDev_20"] else None,
            "price_dev_pct": round(float(latest["Price_Dev_Pct"]), 2) if latest["Price_Dev_Pct"] == latest["Price_Dev_Pct"] else None,
            "z_score": round(float(latest["Z_Score"]), 2) if latest["Z_Score"] == latest["Z_Score"] else None,
        },
        "signals": analyzer.get_signal_summary(),
        "performance": {
            "total_return": round(float(analyzer.df["Cumulative_Return"].iloc[-1]) * 100, 2),
            "high_52w": round(float(analyzer.df["High"].max()), 4),
            "low_52w": round(float(analyzer.df["Low"].min()), 4),
            "avg_volume": int(analyzer.df["Volume"].mean()),
            "volatility": round(float(analyzer.df["Daily_Return"].std() * (252**0.5) * 100), 2),
        },
        "deviation_history": [
            {
                "date": row.Index.strftime("%Y-%m-%d"),
                "close": round(float(row.Close), 4),
                "sma_20": round(float(row.SMA_20), 4) if row.SMA_20 == row.SMA_20 else None,
                "price_dev_pct": round(float(row.Price_Dev_Pct), 2) if row.Price_Dev_Pct == row.Price_Dev_Pct else None,
                "z_score": round(float(row.Z_Score), 2) if row.Z_Score == row.Z_Score else None,
                "upper_2": round(float(row.Dev_Upper_2), 4) if row.Dev_Upper_2 == row.Dev_Upper_2 else None,
                "lower_2": round(float(row.Dev_Lower_2), 4) if row.Dev_Lower_2 == row.Dev_Lower_2 else None,
            }
            for row in analyzer.df.tail(60).itertuples()
        ],
    }
    return jsonify(data)


@app.route("/divergence")
def divergence_page():
    """Divergence scanner page."""
    return render_template("divergence.html")


@app.route("/api/divergence-scan")
def api_divergence_scan():
    """Scan top stocks for DE divergence signals. Uses all KLSE stocks from klsescreener."""
    top_n = request.args.get("top", 80, type=int)
    # Get all stocks from klsescreener sorted by volume
    all_stocks = get_all_stock_symbols(top_n=top_n)
    if not all_stocks:
        # Fallback to hardcoded list
        all_stocks = KLSE_STOCKS
    results = scan_top_stocks(all_stocks, max_stocks=top_n)
    return jsonify({
        "results": results,
        "count": len(results),
        "total_scanned": min(top_n, len(all_stocks)),
    })


@app.route("/api/klse-all")
def api_klse_all():
    """Get all KLSE stocks from klsescreener.com (Main + ACE + LEAP)."""
    market = request.args.get("market", "all")  # "all", "MAIN", "ACE", "LEAP"
    top_n = request.args.get("top", 100, type=int)
    stocks = fetch_all_stocks_by_volume(market=market, top_n=top_n)
    return jsonify({
        "stocks": stocks,
        "count": len(stocks),
        "market": market,
    })


@app.route("/api/signal/<symbol>")
def api_signal(symbol):
    """Generate Buy/Sell/Hold signal for a stock using all indicators."""
    result = generate_signal(symbol)
    return jsonify(result)


@app.route("/forecast")
def forecast_page():
    """Accumulation forecast page."""
    return render_template("forecast.html")


@app.route("/rainbow")
def rainbow_page():
    """Rainbow crossover scanner page."""
    return render_template("rainbow_scan.html")


@app.route("/api/accumulation-scan")
def api_accumulation_scan():
    """Scan for stocks with accumulation pattern."""
    top_n = request.args.get("top", 80, type=int)
    days = request.args.get("days", 30, type=int)
    all_stocks = get_all_stock_symbols(top_n=top_n)
    if not all_stocks:
        all_stocks = KLSE_STOCKS
    results = scan_accumulation(all_stocks, max_stocks=top_n, days=days)
    return jsonify({
        "results": results,
        "count": len(results),
        "total_scanned": min(top_n, len(all_stocks)),
        "days": days,
    })


@app.route("/api/rainbow-scan")
def api_rainbow_scan():
    """Scan for stocks with Rainbow crossover + volume increase."""
    top_n = request.args.get("top", 80, type=int)
    all_stocks = get_all_stock_symbols(top_n=top_n)
    if not all_stocks:
        all_stocks = KLSE_STOCKS
    results = scan_rainbow_crossover(all_stocks, max_stocks=top_n)
    return jsonify({
        "results": results,
        "count": len(results),
        "total_scanned": min(top_n, len(all_stocks)),
    })


@app.route("/api/stock/<symbol>/history")
def api_stock_history(symbol):
    """Full price history for charting."""
    if not symbol.endswith(".KL"):
        symbol = symbol + ".KL"

    period = request.args.get("period", "1y")
    interval = request.args.get("interval", "1d")
    df = get_stock_history(symbol, period=period, interval=interval)

    if df.empty:
        return jsonify({"error": f"No data for {symbol}", "history": []})

    analyzer = StockAnalyzer(df, symbol)

    history = []
    for row in analyzer.df.itertuples():
        # Use datetime format for intraday, date-only for daily
        if interval in ("1d", "5d", "1wk", "1mo"):
            date_str = row.Index.strftime("%Y-%m-%d")
        else:
            date_str = row.Index.strftime("%Y-%m-%d %H:%M")

        history.append({
            "date": date_str,
            "open": round(float(row.Open), 4),
            "high": round(float(row.High), 4),
            "low": round(float(row.Low), 4),
            "close": round(float(row.Close), 4),
            "volume": int(row.Volume),
            "sma_20": round(float(row.SMA_20), 4) if row.SMA_20 == row.SMA_20 else None,
            "sma_50": round(float(row.SMA_50), 4) if row.SMA_50 == row.SMA_50 else None,
            "rsi": round(float(row.RSI), 2) if row.RSI == row.RSI else None,
            "macd": round(float(row.MACD), 4) if row.MACD == row.MACD else None,
            "macd_signal": round(float(row.MACD_Signal), 4) if row.MACD_Signal == row.MACD_Signal else None,
            "bb_upper": round(float(row.BB_Upper), 4) if row.BB_Upper == row.BB_Upper else None,
            "bb_lower": round(float(row.BB_Lower), 4) if row.BB_Lower == row.BB_Lower else None,
            "price_dev_pct": round(float(row.Price_Dev_Pct), 2) if row.Price_Dev_Pct == row.Price_Dev_Pct else None,
            "z_score": round(float(row.Z_Score), 2) if row.Z_Score == row.Z_Score else None,
            "homily_sar": round(float(row.Homily_SAR), 4) if row.Homily_SAR == row.Homily_SAR else None,
            "homily_color": row.Homily_Color,
            "de_value": round(float(row.DE_Value), 4) if row.DE_Value == row.DE_Value else None,
            "de_color": row.DE_Color,
            "l3_banker": round(float(row.L3_Banker), 4) if row.L3_Banker == row.L3_Banker else None,
            "l3_signal": row.L3_Banker_Signal,
            "mcdx_banker": round(float(row.MCDX_Banker), 2) if row.MCDX_Banker == row.MCDX_Banker else None,
            "mcdx_hot": round(float(row.MCDX_HotMoney), 2) if row.MCDX_HotMoney == row.MCDX_HotMoney else None,
            "mcdx_retail": round(float(row.MCDX_Retail), 2) if hasattr(row, 'MCDX_Retail') and row.MCDX_Retail == row.MCDX_Retail else None,
            "mcdx_signal": row.MCDX_Signal,
            "qsw": round(float(row.QSW), 4) if row.QSW == row.QSW else None,
            "qsw_signal": round(float(row.QSW_Signal), 4) if row.QSW_Signal == row.QSW_Signal else None,
            "qsw_hist": round(float(row.QSW_Hist), 4) if row.QSW_Hist == row.QSW_Hist else None,
            "rainbow_red": round(float(row.Rainbow_Red), 4) if row.Rainbow_Red == row.Rainbow_Red else None,
            "rainbow_yellow": round(float(row.Rainbow_Yellow), 4) if row.Rainbow_Yellow == row.Rainbow_Yellow else None,
            "rainbow_green": round(float(row.Rainbow_Green), 4) if row.Rainbow_Green == row.Rainbow_Green else None,
            "rainbow_blue": round(float(row.Rainbow_Blue), 4) if row.Rainbow_Blue == row.Rainbow_Blue else None,
            "rainbow_white": round(float(row.Rainbow_White), 4) if row.Rainbow_White == row.Rainbow_White else None,
            "position_life": round(float(row.Position_Life), 4) if row.Position_Life == row.Position_Life else None,
            "position_upper": round(float(row.Position_Upper), 4) if row.Position_Upper == row.Position_Upper else None,
            "position_lower": round(float(row.Position_Lower), 4) if row.Position_Lower == row.Position_Lower else None,
            "banker_holding": round(float(row.Banker_Holding), 2) if row.Banker_Holding == row.Banker_Holding else None,
            "banker_control": round(float(row.Banker_Control), 2) if row.Banker_Control == row.Banker_Control else None,
        })

    return jsonify({"symbol": symbol, "history": history})


if __name__ == "__main__":
    print("=" * 50)
    print("  KLSE Stock Analyzer - Web Interface")
    print("  Open http://localhost:5000 in your browser")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=5000)
