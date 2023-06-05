from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED, PLACE_TRADES, MANAGE_EXITS
from func_connections import connect_dydx
from func_private import abort_all_positions
from func_public import construct_market_prices
from func_cointegration import store_cointegration_results
from func_entry_pairs import open_positions
from func_exit_pairs import manage_trade_exits
from func_messaging import send_message

if __name__ == "__main__":

    # Message from start
    send_message("Here we go again! Bot launch successful...")

    try:
        print("Connecting to client...")
        client = connect_dydx()
    except Exception as e:
        print("Error connecting to client: ", e)
        send_message(f"Failed to connect to client: {e}")
        exit(1)

    # Abort all positions
    if ABORT_ALL_POSITIONS:
        try:
            print("Closing all positions...")
            close_orders = abort_all_positions(client)
        except Exception as e:
            print("Error closing positions: ", e)
            send_message(f"Error closing all positions: {e}")
            exit(1)

    # Find cointegrated pairs
    if FIND_COINTEGRATED:

        # Construct market prices
        try:
            print("Fetching market prices, please allow 3 minutes...")
            df_market_prices = construct_market_prices(client)
        except Exception as e:
            print("Error constructing market prices: ", e)
            send_message(f"Error constructing market prices: {e}")
            exit(1)

        # Store cointegrated pairs
        try:
            print("Storing cointegrated pairs...")
            stores_result = store_cointegration_results(df_market_prices)
            if stores_result != "saved":
                print("Error saving cointegrated pairs")
                exit(1)
        except Exception as e:
            print("Error saving cointegrated pairs: ", e)
            send_message(f"Error saving cointegrated pairs: {e}")
            exit(1)

    # Run as always on
    while True:

        if MANAGE_EXITS:
            try:
                print("Managing exits...")
                manage_trade_exits(client)
            except Exception as e:
                print("Error managing exiting positions: ", e)
                send_message(f"Error managing exiting positions: {e}")
                exit(1)

        # Place trades for opening positions
        if PLACE_TRADES:
            try:
                print("Finding trading opportunities...")
                open_positions(client)
            except Exception as e:
                print("Error trading pairs: ", e)
                send_message(f"Error opening trades: {e}")
                exit(1)
