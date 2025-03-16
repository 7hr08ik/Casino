# ===========================
# Maze
#
# Author: Rob Hickling - E4491341
# 07/02/2025
# ===========================
#
# Main Imports
import subprocess
import sys

import pygame as pg

# Local Imports
import conf
from logic.player import Player
from logic.ui import Ui


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

    # ----------------------------------
    # 4 - Main game loop
    while True:
        # Limit FPS to 60
        conf.CLOCK.tick(60)
        # Delta-Time for animations
        dt = conf.CLOCK.tick(30) / 1000

        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # Fill the screen - Makes carpet colour
        # screen.fill((90, 30, 105))
        screen.fill("grey12")

        # Print Background image
        screen.blit(conf.FLOOR_IMG, (0, 0))
        screen.blit(conf.BG_IMG, (0, 0))

        # Draw UI elements
        ui.draw_ui(screen)

        # Draw player
        player.draw(screen)

        # Update Player
        player.update(dt)

        # ----------------------------------
        # Draw the target
        #
        # Create surface
        target_surface = pg.Surface((conf.t_pos[0], conf.t_pos[1]), pg.SRCALPHA)
        # Make the surface transparent
        target_surface.fill(conf.TRANSPARENT)
        # Put surface in a rectangle
        pg.draw.rect(
            target_surface,
            conf.t_colour,
            (conf.t_pos[0], conf.t_pos[1], conf.t_size, conf.t_size),
        )

        # ----------------------------------
        # Give Targets an action
        #
        # Target 1 - Pinball
        if player.rect.colliderect(pg.Rect(conf.t_pos[0], conf.t_pos[1], conf.t_size, conf.t_size)):
            pg.quit()
            subprocess.run(conf.GAME_LOBBY, check=False)
            sys.exit()

        # ----------------------------------
        # Add if statements to handle zero score
        # if player.score == 0:
        #     pg.quit()
        #     subprocess.run(conf.GAME_LOBBY, check=False)
        #     sys.exit()

        # Update the display
        pg.display.flip()


if __name__ == "__main__":
    main()
