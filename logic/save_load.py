# ===========================
# Python game suite
#
# Casino Lobby
# ===========================
#
# Main Imports
import datetime
import json
import os

# For game_integration
# Platform agnostic temp file
casino_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
USR_FILE = os.path.join(casino_root, "data", "players_database.json")

# -------------------------------------------------------------------------
# Utilities
#


def get_cash_score(player):
    """
    Return the High score of a player
    """
    return player["high_scores"]["cash"]


def load_all_players():
    """
    Load all players data from the JSON file
    """
    try:
        with open(USR_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return empty dict if file doesn't exist or is corrupted
        return {}


# -------------------------------------------------------------------------
# Helpers
#


def get_players_display_data():
    """
    Get a list of player data for display in the UI
    """
    all_players = load_all_players()
    display_data = []

    for name, data in all_players.items():
        # Create a display entry with name, cash balance, and last played date
        display_data.append(
            {
                "name": name,
                "cash_balance": data.get("cash_balance", 0),
                "last_played": data.get("last_played", "Unknown"),
            }
        )

    # Sort by most recently played
    display_data.sort(key=lambda x: x["last_played"], reverse=True)

    return display_data


# -------------------------------------------------------------------------
# Main Functions
#


def save_player_data(player_name, cash_balance, high_scores=None):
    """
    Save player data to a JSON file
    Assigned defaults if no data
    Update high score if applicable
    Limit the number of entries in the DB
    """

    # Initialize some things with defaults
    high_scores = high_scores or {"cash": 0}
    # Convert cash balance to integer if it's a string
    cash_balance = int(cash_balance) if cash_balance else 0

    # Variables
    all_players = load_all_players()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_players[player_name] = {
        "player_name": player_name,
        "cash_balance": cash_balance,
        "high_scores": high_scores,
        "last_played": current_time,
    }

    # Update high score if current balance is higher
    # Ensure we're comparing integers
    high_scores_cash = int(high_scores["cash"])
    if cash_balance > high_scores_cash:
        high_scores["cash"] = cash_balance

    # Keep only top 20 players
    if len(all_players) > 20:
        sorted_players = sorted(
            all_players.items(),
            key=lambda x: datetime.datetime.strptime(
                x[1]["last_played"], "%Y-%m-%d %H:%M:%S"
            ),
        )
        del all_players[sorted_players[0][0]]

    # Save to main data file
    with open(USR_FILE, "w") as f:
        json.dump(all_players, f, indent=4)


def load_player_data(player_name):
    """
    Load specific players data from the JSON file
    """
    all_players = load_all_players()

    # Return the requested player data if it exists
    if player_name in all_players:
        return all_players[player_name]

    return None


def delete_player(player_name):
    """
    Delete a player from the saved data
    """
    all_players = load_all_players()

    if player_name in all_players:
        del all_players[player_name]

        # Save the updated players data
        with open(USR_FILE, "w") as f:
            json.dump(all_players, f, indent=4)

        return True

    return False


def load_all_high_scores():
    """
    Load and sort list of players by high score
    """
    try:
        # Load all players data
        all_players = load_all_players()

        # If no players exist, return empty list
        if not all_players:
            return []

        # Extract valid players with high scores
        players = []
        for player_data in all_players.items():
            if player_data is not None and "high_scores" in player_data:
                players.append(player_data)

        # Sort by cash high score
        sorted_players = sorted(players, key=get_cash_score, reverse=True)

        return sorted_players
    except Exception:
        # Return empty list if any error occurs
        return []


# -------------------------------------------------------------------------
