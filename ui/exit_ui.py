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
from ui.ui import UIElements


class ExitUI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.Font(None, 36)
        self.delete_player = delete_player(player_name=None)
        self.save_player = save_player_data(player_name=None, cash_balance=None, high_scores=None)
        self.load_player = load_player_data(player_name=None)
        self.back_button = {"rect": pg.Rect(20, self.screen.get_height() - 70, 100, 40), "text": "Back", "hover": False}

    # -------------------------------------------------------------------------
    # Utilities
    #

    # -------------------------------------------------------------------------
    # Calculations
    #

    # -------------------------------------------------------------------------
    # Functions / Methods
    #

    # -------------------------------------------------------------------------

    def draw_exit_main(self, screen):
        """
        Draw the Main Exit screen
        """

        ui = UIElements(screen)
        player_data = ui.main_menu()

        # Current Players Data
        current_player = self.load_player(player_data["player_name"])
        top_box = pg.Rect(50, 80, self.screen.get_width() - 100, 150)
        pg.draw.rect(self.screen, (200, 200, 0), top_box, 2)

        top_name_text = self.font.render(f"Top Player: {current_player['player_name']}", True, (255, 255, 255))
        self.screen.blit(top_name_text, (top_box.x + 20, top_box.y + 20))

        top_score_text = self.font.render(
            f"Highest Score: ${current_player['high_scores']['cash']}", True, (255, 255, 255)
        )
        self.screen.blit(top_score_text, (top_box.x + 20, top_box.y + 60))

        current_balance_text = self.font.render(
            f"Current Balance: ${current_player['cash_balance']}", True, (255, 255, 255)
        )
        self.screen.blit(current_balance_text, (top_box.x + 20, top_box.y + 100))

        # Add centered text box saying goodbye
        goodbye_msg = """Thank you for visiting the Casino! \n
                        We hope to see you again soon! \n
                        \n
                        Goodbye!"""
        goodbye_text = self.font.render(goodbye_msg, True, (255, 255, 255))
        goodbye_rect = goodbye_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(goodbye_text, goodbye_rect)

        # Save the current player from the json file
        save_player_data(player_data["player_name"], player_data["cash_balance"], player_data["high_scores"])
        pg.quit()
        sys.exit()

    def draw_exit_loser(self, screen, player_name):
        """
        Print loser screen and remove player from json file
        """

        # Load, loser page
        screen.blit(conf.LOSER_IMG, (0, 0))
        pg.display.flip()
        pg.time.wait(conf.LOAD_SCRN_DLY)  # Wait for X seconds

        # Delete the current player from the json file
        delete_player(player_name)
        pg.quit()
        sys.exit()

    def back_btn(self):
        """Draw the back button"""
        bg_color = (150, 150, 150) if self.back_button["hover"] else (100, 100, 100)
        pg.draw.rect(self.screen, bg_color, self.back_button["rect"])
        back_text = self.font.render(self.back_button["text"], True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=self.back_button["rect"].center)
        self.screen.blit(back_text, back_text_rect)
        pg.draw.rect(self.screen, (200, 200, 200), self.back_button["rect"], 2)

    def key_input(self, event):
        """
        Handle key input, and mouse input for exit screens
        """

        if event.type == pg.MOUSEMOTION:
            self.back_button["hover"] = self.back_button["rect"].collidepoint(pg.mouse.get_pos())
        elif event.type == pg.MOUSEBUTTONDOWN:
            if self.back_button["rect"].collidepoint(pg.mouse.get_pos()):
                return True  # Return True to indicate we should go back
        elif event.type == pg.KEYDOWN and (event.key == pg.K_q or event.key == pg.K_RETURN):
            return True  # Return True to indicate we should go back

        return False
