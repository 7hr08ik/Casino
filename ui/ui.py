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
        self.btn_width = 200
        self.btn_height = 50
        self.btn_space = 20

        # Initialize parts
        self.btns = []
        self.create_btns()
        self.selected_btn = 0
        self.current_player = None
        self.new_player_active = False
        self.input_text = ""
        self.new_player_rect = pg.Rect(0, 0, 400, 50)
        self.new_player_prompt = ""
        self.font = pg.font.Font(None, 36)
        self.small_font = pg.font.Font(None, 24)

        # Player selection variables
        self.tgl_saved_lst = False
        self.player_list = []
        self.selected_player_index = 0
        self.player_list_scroll = 0
        self.max_list_size = 8

        # Initialize High Scores UI
        self.high_scores_ui = HighScoresUI(screen)

    # -------------------------------------------------------------------------
    # Utilities
    #

    def exit_game(self):
        """
        ExItS ThU GaAmE!
        """
        pg.quit()
        sys.exit()

    def db_add_player(self, player_name):
        """
        Create a new player in the db with the given name
        """
        # Initialize with default values
        cash_balance = conf.starting_cash
        high_scores = {}
        # Save the player data in the db
        save_player_data(player_name, cash_balance, high_scores)
        # Set as current player
        self.current_player = {"player_name": player_name, "cash_balance": cash_balance, "high_scores": high_scores}
        print(f"New player '{player_name}' created with ${cash_balance}")

    def mouse_hover(self, pos):
        """
        Check if mouse is colliding with any button
        """
        for button in self.btns:
            if button["rect"].collidepoint(pos):
                button["hover"] = True
            else:
                button["hover"] = False

    def mouse_click(self, pos):
        """
        Check if any button was clicked
        """
        for button in self.btns:
            if button["rect"].collidepoint(pos):
                button["action"]()

    # -------------------------------------------------------------------------
    # Toggleable UI options
    # draw_main_ui has statements to check for these to be True
    #

    def toggle_new_player(self):
        """
        Used to toggle new player creation variables.
        """
        self.new_player_active = True
        self.new_player_prompt = "Enter your name:"
        self.input_text = ""

    def toggle_saved_list(self):
        """
        Toggle for showing the list of saved games.
        """
        # Get player data from save_load.py
        self.player_list = get_players_display_data()

        # If player list is empty
        if not self.player_list:
            print("No saved players found. Please create a new player.")
            self.toggle_new_player()
            return

        # Toggle player selection
        self.selected_player_index = 0
        self.player_list_scroll = 0
        self.tgl_saved_lst = True

    # -------------------------------------------------------------------------
    # Helpers
    #

    def create_btns(self):
        """
        Create all the buttons for the player selection screen
        """

        # Variables
        buttons = [  # Button, command
            ("New Player", self.toggle_new_player),
            ("Load Player", self.toggle_saved_list),
            ("High Scores", self.show_high_scores),
            ("Exit", self.exit_game),
        ]
        start_x = (self.screen.get_width() - self.btn_width) / 2
        start_y = (self.screen.get_height() - (self.btn_height + self.btn_space) * len(buttons)) / 2

        # Create buttons
        for i, (text, command) in enumerate(buttons):
            # Set Button locations. y + button * number in list
            x = start_x
            y = start_y + (self.btn_height + self.btn_space) * i
            # Create default button details
            button = {
                "rect": pg.Rect(x, y, self.btn_width, self.btn_height),
                "text": text,
                "action": command,
                "hover": False,
            }
            # Add button to the list
            self.btns.append(button)

    def load_selected_player(self):
        """
        Load the currently selected player
        """
        # If player list is empty
        if not self.player_list:
            print("No saved players found. Please create a new player.")
            self.toggle_new_player()
            return

        # Variables
        selected_player_name = self.player_list[self.selected_player_index]["name"]
        player_data = load_player_data(selected_player_name)
        self.current_player = player_data

        # Set player data
        player_name = player_data["player_name"]
        cash_balance = player_data["cash_balance"]
        print(f"Loaded player '{player_name}' with ${cash_balance}")

        # Exit player selection mode
        self.tgl_saved_lst = False

    # -------------------------------------------------------------------------
    # Input Handling
    #

    def show_high_scores(self):
        """Show high scores screen"""
        running = True
        while running:
            self.high_scores_ui.draw()
            pg.display.flip()

            # Let HighScoresUI handle its own events through its key_input method
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit_game()
                elif self.high_scores_ui.key_input(event):
                    running = False

    def handle_text_input(self, event):
        """
        Handle text input
        """
        if event.type == pg.KEYDOWN:
            # Create standard keyboard input
            if event.key == pg.K_RETURN:
                # self.process_txt()
                self.db_add_player(self.input_text)
            elif event.key == pg.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pg.K_ESCAPE:
                self.new_player_active = False
                self.input_text = ""
            else:
                # Process input
                if len(self.input_text) < 20:  # Limit input length to prevent overflow
                    self.input_text += event.unicode

    def handle_player_selection_input(self, event):
        """
        Handle input for player selection screen
        """
        if event.type == pg.KEYDOWN:
            # Standard keyboard controls for menus
            if event.key == pg.K_ESCAPE:
                self.tgl_saved_lst = False
            elif event.key == pg.K_UP:
                self.selected_player_index = max(0, self.selected_player_index - 1)
                # Stop at the top
                if self.selected_player_index < self.player_list_scroll:
                    self.player_list_scroll = self.selected_player_index
            elif event.key == pg.K_DOWN:
                self.selected_player_index = min(len(self.player_list) - 1, self.selected_player_index + 1)
                # Stop at the bottom
                if self.selected_player_index >= self.player_list_scroll + self.max_list_size:
                    self.player_list_scroll = self.selected_player_index - self.max_list_size + 1
            elif event.key == pg.K_RETURN and self.player_list:
                self.load_selected_player()
        elif event.type == pg.MOUSEBUTTONDOWN:
            # List dimentions
            list_width = 600
            list_height = 400
            list_x = (self.screen.get_width() - list_width) // 2
            list_y = 100

            # Check if click is within player list area
            mouse_pos = pg.mouse.get_pos()
            if list_x <= mouse_pos[0] <= list_x + list_width and list_y + 50 <= mouse_pos[1] <= list_y + list_height:
                # Calculate which player was clicked
                entry_height = 40
                player_clicked = (mouse_pos[1] - (list_y + 50)) // entry_height + self.player_list_scroll

                if 0 <= player_clicked < len(self.player_list):
                    self.selected_player_index = player_clicked
                    self.load_selected_player()

    def handle_main_menu_input(self, event):
        """
        Handle input for main menu
        """
        if event.type == pg.MOUSEMOTION:
            self.mouse_hover(pg.mouse.get_pos())
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.mouse_click(pg.mouse.get_pos())
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                # Modulus is used to loop through the buttons
                self.selected_btn = (self.selected_btn - 1) % len(self.btns)
            elif event.key == pg.K_DOWN:
                # Modulus is used to loop through the buttons
                self.selected_btn = (self.selected_btn + 1) % len(self.btns)
            elif event.key == pg.K_RETURN:
                self.btns[self.selected_btn]["action"]()

    # -------------------------------------------------------------------------
    # Main Functions / Methods
    #

    def input_main(self, event):
        """
        Essentially a distro hub for input handling
        """
        if self.new_player_active:
            self.handle_text_input(event)
        elif self.tgl_saved_lst:
            self.handle_player_selection_input(event)
        else:
            self.handle_main_menu_input(event)

    def draw_ui(self):
        """
        Draw the UI elements to the screen
        """

        # If IN player selection, draw player list
        if self.tgl_saved_lst:
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

            # Nav text in center screen below box
            nav_text = self.small_font.render(
                "Use arrow keys to navigate, Enter to select, Esc to cancel", True, (255, 255, 255)
            )
            nav_rect = nav_text.get_rect(center=(self.screen.get_width() // 2, list_y + list_height + 30))
            self.screen.blit(nav_text, nav_rect)

        # If NOT in player selection, draw buttons
        if not self.tgl_saved_lst:
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
        if self.new_player_active:
            # Center the input box
            self.new_player_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)

            # Draw prompt text
            prompt_text = self.font.render(self.new_player_prompt, True, (255, 255, 255))
            prompt_rect = prompt_text.get_rect(
                center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50)
            )
            self.screen.blit(prompt_text, prompt_rect)

            # Draw input box
            pg.draw.rect(self.screen, (255, 255, 255), self.new_player_rect, 2)

            # Draw input text
            text_surface = self.font.render(self.input_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (self.new_player_rect.x + 10, self.new_player_rect.y + 10))

    def main_menu(self):
        """
        Show the player selection screen
        """
        clock = pg.time.Clock()

        while not self.current_player:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit_game()
                # For ANY event, run input handling
                self.input_main(event)

            # Clear screen and draw UI
            self.screen.fill((0, 0, 0))
            self.draw_ui()

            # Update display
            pg.display.flip()
            clock.tick(60)

        return self.current_player

    # -------------------------------------------------------------------------
