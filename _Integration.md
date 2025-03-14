
I'll help you create a solution for integrating your games with the player data system. Your idea of creating a reusable module that can be included in each game is excellent.



Let's create a `player_scores.py` file that can be copied into each game directory. This module will handle:

1. Loading the current player's data when a game starts
2. Updating the player's cash balance when the game ends
3. Updating game-specific high scores
4. Saving the updated player data back to the JSON file

```python
# ===========================
# Python game suite
#
# Casino Game Integration Module
# ===========================
#
# Main Imports
import os
import sys
import json
import datetime

# Add parent directory to path to allow importing from the main Casino directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Try to import from the Casino's logic directory
try:
    from logic.save_load import save_player_data, load_player_data, load_all_players
    from logic.player_selection import update_player_high_score
except ImportError:
    # If we can't import directly, define the necessary functions here
    def load_all_players():
        """Load all players data from the JSON file"""
        try:
            # Look for the data file in the parent directory structure
            data_paths = [
                "data/players_data.json",  # Same directory
                "../data/players_data.json",  # One level up
                "../../data/players_data.json",  # Two levels up
            ]
            
            for path in data_paths:
                if os.path.exists(path):
                    with open(path) as f:
                        data = json.load(f)
                        return data
            
            # If we get here, we couldn't find the file
            print("Warning: Could not find players_data.json")
            return {}
        except (FileNotFoundError, json.JSONDecodeError):
            # Return empty dict if file doesn't exist or is invalid
            return {}

    def load_player_data(player_name):
        """Load specific player data from the JSON file"""
        all_players = load_all_players()

        # Return the requested player data if it exists
        if player_name in all_players:
            return all_players[player_name]

        return None

    def save_player_data(player_name, cash_balance, high_scores):
        """Save player data to a JSON file, updating high score if applicable"""
        all_players = load_all_players()

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update high score if current balance is higher
        if cash_balance > high_scores.get("cash", 0):
            high_scores["cash"] = cash_balance

        all_players[player_name] = {
            "player_name": player_name,
            "cash_balance": cash_balance,
            "high_scores": high_scores,
            "last_played": current_time,
        }

        # Keep only top 20 players
        if len(all_players) > 20:
            sorted_players = sorted(
                all_players.items(), key=lambda x: datetime.datetime.strptime(x[1]["last_played"], "%Y-%m-%d %H:%M:%S")
            )
            del all_players[sorted_players[0][0]]

        # Look for the data directory in various locations
        data_paths = [
            "data",  # Same directory
            "../data",  # One level up
            "../../data",  # Two levels up
        ]
        
        for path in data_paths:
            if os.path.exists(path):
                # Make sure the directory exists
                os.makedirs(path, exist_ok=True)
                
                # Save the file
                with open(f"{path}/players_data.json", "w") as f:
                    json.dump(all_players, f, indent=4)
                return True
        
        # If we get here, we couldn't find a suitable location
        print("Warning: Could not find a suitable location to save player data")
        return False


class GamePlayerData:
    """
    A class to handle player data for individual games in the Casino suite.
    
    This class provides methods to:
    - Load the current player's data
    - Update the player's cash balance
    - Update game-specific high scores
    - Save the updated player data back to the JSON file
    """
    
    def __init__(self, game_name):
        """
        Initialize the GamePlayerData with the game name.
        
        Args:
            game_name (str): The name of the game (e.g., "Blackjack", "Pinball")
        """
        self.game_name = game_name
        self.player_data = None
        self.player_name = None
        
        # Try to get the current player from command line arguments
        if len(sys.argv) > 1:
            self.player_name = sys.argv[1]
            self.load_player()
    
    def load_player(self, player_name=None):
        """
        Load player data from the JSON file.
        
        Args:
            player_name (str, optional): The name of the player to load.
                                         If None, uses the name provided at initialization.
        
        Returns:
            bool: True if player data was loaded successfully, False otherwise.
        """
        if player_name:
            self.player_name = player_name
            
        if not self.player_name:
            print("Error: No player name provided")
            return False
            
        self.player_data = load_player_data(self.player_name)
        
        if not self.player_data:
            print(f"Error: Could not load data for player '{self.player_name}'")
            return False
            
        return True
    
    def get_cash_balance(self):
        """
        Get the player's current cash balance.
        
        Returns:
            int: The player's cash balance, or 0 if no player data is loaded.
        """
        if not self.player_data:
            return 0
            
        return self.player_data.get("cash_balance", 0)
    
    def update_cash_balance(self, new_balance):
        """
        Update the player's cash balance.
        
        Args:
            new_balance (int): The new cash balance for the player.
            
        Returns:
            bool: True if the update was successful, False otherwise.
        """
        if not self.player_data:
            return False
            
        self.player_data["cash_balance"] = new_balance
        return True
    
    def adjust_cash_balance(self, amount):
        """
        Adjust the player's cash balance by adding or subtracting an amount.
        
        Args:
            amount (int): The amount to add (positive) or subtract (negative).
            
        Returns:
            int: The new balance after adjustment, or None if no player data is loaded.
        """
        if not self.player_data:
            return None
            
        current_balance = self.player_data.get("cash_balance", 0)
        new_balance = current_balance + amount
        
        # Ensure balance doesn't go below 0
        if new_balance < 0:
            new_balance = 0
            
        self.player_data["cash_balance"] = new_balance
        return new_balance
    
    def update_high_score(self, score):
        """
        Update the player's high score for this game if the new score is higher.
        
        Args:
            score (int): The new score to check against the current high score.
            
        Returns:
            bool: True if a new high score was set, False otherwise.
        """
        if not self.player_data:
            return False
            
        high_scores = self.player_data.get("high_scores", {})
        
        # Initialize the game entry if it doesn't exist
        if self.game_name not in high_scores:
            high_scores[self.game_name] = 0
            
        # Update if the new score is higher
        if score > high_scores.get(self.game_name, 0):
            high_scores[self.game_name] = score
            self.player_data["high_scores"] = high_scores
            return True
            
        return False
    
    def save(self):
        """
        Save the player's data back to the JSON file.
        
        Returns:
            bool: True if the save was successful, False otherwise.
        """
        if not self.player_data or not self.player_name:
            return False
            
        return save_player_data(
            self.player_name,
            self.player_data.get("cash_balance", 0),
            self.player_data.get("high_scores", {})
        )
    
    def exit_game(self, return_to_lobby=True):
        """
        Save the player's data and exit the game.
        
        Args:
            return_to_lobby (bool): If True, returns to the Casino lobby after saving.
        
        Note:
            This method calls sys.exit() and will terminate the program.
        """
        # Save player data
        self.save()
        
        if return_to_lobby:
            # Try to find and run the Casino lobby
            lobby_paths = [
                "main.py",  # Same directory
                "../main.py",  # One level up
                "../../main.py",  # Two levels up
            ]
            
            for path in lobby_paths:
                if os.path.exists(path):
                    import subprocess
                    subprocess.run([sys.executable, path, self.player_name], check=False)
                    break
        
        # Exit the game
        sys.exit()


# Example usage in a game:
if __name__ == "__main__":
    # This is just for demonstration purposes
    player_manager = GamePlayerData("ExampleGame")
    
    if not player_manager.player_data:
        # If no player was specified in command line, you could implement
        # a player selection screen here, or just use a default
        player_manager.load_player("DefaultPlayer")
    
    print(f"Player: {player_manager.player_name}")
    print(f"Cash Balance: ${player_manager.get_cash_balance()}")
    
    # Example game logic
    print("Playing game...")
    
    # Example: Player wins $50
    new_balance = player_manager.adjust_cash_balance(50)
    print(f"New balance: ${new_balance}")
    
    # Example: Update high score
    if player_manager.update_high_score(1000):
        print("New high score!")
    
    # Save and exit
    player_manager.save()
    print("Game over, data saved.")
```


