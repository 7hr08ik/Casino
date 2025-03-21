# ===========================
# BlackJack
#
# Author: Paul Leanca
# 07/02/2025
#
# Modified by: Rob Hickling
# 21/03/2025
# Added functionality for saving and loading player data
# required for integration into the lobby
# ===========================

import random
import sys
import time

import pygame

# For game_integration
from game_integration import check_balance, load_player_data, save_and_exit

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Blackjack Game")

# Load images
pop_image = pygame.image.load("games/blackjack/img/pop_up.png")
pop_image = pygame.transform.scale(pop_image, (1300, 800))
screen.blit(pop_image, (0, 0))
pygame.display.update()

# Wait a few seconds before starting the game
time.sleep(1)

bg_image = pygame.image.load("games/blackjack/img/background.jpg")
card_back = pygame.image.load("games/blackjack/img/card_back.png")
card_back = pygame.transform.scale(card_back, (111, 200))

# Define suits
suits = ["Clubs", "Spades", "Hearts", "Diamonds"]

# Load card images
card_images = {}
for suit in suits:
    for value in range(2, 15):  # 2 to Ace (14)
        try:
            image = pygame.image.load(f"games/blackjack/img/cards/{value}_of_{suit}.png")
            image = pygame.transform.scale(image, (111, 200))
            card_images[(value, suit)] = image
        except pygame.error:
            card_images[(value, suit)] = None

# Font setup
font = pygame.font.Font(None, 36)


# Button class
class Button:
    def __init__(self, text, x, y, width, height, color, action):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# Card class
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.image = card_images.get((value, suit))

    def card_value(self):
        if self.value in [11, 12, 13]:
            return 10  # Jack, Queen, King
        elif self.value == 14:
            return 11  # Ace (will be adjusted in score calculation)
        return self.value


# Deck class
class Deck:
    def __init__(self):
        self.cards = [Card(value, suit) for suit in suits for value in range(2, 15)]
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop() if self.cards else None


# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def calculate_score(self):
        score = sum(card.card_value() for card in self.hand)
        ace_count = sum(1 for card in self.hand if card.value == 14)
        # Adjust for aces if score > 21:
        while score > 21 and ace_count:
            score -= 10
            ace_count -= 1
        return score

    def is_busted(self):
        return self.calculate_score() > 21


# Betting system # Original
# gambling_credits = 100 # Original
# For game_integration
player_data = load_player_data()
balance = player_data["cash_balance"]
gambling_credits = balance

bet = 10

