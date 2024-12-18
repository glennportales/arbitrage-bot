import ccxt
import time
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

# =========================
# Configuration Parameters
# =========================

paper_trade = True
exchanges = {
    "binance": ccxt.binance(),
    "kraken": ccxt.kraken(),
    # Add more exchanges if desired
}

symbol = "SOL/USDT"
fee_tolerance = 0.005
sleep_interval = 10
timeframe = '1m'
limit = 50

# =========================
# Helper Functions
# =========================

def get_prices():
    prices = {}
    for name, exchange in exchanges.items():
        try:
            ticker = exchange.fetch_ticker(symbol)
            if ticker['bid'] is not None and ticker['ask'] is not None:
                prices[name] = {
                    "bid": ticker["bid"],
                    "ask": ticker["ask"]
                }
        except Exception as e:
            print(f"Error fetching prices from {name}: {e}")
    return prices

def find_arbitrage_opportunity(prices):
    for exchange_a, data_a in prices.items():
        for exchange_b, data_b in prices.items():
            if exchange_a != exchange_b:
                buy_price = data_a["ask"]
                sell_price = data_b["bid"]
                profit = sell_price - buy_price
                if profit > buy_price * fee_tolerance:
                    return (exchange_a, exchange_b, buy_price, sell_price, profit)
    return None

def execute_trade(buy_exchange_name, sell_exchange_name, buy_price, sell_price, amount):
    buy_exchange = exchanges[buy_exchange_name]
    sell_exchange = exchanges[sell_exchange_name]

    try:
        print(f"Placing buy order on {buy_exchange_name} for {amount} {symbol} at market price.")
        buy_order = buy_exchange.create_order(symbol, 'market', 'buy', amount)
        print(f"Buy order placed: {buy_order}")

        print(f"Placing sell order on {sell_exchange_name} for {amount} {symbol} at market price.")
        sell_order = sell_exchange.create_order(symbol, 'market', 'sell', amount)
        print(f"Sell order placed: {sell_order}")

    except Exception as e:
        print(f"Error executing trade: {e}")

def fetch_ohlcv_data(exchange, symbol, timeframe='1m', limit=50):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        if not ohlcv:
            return pd.DataFrame()

        df = pd.DataFrame(ohlcv, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
        df['Date'] = pd.to_datetime(df['Date'], unit='ms', errors='coerce')
        df.set_index('Date', inplace=True)

        if df.empty or not isinstance(df.index, pd.DatetimeIndex):
            return pd.DataFrame()

        return df
    except Exception as e:
        print(f"Error fetching OHLCV data: {e}")
        return pd.DataFrame()

# =========================
# Chart Setup
# =========================

plt.ion()

num_exchanges = len(exchanges)
fig, axes = plt.subplots(num_exchanges, 1, figsize=(10, 5 * num_exchanges), sharex=True)

# If there's only one exchange, axes won't be an array, so wrap it in a list
if num_exchanges == 1:
    axes = [axes]

fig.show()

exchange_list = list(exchanges.keys())

# =========================
# Main Loop
# =========================

def main():
    print("Starting arbitrage bot...")

    while True:
        prices = get_prices()
        if len(prices) < 2:
            print("Could not fetch enough price data to find opportunities.")
            time.sleep(sleep_interval)
            continue

        opportunity = find_arbitrage_opportunity(prices)
        if opportunity:
            buy_exchange, sell_exchange, buy_price, sell_price, profit = opportunity
            print(f"\nArbitrage opportunity found:")
            print(f"Buy on {buy_exchange} at {buy_price}, Sell on {sell_exchange} at {sell_price}")
            print(f"Estimated profit per unit: {profit}\n")

            if paper_trade:
                print(f"Simulated trade: Buy on {buy_exchange}, sell on {sell_exchange}")
            else:
                trade_amount = 1.0
                execute_trade(buy_exchange, sell_exchange, buy_price, sell_price, trade_amount)
        else:
            print("No arbitrage opportunities found.")

        # Update charts for all exchanges
        for i, ex_name in enumerate(exchange_list):
            ax = axes[i]
            df = fetch_ohlcv_data(exchanges[ex_name], symbol, timeframe=timeframe, limit=limit)

            ax.clear()
            if df.empty:
                ax.set_title(f"{ex_name.upper()} {symbol} (No Data)")
            else:
                mpf.plot(df, type='candle', ax=ax, style='charles', show_nontrading=False)
                ax.set_title(f"{ex_name.upper()} {symbol} {timeframe} Candles")

        plt.pause(0.01)  
        time.sleep(sleep_interval)

if __name__ == "__main__":
    main()
