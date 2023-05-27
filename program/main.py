from constants import ABORT_ALL_POSITIONS
from func_connections import connect_dydx
from func_private import abort_all_positions, place_market_order

if __name__ == "__main__":
    try:
        print("Connecting to client...")
        client = connect_dydx()
    except Exception as e:
        print("Error connecting to client: ", e)
        exit(1)

    # Abort all positions
    if ABORT_ALL_POSITIONS:
        try:
            print("Closing all positions...")
            close_orders = abort_all_positions(client)
        except Exception as e:
            print("Error closing positions: ", e)
            exit(1)
