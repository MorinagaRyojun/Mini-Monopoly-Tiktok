# monopoly/board.py
import random

class Space:
    def __init__(self, name, space_type):
        self.name = name
        self.space_type = space_type # e.g., "PROPERTY", "CHANCE", "TAX", "GO"

    def __str__(self):
        return f"[{self.name}]"

class Property(Space):
    def __init__(self, name, color, price, rent):
        super().__init__(name, "PROPERTY")
        self.color = color
        self.price = price
        self.rent = rent
        self.owner = None

    def __str__(self):
        owner_str = f", Owner: {self.owner.name}" if self.owner else ""
        return f"[{self.name} ({self.color}) - Price: ${self.price}, Rent: ${self.rent}{owner_str}]"

class Board:
    def __init__(self, num_spaces=12):
        self.num_spaces = num_spaces
        self.spaces = []
        self.color_map = {}
        self._create_board(self.num_spaces)

    @property
    def size(self):
        return len(self.spaces)

    def _create_board(self, num_spaces):
        # This is a sample board creation.
        # We will make this more dynamic and configurable later.
        self.spaces.append(Space("GO", "GO"))
        self.spaces.append(Property("Cotton Street", "Light Blue", 60, 2))
        self.spaces.append(Space("Chance", "CHANCE"))
        self.spaces.append(Property("Bamboo Ave", "Light Blue", 60, 4))
        self.spaces.append(Space("Tax", "TAX"))
        self.spaces.append(Space("Jail/Just Visiting", "JAIL"))
        self.spaces.append(Property("Coral Rd", "Orange", 100, 6))
        self.spaces.append(Space("Chance", "CHANCE"))
        self.spaces.append(Property("Amber Ln", "Orange", 120, 8))
        self.spaces.append(Space("Tax", "TAX"))
        self.spaces.append(Space("Free Parking", "FREE_PARKING"))
        self.spaces.append(Property("Pearl Sq", "Pink", 140, 10))
        # Trim or extend the board to match num_spaces if necessary
        # For now, it's fixed at 12.

        # Populate the color map
        for space in self.spaces:
            if isinstance(space, Property):
                if space.color not in self.color_map:
                    self.color_map[space.color] = []
                self.color_map[space.color].append(space)

    def get_space(self, position):
        return self.spaces[position]

    def display(self):
        board_str = ""
        for i, space in enumerate(self.spaces):
            board_str += f"{i}: {space}\n"
        return board_str
