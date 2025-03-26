# ===========================
# BlackJack
#
# Author: Viorica Anghel
# 07/02/2025
#
# Modified by: Rob Hickling
# 21/03/2025
# Added functionality for saving and loading player data
# required for integration into the lobby
# all commented with;
#    # For game_integration
# ===========================

import os
import random
import sys

import pygame

# For game_integration
from game_integration import check_balance, load_player_data, save_and_exit

pygame.init()

# Global constants for screen dimensions
W = 1280
H = 720
SCREEN = pygame.display.set_mode((W, H))
pygame.display.set_caption("Teesside Lottery")
CLOCK = pygame.time.Clock()

TITLE_FONT = pygame.font.SysFont("Arial", 48, True)
BIG_TITLE_FONT = pygame.font.SysFont("Arial", 72, True)
TEXT_FONT = pygame.font.SysFont("Arial", 28)
SMALL_FONT = pygame.font.SysFont("Arial", 20)

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
BLUE = (50, 150, 255)
GREEN = (50, 220, 50)
RED = (240, 50, 50)
YELLOW = (255, 215, 0)
ORANGE = (255, 165, 0)

# Load and scale the background image (Rob)
BG_IMAGE = pygame.image.load(
    "games/lottery/img/background_image.png"
).convert_alpha()
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (W, H))

