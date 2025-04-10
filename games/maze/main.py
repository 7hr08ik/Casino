# ===========================
# Maze
#
# Author: Rob Hickling - E4491341
# 07/02/2025
# ===========================
#
# Main Imports
import json
import os
import sys
import tempfile

# Local Imports
import conf
import pygame as pg
from maze_logic.player import Player
from maze_logic.ui import Ui

# For game_integration
# Add Casino project root directory to Python path
casino_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)  # Up 2 folders
sys.path.append(casino_root)  # Append to imports below this
from integration_module.game_integration import (  # noqa: E402
    check_balance,
    load_player_data,
    maze_exit,
)

# For game_integration
# Platform agnostic temp file
TEMP_FILE = os.path.join(tempfile.gettempdir(), "current_player.json")


def main():
    # 1 - Initialize Pygame - Set window name and size
    pg.init()
    pg.display.set_caption(conf.GAME_NAME)
    screen = pg.display.set_mode(conf.WINDOW_SIZE)

    # 2 - Display loading screen
    screen.blit(conf.LOAD_SCR_IMG, (0, 0))
    pg.display.flip()
    pg.time.wait(conf.LOAD_SCRN_DLY)  # Wait for X seconds

    # 3 - Initialize game elements
    player = Player(conf.p_pos[0], conf.p_pos[1])
    ui = Ui()
    dt = 0
    running = True

    # ----------------------------------
    # 4 - Main game loop
    while running:
        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Fill the screen - Makes carpet colour
        screen.fill("grey12")

        # Print Background images
        screen.blit(conf.FLOOR_IMG, (0, 0))
        screen.blit(conf.BG_IMG, (0, 0))  # Collision only here

        # Draw UI elements
        ui.draw_ui(screen)

        # Draw player
        player.draw(screen)

        # Update Player
        player.update(dt)

        # For game_integration
        player_data = load_player_data()
        ui_balance = ui.get_balance()
        player_data["cash_balance"] = ui_balance
        check_balance(screen, player_data)

        # ----------------------------------
        # Draw the target
        #
        # Create surface
        target_surface = pg.Surface((conf.t_pos[0], conf.t_pos[1]), pg.SRCALPHA)
        target_surface.fill(conf.TRANSPARENT)  # Make the surface transparent
        # Put surface in a rectangle
        pg.draw.rect(
            target_surface,
            conf.t_colour,
            (conf.t_pos[0], conf.t_pos[1], conf.t_size, conf.t_size),
        )

        # ----------------------------------
        # Give Targets an action
        #
        # Target 1
        if player.rect.colliderect(
            pg.Rect(conf.t_pos[0], conf.t_pos[1], conf.t_size, conf.t_size)
        ):
            # For game_integration
            with open(TEMP_FILE, "w") as f:  # Save current data to tmp
                json.dump(player_data, f)
            maze_exit(screen, player_data)  # run exit sequence with latest data

            pg.quit()
            sys.exit()

        # Update the display
        pg.display.flip()
        conf.CLOCK.tick(60)  # Limit FPS to 60
        dt = conf.CLOCK.tick(30) / 1000  # Delta-Time for animations


if __name__ == "__main__":
    main()
