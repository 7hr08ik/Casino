# ===========================
# Shell Game
#
# Author: Paul Leanca
# 07/02/2025
# ===========================
#
import random
import time

import pygame

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Three Shell Game")

# Pop image
pop_image = pygame.image.load("games/shell/img/pop_up.png")
pop_image = pygame.transform.scale(pop_image, (1300, 800))
screen.blit(pop_image, (0, 0))
pygame.display.update()
time.sleep(2)

# Load images
shell_image = pygame.image.load("games/shell/img/shell_empty_closed.png")
shell_image = pygame.transform.scale(shell_image, (200, 200))
ball_image = pygame.image.load("games/shell/img/open_shell_full.png")
ball_image = pygame.transform.scale(ball_image, (250, 200))
bg_image = pygame.image.load("games/shell/img/background.jpg")

# Load character sprites
player_sprite = pygame.image.load("games/shell/img/3.png")
player_victory_sprite = pygame.image.load("games/shell/img/3_victory.png")
player_victory_sprite = pygame.transform.scale(player_victory_sprite, (200, 350))

# Define shell positions
shell_positions = [(250, 200), (500, 200), (750, 200)]
ball_position = random.choice([0, 1, 2])

# Define button properties
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 60
quit_button = pygame.Rect(500, 500, BUTTON_WIDTH, BUTTON_HEIGHT)
play_again_button = pygame.Rect(700, 500, BUTTON_WIDTH, BUTTON_HEIGHT)

# Betting System
cash_credit = 100  # Starting credit
bet = 10  # Minimum bet
increase_bet_button = pygame.Rect(1050, 500, 80, 50)
decrease_bet_button = pygame.Rect(1150, 500, 80, 50)

# Define font
font = pygame.font.Font(None, 40)
message_font = pygame.font.Font(None, 60)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def draw_game(show_ball=False, message=None, victory=False):
    screen.blit(bg_image, (0, 0))

    for i, pos in enumerate(shell_positions):
        screen.blit(shell_image, pos)
        if show_ball and i == ball_position:
            screen.blit(ball_image, (pos[0] - 25, pos[1] + 30))

    player_x, player_y = 1050, 250
    screen.blit(player_victory_sprite if victory else player_sprite, (player_x, player_y))

    pygame.draw.rect(screen, (200, 0, 0), quit_button, border_radius=10)
    pygame.draw.rect(screen, (0, 200, 0), play_again_button, border_radius=10)
    draw_text("Quit", font, (255, 255, 255), screen, quit_button.centerx, quit_button.centery)
    draw_text(
        "Play Again",
        font,
        (255, 255, 255),
        screen,
        play_again_button.centerx,
        play_again_button.centery,
    )

    if message:
        draw_text(message, message_font, (255, 215, 0), screen, WIDTH // 2, HEIGHT // 2 - 100)

    draw_text(f"Credit: £{cash_credit}", font, (255, 255, 255), screen, 1100, 420)
    draw_text(f"Bet: £{bet}", font, (255, 255, 255), screen, 1100, 460)

    pygame.draw.rect(screen, (0, 200, 200), increase_bet_button, border_radius=5)
    pygame.draw.rect(screen, (200, 100, 0), decrease_bet_button, border_radius=5)
    draw_text(
        "+£10",
        font,
        (255, 255, 255),
        screen,
        increase_bet_button.centerx,
        increase_bet_button.centery,
    )
    draw_text(
        "-£10",
        font,
        (255, 255, 255),
        screen,
        decrease_bet_button.centerx,
        decrease_bet_button.centery,
    )

    pygame.display.update()


running = True
selected_shell = None
show_result = False
result_message = None
result_timer = None
victory_animation = False


def adjust_bet(amount):
    global bet  # noqa: PLW0603
    if 10 <= bet + amount <= cash_credit:
        bet += amount


while running:
    draw_game(show_result, result_message, victory_animation)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if quit_button.collidepoint((x, y)):
                running = False
            elif play_again_button.collidepoint((x, y)):
                ball_position = random.choice([0, 1, 2])
                show_result = False
                result_message = None
                result_timer = None
                victory_animation = False
            elif increase_bet_button.collidepoint((x, y)):
                adjust_bet(10)
            elif decrease_bet_button.collidepoint((x, y)):
                adjust_bet(-10)
            elif not show_result:
                for i, (sx, sy) in enumerate(shell_positions):
                    if sx < x < sx + 200 and sy < y < sy + 200:
                        selected_shell = i
                        if selected_shell == ball_position:
                            cash_credit += bet
                            result_message = "You Won!"
                            victory_animation = True
                        else:
                            cash_credit -= bet
                            result_message = "You Lost!"
                            victory_animation = False
                        result_timer = pygame.time.get_ticks()
                        show_result = True

    if show_result and result_timer and pygame.time.get_ticks() - result_timer > 2000:
        show_result = False
        result_message = None
        result_timer = None
        victory_animation = False
        ball_position = random.choice([0, 1, 2])
    if cash_credit <= 0:
        break  # TODO: Put code in here for finishing the game
pygame.quit()