Now, let's modify the main.py file to pass the player name to the games when they're launched:

```python
# Target 1 - Pinball
if player.rect.colliderect(pg.Rect(conf.t_pos[0], conf.t_pos[1], conf.t_size, conf.t_size)):
    # Save player data before launching game
    save_player_data(player_data["player_name"], player_data["cash_balance"], player_data["high_scores"])
    pg.quit()
    # Pass player name as command line argument
    subprocess.run(conf.GAME_PINBALL + [player_data["player_name"]], check=False)
    sys.exit()

# Target 2 - Maze
if player.rect.colliderect(pg.Rect(conf.t2_pos[0], conf.t2_pos[1], conf.t2_size, conf.t2_size)):
    # Save player data before launching game
    save_player_data(player_data["player_name"], player_data["cash_balance"], player_data["high_scores"])
    pg.quit()
    # Pass player name as command line argument
    subprocess.run(conf.GAME_MAZE + [player_data["player_name"]], check=False)
    sys.exit()

# Target 3 - Lottery
if player.rect.colliderect(pg.Rect(conf.t3_pos[0], conf.t3_pos[1], conf.t3_size, conf.t3_size)):
    # Save player data before launching game
    save_player_data(player_data["player_name"], player_data["cash_balance"], player_data["high_scores"])
    pg.quit()
    # Pass player name as command line argument
    subprocess.run(conf.GAME_LOTTERY + [player_data["player_name"]], check=False)
    sys.exit()

# Target 4 - Blackjack
if player.rect.colliderect(pg.Rect(conf.t4_pos[0], conf.t4_pos[1], conf.t4_size, conf.t4_size)):
    # Save player data before launching game
    save_player_data(player_data["player_name"], player_data["cash_balance"], player_data["high_scores"])
    pg.quit()
    # Pass player name as command line argument
    subprocess.run(conf.GAME_BLACKJACK + [player_data["player_name"]], check=False)
    sys.exit()

# Target 5 - Dice game
if player.rect.colliderect(pg.Rect(conf.t5_pos[0], conf.t5_pos[1], conf.t5_size, conf.t5_size)):
    # Save player data before launching game
    save_player_data(player_data["player_name"], player_data["cash_balance"], player_data["high_scores"])
    pg.quit()
    # Pass player name as command line argument
    subprocess.run(conf.GAME_DICE + [player_data["player_name"]], check=False)
    sys.exit()

# Target 6 - Roulette
if player.rect.colliderect(pg.Rect(conf.t6_pos[0], conf.t6_pos[1], conf.t6_size, conf.t6_size)):
    # Save player data before launching game
    save_player_data(player_data["player_name"], player_data["cash_balance"], player_data["high_scores"])
    pg.quit()
    # Pass player name as command line argument
    subprocess.run(conf.GAME_ROULETTE + [player_data["player_name"]], check=False)
    sys.exit()

# Target 7 - High Scores
if player.rect.colliderect(pg.Rect(conf.t7_pos[0], conf.t7_pos[1], conf.t7_size, conf.t7_size)):
    # Save player data before launching game
    save_player_data(player_data["player_name"], player_data["cash_balance"], player_data["high_scores"])
    pg.quit()
    # Pass player name as command line argument
    subprocess.run(conf.GAME_SCORES + [player_data["player_name"]], check=False)
    sys.exit()
```


