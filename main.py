"""
KLSE Stock Analyzer
Retrieve and analyze Bursa Malaysia stock data from Yahoo Finance.

Yahoo Finance uses the suffix '.KL' for KLSE-listed stocks.
Example: Maybank = 1155.KL, CIMB = 1023.KL, Tenaga = 5347.KL
"""

from data_fetcher import fetch_stock_data, get_popular_klse_stocks
from analyzer import StockAnalyzer
from visualizer import plot_stock_analysis


def main():
    print("=" * 60)
    print("KLSE Stock Analyzer")
    print("=" * 60)

    # Show popular KLSE stocks
    popular = get_popular_klse_stocks()
    print("\nPopular KLSE Stocks:")
    print("-" * 40)
    for symbol, name in popular.items():
        print(f"  {symbol:<10} - {name}")

    # Fetch data for a default stock (Maybank)
    symbol = "1155.KL"
    print(f"\nFetching data for {popular.get(symbol, symbol)} ({symbol})...")
    df = fetch_stock_data(symbol, period="1y")

    if df.empty:
        print("No data retrieved. Check your internet connection or symbol.")
        return

    print(f"Retrieved {len(df)} trading days of data.")
    print(f"Date range: {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}")

    # Run analysis
    analyzer = StockAnalyzer(df, symbol)

    print("\n" + "=" * 60)
    print("PRICE SUMMARY")
    print("=" * 60)
    analyzer.print_price_summary()

    print("\n" + "=" * 60)
    print("TECHNICAL INDICATORS")
    print("=" * 60)
    analyzer.print_technical_indicators()

    print("\n" + "=" * 60)
    print("PERFORMANCE METRICS")
    print("=" * 60)
    analyzer.print_performance_metrics()

    # Generate charts
    print("\nGenerating analysis charts...")
    plot_stock_analysis(analyzer.df, symbol)
    print("Charts saved to 'output/' folder.")


if __name__ == "__main__":
    main()
