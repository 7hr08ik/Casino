import random
import sys

import pygame

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("3 Dice Casino Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)

# Dice images (make sure to add your dice images in the same directory)
DICE_IMAGES = {
    1: pygame.image.load("games/dice/img/dice_1.png"),
    2: pygame.image.load("games/dice/img/dice_2.png"),
    3: pygame.image.load("games/dice/img/dice_3.png"),
    4: pygame.image.load("games/dice/img/dice_4.png"),
    5: pygame.image.load("games/dice/img/dice_5.png"),
    6: pygame.image.load("games/dice/img/dice_6.png"),
}

# Resize the dice images to 100x100
DICE_IMAGES = {key: pygame.transform.scale(image, (60, 60)) for key, image in DICE_IMAGES.items()}

# Font setup
font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 48)


# Button class
class Button:
    def __init__(self, text, x, y, width, height, inactive_color, active_color):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont("Arial", 32)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.active_color, self.rect)
        else:
            pygame.draw.rect(screen, self.inactive_color, self.rect)

        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return bool(event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos))


# Function to roll 3 dice
def roll_dice():
    return random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)


# Function to calculate the sum of the dice rolls
def sum_dice(dice):
    return sum(dice)


# Function to display text on the screen
def display_text(text, x, y, color, font_size=24):
    font = pygame.font.SysFont("Arial", font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


# Function to add suspenseful delay before rolling
def suspense_delay():
    for i in range(3, 0, -1):
        screen.fill(GRAY)
        display_text(
            f"Rolling in {i}...", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, BLACK, 48
        )
        pygame.display.update()
        pygame.time.wait(1000)


# Function to get player's bet amount
def get_bet_amount(player_money):
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 300, 50)
    color_inactive = pygame.Color("lightskyblue3")
    color_active = pygame.Color("dodgerblue2")
    color = color_inactive
    text = ""
    active = False
    clock = pygame.time.Clock()

    while True:
        screen.fill(GRAY)
        display_text(
            f"Enter your bet (Max: £{player_money}):",
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT // 2 - 100,
            BLACK,
            32,
        )
        pygame.draw.rect(screen, color, input_box, 2)
        bet_text = pygame.font.SysFont("Arial", 32).render(text, True, color)
        screen.blit(bet_text, (input_box.x + 5, input_box.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = not active if input_box.collidepoint(event.pos) else False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    try:
                        bet = int(text)
                        if 0 < bet <= player_money:
                            return bet
                        else:
                            display_text(
                                "Invalid bet! Must be between 1 and your balance.",
                                150,
                                SCREEN_HEIGHT // 2 + 100,
                                RED,
                                32,
                            )
                            pygame.display.update()
                            pygame.time.wait(1000)
                            text = ""
                    except ValueError:
                        display_text(
                            "Invalid input! Please enter a number.",
                            150,
                            SCREEN_HEIGHT // 2 + 100,
                            RED,
                            32,
                        )
                        pygame.display.update()
                        pygame.time.wait(1000)
                        text = ""
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        pygame.display.update()
        clock.tick(30)


# Function to prompt for player's name
def get_player_name():
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50)
    color_inactive = pygame.Color("lightskyblue3")
    color_active = pygame.Color("dodgerblue2")
    color = color_inactive
    text = ""
    active = False
    clock = pygame.time.Clock()

    while True:
        screen.fill(GRAY)
        display_text(
            " What is your name?", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, BLACK, 32
        )
        pygame.draw.rect(screen, color, input_box, 2)
        name_text = pygame.font.SysFont("Arial", 32).render(text, True, color)
        screen.blit(name_text, (input_box.x + 5, input_box.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = not active if input_box.collidepoint(event.pos) else False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN and text != "":
                    return text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        pygame.display.update()
        clock.tick(30)


# Main game loop
def game_loop(player_name):
    house_money = 1000
    player_money = 100
    bet = 0
    player_roll_history = []
    house_roll_history = []

    while True:
        screen.fill(GRAY)
        display_text(f"{player_name} Money: £{player_money}", 20, 20, BLACK, 32)
        display_text(f"House Money: £{house_money}", SCREEN_WIDTH - 300, 20, BLACK, 32)
        display_text(f"Bet: £{bet}", 20, 60, BLACK, 32)
        display_text("Press 'Q' to Quit or 'R' to Roll", 20, 100, BLACK, 32)
        display_text(f"{player_name}'s Last Rolls:", 20, 140, BLUE, 24)
        for i, roll in enumerate(player_roll_history[-5:], 1):
            display_text(f"{i}. {roll}", 20, 140 + i * 30, BLUE, 24)
        display_text("House's Last Rolls:", SCREEN_WIDTH - 350, 140, RED, 22)
        for i, roll in enumerate(house_roll_history[-5:], 1):
            display_text(f"{i}. {roll}", SCREEN_WIDTH - 200, 140 + i * 30, RED, 24)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    if bet <= 0:
                        bet = get_bet_amount(player_money)
                    if bet > player_money:
                        display_text("Invalid bet!", 20, 180, RED, 32)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        continue

                    suspense_delay()
                    player_dice = roll_dice()
                    house_dice = roll_dice()
                    player_sum = sum_dice(player_dice)
                    house_sum = sum_dice(house_dice)
                    player_roll_history.append(f"{player_dice} (Sum: {player_sum})")
                    house_roll_history.append(f"{house_dice} (Sum: {house_sum})")

                    screen.fill(WHITE)
                    screen.blit(DICE_IMAGES[player_dice[0]], (200, 200))
                    screen.blit(DICE_IMAGES[player_dice[1]], (250, 200))
                    screen.blit(DICE_IMAGES[player_dice[2]], (300, 200))
                    display_text(f"{player_name}'s Dice: {player_dice}", 200, 300, BLUE)
                    screen.blit(DICE_IMAGES[house_dice[0]], (500, 200))
                    screen.blit(DICE_IMAGES[house_dice[1]], (550, 200))
                    screen.blit(DICE_IMAGES[house_dice[2]], (600, 200))
                    display_text(f"House Dice: {house_dice}", 500, 300, RED)

                    if player_sum > house_sum:
                        display_text(f"{player_name} Wins £{bet}", 300, 400, GREEN, 48)
                        player_money += bet
                        house_money -= bet
                    elif player_sum < house_sum:
                        display_text(f"The House Wins £{bet}", 300, 400, RED, 48)
                        player_money -= bet
                        house_money += bet
                    else:
                        display_text("It's a Tie!", 300, 400, BLACK, 48)

                    pygame.display.update()
                    pygame.time.wait(2000)
                    bet = 0

        pygame.display.update()


# Menu function
def main_menu():
    start_button = Button(
        "Start Game", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 50, GRAY, GREEN
    )
    quit_button = Button(
        "Quit Game", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50, GRAY, RED
    )
    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)
        display_text(
            "3 Dice Teesside Casino", SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 200, WHITE, 48
        )

        start_button.draw(screen)
        quit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if start_button.is_clicked(event):
                player_name = get_player_name()
                game_loop(player_name)
            if quit_button.is_clicked(event):
                # TODO: add code to return to lobby
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(30)


# Start the game with the menu
main_menu()
