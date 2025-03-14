# ===========================
# Maze
#
# Author: Rob Hickling - E4491341
# 07/02/2025
# ===========================
#
# Main Imports
import pygame as pg

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

        # Best time tracking
        self.best_time = float("inf")

        # UI styling
        self.text_color = (0, 0, 0)  # White text
        self.background_color = (128, 128, 128, 128)
        self.border_color = (255, 100, 0)  # Orange border
        self.border_width = 2

    def draw_ui(self, screen):
        # Update timer and cost
        current_time = pg.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000  # Convert to seconds
        cost = int(elapsed_time * conf.cost_per_second)

        # Update best time
        if elapsed_time < self.best_time:
            self.best_time = elapsed_time

        # Create timer text
        timer_text = self.font.render(f"Time: {int(elapsed_time)}s", True, self.text_color)
        timer_rect = timer_text.get_rect(topleft=(1080, 10))

        # Create cost text
        cost_text = self.font.render(f"Cost: ${cost}", True, self.text_color)
        cost_rect = cost_text.get_rect(topleft=(1080, 50))

        # Create best time text
        best_time_text = self.font.render(f"Best: {int(self.best_time)}s", True, self.text_color)
        best_time_rect = best_time_text.get_rect(topleft=(1080, 90))

        # Draw background
        background_rect = pg.Rect(1075, 0, 200, 170)  # Bounding box for UI
        pg.draw.rect(screen, self.background_color, background_rect)

        # Draw border
        pg.draw.rect(screen, self.border_color, background_rect, self.border_width)

        # Draw UI elements
        screen.blit(timer_text, timer_rect)
        screen.blit(cost_text, cost_rect)
        screen.blit(best_time_text, best_time_rect)
