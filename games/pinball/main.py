# # ===========================
# # Pinball
# #
# # Author: Rob Hickling -- E4491341
# # 04/02/2025
# # ===========================
# #
# # Imports
import pygame as pg
from ball import PlayerBall
from board import GameBoard

import conf


def main():
    # Initialize game settings
    pg.init()
    pg.display.set_caption(conf.game_name)
    screen = conf.screen
    fps = conf.clock

    # Variables
    board = GameBoard()
    ball = PlayerBall(conf.b_size, conf.pos)

    # ----------------------------------
    # Main game loop
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Input handling. Update flippers
        board.key_input()

        # Update the board.
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