# Lottery setup: number of picks and grid for number buttons
N = 6
btns = [
    (
        i,
        pygame.Rect(
            20 + ((i - 1) % 10) * 50, 115 + ((i - 1) // 10) * 50, 45, 45
        ),
    )
    for i in range(1, 60)
]

# Global game state variables
u_nums, d_nums, matches = [], [], []
history, favs = [], []
msg, msg_t = "", 0
editing_index = None

# Game pot and prize won values
# pot = 500 # Original
# For game_integration
player_data = load_player_data()
pot = player_data["cash_balance"]

prize_won = 0


# ---------------------------------------------------------------------------
# File handling functions
# ---------------------------------------------------------------------------
def load_history():
    """Load the last 5 draws from the history file into the history list."""
    global history
    if os.path.exists("games/lottery/logs/history.txt"):
        with open("games/lottery/logs/history.txt") as f:
            history = f.read().splitlines()[-5:]
    else:
        history = []


def save_history(draw):
    """Append a new draw to the history file and reload the history list."""
    with open("games/lottery/logs/history.txt", "a") as f:
        f.write(draw + "\n")
    load_history()


def load_favs():
    """Load favourite number sets from the 'favs.txt' file."""
    global favs
    if os.path.exists("games/lottery/logs/favs.txt"):
        with open("games/lottery/logs/favs.txt") as f:
            favs = [
                list(map(int, line.strip().split(",")))
                for line in f.read().splitlines()
                if line.strip()
            ]
    # else:
    #     favs = []
    #     print("favs load")


def save_favs():
    """Save the current favourite number sets to the 'favs.txt' file."""
    with open("games/lottery/logs/favs.txt", "w") as f:
        f.write("\n".join([",".join(map(str, fav)) for fav in favs]))


# ---------------------------------------------------------------------------
# Drawing helper functions
# ---------------------------------------------------------------------------
def txt(t, font, c, x, y, center=False):
    """
    Render text using the specified font and color at (x, y).
    If center is True, the text is centered on (x, y).
    """
    text_surface = font.render(t, True, c)
    if center:
        rect = text_surface.get_rect(center=(x, y))
    else:
        rect = text_surface.get_rect(topleft=(x, y))
    SCREEN.blit(text_surface, rect)


def btn(r, t, sel=False):
    """
    Draw a button with rectangle r and label t.
    If sel is True, the button uses the GREEN color; otherwise BLUE.
    """
    color = GREEN if sel else BLUE
    pygame.draw.rect(SCREEN, color, r, border_radius=8)
    pygame.draw.rect(SCREEN, BLACK, r, 2, border_radius=8)
    txt(str(t), TEXT_FONT, BLACK, r.centerx, r.centery, True)


def bg(image=True):
    """
    Draw the background image if image is True;
    otherwise, fill the screen with GREY.
    """
    if image:
        SCREEN.blit(BG_IMAGE, (0, 0))
    else:
        SCREEN.fill(GREY)


def nav(home, menu, exit):
    """
    Draw navigation buttons ("Home", "Menu", "Exit") at the bottom of the screen.
    Each button calls its respective function when clicked.
    Returns the list of navigation buttons.
    """
    nav_btns = [
        {
            "l": "Home",
            "r": pygame.Rect(20, H - 60, 120, 40),
            "a": home,
            "c": ORANGE,
        },
        {
            "l": "Menu",
            "r": pygame.Rect(160, H - 60, 120, 40),
            "a": menu,
            "c": BLUE,
        },
        {
            "l": "Exit",
            "r": pygame.Rect(W - 140, H - 60, 120, 40),
            "a": exit,
            "c": RED,
        },
    ]
    for b in nav_btns:
        pygame.draw.rect(SCREEN, b["c"], b["r"], border_radius=8)
        pygame.draw.rect(SCREEN, BLACK, b["r"], 2, border_radius=8)
        txt(b["l"], TEXT_FONT, BLACK, b["r"].centerx, b["r"].centery, True)
    return nav_btns


# ---------------------------------------------------------------------------
# Game action functions
# ---------------------------------------------------------------------------
def lucky_dip():
    """Randomly select 6 unique numbers for the user."""
    global u_nums
    u_nums = sorted(random.sample(range(1, 60), N))


def reset():
    """Reset the user-selected numbers and clear the editing mode."""
    global u_nums, msg, msg_t, editing_index
    u_nums = []
    editing_index = None
    msg, msg_t = "Reset!", 120


def save_fav():
    """
    Save the current selection as a favourite.
    If editing_index is set, update that favourite; otherwise, add a new one.
    """
    global msg, msg_t, editing_index, favs
    if len(u_nums) == N:
        if editing_index is not None:
            favs[editing_index] = u_nums[:]
            save_favs()
            msg, msg_t = "Updated!", 120
            editing_index = None
        else:
            if u_nums not in favs:
                favs.append(u_nums[:])
                save_favs()
                msg, msg_t = "Saved!", 120
            else:
                msg, msg_t = "Exists!", 120


def play_fav():
    """
    If there are saved favourite sets, open the favourites screen;
    otherwise, display a message.
    """
    global msg, msg_t
    if favs:
        play_favs_screen()
    else:
        msg, msg_t = "No Favs!", 120


# ---------------------------------------------------------------------------
# Screen functions
# ---------------------------------------------------------------------------
def start_screen():
    """Display the main start screen with navigation and game status."""
    # Check if favs.txt exists, otherwise create.
    # To solve error when no favs exisit (Rob)
    if os.path.exists("games/lottery/logs/favs.txt"):
        pass
    else:
        save_favs()

    load_history()
    load_favs()
    jackpot = "£10M"
    btns_list = [
        {
            "l": "Play",
            "r": pygame.Rect(20, 250, 200, 50),
            "a": selection_screen,
        },
        {
            "l": "Lucky Dip",
            "r": pygame.Rect(20, 320, 200, 50),
            "a": lambda: [reset(), lucky_dip(), run_lottery(SCREEN)],
        },
        {"l": "Favourites", "r": pygame.Rect(20, 390, 200, 50), "a": play_fav},
        {"l": "Rules", "r": pygame.Rect(20, 460, 200, 50), "a": rules_screen},
        {
            "l": "Exit",
            "r": pygame.Rect(20, 530, 200, 50),
            "a": lambda: [
                # For game_integration
                save_and_exit(SCREEN, player_data),
                pygame.quit(),
                sys.exit(),
            ],
            "c": RED,
        },
    ]
    while True:
        CLOCK.tick(60)
        bg(image=True)
        # txt("LOTTERY", BIG_TITLE_FONT, WHITE, W // 2, 80, True)
        txt(f"Jackpot: {jackpot}", TEXT_FONT, RED, int(W / 1.3), 100, True)
        txt("Last Draws:", TEXT_FONT, RED, 1000, 200, True)
        for i, d in enumerate(history):
            txt(d, SMALL_FONT, ORANGE, 1000, 240 + i * 30, True)
        txt(f"Pot: £{pot}", TEXT_FONT, YELLOW, W - 100, 40, True)
        for b in btns_list:
            pygame.draw.rect(SCREEN, b.get("c", BLUE), b["r"], border_radius=8)
            pygame.draw.rect(SCREEN, WHITE, b["r"], 2, border_radius=8)
            txt(b["l"], TEXT_FONT, WHITE, b["r"].centerx, b["r"].centery, True)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                # For game_integration
                save_and_exit(SCREEN, player_data)
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                m = pygame.mouse.get_pos()
                for b in btns_list:
                    if b["r"].collidepoint(m):
                        b["a"]()
                        return

        # For game_integration
        player_data = load_player_data()  # Load it
        player_data["cash_balance"] = pot  # Override it
        check_balance(SCREEN, player_data)  # Save it? I hope...

        pygame.display.update()


def selection_screen():
    """
    Display the selection screen where the user chooses 6 numbers.
    Shows the grid of number buttons, extra options, and a 'Draw' button when ready.
    """
    global msg, msg_t, editing_index, pot
    extra = [
        {"l": "Lucky Dip", "r": pygame.Rect(20, 440, 160, 40), "a": lucky_dip},
        {"l": "Reset", "r": pygame.Rect(200, 440, 160, 40), "a": reset},
        {
            "l": "Update Fav" if editing_index is not None else "Save Fav",
            "r": pygame.Rect(20, 500, 160, 40),
            "a": save_fav,
        },
        {"l": "Play Favs", "r": pygame.Rect(200, 500, 160, 40), "a": play_fav},
    ]
    while True:
        CLOCK.tick(60)
        bg(image=False)
        # Display screen title and instructions
        txt("LOTTERY", BIG_TITLE_FONT, WHITE, W // 2, 40, True)
        txt("Select 6 Numbers", TEXT_FONT, WHITE, W // 2, 100, True)
        txt(f"Pot: £{pot}", TEXT_FONT, YELLOW, W - 100, 40, True)
        # Draw the grid of number buttons
        for n, r in btns:
            btn(r, n, n in u_nums)
        # Place the Draw button below the grid if 6 numbers are selected
        draw_button_rect = None
        if len(u_nums) == N:
            draw_button_rect = pygame.Rect(400, 460, 190, 60)
            btn(draw_button_rect, "Draw", sel=True)
        # Draw extra option buttons
        for b in extra:
            btn(b["r"], b["l"])
        # Display any message to the user
        if msg_t > 0:
            txt(msg, TEXT_FONT, ORANGE, W // 2, H - 100, True)
            msg_t -= 1
        # Navigation buttons at the bottom
        n_buttons = nav(
            start_screen,
            selection_screen,
            lambda: [
                # For game_integration
                save_and_exit(SCREEN, player_data),
                pygame.quit(),
                sys.exit(),
            ],
        )
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                m = pygame.mouse.get_pos()
                # Check extra buttons
                for b in extra:
                    if b["r"].collidepoint(m):
                        b["a"]()
                # Check navigation buttons
                for b in n_buttons:
                    if b["r"].collidepoint(m):
                        b["a"]()
                        return
                # Check if user is selecting a number
                if len(u_nums) < N:
                    for n_val, r in btns:
                        if r.collidepoint(m) and n_val not in u_nums:
                            u_nums.append(n_val)
                            break
                # If Draw button is clicked, run the lottery draw
                if draw_button_rect and draw_button_rect.collidepoint(m):
                    run_lottery(SCREEN)
                    return
        pygame.display.update()


def play_favs_screen():
    """
    Display the favourites screen where saved number sets are shown.
    Allows the user to set, edit, or delete favourite number sets.
    """
    global editing_index, u_nums, favs
    while True:
        CLOCK.tick(60)
        bg(image=False)
        txt("Favourite Sets", BIG_TITLE_FONT, YELLOW, W // 2, 100, True)
        fav_btns = []
        # Create button rectangles for each favourite set and for edit/delete options
        for i, fav in enumerate(favs):
            base_rect = pygame.Rect((W - 300) // 2, 200 + i * 50, 300, 40)
            edit_rect = pygame.Rect(base_rect.right + 10, base_rect.top, 60, 40)
            delete_rect = pygame.Rect(
                edit_rect.right + 10, base_rect.top, 60, 40
            )
            fav_btns.append((i, fav, base_rect, edit_rect, delete_rect))
        # Draw each favourite set and its Edit/Delete buttons
        for i, fav, base_rect, edit_rect, delete_rect in fav_btns:
            btn(base_rect, f"Set {i + 1}: {', '.join(map(str, fav))}")
            pygame.draw.rect(SCREEN, ORANGE, edit_rect, border_radius=8)
            pygame.draw.rect(SCREEN, BLACK, edit_rect, 2, border_radius=8)
            txt(
                "Edit",
                TEXT_FONT,
                BLACK,
                edit_rect.centerx,
                edit_rect.centery,
                True,
            )
            pygame.draw.rect(SCREEN, RED, delete_rect, border_radius=8)
            pygame.draw.rect(SCREEN, BLACK, delete_rect, 2, border_radius=8)
            txt(
                "Delete",
                TEXT_FONT,
                BLACK,
                delete_rect.centerx,
                delete_rect.centery,
                True,
            )
        n_buttons = nav(
            start_screen,
            selection_screen,
            lambda: [
                # For game_integration
                save_and_exit(SCREEN, player_data),
                pygame.quit(),
                sys.exit(),
            ],
        )
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                # For game_integration
                save_and_exit(SCREEN, player_data)
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                m = pygame.mouse.get_pos()
                # Check navigation buttons
                for b in n_buttons:
                    if b["r"].collidepoint(m):
                        b["a"]()
                        return
                # Check favourite set buttons
                for i, fav, base_rect, edit_rect, delete_rect in fav_btns:
                    if base_rect.collidepoint(m):
                        u_nums = fav[:]
                        selection_screen()
                        return
                    if edit_rect.collidepoint(m):
                        editing_index = i
                        u_nums = fav[:]
                        selection_screen()
                        return
                    if delete_rect.collidepoint(m):
                        favs.pop(i)
                        save_favs()
                        break
        pygame.display.update()


def wrap_text(text, font, max_width):
    """
    Wrap text to fit within a maximum width.
    Returns a list of text lines.
    """
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + (" " if current_line != "" else "") + word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines


def rules_screen():
    """
    Display the rules screen with game instructions.
    Text is wrapped and displayed over a semi-transparent panel.
    """
    rules = [
        "1. Objective: Match your 6 numbers to the drawn numbers to win.",
        "2. Selection: Click 6 numbers (1-59) or use 'Lucky Dip' for random picks.",
        "3. Drawing: Click the Draw button when 6 numbers are selected.",
        "4. Favourites: Save your number sets with 'Save Fav' and load with 'Play Favs'.",
        "5. History: Last 5 draws are shown on the start screen.",
        "6. Prizes: 2 matches = £50, 3 matches = £500, 5 matches = £10,000, 6 matches = £10M.",
        "7. Navigation: Use the buttons to navigate between screens.",
    ]
    while True:
        CLOCK.tick(60)
        bg(image=False)
        txt("Rules", BIG_TITLE_FONT, BLACK, W // 2, 30, True)
        # Create a semi-transparent panel for rule text
        panel_margin = 10
        panel_rect = pygame.Rect(
            panel_margin, 60, W - 2 * panel_margin, H - 100
        )
        panel_surface = pygame.Surface((panel_rect.width, panel_rect.height))
        panel_surface.set_alpha(200)
        panel_surface.fill(GREY)
        SCREEN.blit(panel_surface, panel_rect.topleft)
        start_x = panel_rect.left + 10
        current_y = panel_rect.top + 10
        line_spacing = TEXT_FONT.get_height() + 5
        gap = 10
        # Wrap and display each rule with numbering
        for rule in rules:
            if ". " in rule:
                num, text = rule.split(". ", 1)
            else:
                num, text = "", rule
            if num:
                num_surface = TEXT_FONT.render(num + ".", True, ORANGE)
                num_width = num_surface.get_width()
            else:
                num_width = 0
            indent = num_width + gap if num else 0
            available_width = panel_rect.right - (start_x + indent) - 10
            lines = wrap_text(text, TEXT_FONT, available_width)
            if num:
                SCREEN.blit(num_surface, (start_x, current_y))
            if lines:
                first_line_surface = TEXT_FONT.render(lines[0], True, WHITE)
                SCREEN.blit(first_line_surface, (start_x + indent, current_y))
                current_y += line_spacing
                for extra_line in lines[1:]:
                    extra_line_surface = TEXT_FONT.render(
                        extra_line, True, WHITE
                    )
                    SCREEN.blit(
                        extra_line_surface, (start_x + indent, current_y)
                    )
                    current_y += line_spacing
            else:
                current_y += line_spacing
            current_y += 5
        n_buttons = nav(
            start_screen,
            selection_screen,
            lambda: [
                # For game_integration
                save_and_exit(SCREEN, player_data),
                pygame.quit(),
                sys.exit(),
            ],
        )
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                # For game_integration
                save_and_exit(SCREEN, player_data)
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                m = pygame.mouse.get_pos()
                for b in n_buttons:
                    if b["r"].collidepoint(m):
                        b["a"]()
                        return
        pygame.display.update()


def run_lottery(screen):
    """
    Execute a lottery draw:
    Deduct ticket cost, randomly draw numbers, compare with user-selected numbers,
    add any prize to the pot, and then show the results screen.
    """
    global d_nums, matches, pot, prize_won, msg, msg_t
    # For game_integration
    player_data = load_player_data()  # Load data
    check_balance(SCREEN, player_data)  # check for no money

    ticket_cost = 10
    if pot < ticket_cost:
        msg, msg_t = "Not enough money!", 120
        selection_screen()
        return
    pot -= ticket_cost
    player_data["cash_balance"] -= ticket_cost  # For game_integration
    d_nums = sorted(random.sample(range(1, 60), N))
    matches = list(set(u_nums) & set(d_nums))
    save_history(", ".join(map(str, d_nums)))
    prize_dict = {2: 50, 3: 500, 5: 10000, 6: 10000000}
    prize_won = prize_dict.get(len(matches), 0)
    pot += prize_won
    player_data["cash_balance"] += prize_won  # For game_integration

    game_screen()


def game_screen():
    """
    Display the results screen showing the drawn numbers, the matches,
    the prize won, the ticket cost, and the updated pot.
    """
    global prize_won, pot

    # For game_integration
    check_balance(SCREEN, player_data)  # check for no money

    while True:
        CLOCK.tick(60)
        bg(image=False)
        txt("Results", BIG_TITLE_FONT, BLACK, W // 2, 40, True)
        txt(
            f"Your Numbers: {', '.join(map(str, sorted(u_nums)))}",
            TEXT_FONT,
            WHITE,
            W // 2,
            120,
            True,
        )
        txt(
            f"Drawn: {', '.join(map(str, d_nums))}",
            TEXT_FONT,
            WHITE,
            W // 2,
            160,
            True,
        )
        txt(
            f"Matches: {', '.join(map(str, matches)) if matches else 'None'}",
            TEXT_FONT,
            WHITE,
            W // 2,
            200,
            True,
        )
        txt(
            f"Prize Won: £{prize_won}",
            TEXT_FONT,
            GREEN if prize_won > 0 else RED,
            W // 2,
            240,
            True,
        )
        txt("Ticket Cost: £10", TEXT_FONT, WHITE, W // 2, 280, True)
        txt(f"Pot: £{pot}", TEXT_FONT, YELLOW, W - 100, 80, True)
        n_buttons = nav(
            start_screen,
            selection_screen,
            lambda: [
                # For game_integration
                save_and_exit(SCREEN, player_data),
                pygame.quit(),
                sys.exit(),
            ],
        )
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                # For game_integration
                save_and_exit(SCREEN, player_data)
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                m = pygame.mouse.get_pos()
                for b in n_buttons:
                    if b["r"].collidepoint(m):
                        b["a"]()
                        reset()
                        return
        pygame.display.update()


if __name__ == "__main__":
    start_screen()