Now, let's create a simple example of how to use this module in a game:



===============================================================================================================
        ------------------------------------------------------------------------------------------------
===============================================================================================================





Here's an example of how to integrate the `player_scores.py` module into your pinball game:

```python
# ===========================
# Pinball
#
# Author: Rob Hickling -- E4491341
# 04/02/2025
# ===========================
#
# Imports
import pygame as pg
import sys
from ball import PlayerBall
from board import GameBoard
from player_scores import GamePlayerData  # Import the player data module

import conf


def main():
    # Initialize game settings
    pg.init()
    pg.display.set_caption(conf.game_name)
    screen = conf.screen
    fps = conf.clock

    # Initialize player data
    player_manager = GamePlayerData("Pinball")
    if not player_manager.player_data:
        # If no player was specified in command line, you could implement
        # a player selection screen here, or just use a default
        player_manager.load_player("DefaultPlayer")
    
    # Get starting cash balance
    starting_balance = player_manager.get_cash_balance()
    
    # Game variables
    score = 0
    game_over = False
    
    # Set up game elements
    board = GameBoard()
    ball = PlayerBall(conf.b_size, conf.pos)

    # Create a font for displaying score and balance
    font = pg.font.Font(None, 36)

    # ----------------------------------
    # Main game loop
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # Save player data before exiting
                player_manager.save()
                running = False

        # Input handling. Update flippers
        board.key_input()

        # Update the board.
        board.update_board()

        # Set screen fill
        screen.fill(pg.Color("gray12"))

        # Draw items on the screen
        board.draw_background(screen)
        board.draw_flippers(screen)
        ball.draw(screen)

        # Update the ball position and get points earned this frame
        points_earned = ball.update_position(board, [board.left_flipper, board.right_flipper])
        
        # Update score if points were earned
        if points_earned > 0:
            score += points_earned
            
        # Check if ball is lost
        if ball.is_lost():
            if not game_over:
                game_over = True
                # Update player's high score if applicable
                player_manager.update_high_score(score)
                
                # Award cash based on score (example: 1 cash per 100 points)
                cash_award = score // 100
                player_manager.adjust_cash_balance(cash_award)
                
                # Save player data
                player_manager.save()
                
                # Wait 3 seconds before returning to lobby
                pg.time.delay(3000)
                running = False
                player_manager.exit_game(return_to_lobby=True)
            
        # Display player info, score and balance
        player_text = font.render(f"Player: {player_manager.player_name}", True, (255, 255, 255))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        balance_text = font.render(f"Balance: ${starting_balance}", True, (255, 255, 255))
        
        screen.blit(player_text, (10, 10))
        screen.blit(score_text, (10, 50))
        screen.blit(balance_text, (10, 90))
        
        # If game is over, display game over message
        if game_over:
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            cash_award_text = font.render(f"Cash Award: ${cash_award}", True, (0, 255, 0))
            new_balance_text = font.render(f"New Balance: ${player_manager.get_cash_balance()}", True, (0, 255, 0))
            
            # Center the text on screen
            screen.blit(game_over_text, (conf.screen.get_width() // 2 - game_over_text.get_width() // 2, 
                                         conf.screen.get_height() // 2 - 60))
            screen.blit(cash_award_text, (conf.screen.get_width() // 2 - cash_award_text.get_width() // 2, 
                                         conf.screen.get_height() // 2))
            screen.blit(new_balance_text, (conf.screen.get_width() // 2 - new_balance_text.get_width() // 2, 
                                         conf.screen.get_height() // 2 + 60))

        # Refresh display
        pg.display.flip()
        fps.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()
```


