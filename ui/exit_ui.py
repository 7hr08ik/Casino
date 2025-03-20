# ===========================
# Python game suite
#
# Casino Lobby - Exit Screens
# ===========================
#
# Main Imports
import sys

import pygame as pg

import conf
from logic.save_load import delete_player, load_player_data, save_player_data


class ExitUI:
    """
    Initialize the ExitUI class with two versions of the screen.
    One for the players when they leave.
    Another for the bums that have no cash.

    Sets up the screen, various UI components, including buttons,
    and methods to draw the Exit screen.
    """
    def __init__(self, screen):

        self.screen = screen
        self.font = pg.font.Font(None, 36)
        self.small_font = pg.font.Font(None, 24)
        self.delete_player = delete_player
        self.save_player = save_player_data
        self.load_player = load_player_data
        self.back_button = {"rect": pg.Rect(20, self.screen.get_height() - 70, 100, 40), "text": "Back", "hover": False}

    # -------------------------------------------------------------------------
    # Functions / Methods
    #
    def draw_main_exit(self, screen, player_data):
        """
        Draw the Main Exit screen

        Goodbye messages, Account details, and credits
        """

        # ----------------------------------
        # Variables

        # Boxes
        info_box_width = 1180  # 50 Border on each side
        info_box_height = 150
        info_box = pg.Rect(50, 80, info_box_width, info_box_height)
        credits_box_width = 300  # 1/4 of the screen with 50 border
        credits_box_height = 400 - info_box_height  # Remaining height with 50 border
        credits_box = pg.Rect(
            1230 - credits_box_width,  # (screen width - border) - credits width
            700 - credits_box_height,  # (screen height - border) - credits height
            credits_box_width,
            credits_box_height,
        )

        # Current players data
        current_player = self.load_player(player_data["player_name"])
        player_name_text = self.font.render(f"Player: {current_player['player_name']}", True, ("white"))

        # Text
        title_text = self.font.render("Your Account Details:", True, ("white"))
        high_score_text = self.font.render(f"Highest Score: ${current_player['high_scores']['cash']}", True, ("white"))
        cash_balance_text = self.font.render(f"Current Balance: ${current_player['cash_balance']}", True, ("white"))
        goodbye_lines = ["Thank you for visiting the Casino!", "We hope to see you again soon!", "Goodbye!"]
        goodbye_texts = [self.font.render(line, True, ("white")) for line in goodbye_lines]
        help_text = self.small_font.render("Press the 'ANY' key to continue ;)", True, ("white"))
        credits_text = self.small_font.render("Project Credits:", True, ("white"))
        names = ["Rob Hickling", "Paul Leanka", "Viorica Anghel", "Sorin Sofronov", "James Young"]
        names_texts = [self.small_font.render(name, True, ("white")) for name in names]
        help_rect = help_text.get_rect(topleft=(50, 680))

        # ----------------------------------
        # Draw Items

        # Background fill
        self.screen.fill((0, 0, 0))

        # Boxes
        pg.draw.rect(self.screen, (200, 200, 0), info_box, 2)
        pg.draw.rect(self.screen, ("white"), credits_box, 2)

        # Blit Items to the screen
        self.screen.blit(title_text, (self.screen.get_width() / 2 - title_text.get_width() / 2, 20))
        self.screen.blit(player_name_text, (info_box.x + 20, info_box.y + 20))
        self.screen.blit(high_score_text, (info_box.x + 20, info_box.y + 60))
        self.screen.blit(cash_balance_text, (info_box.x + 20, info_box.y + 100))
        self.screen.blit(credits_text, (credits_box.x + 20, credits_box.y + 20))

        # Blit each name in the list
        for i, name_text in enumerate(names_texts):
            self.screen.blit(name_text, (credits_box.x + 20, credits_box.y + 60 + i * 30))

        # Blit each goodbye message in the list
        y_offset = 200 + info_box_height
        for i, text in enumerate(goodbye_texts):
            self.screen.blit(text, (50, y_offset + i * 60))

        # Blit help text
        self.screen.blit(help_text, help_rect)

        # ----------------------------------
        # Finally
        # Save the current player data
        self.save_player(player_data["player_name"], player_data["cash_balance"], player_data["high_scores"])

    def print_exit_ui(self, screen, player_data):
        """
        Show exit screen
        """

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            self.draw_main_exit(screen, player_data)
            pg.display.flip()
            pg.time.wait(conf.EXIT_DLY)
            running = False

        # Save player data and exit
        self.save_player(player_data["player_name"], player_data["cash_balance"], player_data["high_scores"])
        print("Player data saved. Exiting game.")
        running = False
        pg.quit()
        sys.exit()

    def draw_exit_loser(self, screen, player_name):
        """
        Print loser screen and remove player from json file
        """
        # Load and display loser page
        screen.blit(conf.LOSER_IMG, (0, 0))
        pg.display.flip()
        pg.time.wait(conf.EXIT_DLY)  # Wait for configured time

        # Delete the current player from the json file
        self.delete_player(player_name)
        pg.quit()
        sys.exit()

    # -------------------------------------------------------------------------
