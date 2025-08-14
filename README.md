# Mini Monopoly for TikTok Live

A simplified, text-based Monopoly-style game designed to be played interactively through a chat interface, like a TikTok Live stream. This version is a proof-of-concept running locally in a terminal.

## How to Run the Game

1.  Ensure you have Python 3 installed.
2.  Navigate to the project directory in your terminal.
3.  Run the game using the following command:

    ```bash
    python main.py
    ```

4.  The game will start in a "WAITING" state. Players can begin to join.

## Game Rules

- **Objective:** Be the last player remaining who has not gone bankrupt.
- **Joining:** Before the game starts, players can join by typing `YourName:!join`.
- **Starting:** Any player can type `YourName:!start` to begin the game once at least 2 players have joined. Player order is randomized.
- **Turns:** The game will announce whose turn it is. That player must type `TheirName:!roll` to roll the dice and move.
- **Properties:** If you land on an unowned property, you can choose to buy it (`!buy`) or pass (`!pass`). If you land on an owned property, you automatically pay rent to the owner.
- **Color Set Bonus:** If a player owns all properties of the same color, the rent on all those properties is **doubled**.
- **Bankruptcy:** If you cannot afford to pay rent or a tax, you are declared bankrupt. Your properties are returned to the bank (unowned), and you are removed from the game.
- **Winning:** The last player standing wins the game!

## Command List

The game uses a `username:!command` format for most actions to simulate different users in a chat.

-   `<username>:!join` - Join the game before it starts.
-   `<username>:!start` - Start the game.
-   `<username>:!roll` - Roll the dice on your turn.
-   `<username>:!buy` - Buy the property you just landed on.
-   `<username>:!pass` - Decline to buy the property you just landed on.
-   `<username>:!status` - Check your own money and list of properties.
-   `!board` - Display the current state of the entire board, including property owners.
-   `!players` - See a list of all players currently in the game.
-   `!exit` - Stop the game server (for the host).