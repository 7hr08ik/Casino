# ===========================
# Python game suite
#
# Casino Lobby - Player Selection
# ===========================
#
# Main Imports
import pygame as pg

from logic.save_load import load_high_scores


class HighScoresUI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.Font(None, 36)
        self.high_scores = load_high_scores()
        self.back_button = {"rect": pg.Rect(20, self.screen.get_height() - 70, 100, 40), "text": "Back", "hover": False}

    def draw(self):
        """Draw the High Scores screen"""
        self.screen.fill((0, 0, 0))

        # Display title
        title_text = self.font.render("Hall of Fame", True, (255, 255, 255))
        self.screen.blit(title_text, (self.screen.get_width() / 2 - title_text.get_width() / 2, 20))

        if not self.high_scores:
            no_scores_text = self.font.render("No scores available", True, (255, 255, 255))
            self.screen.blit(no_scores_text, (self.screen.get_width() / 2 - no_scores_text.get_width() / 2, 100))
        else:
            self._draw_high_scores()

        # Draw back button
        self._draw_back_button()

    def _draw_high_scores(self):
        """Draw the high scores list"""
        # Highlight top player
        top_player = self.high_scores[0]
        top_box = pg.Rect(50, 80, self.screen.get_width() - 100, 150)
        pg.draw.rect(self.screen, (200, 200, 0), top_box, 2)

        top_name_text = self.font.render(f"Top Player: {top_player['player_name']}", True, (255, 255, 255))
        self.screen.blit(top_name_text, (top_box.x + 20, top_box.y + 20))

        top_score_text = self.font.render(f"Highest Score: ${top_player['high_scores']['cash']}", True, (255, 255, 255))
        self.screen.blit(top_score_text, (top_box.x + 20, top_box.y + 60))

        current_balance_text = self.font.render(
            f"Current Balance: ${top_player['cash_balance']}", True, (255, 255, 255)
        )
        self.screen.blit(current_balance_text, (top_box.x + 20, top_box.y + 100))

        # Display other players
        y_pos = 240
        for index, player in enumerate(self.high_scores[1:], 1):
            box = pg.Rect(50, y_pos, self.screen.get_width() - 100, 60)
            pg.draw.rect(self.screen, (255, 255, 255), box, 1)

            rank_text = self.font.render(f"{index}.", True, (255, 255, 255))
            self.screen.blit(rank_text, (box.x + 20, box.y + 20))

            name_text = self.font.render(player["player_name"], True, (255, 255, 255))
            self.screen.blit(name_text, (box.x + 50, box.y + 20))

            score_text = self.font.render(f"${player['high_scores']['cash']}", True, (255, 255, 255))
            self.screen.blit(score_text, (box.x + 200, box.y + 20))

            balance_text = self.font.render(f"Current: ${player['cash_balance']}", True, (255, 255, 255))
            self.screen.blit(balance_text, (box.x + 350, box.y + 20))

            y_pos += 65

            if y_pos > self.screen.get_height() - 100:
                break

    def _draw_back_button(self):
        """Draw the back button"""
        bg_color = (150, 150, 150) if self.back_button["hover"] else (100, 100, 100)
        pg.draw.rect(self.screen, bg_color, self.back_button["rect"])
        back_text = self.font.render(self.back_button["text"], True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=self.back_button["rect"].center)
        self.screen.blit(back_text, back_text_rect)
        pg.draw.rect(self.screen, (200, 200, 200), self.back_button["rect"], 2)

    def handle_event(self, event):
        """Handle events for the High Scores screen"""
        if event.type == pg.MOUSEMOTION:
            self.back_button["hover"] = self.back_button["rect"].collidepoint(pg.mouse.get_pos())
        elif event.type == pg.MOUSEBUTTONDOWN:
            if self.back_button["rect"].collidepoint(pg.mouse.get_pos()):
                return True  # Return True to indicate we should go back
        elif event.type == pg.KEYDOWN and (event.key == pg.K_q or event.key == pg.K_RETURN):
            return True  # Return True to indicate we should go back

        return False
