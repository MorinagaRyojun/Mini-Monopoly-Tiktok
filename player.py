# monopoly/player.py

class Player:
    def __init__(self, name, start_money):
        self.name = name
        self.money = start_money
        self.properties = []
        self.position = 0
        self.is_in_jail = False
        self.jail_turns = 0
        self.is_bankrupt = False

    def move(self, steps, board_size):
        old_position = self.position
        self.position = (self.position + steps) % board_size

        # Player passes GO if their new position is a smaller number than their old one
        # (unless they went backwards, which is not a feature yet)
        passed_go = self.position < old_position
        return passed_go

    def pay(self, amount):
        if self.money >= amount:
            self.money -= amount
            return True
        else:
            # Not enough money, this player is now bankrupt
            self.money = 0
            self.is_bankrupt = True
            return False

    def receive(self, amount):
        self.money += amount

    def buy_property(self, property_obj):
        if self.pay(property_obj.price):
            self.properties.append(property_obj)
            property_obj.owner = self
            return True
        return False

    def get_status(self):
        prop_names = [p.name for p in self.properties]
        return f"Player: {self.name}, Money: ${self.money}, Properties: {', '.join(prop_names) or 'None'}"

    def owns_all_properties_in_set(self, property_set):
        """Checks if the player owns all properties in a given set (list of properties)."""
        return all(prop in self.properties for prop in property_set)
