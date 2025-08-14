import random
from player import Player
from board import Board, Property

class Game:
    def __init__(self, config, game_options=None):
        self.config = config
        self.game_options = game_options if game_options else {}

        board_size = self.game_options.get("board_size", 12)
        image_urls = self.game_options.get("image_urls", {})

        self.board = Board(num_spaces=board_size, image_urls=image_urls)
        self.players = []
        self.current_turn_index = 0
        self.game_state = "WAITING"
        self.player_map = {}
        self.pending_action = None
        self.log = [f"Game created with a {board_size}-space board. Waiting for players to join."]

    def _add_log(self, message):
        self.log.append(message)

    def get_and_clear_log(self):
        log_copy = self.log[:]
        self.log = []
        return log_copy

    def get_state(self):
        """Returns the entire game state as a dictionary."""
        safe_pending_action = None
        if self.pending_action:
            safe_pending_action = self.pending_action

        board_state = []
        for space in self.board.spaces:
            space_dict = {
                "name": space.name,
                "type": space.space_type,
                "image_url": space.image_url
            }
            if isinstance(space, Property):
                space_dict.update({
                    "color": space.color,
                    "price": space.price,
                    "rent": space.rent,
                    "owner": space.owner.name if space.owner else None
                })
            board_state.append(space_dict)

        return {
            "gameState": self.game_state,
            "players": [p.get_state() for p in self.players],
            "board": board_state,
            "currentPlayerName": self.get_current_player().name if self.game_state == "IN_PROGRESS" and self.get_current_player() else None,
            "pendingAction": safe_pending_action,
            "log": self.log
        }

    def run_command(self, command, player_name, args=None):
        # ... (rest of the command handling logic remains the same)
        if command == "join": self._add_player(player_name)
        elif command == "start": self._start_game()
        elif command == "roll": self._handle_roll(player_name)
        elif command == "buy": self._handle_buy(player_name)
        elif command == "pass": self._handle_pass(player_name)
        elif command == "status": self._handle_status(player_name)
        else: self._add_log(f"Unknown command: {command}")

    def _start_game(self):
        min_players = self.config.get('MIN_PLAYERS', 2)
        if len(self.players) >= min_players:
            self.game_state = "IN_PROGRESS"
            random.shuffle(self.players)
            player_order = ", ".join([p.name for p in self.players])
            self._add_log(f"The game has started! Player order: {player_order}")
            self._add_log(f"It's {self.get_current_player().name}'s turn.")
        else:
            self._add_log(f"Need at least {min_players} players to start.")

    def _add_player(self, player_name):
        if self.game_state != "WAITING":
            self._add_log("Cannot join a game that is already in progress.")
            return
        if player_name in self.player_map:
            self._add_log(f"Player {player_name} is already in the game.")
            return
        max_players = self.config.get('MAX_PLAYERS', 8)
        if len(self.players) >= max_players:
            self._add_log(f"The game is full. Cannot add more than {max_players} players.")
            return
        new_player = Player(player_name, self.config.get('STARTING_MONEY', 1500))
        self.players.append(new_player)
        self.player_map[player_name] = new_player
        self._add_log(f"Player {player_name} has joined the game. Total players: {len(self.players)}")

    def next_turn(self):
        if not self.players:
            self.game_state = "FINISHED"
            return
        self.current_turn_index = (self.current_turn_index + 1) % len(self.players)

    def get_current_player(self):
        if not self.players:
            return None
        return self.players[self.current_turn_index]

    def _end_turn(self):
        self.next_turn()
        if self.game_state != "FINISHED":
            next_player = self.get_current_player()
            self._add_log(f"\nIt's now {next_player.name}'s turn.")

    def _handle_roll(self, player_name):
        if self.game_state != "IN_PROGRESS":
            self._add_log("The game has not started yet."); return
        if self.pending_action:
            self._add_log(f"There is a pending action for {self.pending_action['player']}. Please resolve it with !buy or !pass."); return
        current_player = self.get_current_player()
        if not current_player or current_player.name != player_name:
            self._add_log(f"It's not your turn, {player_name}. It's {current_player.name}'s turn."); return
        die1 = random.randint(1, 6); die2 = random.randint(1, 6)
        total_roll = die1 + die2
        self._add_log(f"{current_player.name} rolled a {die1} + {die2} = {total_roll}.")
        if current_player.move(total_roll, self.board.size):
            go_money = self.config.get('PASS_GO_MONEY', 200)
            current_player.receive(go_money)
            self._add_log(f"{current_player.name} passed GO and collected ${go_money}.")
        new_space = self.board.get_space(current_player.position)
        self._add_log(f"{current_player.name} landed on {new_space.name}.")
        self._resolve_space_action(current_player, new_space)
        if not self.pending_action:
            state = current_player.get_state()
            self._add_log(f"Status: Player: {state['name']}, Money: ${state['money']}, Properties: {len(state['properties'])}")
            self._end_turn()

    def _resolve_space_action(self, player, space):
        space_type = space.space_type
        if space_type == "GO_TO_JAIL":
            self._add_log(f"Oh no! {player.name} is sent to Jail!")
            player.position = self.board.jail_pos
            # Add actual jail logic later if needed (e.g., skipping turns)
        elif space_type == "PROPERTY":
            if space.owner is None:
                self._add_log(f"This property is unowned. You can buy it for ${space.price}.")
                self._add_log(f"Type '{player.name}:!buy' or '{player.name}:!pass'.")
                self.pending_action = {"player": player.name, "action": "buy_or_pass", "space_pos": player.position}
            elif space.owner != player:
                owner = space.owner
                rent = space.rent
                color_set = self.board.color_map.get(space.color)
                if color_set and owner.owns_all_properties_in_set(color_set):
                    rent *= 2
                    self._add_log(f"!!! {owner.name} owns all {space.color} properties. Rent is DOUBLED!")
                self._add_log(f"This property is owned by {owner.name}. You owe ${rent} in rent.")
                if not player.pay(rent): self._handle_bankruptcy(player)
                else: owner.receive(rent); self._add_log(f"{player.name} paid ${rent} to {owner.name}.")
        elif space_type == "TAX":
            tax_amount = self.config.get('TAX_AMOUNT', 100)
            self._add_log(f"You landed on a Tax space. You must pay ${tax_amount}.")
            if not player.pay(tax_amount): self._handle_bankruptcy(player)
        elif space_type == "FREE_PARKING":
            bonus = self.config.get('FREE_PARKING_BONUS', 50)
            self._add_log(f"You landed on Free Parking! You collect a bonus of ${bonus}.")
            player.receive(bonus)
        elif space_type == "CHANCE":
            outcome = random.choice([-50, 20, 50, 100])
            if outcome > 0: self._add_log(f"Chance! You found ${outcome}."); player.receive(outcome)
            else: self._add_log(f"Chance! You lost ${abs(outcome)}.");
            if not player.pay(abs(outcome)): self._handle_bankruptcy(player)
        else:
            self._add_log(f"Landed on {space.name}. No special action.")

    def _handle_buy(self, player_name):
        if not self.pending_action or self.pending_action["player"] != player_name:
            self._add_log("It's not your turn to buy."); return
        player = self.player_map[player_name]
        space_to_buy = self.board.get_space(self.pending_action["space_pos"])
        if player.buy_property(space_to_buy):
            self._add_log(f"{player.name} has bought {space_to_buy.name} for ${space_to_buy.price}!")
        else:
            self._add_log(f"{player.name} does not have enough money.")
        self.pending_action = None
        state = player.get_state()
        self._add_log(f"Status: Player: {state['name']}, Money: ${state['money']}")
        self._end_turn()

    def _handle_pass(self, player_name):
        if not self.pending_action or self.pending_action["player"] != player_name:
            self._add_log("It's not your turn to pass."); return
        self._add_log(f"{player_name} decided not to buy the property.")
        self.pending_action = None
        self._end_turn()

    def _handle_status(self, player_name):
        if player_name in self.player_map:
            player = self.player_map[player_name]
            state = player.get_state()
            prop_list = ', '.join(state['properties']) or 'None'
            self._add_log(f"Status for {state['name']}: Money: ${state['money']}, Properties: {prop_list}")
        else:
            self._add_log(f"Player {player_name} not found in the game.")

    def _check_game_over(self):
        if len(self.players) <= 1:
            self.game_state = "FINISHED"
            if self.players:
                winner = self.players[0]
                state = winner.get_state()
                self._add_log(f"\n--- GAME OVER ---")
                self._add_log(f"The winner is {state['name']}!")
            else:
                self._add_log(f"\n--- GAME OVER ---")
                self._add_log("All players went bankrupt!")
            return True
        return False

    def _handle_bankruptcy(self, player):
        self._add_log(f"--- {player.name} is bankrupt! ---")
        for prop in player.properties: prop.owner = None
        self._add_log(f"All properties of {player.name} are now back on the market.")
        del self.player_map[player.name]
        bankrupt_player_index = self.players.index(player)
        self.players.remove(player)
        if not self.players: self._check_game_over(); return
        if self.current_turn_index > bankrupt_player_index: self.current_turn_index -= 1
        if self.current_turn_index >= len(self.players): self.current_turn_index = 0
        if not self._check_game_over():
             self.current_turn_index = (self.current_turn_index - 1 + len(self.players)) % len(self.players)
