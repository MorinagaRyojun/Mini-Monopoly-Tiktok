# monopoly/game.py
import random
from player import Player
from board import Board, Property

class Game:
    def __init__(self, config):
        self.board = Board(config.get('BOARD_SIZE', 12))
        self.players = []
        self.current_turn_index = 0
        self.game_state = "WAITING"  # WAITING, IN_PROGRESS, FINISHED
        self.config = config
        self.player_map = {} # For quick lookup
        self.pending_action = None # To handle buy/pass decisions

    def start_game(self):
        min_players = self.config.get('MIN_PLAYERS', 2)
        if len(self.players) >= min_players:
            self.game_state = "IN_PROGRESS"
            random.shuffle(self.players)
            player_order = ", ".join([p.name for p in self.players])
            print(f"The game has started! Player order: {player_order}")
            print(f"It's {self.get_current_player().name}'s turn.")
            return True
        else:
            print(f"Need at least {min_players} players to start.")
            return False

    def add_player(self, player_name):
        if self.game_state != "WAITING":
            print("Cannot join a game that is already in progress.")
            return False

        if player_name in self.player_map:
            print(f"Player {player_name} is already in the game.")
            return False

        max_players = self.config.get('MAX_PLAYERS', 8)
        if len(self.players) >= max_players:
            print(f"The game is full. Cannot add more than {max_players} players.")
            return False

        new_player = Player(player_name, self.config.get('STARTING_MONEY', 1500))
        self.players.append(new_player)
        self.player_map[player_name] = new_player
        print(f"Player {player_name} has joined the game. Total players: {len(self.players)}")
        return True

    def next_turn(self):
        self.current_turn_index = (self.current_turn_index + 1) % len(self.players)

    def get_current_player(self):
        if not self.players:
            return None
        return self.players[self.current_turn_index]

    def _end_turn(self):
        self.next_turn()
        next_player = self.get_current_player()
        print(f"\nIt's now {next_player.name}'s turn.")

    def handle_roll(self, player_name):
        if self.game_state != "IN_PROGRESS":
            print("The game has not started yet.")
            return

        if self.pending_action:
            print(f"There is a pending action for {self.pending_action['player'].name}. Please resolve it with !buy or !pass.")
            return

        current_player = self.get_current_player()
        if not current_player or current_player.name != player_name:
            print(f"It's not your turn, {player_name}. It's {current_player.name}'s turn.")
            return

        # Roll the dice
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total_roll = die1 + die2
        print(f"{current_player.name} rolled a {die1} + {die2} = {total_roll}.")

        # Move the player
        passed_go = current_player.move(total_roll, self.board.size)
        if passed_go:
            go_money = self.config.get('PASS_GO_MONEY', 200)
            current_player.receive(go_money)
            print(f"{current_player.name} passed GO and collected ${go_money}.")

        # Announce new position and resolve the space action
        new_space = self.board.get_space(current_player.position)
        print(f"{current_player.name} landed on {new_space.name}.")

        self.resolve_space_action(current_player, new_space)

        # If no pending action, the turn ends automatically
        if not self.pending_action:
            print(f"Status: {current_player.get_status()}")
            self._end_turn()

    def resolve_space_action(self, player, space):
        space_type = space.space_type

        if space_type == "PROPERTY":
            if space.owner is None:
                print(f"This property is unowned. You can buy it for ${space.price}.")
                print(f"Type '{player.name}:!buy' to purchase or '{player.name}:!pass' to skip.")
                self.pending_action = {"player": player, "action": "buy_or_pass", "space": space}
            elif space.owner == player:
                print("You landed on your own property. No rent needed.")
            else:
                owner = space.owner
                rent = space.rent

                # Check for color set bonus
                color_set = self.board.color_map.get(space.color)
                if color_set and owner.owns_all_properties_in_set(color_set):
                    rent *= 2
                    print(f"!!! {owner.name} owns all {space.color} properties. Rent is DOUBLED!")

                print(f"This property is owned by {owner.name}. You owe ${rent} in rent.")
                if player.pay(rent):
                    owner.receive(rent)
                    print(f"{player.name} paid ${rent} to {owner.name}.")
                else:
                    self._handle_bankruptcy(player)

        elif space_type == "TAX":
            tax_amount = self.config.get('TAX_AMOUNT', 100)
            print(f"You landed on a Tax space. You must pay ${tax_amount}.")
            if not player.pay(tax_amount):
                self._handle_bankruptcy(player)

        elif space_type == "FREE_PARKING":
            bonus = self.config.get('FREE_PARKING_BONUS', 50)
            print(f"You landed on Free Parking! You collect a bonus of ${bonus}.")
            player.receive(bonus)

        elif space_type == "CHANCE":
            outcome = random.choice([-50, -20, 20, 50, 100])
            if outcome > 0:
                print(f"Chance! You found ${outcome}.")
                player.receive(outcome)
            else:
                print(f"Chance! You lost ${abs(outcome)}.")
                if not player.pay(abs(outcome)):
                    self._handle_bankruptcy(player)

        # Other spaces like GO, JAIL have no direct landing action
        else:
            print(f"Landed on {space.name}. No special action.")

    def handle_buy(self, player_name):
        if not self.pending_action or self.pending_action["action"] != "buy_or_pass":
            print("There is nothing to buy right now.")
            return

        player = self.get_current_player()
        if player.name != player_name:
            print(f"It is not your turn to buy, {player_name}.")
            return

        space_to_buy = self.pending_action["space"]
        if player.buy_property(space_to_buy):
            print(f"{player.name} has bought {space_to_buy.name} for ${space_to_buy.price}!")
        else:
            print(f"{player.name} does not have enough money to buy {space_to_buy.name}.")

        self.pending_action = None
        print(f"Status: {player.get_status()}")
        self._end_turn()

    def handle_pass(self, player_name):
        if not self.pending_action or self.pending_action["action"] != "buy_or_pass":
            print("There is nothing to pass on right now.")
            return

        player = self.get_current_player()
        if player.name != player_name:
            print(f"It is not your turn to pass, {player_name}.")
            return

        print(f"{player.name} decided not to buy the property.")
        self.pending_action = None
        self._end_turn()

    def handle_status(self, player_name):
        if player_name in self.player_map:
            player = self.player_map[player_name]
            print(player.get_status())
        else:
            print(f"Player {player_name} not found in the game.")

    def handle_board(self):
        print("--- Current Board State ---")
        print(self.board.display())
        print("-------------------------")

    def _check_game_over(self):
        if len(self.players) == 1:
            self.game_state = "FINISHED"
            winner = self.players[0]
            print(f"\n--- GAME OVER ---")
            print(f"The winner is {winner.name}!")
            print(f"Final status: {winner.get_status()}")
            return True
        return False

    def _handle_bankruptcy(self, player):
        print(f"--- {player.name} is bankrupt! ---")

        # Release properties
        for prop in player.properties:
            prop.owner = None
        print(f"All properties of {player.name} are now back on the market.")

        # Remove player from game
        del self.player_map[player.name]

        # Important: find the index of the bankrupt player BEFORE removing them
        bankrupt_player_index = self.players.index(player)
        self.players.remove(player)

        # Adjust turn index if necessary
        if self.current_turn_index > bankrupt_player_index:
            self.current_turn_index -= 1
        # If the bankrupt player was the last in the list, the index might become out of bounds after wrapping
        if self.current_turn_index >= len(self.players):
            self.current_turn_index = 0

        # Check for a winner
        if not self._check_game_over():
             # If the game is not over, make sure the turn moves to the correct next player
             # The _end_turn() logic might not be called if bankruptcy happens mid-turn
             # so we ensure the next player is announced.
             # We set the turn index back by one, so the next call to next_turn() will land on the correct player
             self.current_turn_index = (self.current_turn_index - 1 + len(self.players)) % len(self.players)
