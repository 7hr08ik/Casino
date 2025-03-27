# ===========================
# Pinball
#
# Author: Rob Hickling -- E4491341
# 04/02/2025
#
# Modified by: Rob Hickling
# 21/03/2025
# Added functionality for saving and loading player data
# required for integration into the lobby
# all commented with;
#    # For game_integration
# ===========================

# Imports
import os
import sys

import conf
import pygame as pg
from ball import PlayerBall
from board import GameBoard

# For game_integration
# Add Casino project root directory to Python path
casino_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)  # Up 2 folders
sys.path.append(casino_root)  # Append to imports below this
from integration_module.game_integration import (  # noqa: E402
    check_balance,
    load_player_data,
    save_and_exit,
)


def main():
    # Initialize game settings
    pg.init()
    pg.display.set_caption(conf.game_name)
    screen = conf.screen
    fps = conf.clock

    # Variables
    board = GameBoard()
    ball = PlayerBall(conf.b_size, conf.pos)
    # For game_integration
    player_data = load_player_data()  # Load the data

    # ----------------------------------
    # Main game loop
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # For game_integration
                save_and_exit(screen, player_data)
                running = False

        # Input handling. Update flippers
        board.key_input(screen, player_data)

        # Update the board.
        check_balance(screen, player_data)  # check for no money
        board.update_board()

        # Set screen fill
        screen.fill(pg.Color("gray12"))

        # Draw items on the screen
        board.draw_background(screen)
        board.draw_flippers(screen)
        ball.draw(screen)

        # Update the ball position
        ball.update_position(board, [board.left_flipper, board.right_flipper])

        # Refresh display
        pg.display.flip()
        fps.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()
