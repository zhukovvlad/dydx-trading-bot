from constants import CLOSE_AT_ZSCORE_CROSS
from func_utils import format_number
from func_public import get_candles_recent
from func_cointegration import calculate_zscore
from func_private import place_market_order
import json
import time

from pprint import pprint

# Close positions manage
def manage_trade_exits(client):
    """
	Manage exiting open positions
    Based upon criteria set in constants
    """
    
	# Initialize saving output
    save_output = []
    
	# Opening JSON file
    try:
        open_positions_file = open("bot_agents.json")
        open_positions_dict = json.load(open_positions_file)
    except:
        return "complete"
    
	# Guard: Exit if no open position in file
    if len(open_positions_dict) < 1:
        return "complete"
    
	# Get all open positions
    exchange_pos = client.private.get_positions(status="OPEN")
    all_exc_positions = exchange_pos.data["positions"]
    markets_live = [x["market"] for x in all_exc_positions]
    
	# Protect API
    time.sleep(0.5)
    
	# Check all saved positions match order record
	# Exit trade according to any exit rule
    for position in open_positions_dict:

        # Initialize close trigger
        is_close = False
        
        # Exctract position matching information from file - market_1
        position_market_m1 = position["market_1"]
        position_size_m1 = position["order_m1_size"]
        position_side_m1 = position["order_m1_side"]
        
		# Exctract position matching information from file - market_1
        position_market_m2 = position["market_2"]
        position_size_m2 = position["order_m2_size"]
        position_side_m2 = position["order_m2_side"]
        
		# Protect API
        time.sleep(0.5)