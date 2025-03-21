# ===========================
# Maze
#
# Author: Rob Hickling - E4491341
# 07/02/2025
# ===========================
#
# Main Imports
import sys
from pathlib import Path

# Local Imports
import conf
import pygame as pg

# For game_integration
from game_integration import check_balance, load_player_data, maze_exit

from logic.player import Player
from logic.ui import Ui

# For game_integration
TEMP_FILE = Path("/tmp/current_player.json")  # Platform-agnostic temp file?


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

    # For game_integration
    player_data = load_player_data()
    ui_balance = ui.get_balance()

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
        check_balance(screen, player_data)
        # Update the player balance
        ui_balance = ui.get_balance()
        player_data["cash_balance"] = ui_balance

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
        if player.rect.colliderect(pg.Rect(conf.t_pos[0], conf.t_pos[1], conf.t_size, conf.t_size)):
            # For game_integration
            maze_exit(screen, player_data)

            pg.quit()
            sys.exit()

        # Update the display
        pg.display.flip()
        conf.CLOCK.tick(60)  # Limit FPS to 60
        dt = conf.CLOCK.tick(30) / 1000  # Delta-Time for animations


if __name__ == "__main__":
    main()
