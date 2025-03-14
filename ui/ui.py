# ===========================
# Python game suite
#
# Casino Lobby
# ===========================
#
# Main Imports
import sys

import pygame as pg

import conf
from logic.save_load import get_players_display_data, load_player_data, save_player_data
from ui.high_scores_ui import HighScoresUI


class UIElements:
    def __init__(self, screen):
        # Set Variables
        self.screen = screen
        self.btn_wdth = 200
        self.btn_high = 50
        self.btn_space = 20

        # Initialize parts
        self.btns = []
        self.selected_btn = 0
        self.current_player = None
        self.input_active = False
        self.input_text = ""
        self.input_rect = pg.Rect(0, 0, 400, 50)
        self.input_prompt = ""
        self.font = pg.font.Font(None, 36)
        self.small_font = pg.font.Font(None, 24)

        # Player selection variables
        self.player_selection_active = False
        self.player_list = []
        self.selected_player_index = 0
        self.player_list_scroll = 0
        self.max_list_size = 8

        # Initialize High Scores UI
        self.high_scores_ui = HighScoresUI(screen)

        self.create_btns()

    def create_btns(self):
        """
        Create all the buttons for the player selection screen
        """
        buttons = [
            ("New Player", self.new_player),
            ("Load Player", self.show_player_selection),
            ("High Scores", self.show_high_scores),
            ("Exit", self.exit_game),
        ]

        # Calculate starting position
        start_x = (self.screen.get_width() - self.btn_wdth) / 2
        start_y = (self.screen.get_height() - (self.btn_high + self.btn_space) * len(buttons)) / 2

        # Use enumeration to assign numbers to each button
        for i, (text, action) in enumerate(buttons):
            x = start_x
            y = start_y + (self.btn_high + self.btn_space) * i
            button = {
                "rect": pg.Rect(x, y, self.btn_wdth, self.btn_high),
                "text": text,
                "action": action,
                "hover": False,
            }
            self.btns.append(button)

    def draw_ui(self):
        """
        Draw the UI elements to the screen
        """

        # If IN player selection, draw player list
        if self.player_selection_active:
            # Draw title
            title_text = self.font.render("Select Player", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
            self.screen.blit(title_text, title_rect)

            # Draw player list
            list_width = 600
            list_height = 400
            list_x = (self.screen.get_width() - list_width) // 2
            list_y = 100

            # Draw list background
            list_rect = pg.Rect(list_x, list_y, list_width, list_height)
            pg.draw.rect(self.screen, (50, 50, 50), list_rect)
            pg.draw.rect(self.screen, (200, 200, 200), list_rect, 2)

            # Draw column headers
            header_y = list_y + 10
            pg.draw.line(self.screen, (200, 200, 200), (list_x, header_y + 30), (list_x + list_width, header_y + 30))
            name_header = self.small_font.render("Player Name", True, (255, 255, 255))
            balance_header = self.small_font.render("Cash Balance", True, (255, 255, 255))
            date_header = self.small_font.render("Last Played", True, (255, 255, 255))
            self.screen.blit(name_header, (list_x + 20, header_y))
            self.screen.blit(balance_header, (list_x + 250, header_y))
            self.screen.blit(date_header, (list_x + 400, header_y))

            # Draw player entries
            entry_height = 40
            visible_range = range(
                self.player_list_scroll, min(self.player_list_scroll + self.max_list_size, len(self.player_list))
            )
            for i, idx in enumerate(visible_range):
                player = self.player_list[idx]
                entry_y = list_y + 50 + (i * entry_height)
                # Highlight selected player
                if idx == self.selected_player_index:
                    highlight_rect = pg.Rect(list_x + 2, entry_y, list_width - 4, entry_height)
                    pg.draw.rect(self.screen, (100, 100, 255), highlight_rect)

                # Draw player info
                name_text = self.small_font.render(player["name"], True, (255, 255, 255))
                balance_text = self.small_font.render(f"${player['cash_balance']}", True, (255, 255, 255))
                date_text = self.small_font.render(player["last_played"], True, (255, 255, 255))
                self.screen.blit(name_text, (list_x + 20, entry_y + 10))
                self.screen.blit(balance_text, (list_x + 250, entry_y + 10))
                self.screen.blit(date_text, (list_x + 400, entry_y + 10))

            # Nav text in center sccreen below box
            nav_text = self.small_font.render(
                "Use arrow keys to navigate, Enter to select, Esc to cancel", True, (255, 255, 255)
            )
            nav_rect = nav_text.get_rect(center=(self.screen.get_width() // 2, list_y + list_height + 30))
            self.screen.blit(nav_text, nav_rect)

        # If NOT in player selection, draw buttons
        if not self.player_selection_active:
            for i, button in enumerate(self.btns):
                # Set colors based on state
                if i == self.selected_btn:
                    bg_color = (255, 255, 0)  # Yellow when selected
                elif button["hover"]:
                    bg_color = (255, 255, 255)  # White when hovered
                else:
                    bg_color = (100, 100, 100)  # Gray default

                # Draw button
                pg.draw.rect(self.screen, bg_color, button["rect"])

                # Draw text
                text = self.font.render(button["text"], True, (0, 0, 0))
                text_rect = text.get_rect(center=button["rect"].center)
                self.screen.blit(text, text_rect)

        # Create input box for New player name
        if self.input_active:
            # Center the input box
            self.input_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)

            # Draw prompt text
            prompt_text = self.font.render(self.input_prompt, True, (255, 255, 255))
            prompt_rect = prompt_text.get_rect(
                center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50)
            )
            self.screen.blit(prompt_text, prompt_rect)

            # Draw input box
            pg.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)

            # Draw input text
            text_surface = self.font.render(self.input_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (self.input_rect.x + 10, self.input_rect.y + 10))

    def handle_event(self, event):
        """Handle mouse and keyboard events for the UI"""
        if self.input_active:
            self.handle_input_event(event)
        elif self.player_selection_active:
            self.handle_player_selection_event(event)
        else:
            if event.type == pg.MOUSEMOTION:
                self.check_hover(pg.mouse.get_pos())
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.check_click(pg.mouse.get_pos())
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.move_selection(-1)
                elif event.key == pg.K_DOWN:
                    self.move_selection(1)
                elif event.key == pg.K_RETURN:
                    self.execute_selected()

    def handle_player_selection_event(self, event):
        """Handle events when player selection is active"""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.player_selection_active = False
            elif event.key == pg.K_UP:
                self.selected_player_index = max(0, self.selected_player_index - 1)
                # Adjust scroll if needed
                if self.selected_player_index < self.player_list_scroll:
                    self.player_list_scroll = self.selected_player_index
            elif event.key == pg.K_DOWN:
                self.selected_player_index = min(len(self.player_list) - 1, self.selected_player_index + 1)
                # Adjust scroll if needed
                if self.selected_player_index >= self.player_list_scroll + self.max_list_size:
                    self.player_list_scroll = self.selected_player_index - self.max_list_size + 1
            elif event.key == pg.K_RETURN and self.player_list:
                self.load_selected_player()
        elif event.type == pg.MOUSEBUTTONDOWN:
            # Check if click is within player list area
            list_width = 600
            list_height = 400
            list_x = (self.screen.get_width() - list_width) // 2
            list_y = 100

            mouse_pos = pg.mouse.get_pos()
            if list_x <= mouse_pos[0] <= list_x + list_width and list_y + 50 <= mouse_pos[1] <= list_y + list_height:
                # Calculate which player was clicked
                entry_height = 40
                clicked_index = (mouse_pos[1] - (list_y + 50)) // entry_height + self.player_list_scroll

                if 0 <= clicked_index < len(self.player_list):
                    self.selected_player_index = clicked_index
                    self.load_selected_player()

    def handle_input_event(self, event):
        """Handle events when input box is active"""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.process_input()
            elif event.key == pg.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pg.K_ESCAPE:
                self.input_active = False
                self.input_text = ""
            else:
                # Limit input length to prevent overflow
                if len(self.input_text) < 20:
                    self.input_text += event.unicode

    def process_input(self):
        """Process the input text based on current context"""
        if self.input_prompt == "Enter your name:" and self.input_text:
            # Create a new player
            self.create_new_player(self.input_text)

        # Reset input state
        self.input_active = False
        self.input_text = ""

    def check_hover(self, pos):
        """Check if mouse is hovering over any button"""
        for button in self.btns:
            if button["rect"].collidepoint(pos):
                button["hover"] = True
            else:
                button["hover"] = False

    def check_click(self, pos):
        """Check if any button was clicked"""
        for button in self.btns:
            if button["rect"].collidepoint(pos):
                button["action"]()

    def move_selection(self, direction):
        """Move the selection highlight up or down"""
        self.selected_btn = (self.selected_btn + direction) % len(self.btns)

    def execute_selected(self):
        """Execute the action of the currently selected button"""
        self.btns[self.selected_btn]["action"]()

    def new_player(self):
        """Handle new player creation"""
        self.input_active = True
        self.input_prompt = "Enter your name:"
        self.input_text = ""

    def create_new_player(self, player_name):
        """Create a new player with the given name"""
        # Initialize with default values
        cash_balance = conf.starting_cash  # Starting cash
        high_scores = {}  # Empty high scores dictionary

        # Save the player data
        save_player_data(player_name, cash_balance, high_scores)

        # Set as current player
        self.current_player = {"player_name": player_name, "cash_balance": cash_balance, "high_scores": high_scores}

        print(f"New player '{player_name}' created with ${cash_balance}")

        # Here you would typically transition to the main game screen
        # For now, we'll just print a message

    def show_player_selection(self):
        """Show the player selection screen"""
        # Get player data from save_load.py
        self.player_list = get_players_display_data()

        if not self.player_list:
            print("No saved players found. Please create a new player.")
            self.new_player()
            return

        # Reset selection
        self.selected_player_index = 0
        self.player_list_scroll = 0
        self.player_selection_active = True

    def load_selected_player(self):
        """Load the currently selected player"""
        if not self.player_list:
            return

        selected_player_name = self.player_list[self.selected_player_index]["name"]
        player_data = load_player_data(selected_player_name)

        if player_data:
            self.current_player = player_data
            player_name = player_data["player_name"]
            cash_balance = player_data["cash_balance"]
            print(f"Loaded player '{player_name}' with ${cash_balance}")

            # Exit player selection mode
            self.player_selection_active = False

            # Here you would typically transition to the main game screen
            # For now, we'll just print a message

    def show_high_scores(self):
        """Show high scores screen"""
        running = True
        while running:
            self.high_scores_ui.draw()
            pg.display.flip()

            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit_game()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_q or event.key == pg.K_RETURN:
                        running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.high_scores_ui.handle_event(event):
                        running = False
                elif event.type == pg.MOUSEMOTION:
                    self.high_scores_ui.handle_event(event)

    def exit_game(self):
        """Exit the game"""
        pg.quit()
        sys.exit()

    def main_menu(self):
        """Show the player selection screen and handle player creation/loading"""
        clock = pg.time.Clock()

        while not self.current_player:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                self.handle_event(event)

            # Clear screen and draw UI
            self.screen.fill((0, 0, 0))
            self.draw_ui()

            # Update display
            pg.display.flip()
            clock.tick(60)

        return self.current_player

    def update_player_balance(self, player_data, amount_change):
        """Update player's cash balance and save the changes"""
        player_data["cash_balance"] += amount_change
        save_player_data(player_data["player_name"], player_data["cash_balance"], player_data["high_scores"])
        return player_data

    def update_player_high_score(self, player_data, game_name, score):
        """Update player's high score for a specific game if it's higher than the current one"""
        high_scores = player_data["high_scores"]

        # Initialize the game entry if it doesn't exist
        if game_name not in high_scores:
            high_scores[game_name] = 0

        # Update if the new score is higher
        if score > high_scores[game_name]:
            high_scores[game_name] = score

            # Save the updated high scores
            save_player_data(player_data["player_name"], player_data["cash_balance"], high_scores)
            return True  # Indicate that a new high score was set

        return False  # No new high score