```python
# This is a partial implementation showing the key changes needed to the ball class
# You would need to integrate this with your existing ball.py file

class PlayerBall:
    def __init__(self, size, pos):
        # Existing initialization code...
        self.size = size
        self.pos = pos
        self.velocity = [0, 0]
        self.lost = False
        # Add score tracking
        self.points_earned = 0
        
    def is_lost(self):
        """Check if the ball is lost (fell off the bottom of the screen)"""
        return self.lost
        
    def update_position(self, board, flippers):
        """
        Update the ball's position based on physics and collisions.
        Returns the points earned during this update.
        """
        # Reset points earned for this frame
        self.points_earned = 0
        
        # Existing physics and collision code...
        
        # Example: Check for collisions with scoring elements
        # This is just an example - implement according to your game's design
        for bumper in board.bumpers:
            if self.check_collision(bumper):
                # Award points for bumper hit
                self.points_earned += 10
                
        for target in board.targets:
            if self.check_collision(target):
                # Award points for target hit
                self.points_earned += 25
                
        # Check if ball fell off the bottom
        if self.pos[1] > board.height:
            self.lost = True
            
        # Return points earned during this update
        return self.points_earned
        
    def check_collision(self, game_object):
        """Check if the ball collides with a game object"""
        # Implement collision detection logic
        # This is just a placeholder - implement according to your game's design
        return False
        
    def draw(self, screen):
        # Existing drawing code...
        pass
```


