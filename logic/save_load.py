# ===========================
# Python game suite
#
# Casino Lobby
# ===========================
#
# Main Imports
import datetime
import json

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
        with open("data/players_database.json") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return empty dict if file doesn't exist or is invalid
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
    cash_balance = cash_balance or 0

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
    if cash_balance > high_scores["cash"]:
        high_scores["cash"] = cash_balance

    # Keep only top 20 players
    if len(all_players) > 20:
        sorted_players = sorted(
            all_players.items(), key=lambda x: datetime.datetime.strptime(x[1]["last_played"], "%Y-%m-%d %H:%M:%S")
        )
        del all_players[sorted_players[0][0]]

    # Save to main data file
    with open("data/players_database.json", "w") as f:
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
        with open("data/players_database.json", "w") as f:
            json.dump(all_players, f, indent=4)

        return True

    return False


def load_all_high_scores():
    """
    Load and sort list of players by high score
    """
    # Variables
    all_players = load_all_players()
    players = [p for p in all_players.values() if p is not None]

    sorted_players = sorted(players, key=get_cash_score, reverse=True)

    return sorted_players


# -------------------------------------------------------------------------
