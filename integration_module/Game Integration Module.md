Instructions for mini-game integration:
=======================================

Key integration points for each mini-game:
------------------------------------------

Import the integration module
Load player data at startup
Use player_data["cash_balance"] instead of local cash variables
Call check_balance() regularly in the game loop
Use save_and_exit() instead of normal exit procedures
Remove any existing save/load systems

Note to add
-----------

# Modified by: Rob Hickling
# 21/03/2025
# Added functionality for saving and loading player data
# required for integration into the lobby
# all commented with;
#    # For game_integration
# ===========================

Add Imports:
------------
```py

# For game_integration
# Add Casino project root directory to Python path
casino_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
) # Up 2 folders
sys.path.append(casino_root) # Append to imports below this
from integration_module.game_integration import (  # noqa: E402
    check_balance,
    load_player_data,
    save_and_exit,
    maze_exit,
)

```

Game Loop:
----------
```py
def main():

    # For game_integration
    # Replace original cash variable:
    current_cash = player_data["cash_balance"]
    
    # Add this to your game loop:
    while running:
        # For game_integration
        player_data = load_player_data() # Load the data
        # Other tweaks may be needed. To make sure the balance is upto date
        player_data["cash_balance"] = ui_balance
        check_balance(screen, player_data) # check for no money
        # ... existing game logic
        
    # When exiting normally:
    # For game_integration
    save_and_exit(screen, player_data)
```

Update all cash references:
===========================
Replace all cash = starting_value with references to current_cash

When modifying cash, update both the local variable AND player_data:

# For game_integration
player_data = load_player_data()
self.balance = player_data["cash_balance"]

player_data["cash_balance"] += amount  # or -= amount
current_cash = player_data["cash_balance"]


Testing procedure:
==================

Verify player data persists between games
Test cash updates reflect in the lobby
Verify loser screen triggers at < $1
Check high scores are maintained
Test returning to lobby after game exit