```python
# ===========================
# Maze Game
#
# Author: Rob Hickling
# ===========================
#
# Imports
import pygame as pg
import sys
import subprocess
from player import Player
from ui import Ui
from player_scores import GamePlayerData  # Import the player data module

import conf

def main():
    # Initialize Pygame - Set window name and size
    pg.init()
    pg.display.set_caption(conf.GAME_NAME)
    screen = pg.display.set_mode(conf.WINDOW_SIZE)

    # Initialize player data
    player_manager = GamePlayerData("Maze")
    if not player_manager.player_data:
        # If no player was specified in command line, you could implement
        # a player selection screen here, or just use a default
        player_manager.load_player("DefaultPlayer")
    
    # Get starting cash balance
    starting_balance = player_manager.get_cash_balance()
    
    # Game variables
    score = 0
    time_remaining = 60  # 60 seconds to complete the maze
    start_time = pg.time.get_ticks()
    game_over = False
    game_won = False

    # Initialize game elements
    player = Player(conf.p_pos[0], conf.p_pos[1])
    ui = Ui()

    # Create a font for displaying score and balance
    font = pg.font.Font(None, 36)

    # ----------------------------------
    # Main game loop
    running = True
    while running:
        # Limit FPS to 60
        conf.CLOCK.tick(60)
        dt = conf.CLOCK.tick(30) / 1000

        # Calculate time remaining
        if not game_over:
            elapsed_time = (pg.time.get_ticks() - start_time) // 1000
            time_remaining = max(0, 60 - elapsed_time)
            
            # Check if time ran out
            if time_remaining <= 0 and not game_over:
                game_over = True
                # No reward for running out of time
                player_manager.save()
                
                # Wait 3 seconds before returning to lobby
                pg.time.delay(3000)
                player_manager.exit_game(return_to_lobby=True)

        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # Save player data before exiting
                player_manager.save()
                pg.quit()
                sys.exit()

        # Fill the screen with the background color
        screen.fill((90, 30, 105))

        # Print Background image
        screen.blit(conf.FLOOR_IMG, (0, 0))
        screen.blit(conf.BG_IMG, (0, 0))

        # Draw UI elements
        ui.draw_ui(screen)

        # Draw player on screen
        player.draw(screen)

        # Update Player if game is not over
        if not game_over:
            player.update(dt)

        # ----------------------------------
        # Draw the exit
        pg.draw.rect(
            screen,
            conf.t_colour,
            (conf.t_pos[0], conf.t_pos[1], conf.t_size, conf.t_size),
        )

        # ----------------------------------
        # Check if player reached the exit
        if player.rect.colliderect(pg.Rect(conf.t_pos[0], conf.t_pos[1], conf.t_size, conf.t_size)):
            if not game_over:
                game_over = True
                game_won = True
                
                # Calculate score based on time remaining
                score = time_remaining * 10
                
                # Update player's high score if applicable
                player_manager.update_high_score(score)
                
                # Award cash based on score (example: 1 cash per 10 points)
                cash_award = score // 10
                player_manager.adjust_cash_balance(cash_award)
                
                # Save player data
                player_manager.save()
                
                # Wait 3 seconds before returning to lobby
                pg.time.delay(3000)
                running = False
                player_manager.exit_game(return_to_lobby=True)

        # Display player info, score, time and balance
        player_text = font.render(f"Player: {player_manager.player_name}", True, (255, 255, 255))
        time_text = font.render(f"Time: {time_remaining}s", True, (255, 255, 255))
        balance_text = font.render(f"Balance: ${starting_balance}", True, (255, 255, 255))
        
        screen.blit(player_text, (10, 10))
        screen.blit(time_text, (10, 50))
        screen.blit(balance_text, (10, 90))
        
        # If game is over, display game over message
        if game_over:
            if game_won:
                game_over_text = font.render("MAZE COMPLETED!", True, (0, 255, 0))
                score_text = font.render(f"Score: {score}", True, (255, 255, 255))
                cash_award_text = font.render(f"Cash Award: ${cash_award}", True, (0, 255, 0))
                new_balance_text = font.render(f"New Balance: ${player_manager.get_cash_balance()}", True, (0, 255, 0))
            else:
                game_over_text = font.render("TIME'S UP!", True, (255, 0, 0))
                score_text = font.render(f"Score: 0", True, (255, 255, 255))
                cash_award_text = font.render(f"Cash Award: $0", True, (255, 0, 0))
                new_balance_text = font.render(f"Balance: ${player_manager.get_cash_balance()}", True, (255, 255, 255))
            
            # Center the text on screen
            screen.blit(game_over_text, (conf.WINDOW_SIZE[0] // 2 - game_over_text.get_width() // 2, 
                                         conf.WINDOW_SIZE[1] // 2 - 90))
            screen.blit(score_text, (conf.WINDOW_SIZE[0] // 2 - score_text.get_width() // 2, 
                                     conf.WINDOW_SIZE[1] // 2 - 30))
            screen.blit(cash_award_text, (conf.WINDOW_SIZE[0] // 2 - cash_award_text.get_width() // 2, 
                                         conf.WINDOW_SIZE[1] // 2 + 30))
            screen.blit(new_balance_text, (conf.WINDOW_SIZE[0] // 2 - new_balance_text.get_width() // 2, 
                                         conf.WINDOW_SIZE[1] // 2 + 90))

        # Update the display
        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()
```


These examples demonstrate how to integrate the `player_scores.py` module into your existing games. Here's a breakdown of the key integration points:

### 1. Import and Initialize
```python
from player_scores import GamePlayerData  # Import the player data module

# Initialize player data
player_manager = GamePlayerData("GameName")
if not player_manager.player_data:
    player_manager.load_player("DefaultPlayer")

# Get starting cash balance
starting_balance = player_manager.get_cash_balance()
```

### 2. Track Score During Gameplay
In the pinball example, we track points earned during ball movement:
```python
# Update score if points were earned
if points_earned > 0:
    score += points_earned
```

In the maze example, we calculate score based on time remaining:
```python
# Calculate score based on time remaining
score = time_remaining * 10
```

### 3. Update Player Data When Game Ends
```python
# Update player's high score if applicable
