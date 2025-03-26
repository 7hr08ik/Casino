# ===========================
# Python game suite
# Casino Lobby
#
# Author: Rob Hickling -- E4491341
# 28/01/2025
# ===========================
#
# Main Imports
import contextlib
import json
import os
import subprocess
import sys
import tempfile
import time

import pygame as pg

# Local Imports
import lobby_conf as conf
from logic.player import Player
from logic.save_load import save_player_data
from ui.exit_ui import ExitUI
from ui.ui import UIElements

# Just needs something to be set to keep VSCode happy
# Used in the activate_target function
leave_game = True

# For game_integration
# Platform agnostic temp file, does NOT work when linking to conf file???
TEMP_FILE = os.path.join(tempfile.gettempdir(), "current_player.json")


# -------------------------------------------------------------------------
# Utilities
#
def draw_target(screen, color, position, size, alpha=0):
    """
    Draw target points on the screen.
    Targets are transparent but have a border.
    """
    # 1 - Create surface
    target_surface = pg.Surface((size, size), pg.SRCALPHA)
    # 2 - Make the surface transparent
    target_surface.fill((color[0], color[1], color[2], alpha))
    # 3 - Put surface in a rectangle
    pg.draw.rect(target_surface, color, (0, 0, size, size), 3)
    # 4 - Print screen with transparent surface in position
    screen.blit(target_surface, position)


def activate_target(
    screen, player_data, player_rect, target_rect, game_command=None
):
    """
    When player reaches target, run given command
    """

    # For game_integration
    # Save player data to temp file to be opened by next game
    with open(TEMP_FILE, "w") as f:
        json.dump(player_data, f)

    if player_rect.colliderect(target_rect):
        if game_command == leave_game:
            exit_ui = ExitUI(screen)
            exit_ui.print_exit_ui(screen, player_data)
            # pg.quit()
            sys.exit()
        if game_command:
            pg.quit()
            subprocess.run(game_command, check=False)
            sys.exit()
        pg.quit()
        sys.exit()


def check_player_balance(screen, player_data):
    """
    Check if player's cash balance has reached 0 or below.
    Display exit screen if player is broke.
    """
    # Ensure cash_balance is an integer to prevent type errors
    if not isinstance(player_data["cash_balance"], int):
        player_data["cash_balance"] = int(player_data["cash_balance"])

    if player_data["cash_balance"] < 1:  # 10 for testing
        exit_ui = ExitUI(screen)
        exit_ui.draw_exit_loser(screen, player_data["player_name"])
    else:
        pass


# -------------------------------------------------------------------------
# Main Loop
#
def main():
    """
    Main function to initialize and run the game loop.
    """
    # 1 - Initialize Pygame - Set window name and size
    pg.init()
    pg.font.init()  # Explicitly initialize font module
    pg.display.set_caption(conf.GAME_NAME)
    screen = pg.display.set_mode(conf.WIN_SIZE)

    # 2 - Display loading screen
    screen.blit(conf.LOAD_SCR_IMG, (0, 0))
    pg.display.flip()
    pg.time.wait(conf.LOAD_SCRN_DLY)  # Wait for X seconds

    # 3 - Player data elements
    ui = UIElements(screen)
    # Check if TEMP_FILE exists and load player data
    try:
        # If temp exists but is older than 60s, delete
        # If it is there, its probably because the game crashed.
        if os.path.exists(TEMP_FILE):
            file_age_limit = 60
            st = os.stat(TEMP_FILE)
            if (time.time() - st.st_mtime) > file_age_limit:
                print(f"Removing outdated temp file: {TEMP_FILE}")
                os.remove(TEMP_FILE)
                # No player data to load, will create new below
                player_data = None
            else:
                # File exists and is recent, load player data
                with open(TEMP_FILE) as f:
                    player_data = json.load(f)
                print(f"Resuming game for player: {player_data['player_name']}")
        else:
            # No temp file exists
            player_data = None
    except Exception as e:
        print(f"Error handling temp file: {e}")
        player_data = None
    # If no player data was loaded, show player selection screen
    if player_data is None:
        # Show player selection screen and create/load player data
        player_data = ui.main_menu()
        # Handle exceptions where no player selected at menu.
        if not player_data:
            print("No player selected. Exiting game.")
            pg.quit()
            sys.exit()
        # Print player info, to check things are working
        print(
            f"Welcome, {player_data['player_name']}! Balance: ${
                player_data['cash_balance']
            }"
        )

    # 4 - Initialize game elements
    running = True
    player = Player(conf.p_pos[0], conf.p_pos[1])
    clock = conf.CLOCK
    dt = 0
    font = pg.font.Font(None, 24)
    small_font = pg.font.Font(None, 24)

    # ----------------------------------
    # 5 - Main game loop
    while running:
        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            # For ANY event, run input handling
            ui.input_main(event)

        # Check player balance
        check_player_balance(screen, player_data)

        # Update Player
        player.update(dt)

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw Background image
        screen.blit(conf.BG_IMG, (0, 0))

        # Draw player on screen
        player.draw(screen)

        # Draw text on screen
        player_info = font.render(
            f"Player: {player_data['player_name']} | Balance: ${
                player_data['cash_balance']
            }",
            True,
            (255, 255, 255),
        )
        instruct_text = small_font.render(
            "WASD, or Arrows keys to move", True, (255, 255, 255)
        )
        instruct_rect = instruct_text.get_rect(
            center=(screen.get_width() // 2, 650)
        )

        screen.blit(player_info, (10, 10))
        screen.blit(instruct_text, instruct_rect)

        # ----------------------------------
        # Exit_targets
        #
        # Draw exit and targets
        targets = [
            # Exit Target
            (conf.e_pos, conf.e_size, leave_game),
            # Target 1 - Pinball
            (conf.t_pos, conf.t_size, conf.GAME_PINBALL),
            # Target 2 - Maze
            (conf.t2_pos, conf.t2_size, conf.GAME_MAZE),
            # Target 3 - Lottery
            (conf.t3_pos, conf.t3_size, conf.GAME_LOTTERY),
            # Target 4 - Blackjack
            (conf.t4_pos, conf.t4_size, conf.GAME_BLACKJACK),
            # Target 5 - Dice game
            (conf.t5_pos, conf.t5_size, conf.GAME_DICE),
            # Target 6 - Roulette
            (conf.t6_pos, conf.t6_size, conf.GAME_ROULETTE),
            # Target 7 - Shell Game
            (conf.t7_pos, conf.t7_size, conf.GAME_SHELL),
        ]

        for pos, size, command in targets:
            draw_target(screen, conf.t_color, pos, size)
            activate_target(
                screen,
                player_data,
                player.rect,
                pg.Rect(*pos, size, size),
                command,
            )

        # Update the display
        pg.display.flip()
        clock.tick(60)  # Limit FPS to 60
        dt = clock.tick(60) / 1000  # Delta Time - subFPS for the animations

    # Save player data before exiting = remove temp file
    save_player_data(
        player_data["player_name"],
        player_data["cash_balance"],
        player_data["high_scores"],
    )
    # Try to delete the TEMP_FILE if it exists
    with contextlib.suppress(OSError):
        os.remove(TEMP_FILE)

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
