# ===========================
# Python game suite
# Casino Lobby
#
# Author: Rob Hickling -- E4491341
# 28/01/2025
# ===========================
#
# Main Imports
import subprocess
import sys

import pygame as pg

# Local Imports
import conf
from logic.player import Player
from logic.save_load import save_player_data
from ui.exit_ui import ExitUI
from ui.ui import UIElements


def draw_target(screen, color, position, size, alpha=0):
    """
    Draw target points on the screen.
    Targets are transparent and have a border.
    """
    # Create surface
    target_surface = pg.Surface((size, size), pg.SRCALPHA)
    # Make the surface transparent
    target_surface.fill((color[0], color[1], color[2], alpha))
    # Put surface in a rectangle
    pg.draw.rect(target_surface, color, (0, 0, size, size), 1)
    # Print screen with transparent surface in position
    screen.blit(target_surface, position)


def activate_target(player_rect, target_rect, game_command=None):
    """
    When player reaches target, activate X game.
    """
    if player_rect.colliderect(target_rect):
        pg.quit()
        if game_command:
            subprocess.run(game_command, check=False)
        sys.exit()


def check_player_balance(screen, player_data):
    """
    Check if player's cash balance has reached 0 or below.
    Display exit screen if player is broke.
    """
    if player_data["cash_balance"] <= 0:
        exit_ui = ExitUI(screen)
        exit_ui.draw_exit_loser(screen, player_data["player_name"])
    else:
        pass


def main():
    """
    Main function to initialize and run the game loop.
    """
    # 1 - Initialize Pygame - Set window name and size
    pg.init()
    pg.display.set_caption(conf.GAME_NAME)
    screen = pg.display.set_mode(conf.WIN_SIZE)

    # 2 - Display loading screen
    screen.blit(conf.LOAD_SCR_IMG, (0, 0))
    pg.display.flip()
    pg.time.wait(conf.LOAD_SCRN_DLY)  # Wait for X seconds

    # 3 - Player data elements
    # Show player selection screen and create/load player data
    ui = UIElements(screen)
    player_data = ui.main_menu()
    # Handle exceptions where no player selected at menu.
    if not player_data:
        print("No player selected. Exiting game.")
        pg.quit()
        sys.exit()
    # Print player info, to check things are working
    print(f"Welcome, {player_data['player_name']}! Balance: ${player_data['cash_balance']}")

    # 4 - Initialize game elements
    player = Player(conf.p_pos[0], conf.p_pos[1])
    clock = conf.CLOCK

    # ----------------------------------
    # 5 - Main game loop
    while True:
        # Limit FPS to 60
        dt = clock.tick(60) / 1000

        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # Save player data before exiting
                save_player_data(player_data["player_name"], player_data["cash_balance"], player_data["high_scores"])
                pg.quit()
                sys.exit()

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

        # Draw player info (name and balance)
        font = pg.font.Font(None, 24)
        player_info = font.render(
            f"Player: {player_data['player_name']} | Balance: ${player_data['cash_balance']}", True, (255, 255, 255)
        )
        screen.blit(player_info, (10, 10))

        # ----------------------------------
        # Exit_targets
        #
        # Draw exit and targets
        targets = [
            (conf.e_pos, conf.e_size, None),  # Exit Target
            # (conf.t_pos, conf.t_size, conf.GAME_PINBALL),  # Target 1 - Pinball
            (conf.t2_pos, conf.t2_size, conf.GAME_MAZE),  # Target 2 - Maze
            (conf.t3_pos, conf.t3_size, conf.GAME_LOTTERY),  # Target 3 - Lottery
            (conf.t4_pos, conf.t4_size, conf.GAME_BLACKJACK),  # Target 4 - Blackjack
            (conf.t5_pos, conf.t5_size, conf.GAME_DICE),  # Target 5 - Dice game
            (conf.t6_pos, conf.t6_size, conf.GAME_ROULETTE),  # Target 6 - Roulette
            (conf.t7_pos, conf.t7_size, conf.GAME_SHELL),  # Target 7 - Shell Game
        ]

        for pos, size, command in targets:
            draw_target(screen, conf.t_color, pos, size)
            activate_target(player.rect, pg.Rect(*pos, size, size), command)

        # Update the display
        pg.display.flip()


if __name__ == "__main__":
    main()