bet_buttons = [
    Button(f"Bet £{i}", 1050, 50 + (i // 10) * 50, 150, 40, (0, 255, 0), i)
    for i in range(10, 101, 10)
]
# Create buttons used during gameplay.
hit_button = Button("Hit", 1000, 600, 100, 50, (255, 0, 0), "hit")
stand_button = Button("Stand", 1150, 600, 100, 50, (255, 0, 0), "stand")
play_again_button = Button("Play Again", 900, 600, 200, 50, (255, 0, 0), "play again")
exit_button = Button("Exit", 1150, 600, 100, 50, (255, 0, 0), "exit")


def play_round():
    global gambling_credits, bet, player_data  # noqa: PLW0603

    if gambling_credits < bet:
        return False

    gambling_credits -= bet
    player_data["cash_balance"] += bet  # For game_integration
    # Initialize a new deck and new players for each round
    deck = Deck()
    dealer = Player("Dealer")
    player = Player("Player")

    # Deal two initial cards to each
    for _ in range(2):
        player.add_card(deck.draw_card())
        dealer.add_card(deck.draw_card())

    player_turn = True
    round_over = False
    outcome = ""

    # Main round loop
    while not round_over:
        # Process events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                # For game_integration
                save_and_exit(screen, player_data)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in bet_buttons:
                    if button.is_clicked(event.pos):
                        bet = button.action
        # Draw background
        screen.blit(bg_image, (0, 0))

        # Draw dealer's cards
        if player_turn:
            # During player's turn, hide dealer's first card:
            screen.blit(card_back, (200, 100))
            for i, card in enumerate(dealer.hand[1:]):
                if card.image:
                    screen.blit(card.image, (200 + (i + 1) * 170, 100))
        else:
            # Reveal all dealer cards once player's turn is over:
            for i, card in enumerate(dealer.hand):
                if card.image:
                    screen.blit(card.image, (200 + i * 170, 100))

        # Draw player's cards
        for i, card in enumerate(player.hand):
            if card.image:
                screen.blit(card.image, (200 + i * 170, 400))

        # Display player's current hand score
        player_score_text = font.render(
            "Player Score: " + str(player.calculate_score()), True, (255, 255, 255)
        )
        screen.blit(player_score_text, (10, 500))
        credits_text = font.render(
            f"Credits: £{gambling_credits}  Bet: £{bet}", True, (255, 255, 255)
        )
        screen.blit(credits_text, (1000, 20))
        # Draw action buttons only during player's turn
        if player_turn:
            hit_button.draw(screen)
            stand_button.draw(screen)

        pygame.display.update()

        # Handle player's turn actions
        if player_turn:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hit_button.is_clicked(event.pos):
                        player.add_card(deck.draw_card())
                        if player.is_busted():
                            outcome = "Player busts! Dealer wins!"
                            player_turn = False
                            round_over = True
                    elif stand_button.is_clicked(event.pos):
                        player_turn = False
        else:
            # Dealer's turn (if not already determined by a bust)
            if not round_over:
                # Dealer draws until reaching at least 17
                while dealer.calculate_score() < 17:
                    dealer.add_card(deck.draw_card())
                # Determine outcome
                player_score = player.calculate_score()
                dealer_score = dealer.calculate_score()

                if dealer.is_busted() or player_score > dealer_score:
                    outcome = "Player wins!"
                    gambling_credits += bet * 2  # Player wins double the bet
                    player_data["cash_balance"] += bet * 2  # For game_integration
                elif player_score < dealer_score:
                    outcome = "Dealer wins!"

                else:
                    outcome = "It's a tie!"
                    gambling_credits += bet  # Refund bet to player
                    player_data["cash_balance"] += bet # For game_integration
                if dealer_score == 21:
                    outcome = "BlackJack"
                if player_score == 21:
                    outcome = "BlackJack"
                round_over = True
        for button in bet_buttons:
            button.draw(screen)

        hit_button.draw(screen)
        stand_button.draw(screen)

        # For game_integration
        player_data = load_player_data()  # Load the data
        player_data["cash_balance"] = gambling_credits
        check_balance(screen, player_data)  # check for no money

        pygame.display.update()
        # Small delay to avoid a busy loop
        pygame.time.wait(100)

    # Round is over: show the final hands, outcome, and player's score
    screen.blit(bg_image, (0, 0))

    # Reveal dealer's full hand
    for i, card in enumerate(dealer.hand):
        if card.image:
            screen.blit(card.image, (200 + i * 170, 100))
    # Show player's hand
    for i, card in enumerate(player.hand):
        if card.image:
            screen.blit(card.image, (200 + i * 170, 400))

    # Display outcome message at the top
    outcome_text = font.render(outcome, True, (255, 255, 255))
    screen.blit(outcome_text, (500, 50))

    # Display player's final hand score
    final_score_text = font.render(
        "Player Score: " + str(player.calculate_score()), True, (255, 255, 255)
    )
    screen.blit(final_score_text, (200, 370))

    # Draw the Play Again and Exit buttons
    play_again_button.draw(screen)
    exit_button.draw(screen)

    pygame.display.update()

    # Wait for the player to choose to play again or exit.
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # For game_integration
                save_and_exit(screen, player_data)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.is_clicked(event.pos):
                    waiting = False
                    return True  # Indicates to play again
                elif exit_button.is_clicked(event.pos):
                    waiting = False
                    return False  # Indicates exit the game
        pygame.time.wait(100)


# Main loop: keep playing rounds until the player chooses to exit.
def main():
    running = True
    while running:
        play_again = play_round()
        if not play_again or gambling_credits <= 0:
            running = False

    # For game_integration
    save_and_exit(screen, player_data)
    pygame.quit()


if __name__ == "__main__":
    main()
