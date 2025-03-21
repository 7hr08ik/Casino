# ===========================
# Maze
#
# Author: Rob Hickling - E4491341
# 07/02/2025
# ===========================
#
# Main Imports
import pygame as pg
from game_integration import load_lobby_player_data

# Local Imports
import conf


class Ui:
    def __init__(self):
        # Initialize UI elements
        pg.font.init()
        self.font = pg.font.Font(None, 32)

        # Timer and cost initialization
        self.start_time = pg.time.get_ticks()
        self.current_time = self.start_time
        self.cost = 0
        # self.starting_balance = 50 # Original
        # For game_integration
        player_data = load_lobby_player_data()
        # Replace original cash variable with:
        self.starting_balance = player_data["cash_balance"]
        self.balance = self.starting_balance

        # UI styling
        self.text_color = (255, 255, 255)
        self.background_color = (50, 50, 50)
        self.border_color = (200, 200, 200)
        self.border_width = 2

    def draw_ui(self, screen):
        # Update timer and cost
        current_time = pg.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000  # Convert to seconds
        cost = int(elapsed_time * conf.cost_per_second)

        # Update balance and best time
        self.balance = self.starting_balance - cost
        # For game_integration
        player_data = load_lobby_player_data()
        self.balance = player_data["cash_balance"]

        # Create timer text
        timer_text = self.font.render(f"Time: {int(elapsed_time)}s", True, self.text_color)
        timer_rect = timer_text.get_rect(topleft=(1080, 70))

        # Create cost text
        cost_text = self.font.render(f"Cost: ${cost}", True, self.text_color)
        cost_rect = cost_text.get_rect(topleft=(1080, 110))

        # Create balance text
        balance_text = self.font.render(f"Balance: ${self.balance}", True, self.text_color)
        balance_rect = balance_text.get_rect(topleft=(1080, 630))

        # Draw background
        background_rect = pg.Rect(1075, 60, 195, 90)  # Bounding box for UI
        pg.draw.rect(screen, self.background_color, background_rect)
        background_rect_1 = pg.Rect(1075, 625, 195, 60)  # Bounding box for UI
        pg.draw.rect(screen, self.background_color, background_rect_1)

        # Draw border
        pg.draw.rect(screen, self.border_color, background_rect, self.border_width)
        pg.draw.rect(screen, self.border_color, background_rect_1, self.border_width)

        # Draw UI elements
        screen.blit(timer_text, timer_rect)
        screen.blit(cost_text, cost_rect)
        screen.blit(balance_text, balance_rect)
