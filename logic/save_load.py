# ===========================
# Python game suite
#
# Casino Lobby
# ===========================
#
# Main Imports
import datetime
import json


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

    with open("data/players_data.json", "w") as f:
        json.dump(all_players, f, indent=4)


def load_high_scores():
    """Load and return sorted list of players by high score"""
    all_players = load_all_players()
    players = [p for p in all_players.values() if p is not None]

    # Sort by high score (cash) in descending order
    sorted_players = sorted(players, key=lambda x: x["high_scores"]["cash"], reverse=True)

    return sorted_players


def load_player_data(player_name):
    """Load specific player data from the JSON file"""
    all_players = load_all_players()

    # Return the requested player data if it exists
    if player_name in all_players:
        return all_players[player_name]

    return None


def load_all_players():
    """Load all players data from the JSON file"""
    try:
        with open("data/players_data.json") as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        # Return empty dict if file doesn't exist or is invalid
        return {}


def get_player_names():
    """Get a list of all saved player names"""
    all_players = load_all_players()
    return list(all_players.keys())


def get_players_display_data():
    """Get a list of player data for display in the UI"""
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


def delete_player(player_name):
    """
    Delete a player from the saved data
    """
    all_players = load_all_players()

    if player_name in all_players:
        del all_players[player_name]

        # Save the updated players data
        with open("data/players_data.json", "w") as f:
            json.dump(all_players, f, indent=4)

        return True

    return False
