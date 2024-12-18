import ccxt
import time

# =========================
# Configuration Parameters
# =========================

# Set paper trading mode to True to simulate trades
# Set to False for live trades (requires valid API keys and caution)
paper_trade = True

# Exchanges configuration: Add or remove exchanges here.
# For live trading, add your API keys, secrets, and any necessary parameters.
exchanges = {
    "binance": ccxt.binance({
        # Uncomment and set when ready for real trading or testnet usage
        # 'apiKey': 'YOUR_BINANCE_API_KEY',
        # 'secret': 'YOUR_BINANCE_SECRET',
        # 'enableRateLimit': True,
        # 'urls': {
        #   'api': {
        #       'public': 'https://testnet.binance.vision/api',
        #       'private': 'https://testnet.binance.vision/api',
        #   }
        # }
    }),
    "kraken": ccxt.kraken({
        # 'apiKey': 'YOUR_KRAKEN_API_KEY',
        # 'secret': 'YOUR_KRAKEN_SECRET',
        # 'enableRateLimit': True
    }),
    # Add more exchanges as needed:
    # "ftx": ccxt.ftx({ ... })
}

symbol = "SOL/USDT"       # The trading pair to look for arbitrage
fee_tolerance = 0.005      # Fee tolerance (0.5%)
sleep_interval = 10        # Interval in seconds between checks

# =========================
# Helper Functions
# =========================

def get_prices():
    """
    Fetch the current bid and ask prices for the specified symbol
    from all configured exchanges.
    """
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
    """
    Find an arbitrage opportunity by comparing prices between exchanges.
    Tries buying on one exchange and selling on another to see if profit > fee tolerance.
    """
    for exchange_a, data_a in prices.items():
        for exchange_b, data_b in prices.items():
            if exchange_a != exchange_b:
                # Potential arbitrage: Buy on A (at ask) and sell on B (at bid)
                buy_price = data_a["ask"]
                sell_price = data_b["bid"]
                profit = sell_price - buy_price
                if profit > buy_price * fee_tolerance:
                    return (exchange_a, exchange_b, buy_price, sell_price, profit)
    return None

def execute_trade(buy_exchange_name, sell_exchange_name, buy_price, sell_price, amount):
    """
    Execute trades if not in paper trade mode.
    For simplicity, this function is a placeholder. In a real scenario:
    - Authenticate with the exchange
    - Create a buy order on buy_exchange_name
    - Create a sell order on sell_exchange_name
    - Handle order confirmations, errors, etc.
    """
    buy_exchange = exchanges[buy_exchange_name]
    sell_exchange = exchanges[sell_exchange_name]

    # For demonstration, we assume market orders. Be careful with slippage in real scenarios.
    try:
        # Buy order
        print(f"Placing buy order on {buy_exchange_name} for {amount} {symbol} at market price.")
        buy_order = buy_exchange.create_order(symbol, 'market', 'buy', amount)
        print(f"Buy order placed: {buy_order}")

        # Sell order
        print(f"Placing sell order on {sell_exchange_name} for {amount} {symbol} at market price.")
        sell_order = sell_exchange.create_order(symbol, 'market', 'sell', amount)
        print(f"Sell order placed: {sell_order}")

    except Exception as e:
        print(f"Error executing trade: {e}")

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
                # Just simulate the trade
                print(f"Simulated trade: Buy on {buy_exchange}, sell on {sell_exchange}")
            else:
                # Execute the trade. Define an amount you want to trade.
                # This could be a parameter or determined dynamically based on your capital.
                trade_amount = 1.0  # Example: 1 SOL
                execute_trade(buy_exchange, sell_exchange, buy_price, sell_price, trade_amount)
        else:
            print("No arbitrage opportunities found.")

        time.sleep(sleep_interval)

if __name__ == "__main__":
    main()
