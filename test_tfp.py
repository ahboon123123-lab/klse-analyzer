from yahoo_api import fetch_most_active_malaysia

quotes = fetch_most_active_malaysia(100)
print(f"Got {len(quotes)} stocks")

found = [q for q in quotes if "0145" in q.get("symbol", "")]
if found:
    q = found[0]
    print(f"Found TFP: {q.get('symbol')} Vol: {q.get('regularMarketVolume',0):,}")
else:
    print("0145.KL not in top 100")
    print("Last 5 stocks in list:")
    for q in quotes[-5:]:
        print(f"  {q.get('symbol')} Vol: {q.get('regularMarketVolume',0):,}")
