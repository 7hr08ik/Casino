Game Integration Module
=======================

Okay, let's tackle this problem. The user wants to integrate their mini-games with the lobby so that the player's cash balance is maintained across all games. The main tasks are to ensure the lobby sends player data to mini-games, mini-games use that data, save on exit, and handle the loser screen if cash drops below 1.
First, I need to check the game_integration.py file they mentioned. Since the user didn't provide its content, I'll assume it's missing or incomplete. My goal is to create this file with necessary functions.

The lobby (main.py) uses subprocess to run mini-games. To pass player data, the lobby can write it to a temporary file when a mini-game is launched. The mini-game then reads this file on startup.

For the game_integration module, it should handle loading the player data at the start of each mini-game. Functions needed include loading the player data, saving it back when the game exits, and checking the cash balance to trigger the exit loser screen if needed.

In each mini-game, they'll need to import game_integration, replace their initial cash variable with the loaded player's cash, and ensure that when the game exits, it saves the updated data back to the temporary file. Also, during gameplay, they should periodically check if the cash is below 1 and call the exit loser function.

I should structure the game_integration.py to have functions like load_player_data, save_player_data, and check_balance. The load function reads the temporary file, save writes back, and check_balance handles the exit condition.

The lobby's activate_target function needs modification to write the player data to a temporary file (like /tmp/current_player.json) before launching the mini-game. Then, each mini-game, upon starting, reads this file to get the player's current state.

When a mini-game exits, it should save the updated player data, which the lobby can read upon returning to update its own player_data. This way, the lobby always has the latest cash balance and high scores.

I also need to ensure that the ExitUI's draw_exit_loser is accessible, maybe by having the game_integration module import it and call it when the cash is too low.

Testing steps are important. The user should verify data passing, cash updates, and loser screen triggering. They'll need to add a few lines to each mini-game's main function to integrate these checks and saves.

Potential issues include file path differences between OSes, so using a platform-independent temp directory would help. Also, ensuring that all mini-games handle exceptions when reading/writing the temp file.

In summary, the game_integration module acts as a bridge, handling data persistence and exit conditions. Each mini-game imports this module, uses its functions to load/save data, and checks the cash balance during gameplay.

I'll help you create a robust game integration system. Let's analyze your requirements and create a solution that works with your existing architecture.

First, let's create the game_integration.py file with all necessary functions:


Modifications needed in your lobby (main.py):
=============================================

Update the activate_target function:
------------------------------------

``` py
def activate_target(screen, player_data, player_rect, target_rect, game_command=None):
    if player_rect.colliderect(target_rect):
        # Save player data to temp file
        with open(TEMP_FILE, 'w') as f:
            json.dump(player_data, f)
            
        if game_command == leave_game:
            exit_ui = ExitUI(screen)
            exit_ui.print_exit_ui(screen, player_data)
        pg.quit()
        if game_command:
            subprocess.run(game_command, check=False)
        sys.exit()
```

Instructions for mini-game integration:
=======================================

In each mini-game's main file, add these imports:
-------------------------------------------------
```py
from game_integration import (
    load_lobby_player_data,
    save_and_exit,
    check_balance,
    setup_game_window
)
```

Replace the game's initialization with:
---------------------------------------
```py
def main():
    screen = setup_game_window()
    player_data = load_lobby_player_data()
    
    # Replace original cash variable with:
    current_cash = player_data["cash_balance"]
    
    # Add this to your game loop:
    while running:
        check_balance(screen, player_data)
        # ... existing game logic
        
    # When exiting normally:
    save_and_exit(screen, player_data)
```

Update all cash references:
===========================
Replace all cash = starting_value with references to current_cash

When modifying cash, update both the local variable AND player_data:
player_data["cash_balance"] += amount  # or -= amount
current_cash = player_data["cash_balance"]

Key integration points for each mini-game:
==========================================

Import the integration module
Load player data at startup
Use player_data["cash_balance"] instead of local cash variables
Call check_balance() regularly in the game loop
Use save_and_exit() instead of normal exit procedures
Remove any existing save/load systems

Testing procedure:
==================

Verify player data persists between games
Test cash updates reflect in the lobby
Verify loser screen triggers at < $1
Check high scores are maintained
Test returning to lobby after game exit

Example mini-game modification (blackjack):
===========================================

# Old code
cash = 1000

# New code
from game_integration import load_lobby_player_data, save_and_exit, check_balance

```py
def main():
    player_data = load_lobby_player_data()
    cash = player_data["cash_balance"]
    
    # In betting logic:
    player_data["cash_balance"] -= bet_amount
    cash = player_data["cash_balance"]
    
    # In exit logic:
    save_and_exit(screen, player_data)
```

This system maintains your architecture while adding minimal overhead. Each game only needs to:
===============================================================================================

Import 4 functions
Initialize with loaded data
Update player_data instead of local vars
Use the provided exit handler
Would you like me to provide specific modification examples for any particular part of the system?
