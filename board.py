import random
import math

class Space:
    def __init__(self, name, space_type, image_url=None):
        self.name = name
        self.space_type = space_type # e.g., "PROPERTY", "CHANCE", "TAX", "GO"
        self.image_url = image_url

    def __str__(self):
        return f"[{self.name}]"

class Property(Space):
    def __init__(self, name, color, price, rent, image_url=None):
        super().__init__(name, "PROPERTY", image_url=image_url)
        self.color = color
        self.price = price
        self.rent = rent
        self.owner = None

    def __str__(self):
        owner_str = f", Owner: {self.owner.name}" if self.owner else ""
        return f"[{self.name} ({self.color}) - Price: ${self.price}, Rent: ${self.rent}{owner_str}]"

class Board:
    def __init__(self, num_spaces=12, image_urls=None):
        if num_spaces < 8 or num_spaces % 4 != 0:
            raise ValueError("Number of spaces must be a multiple of 4 and at least 8.")

        self.num_spaces = num_spaces
        self.image_urls = image_urls if image_urls else {}
        self.spaces = []
        self.color_map = {}
        self.jail_pos = -1
        self._create_board()

    @property
    def size(self):
        return len(self.spaces)

    def _get_sample_properties(self, count):
        """Generates a list of sample properties."""
        colors = ["#a86432", "#a83232", "#a87b32", "#8aa832", "#32a857", "#32a8a4", "#3269a8", "#6732a8", "#a8329b"]
        street_names = ["Oak", "Pine", "Maple", "Cedar", "Elm", "Willow", "Birch", "Aspen", "Spruce", "Hickory"]
        name_suffixes = ["St", "Ave", "Ln", "Rd", "Blvd", "Ct", "Pl"]

        properties = []
        for i in range(count):
            color = random.choice(colors)
            name = f"{random.choice(street_names)} {random.choice(name_suffixes)}"
            price = random.randint(5, 30) * 10  # 50 to 300
            rent = max(1, int(price * 0.1)) # Rent is 10% of price, min 1
            properties.append(Property(name, color, price, rent, image_url=self.image_urls.get("PROPERTY")))
        return properties

    def _create_board(self):
        """Dynamically creates the game board."""
        self.spaces = [None] * self.num_spaces

        # 1. Place corners
        side_len = self.num_spaces // 4
        self.jail_pos = side_len
        self.spaces[0] = Space("GO", "GO", image_url=self.image_urls.get("GO"))
        self.spaces[self.jail_pos] = Space("Jail/Just Visiting", "JAIL", image_url=self.image_urls.get("JAIL"))
        self.spaces[side_len * 2] = Space("Free Parking", "FREE_PARKING", image_url=self.image_urls.get("FREE_PARKING"))
        self.spaces[side_len * 3] = Space("Go To Jail", "GO_TO_JAIL", image_url=self.image_urls.get("GO_TO_JAIL"))

        # 2. Define pool of other spaces
        num_other_spaces = self.num_spaces - 4
        num_properties = math.ceil(num_other_spaces * 0.65)
        num_chance = math.ceil(num_other_spaces * 0.20)
        num_tax = num_other_spaces - num_properties - num_chance

        space_pool = []
        space_pool.extend(self._get_sample_properties(num_properties))
        space_pool.extend([Space("Chance", "CHANCE", image_url=self.image_urls.get("CHANCE"))] * num_chance)
        space_pool.extend([Space("Tax", "TAX", image_url=self.image_urls.get("TAX"))] * num_tax)
        random.shuffle(space_pool)

        # 3. Place other spaces
        for i in range(self.num_spaces):
            if self.spaces[i] is None:
                if space_pool:
                    self.spaces[i] = space_pool.pop()
                else: # Should not happen with correct math, but as a fallback
                    self.spaces[i] = Space("Extra Space", "CHANCE")

        # 4. Populate the color map
        self.color_map = {}
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
