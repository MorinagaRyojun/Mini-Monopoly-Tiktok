from flask import Flask, render_template, jsonify, request
from game import Game
from config import SETTINGS
from command_parser import parse_command

app = Flask(__name__)

# Create a single, global game instance
game_instance = Game(config=SETTINGS)

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/setup')
def setup():
    """Serves the setup page."""
    return render_template('setup.html')

@app.route('/api/game_state')
def game_state():
    """Provides the full game state as JSON."""
    return jsonify(game_instance.get_state())

@app.route('/api/command', methods=['POST'])
def handle_command():
    """Receives and processes a command from the client."""
    print("--- Received a command! ---") # For debugging
    data = request.get_json()
    if not data or 'message' not in data or 'player' not in data:
        return jsonify({"error": "Invalid command format"}), 400

    player_name = data['player']
    message = data['message']

    # Use the existing command parser
    command_data = parse_command(message, player_name, game_instance.game_state)

    if command_data:
        command = command_data.get("command")
        # The game engine's run_command is the new entry point
        game_instance.run_command(command, player_name)
    else:
        game_instance._add_log(f"Invalid command or not allowed in current state: '{message}'")

    # Return the updated game state
    return jsonify(game_instance.get_state())

@app.route('/api/new_game', methods=['POST'])
def new_game():
    """Creates a new game instance, resetting the server state."""
    global game_instance
    options = request.get_json()

    # Basic validation
    board_size = int(options.get("board_size", 12))
    image_urls = options.get("image_urls", {})

    game_options = {
        "board_size": board_size,
        "image_urls": image_urls
    }

    print(f"--- Creating new game with options: {game_options} ---")
    game_instance = Game(config=SETTINGS, game_options=game_options)

    return jsonify(game_instance.get_state())

if __name__ == '__main__':
    # The game is already initialized when the app starts.
    # The server runs in a single thread, so we don't have to worry about race conditions
    # for this simple implementation.
    app.run(debug=True, port=5002)
