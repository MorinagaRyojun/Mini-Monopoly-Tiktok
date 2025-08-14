# monopoly/command_parser.py
import re

def parse_command(message, player_name, game_state):
    """
    Parses a chat message to identify a game command.
    """
    message = message.lower().strip()
    # Basic command cleaning
    message = re.sub(r'[^\w! ]', '', message) # Remove emojis/symbols

    if message == '!join' and game_state == "WAITING":
        return {"command": "join", "player": player_name}

    if message == '!start' and game_state == "WAITING":
        return {"command": "start", "player": player_name}

    if message == '!roll' and game_state == "IN_PROGRESS":
        return {"command": "roll", "player": player_name}

    if message == '!buy' and game_state == "IN_PROGRESS":
        return {"command": "buy", "player": player_name}

    if message == '!pass' and game_state == "IN_PROGRESS":
        return {"command": "pass", "player": player_name}

    if message == '!status':
        return {"command": "status", "player": player_name}

    if message == '!board':
        return {"command": "board", "player": player_name}

    return None # No valid command found
