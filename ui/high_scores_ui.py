# ===========================
# Python game suite
#
# Author: Rob Hickling -- E4491341
# Casino Lobby - High Scores
# ===========================
#
# Main Imports
import pygame as pg

from logic.save_load import load_all_high_scores


class HighScoresUI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.Font(None, 36)
        self.small_font = pg.font.Font(None, 24)
        self.high_scores = load_all_high_scores()
        self.back_button = {
            "rect": pg.Rect(20, self.screen.get_height() - 70, 100, 40),
            "text": "Back",
            "hover": False,
        }

    # -------------------------------------------------------------------------
    # Utilities
    #
    def back_btn(self):
        """
        Draw the back button
        """
        # Variables
        bg_color = (
            (150, 150, 150) if self.back_button["hover"] else (100, 100, 100)
        )
        back_text = self.font.render(
            self.back_button["text"], True, (255, 255, 255)
        )
        back_text_rect = back_text.get_rect(
            center=self.back_button["rect"].center
        )

        # Draw Rectangles
        pg.draw.rect(self.screen, (200, 200, 200), self.back_button["rect"], 2)
        pg.draw.rect(self.screen, bg_color, self.back_button["rect"])

        # Blit the Button to the screen
        self.screen.blit(back_text, back_text_rect)

    def key_input(self, event):
        """
        Handle events for the High Scores screen

        Sends True signal to UI to inform it to close the High Scoers page
        and return to the Main menu
        """
        if event.type == pg.MOUSEMOTION:  # Hover and highlight
            self.back_button["hover"] = self.back_button["rect"].collidepoint(
                pg.mouse.get_pos()
            )
        elif event.type == pg.MOUSEBUTTONDOWN:  # Click on Back button
            if self.back_button["rect"].collidepoint(pg.mouse.get_pos()):
                return True
        elif event.type == pg.KEYDOWN and (  # Press Keys to return
            event.key == pg.K_q or event.key == pg.K_RETURN
        ):
            return True  # Go Back

        return False

    # -------------------------------------------------------------------------
    # Functions / Methods
    #
    def draw_high_scores(self):
        """
        Draw the high scores page
        """

        # ----------------------------------
        # Top Player
        #
        # Variables
        top_player = self.high_scores[0]
        top_box = pg.Rect(50, 80, self.screen.get_width() - 100, 150)
        top_name_text = self.font.render(
            f"Top Player: {top_player['player_name']}", True, (255, 255, 255)
        )
        right_side_x = top_box.right - 200  # Position from the right edge
        top_score_text = self.font.render(
            f"Highest Score: ${top_player['high_scores']['cash']}",
            True,
            (128, 128, 128),
        )
        current_balance_text = self.font.render(
            f"Current Balance: ${top_player['cash_balance']}",
            True,
            (255, 255, 255),
        )
        help_text = self.small_font.render(
            "Press 'Q' or 'Enter to go back", True, (255, 255, 255)
        )
        help_box = help_text.get_rect(
            center=(self.screen.get_width() // 2, 650)
        )

        # Draw Rectangles
        pg.draw.rect(self.screen, (200, 200, 0), top_box, 2)

        # Blit Items
        self.screen.blit(top_name_text, (top_box.x + 20, top_box.y + 20))
        self.screen.blit(top_score_text, (right_side_x - 110, top_box.y + 20))
        self.screen.blit(
            current_balance_text, (right_side_x - 110, top_box.y + 60)
        )
        self.screen.blit(help_text, help_box)

        # ----------------------------------
        # Display other players
        y_pos = 240
        # For players in list of high scores, NOT 1st
        for index, player in enumerate(self.high_scores[1:], 1):
            # Variables
            box = pg.Rect(50, y_pos, self.screen.get_width() - 100, 60)
            rank_text = self.font.render(f"{index}.", True, (255, 255, 255))
            name_text = self.font.render(
                player["player_name"], True, (255, 255, 255)
            )
            right_side_x = box.right - 200  # Position from the right edge
            score_text = self.font.render(
                f"Highest: ${player['high_scores']['cash']}",
                True,
                (128, 128, 128),
            )
            balance_text = self.font.render(
                f"Current: ${player['cash_balance']}", True, (255, 255, 255)
            )

            # Draw Rectangle
            pg.draw.rect(self.screen, (255, 255, 255), box, 1)

            # Blit items
            self.screen.blit(rank_text, (box.x + 20, box.y + 20))
            self.screen.blit(name_text, (box.x + 50, box.y + 20))
            self.screen.blit(score_text, (right_side_x, box.y + 10))
            self.screen.blit(balance_text, (right_side_x, box.y + 35))

            # Iterate through other players
            y_pos += 65
            # Stop at the bottom
            if y_pos > self.screen.get_height() - 100:
                break

    def print_high_scores_ui(self):
        """
        Draw the High Scores screen
        """

        # ----------------------------------
        title_text = self.font.render("Hall of Fame", True, (255, 255, 255))

        # Background fill - Black
        self.screen.fill((0, 0, 0))

        # Blit
        self.screen.blit(
            title_text,
            (self.screen.get_width() / 2 - title_text.get_width() / 2, 20),
        )

        # Detect when there are no high scores
        if not self.high_scores:
            no_scores_text = self.font.render(
                "No scores available", True, (255, 255, 255)
            )
            self.screen.blit(
                no_scores_text,
                (
                    self.screen.get_width() / 2
                    - no_scores_text.get_width() / 2,
                    100,
                ),
            )
        else:
            self.draw_high_scores()

        # Draw back button
        self.back_btn()

    # -------------------------------------------------------------------------
