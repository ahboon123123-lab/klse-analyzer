"""
Visualization module for stock analysis charts.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd


def plot_stock_analysis(df: pd.DataFrame, symbol: str, output_dir: str = "output"):
    """
    Generate comprehensive stock analysis charts.

    Args:
        df: DataFrame with OHLCV data and calculated indicators
        symbol: Stock symbol for chart titles
        output_dir: Directory to save chart images
    """
    os.makedirs(output_dir, exist_ok=True)
    sns.set_style("darkgrid")

    _plot_price_and_volume(df, symbol, output_dir)
    _plot_technical_indicators(df, symbol, output_dir)
    _plot_returns_distribution(df, symbol, output_dir)


def _plot_price_and_volume(df: pd.DataFrame, symbol: str, output_dir: str):
    """Plot price chart with moving averages and volume."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), height_ratios=[3, 1], sharex=True)

    # Price with moving averages
    ax1.plot(df.index, df["Close"], label="Close", linewidth=1.5, color="black")
    ax1.plot(df.index, df["SMA_20"], label="SMA 20", linewidth=1, alpha=0.7)
    ax1.plot(df.index, df["SMA_50"], label="SMA 50", linewidth=1, alpha=0.7)

    if "BB_Upper" in df.columns:
        ax1.fill_between(df.index, df["BB_Upper"], df["BB_Lower"], alpha=0.1, color="gray", label="Bollinger Bands")

    ax1.set_title(f"{symbol} - Price & Moving Averages", fontsize=14, fontweight="bold")
    ax1.set_ylabel("Price (RM)")
    ax1.legend(loc="upper left")
    ax1.grid(True, alpha=0.3)

    # Volume
    colors = ["green" if df["Close"].iloc[i] >= df["Open"].iloc[i] else "red" for i in range(len(df))]
    ax2.bar(df.index, df["Volume"], color=colors, alpha=0.6, width=0.8)
    ax2.set_ylabel("Volume")
    ax2.set_xlabel("Date")

    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{symbol.replace('.', '_')}_price.png"), dpi=150, bbox_inches="tight")
    plt.close()


def _plot_technical_indicators(df: pd.DataFrame, symbol: str, output_dir: str):
    """Plot RSI and MACD indicators."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 6), sharex=True)

    # RSI
    ax1.plot(df.index, df["RSI"], color="purple", linewidth=1.2)
    ax1.axhline(y=70, color="red", linestyle="--", alpha=0.5, label="Overbought (70)")
    ax1.axhline(y=30, color="green", linestyle="--", alpha=0.5, label="Oversold (30)")
    ax1.fill_between(df.index, 70, df["RSI"], where=(df["RSI"] >= 70), alpha=0.2, color="red")
    ax1.fill_between(df.index, 30, df["RSI"], where=(df["RSI"] <= 30), alpha=0.2, color="green")
    ax1.set_title(f"{symbol} - RSI (14)", fontsize=12, fontweight="bold")
    ax1.set_ylabel("RSI")
    ax1.set_ylim(0, 100)
    ax1.legend(loc="upper left")

    # MACD
    ax2.plot(df.index, df["MACD"], label="MACD", color="blue", linewidth=1.2)
    ax2.plot(df.index, df["MACD_Signal"], label="Signal", color="orange", linewidth=1.2)
    ax2.bar(df.index, df["MACD_Histogram"], color=["green" if v >= 0 else "red" for v in df["MACD_Histogram"]], alpha=0.4)
    ax2.axhline(y=0, color="gray", linestyle="-", alpha=0.3)
    ax2.set_title(f"{symbol} - MACD", fontsize=12, fontweight="bold")
    ax2.set_ylabel("MACD")
    ax2.legend(loc="upper left")

    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{symbol.replace('.', '_')}_indicators.png"), dpi=150, bbox_inches="tight")
    plt.close()


def _plot_returns_distribution(df: pd.DataFrame, symbol: str, output_dir: str):
    """Plot returns distribution and cumulative returns."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Returns histogram
    returns = df["Daily_Return"].dropna()
    ax1.hist(returns, bins=50, color="steelblue", alpha=0.7, edgecolor="black", linewidth=0.5)
    ax1.axvline(x=returns.mean(), color="red", linestyle="--", label=f"Mean: {returns.mean() * 100:.2f}%")
    ax1.set_title(f"{symbol} - Daily Returns Distribution", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Daily Return")
    ax1.set_ylabel("Frequency")
    ax1.legend()

    # Cumulative returns
    ax2.plot(df.index, df["Cumulative_Return"] * 100, color="darkgreen", linewidth=1.5)
    ax2.fill_between(df.index, 0, df["Cumulative_Return"] * 100, alpha=0.1, color="green")
    ax2.axhline(y=0, color="gray", linestyle="-", alpha=0.3)
    ax2.set_title(f"{symbol} - Cumulative Return", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Cumulative Return (%)")

    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{symbol.replace('.', '_')}_returns.png"), dpi=150, bbox_inches="tight")
    plt.close()
