import json
import os
import sys
from pathlib import Path

import pygame as pg

# Import your existing systems
from logic.save_load import save_player_data
from ui.exit_ui import ExitUI

TEMP_FILE = Path("/tmp/current_player.json")  # Platform-agnostic temp file?


def load_lobby_player_data():
    """Load player data from lobby's temporary storage"""
    try:
        with open(TEMP_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        print("No player data found! Returning to lobby...")
        return_to_lobby()


def save_and_exit(screen, player_data):
    """Save player data and return to lobby"""
    save_player_data(player_data["player_name"], player_data["cash_balance"], player_data["high_scores"])
    return_to_lobby()


def check_balance(screen, player_data):
    """Check if player's balance is too low"""
    if player_data["cash_balance"] < 1:
        exit_ui = ExitUI(screen)
        exit_ui.draw_exit_loser(screen, player_data["player_name"])


def return_to_lobby():
    """Return control to the main lobby"""
    pg.quit()
    # Launch lobby process
    if sys.platform == "win32":
        os.system("start python main.py")
    else:
        os.system("python3 main.py &")
    sys.exit()


def setup_game_window():
    """Standard game window setup"""
    pg.init()
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("Casino Game")
    return screen
