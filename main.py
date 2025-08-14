"""
Mini Monopoly for TikTok Live

This is the main entry point for the game.
"""
from game import Game
from command_parser import parse_command
from config import SETTINGS

def main():
    print("--- Welcome to Mini Monopoly for TikTok Live! ---")
    print("Game is in WAITING state. Players can !join.")
    print("Commands: <user>:!join, <user>:!start, <user>:!roll, <user>:!buy, <user>:!pass, <user>:!status, !players, !board, !exit")

    game = Game(SETTINGS)

    while True:
        if game.game_state == "FINISHED":
            print("The game has ended. Thanks for playing!")
            break

        raw_input = input("> ")

        if raw_input.lower() == '!exit':
            print("Exiting game.")
            break

        if raw_input.lower() == '!players':
            if not game.players:
                print("No players have joined yet.")
            else:
                player_names = [p.name for p in game.players]
                print(f"Players: {', '.join(player_names)}")
            continue

        if raw_input.lower() == '!board':
            game.handle_board()
            continue

        try:
            player_name, message = raw_input.split(":", 1)
        except ValueError:
            print("Invalid input format. Please use 'username:!command'.")
            continue

        command = parse_command(message, player_name, game.game_state)

        if not command:
            print(f"Invalid command or command not allowed in current state: {message}")
            continue

        cmd = command.get("command")
        player = command.get("player")

        if cmd == "join":
            game.add_player(player)
        elif cmd == "start":
            game.start_game()
        elif cmd == "roll":
            game.handle_roll(player)
        elif cmd == "buy":
            game.handle_buy(player)
        elif cmd == "pass":
            game.handle_pass(player)
        elif cmd == "status":
            game.handle_status(player)
        else:
            print(f"Command '{cmd}' is recognized but not handled in main loop yet.")


if __name__ == "__main__":
    main()
