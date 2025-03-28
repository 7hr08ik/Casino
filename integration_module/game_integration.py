# ===========================
# Python game suite
# Mini-Game Integration module
#
# Author: Rob Hickling
# 19/03/2025
# ===========================

import json
import os
import sys
import tempfile

import pygame as pg

# Add Casino project root directory to Python path
casino_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(casino_root)

# Import your existing systems
from logic.save_load import save_player_data  # noqa: E402
from ui.exit_ui import ExitUI  # noqa: E402

TEMP_FILE = os.path.join(tempfile.gettempdir(), "current_player.json")

"""
Notes on usage:
    load_lobby_player_data() = Load player data from the lobby
    save_and_exit()          = Save player data and return to the lobby
    check_balance()          = Check if player's balance is too low
    maze_exit()              = When exiting the maze
"""

# -------------------------------------------------------------------------
# Utilities
#


def return_to_lobby():
    """
    Return to the main lobby
    """
    pg.quit()
    # Launch lobby process
    if sys.platform == "win32":
        os.system("start python main.py")
    else:
        os.system("python3 -m main")

    sys.exit()


def load_player_data():
    """
    Load player data from lobby's temporary storage
    """
    try:
        with open(TEMP_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        print("No player data found! Returning to lobby...")
        return_to_lobby()


# -------------------------------------------------------------------------
# Functions
#


def save_and_exit(screen, player_data):
    """
    Save player data and return to lobby.
    Data is saved in both the temp file and the full database
    """

    # Save player data to temp file for the lobby
    with open(TEMP_FILE, "w") as f:
        json.dump(player_data, f)

    # Save to full database as well
    save_player_data(
        player_data["player_name"],
        player_data["cash_balance"],
        player_data["high_scores"],
    )

    return_to_lobby()


def check_balance(screen, player_data):
    """
    Check if player's balance is too low.
    If the player has no balance, show the loser screen
    """

    if player_data["cash_balance"] < 1:
        exit_ui = ExitUI(screen)
        exit_ui.draw_exit_loser(screen, player_data["player_name"])


def maze_exit(screen, player_data):
    """
    When exiting the maze:
    1. Save player data to both files
    2. Show exit UI
    """

    player_data = load_player_data()

    # Save to main database
    save_player_data(
        player_data["player_name"],
        player_data["cash_balance"],
        player_data["high_scores"],
    )

    # Show exit UI
    exit_ui = ExitUI(screen)
    exit_ui.print_exit_ui(screen, player_data)
