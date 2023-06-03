from datetime import datetime, timedelta
from func_utils import format_number
import time

from pprint import pprint

# Get open positions


def is_open_positions(client, market):
    """
    Function to check if there are any open positions for a given market.

    Parameters:
    client: The trading client instance.
    market: String representing the market to check.

    Returns:
    bool: True if there are open positions, False otherwise.
    """

    # Protect API
    time.sleep(0.2)

    # Get positions
    all_positions = client.private.get_positions(
        market=market,
        status="OPEN"
    )

    # Determine if open
    if len(all_positions.data["positions"]) > 0:
        return True
    else:
        return False

# Check order status


def check_order_status(client, order_id):
    """
    Function to check the status of an order.

    Parameters:
    client: The trading client instance.
    order_id: The id of the order to check.

    Returns:
    str: The status of the order, or "FAILED" if the order doesn't exist.
    """
    # Retrieve the order by its id
    order = client.private.get_order_by_id(order_id)

    # Return the order's status if the order exists, otherwise return "FAILED"
    if order.data:
        if "order" in order.data.keys():
            return order.data["order"]["status"]
    return "FAILED"


# Place market orders
def place_market_order(client, market, side, size, price, reduce_only):
    # Get position Id
    account_response = client.private.get_account()
    position_id = account_response.data["account"]["positionId"]

    # Get expiration time
    server_time = client.public.get_time()
    expiration = datetime.fromisoformat(
        server_time.data["iso"].replace("Z", "")) + timedelta(seconds=70000)

    # Place an order
    placed_order = client.private.create_order(
        position_id=position_id,
        market=market,
        side=side,
        order_type="MARKET",
        post_only=False,
        size=size,
        price=price,
        limit_fee="0.015",
        expiration_epoch_seconds=expiration.timestamp(),
        time_in_force="FOK",
        reduce_only=reduce_only
    )

    # Return result
    return placed_order.data

# Abort all open positions


def abort_all_positions(client):

    # Cancel orders
    client.private.cancel_all_orders()

    # Protect API
    time.sleep(0.5)

    # Get markets for reference of tick size
    markets = client.public.get_markets().data

    # Get all positions
    positions = client.private.get_positions(status="OPEN")
    all_positions = positions.data["positions"]
    print(all_positions)

    # Handle open positions
    close_orders = []
    if len(all_positions) > 0:

        # Loop through positions
        for position in all_positions:
            # Determine market
            market = position["market"]

            # Determine side
            side = "BUY"
            if position["side"] == "LONG":
                side = "SELL"

            # Get price
            price = float(position["entryPrice"])
            accept_price = price * 1.7 if side == "BUY" else price * 0.3
            tick_size = markets["markets"][market]["tickSize"]
            # print("MARKET IS: ", markets["markets"][market])
            # print("ACCEPT PRICE: ", accept_price)
            # print("TICK SIZE: ", tick_size)
            accept_price = format_number(accept_price, tick_size)

            # Place order
            order = place_market_order(
                client,
                market,
                side,
                position["sumOpen"],
                accept_price,
                True
            )

            # Append results
            close_orders.append(order)

            # Protect API
            time.sleep(0.2)

            # Return close orders
        return close_orders
