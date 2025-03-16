import sys

import pygame as pg

import conf
from logic.save_load import get_players_display_data, load_player_data, save_player_data
from ui.high_scores_ui import HighScoresUI


class UIElements:
    def __init__(self, screen):
        self.screen = screen
        self.btn_wdth = 200
        self.btn_high = 50
        self.btn_space = 20
        self.buttons = []
        self.selected_btn = 0
        self.current_player = None
        self.input_active = False
        self.input_text = ""
        self.input_rect = pg.Rect(0, 0, 400, 50)
        self.input_prompt = ""
        self.font = pg.font.Font(None, 36)
        self.small_font = pg.font.Font(None, 24)
        self.player_selection_active = False
        self.player_list = []
        self.selected_player_index = 0
        self.player_list_scroll = 0
        self.max_list_size = 8
        self.high_scores_ui = HighScoresUI(screen)

        self.create_buttons()
        self.init_ui_elements()

    def init_ui_elements(self):
        """Initialize UI elements and their properties"""
        pg.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)

    def create_buttons(self):
        """Create and position all main menu buttons"""
        buttons = [
            ("New Player", self.new_player),
            ("Load Player", self.show_player_selection),
            ("High Scores", self.show_high_scores),
            ("Exit", self.exit_game),
        ]

        start_x = (self.screen.get_width() - self.btn_wdth) / 2
        start_y = (self.screen.get_height() - (self.btn_high + self.btn_space) * len(buttons)) / 2

        for i, (text, action) in enumerate(buttons):
            x = start_x
            y = start_y + (self.btn_high + self.btn_space) * i
            self.buttons.append(
                {"rect": pg.Rect(x, y, self.btn_wdth, self.btn_high), "text": text, "action": action, "hover": False}
            )

    def draw(self):
        """Draw all UI elements to the screen"""
        self.screen.fill((0, 0, 0))

        if self.player_selection_active:
            self.draw_player_selection()
        else:
            self.draw_buttons()
            self.draw_input_box()

        pg.display.flip()

    def draw_buttons(self):
        """Draw main menu buttons"""
        for i, button in enumerate(self.buttons):
            bg_color = (
                (255, 255, 0) if i == self.selected_btn else (255, 255, 255) if button["hover"] else (100, 100, 100)
            )

            pg.draw.rect(self.screen, bg_color, button["rect"])
            text = self.font.render(button["text"], True, (0, 0, 0))
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)

    def draw_player_selection(self):
        """Draw player selection interface"""
        self.draw_player_list()
        self.draw_selection_navigation()

    def draw_player_list(self):
        """Draw the player list with scrolling"""
        list_width = 600
        list_height = 400
        list_x = (self.screen.get_width() - list_width) // 2
        list_y = 100

        pg.draw.rect(self.screen, (50, 50, 50), (list_x, list_y, list_width, list_height))
        pg.draw.rect(self.screen, (200, 200, 200), (list_x, list_y, list_width, list_height), 2)

        self.draw_column_headers(list_x, list_y, list_width)
        self.draw_player_entries(list_x, list_y, list_width)

    def draw_column_headers(self, list_x, list_y, list_width):
        """Draw column headers for player list"""
        header_y = list_y + 10
        pg.draw.line(self.screen, (200, 200, 200), (list_x, header_y + 30), (list_x + list_width, header_y + 30))

        headers = ["Player Name", "Cash Balance", "Last Played"]
        positions = [20, 250, 400]

        for header, pos in zip(headers, positions):
            text = self.small_font.render(header, True, (255, 255, 255))
            self.screen.blit(text, (list_x + pos, header_y))

    def draw_player_entries(self, list_x, list_y, list_width):
        """Draw player entries with highlighting"""
        entry_height = 40
        visible_range = range(
            self.player_list_scroll, min(self.player_list_scroll + self.max_list_size, len(self.player_list))
        )

        for i, idx in enumerate(visible_range):
            player = self.player_list[idx]
            entry_y = list_y + 50 + (i * entry_height)

            if idx == self.selected_player_index:
                self.draw_highlight(list_x, entry_y, list_width, entry_height)

            self.draw_player_info(player, list_x, entry_y)

    def draw_highlight(self, x, y, width, height):
        """Draw highlight for selected player"""
        highlight_rect = pg.Rect(x + 2, y, width - 4, height)
        pg.draw.rect(self.screen, (100, 100, 255), highlight_rect)

    def draw_player_info(self, player, list_x, entry_y):
        """Draw player information"""
        name_text = self.small_font.render(player["name"], True, (255, 255, 255))
        balance_text = self.small_font.render(f"${player['cash_balance']}", True, (255, 255, 255))
        date_text = self.small_font.render(player["last_played"], True, (255, 255, 255))

        self.screen.blit(name_text, (list_x + 20, entry_y + 10))
        self.screen.blit(balance_text, (list_x + 250, entry_y + 10))
        self.screen.blit(date_text, (list_x + 400, entry_y + 10))

    def draw_selection_navigation(self):
        """Draw navigation text for player selection"""
        nav_text = self.small_font.render(
            "Use arrow keys to navigate, Enter to select, Esc to cancel", True, (255, 255, 255)
        )
        nav_rect = nav_text.get_rect(center=(self.screen.get_width() // 2, (self.screen.get_height() // 2) + 150))
        self.screen.blit(nav_text, nav_rect)

    def draw_input_box(self):
        """Draw input box and prompt text"""
        if self.input_active:
            self.input_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)

            prompt_text = self.font.render(self.input_prompt, True, (255, 255, 255))
            prompt_rect = prompt_text.get_rect(
                center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50)
            )
            self.screen.blit(prompt_text, prompt_rect)

            pg.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
            text_surface = self.font.render(self.input_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (self.input_rect.x + 10, self.input_rect.y + 10))

    def handle_event(self, event):
        """Handle user input events"""
        if self.input_active:
            self.handle_input(event)
        elif self.player_selection_active:
            self.handle_player_selection(event)
        else:
            self.handle_main_menu(event)

    def handle_main_menu(self, event):
        """Handle events in main menu"""
        if event.type == pg.MOUSEMOTION:
            self.check_button_hover(event.pos)
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.check_button_click(event.pos)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.move_selection(-1)
            elif event.key == pg.K_DOWN:
                self.move_selection(1)
            elif event.key == pg.K_RETURN:
                self.execute_selected_action()

    def handle_input(self, event):
        """Handle input box events"""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.process_input()
            elif event.key == pg.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pg.K_ESCAPE:
                self.input_active = False
                self.input_text = ""
            else:
                if len(self.input_text) < 20:
                    self.input_text += event.unicode

    def handle_player_selection(self, event):
        """Handle player selection events"""
        if event.type == pg.KEYDOWN:
            self.handle_selection_keyboard(event)
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.handle_selection_mouse(event)

    def handle_selection_keyboard(self, event):
        """Handle keyboard input in player selection"""
        if event.key == pg.K_ESCAPE:
            self.player_selection_active = False
        elif event.key == pg.K_UP:
            self.navigate_selection(-1)
        elif event.key == pg.K_DOWN:
            self.navigate_selection(1)
        elif event.key == pg.K_RETURN and self.player_list:
            self.load_selected_player()

    def handle_selection_mouse(self, event):
        """Handle mouse input in player selection"""
        mouse_pos = pg.mouse.get_pos()
        list_area = pg.Rect((self.screen.get_width() - 600) // 2, 100, 600, 400)

        if list_area.collidepoint(mouse_pos):
            entry_height = 40
            clicked_index = (mouse_pos[1] - 150) // entry_height + self.player_list_scroll

            if 0 <= clicked_index < len(self.player_list):
                self.selected_player_index = clicked_index
                self.load_selected_player()

    def check_button_hover(self, pos):
        """Check if mouse is hovering over any button"""
        for button in self.buttons:
            button["hover"] = button["rect"].collidepoint(pos)

    def check_button_click(self, pos):
        """Check if any button was clicked"""
        for button in self.buttons:
            if button["rect"].collidepoint(pos):
                button["action"]()

    def move_selection(self, direction):
        """Move selection highlight"""
        self.selected_btn = (self.selected_btn + direction) % len(self.buttons)

    def execute_selected_action(self):
        """Execute selected button action"""
        self.buttons[self.selected_btn]["action"]()

    def new_player(self):
        """Start new player creation process"""
        self.input_active = True
        self.input_prompt = "Enter your name:"
        self.input_text = ""

    def create_new_player(self, player_name):
        """Create a new player with default values"""
        cash_balance = conf.starting_cash
        high_scores = {}

        save_player_data(player_name, cash_balance, high_scores)
        self.current_player = {"player_name": player_name, "cash_balance": cash_balance, "high_scores": high_scores}

        print(f"New player '{player_name}' created with ${cash_balance}")
        self.player_selection_active = False

    def show_player_selection(self):
        """Show player selection screen"""
        self.player_list = get_players_display_data()

        if not self.player_list:
            print("No saved players found. Please create a new player.")
            self.new_player()
            return

        self.selected_player_index = 0
        self.player_list_scroll = 0
        self.player_selection_active = True

    def load_selected_player(self):
        """Load selected player data"""
        if not self.player_list:
            return

        player_name = self.player_list[self.selected_player_index]["name"]
        player_data = load_player_data(player_name)

        if player_data:
            self.current_player = player_data
            print(f"Loaded player '{player_name}' with ${player_data['cash_balance']}")
            self.player_selection_active = False

    def show_high_scores(self):
        """Show high scores screen"""
        self.high_scores_ui.show()

    def exit_game(self):
        """Exit the application"""
        pg.quit()
        sys.exit()

    def main_menu(self):
        """Show main menu and handle player creation/loading"""
        clock = pg.time.Clock()

        while not self.current_player:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit_game()
                self.handle_event(event)

            self.draw()
            clock.tick(60)

        return self.current_player

    def update_player_balance(self, player_data, amount_change):
        """Update player's cash balance and save changes"""
        player_data["cash_balance"] += amount_change
        save_player_data(player_data["player_name"], player_data["cash_balance"], player_data["high_scores"])
        return player_data

    def update_player_high_score(self, player_data, game_name, score):
        """Update player's high score if applicable"""
        high_scores = player_data["high_scores"]

        if game_name not in high_scores or score > high_scores[game_name]:
            high_scores[game_name] = score
            save_player_data(player_data["player_name"], player_data["cash_balance"], high_scores)
            return True

        return False
