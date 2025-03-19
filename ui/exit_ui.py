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
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.Font(None, 36)
        self.delete_player = delete_player
        self.save_player = save_player_data
        self.load_player = load_player_data
        self.back_button = {"rect": pg.Rect(20, self.screen.get_height() - 70, 100, 40), "text": "Back", "hover": False}

    # -------------------------------------------------------------------------
    # Functions / Methods
    #
    def main_exit_details(self, screen, player_data):
        """
        Draw the Main Exit screen with player statistics
        """
        # Create info box
        info_box = pg.Rect(50, 80, self.screen.get_width() - 100, 150)
        pg.draw.rect(self.screen, (200, 200, 0), info_box, 2)

        # Load and display current player data
        current_player = self.load_player(player_data["player_name"])
        if current_player:
            player_name_text = self.font.render(f"Player: {current_player['player_name']}", True, (255, 255, 255))
            self.screen.blit(player_name_text, (info_box.x + 20, info_box.y + 20))

            high_score_text = self.font.render(
                f"Highest Score: ${current_player['high_scores']['cash']}", True, (255, 255, 255)
            )
            self.screen.blit(high_score_text, (info_box.x + 20, info_box.y + 60))

            cash_balance_text = self.font.render(
                f"Current Balance: ${current_player['cash_balance']}", True, (255, 255, 255)
            )
            self.screen.blit(cash_balance_text, (info_box.x + 20, info_box.y + 100))

        # Add centered goodbye message
        goodbye_message = "Thank you for visiting the Casino!"
        goodbye_text = self.font.render(goodbye_message, True, (255, 255, 255))
        goodbye_rect = goodbye_text.get_rect(center=(self.screen.get_width() // 2, 300))
        self.screen.blit(goodbye_text, goodbye_rect)

        # Second line
        goodbye_message2 = "We hope to see you again soon!"
        goodbye_text2 = self.font.render(goodbye_message2, True, (255, 255, 255))
        goodbye_rect2 = goodbye_text2.get_rect(center=(self.screen.get_width() // 2, 350))
        self.screen.blit(goodbye_text2, goodbye_rect2)

        # Third line
        goodbye_message3 = "Goodbye!"
        goodbye_text3 = self.font.render(goodbye_message3, True, (255, 255, 255))
        goodbye_rect3 = goodbye_text3.get_rect(center=(self.screen.get_width() // 2, 420))
        self.screen.blit(goodbye_text3, goodbye_rect3)

        # Save the current player data
        self.save_player(player_data["player_name"], player_data["cash_balance"], player_data["high_scores"])

    def draw_main_exit(self, screen, player_data):
        """
        Draw the Exit screen with account details
        """
        self.screen.fill((0, 0, 0))

        # Display title
        title_text = self.font.render("Your Account Details:", True, (255, 255, 255))
        self.screen.blit(title_text, (self.screen.get_width() / 2 - title_text.get_width() / 2, 20))

        # Draw exit details
        self.main_exit_details(screen, player_data)

    def print_exit_ui(self, screen, player_data):
        """
        Show exit screen
        """
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT or pg.KEYDOWN or pg.MOUSEBUTTONDOWN:
                    running = False

            self.draw_main_exit(screen, player_data)
            pg.display.flip()
            pg.time.wait(conf.EXIT_DLY)
            running = False

        # Save player data and exit
        self.save_player(player_data["player_name"], player_data["cash_balance"], player_data["high_scores"])
        print("Player data saved. Exiting game.")
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
