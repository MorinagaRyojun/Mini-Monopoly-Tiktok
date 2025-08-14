# Mini Monopoly for TikTok Live

A simplified, web-based Monopoly-style game designed to be played interactively through a chat interface, like a TikTok Live stream. This version runs as a local web server, providing a visual interface that can be captured for a stream.

## Setup & Installation

1.  **Ensure you have Python 3 installed.**
2.  **Install Flask:** This project uses Flask as its web server. Install it via pip:
    ```bash
    pip install Flask
    ```
3.  **Run the Game Server:** Navigate to the project directory and run the `app.py` file. This will start the local web server.
    ```bash
    python app.py
    ```
4.  **Open the Game:** Open your web browser and go to the address provided by Flask, which is typically `http://127.0.0.1:5002`. You should see the game interface.

## How to Play (Step-by-Step Guide)

The game is controlled by sending commands through the input form on the web page.

### 1. Joining the Game
Before the game starts, all players must join.
-   **Action:** Each player enters their name in the "Your Name" field and `!join` in the "!command" field, then clicks "Send".
-   **Example:**
    -   Player 1 enters Name: `Ake`, Command: `!join`
    -   Player 2 enters Name: `Ben`, Command: `!join`
-   **Result:** You will see the players appear in the "Players" list and a confirmation message in the "Game Log".

### 2. Starting the Game
Once at least two players have joined, any player can start the game.
-   **Action:** One player enters their name and the `!start` command.
-   **Example:** Name: `Ake`, Command: `!start`
-   **Result:** The game will begin! The Game Log will announce the randomized player order and whose turn it is to roll first. The current player will be highlighted in the player list.

### 3. Taking a Turn
-   **Action:** The player whose turn it is must enter their name and the `!roll` command.
-   **Result:** The game log will show the dice roll result. Your player marker will move on the board, and the action for the space you landed on will be resolved automatically.

### 4. Buying Property
-   If you land on an unowned property, the Game Log will tell you that you can buy it.
-   **Action:** To purchase it, send the `!buy` command. To skip, send the `!pass` command.
-   **Example:** Name: `Ake`, Command: `!buy`
-   **Result:** If you have enough money, the property will be added to your asset list, and the money will be deducted. The board will update to show you as the owner.

### 5. Game Progression
-   Players continue taking turns rolling, buying properties, and paying rent automatically when landing on others' properties.
-   If a player cannot afford rent or a tax, they go bankrupt and are removed from the game.
-   The last player remaining wins!

## Full Command List

-   `<name>:!join`: Join the game before it starts.
-   `<name>:!start`: Start the game (requires >= 2 players).
-   `<name>:!roll`: Roll the dice on your turn.
-   `<name>:!buy`: Buy the property you just landed on.
-   `<name>:!pass`: Decline to buy the property you just landed on.
-   `<name>:!status`: Get a detailed status of your assets in the Game Log.
-   `!board`: Get a text-based representation of the board state in the Game Log (Note: The UI provides a better visual).
-   `!players`: (This command is not available in the UI version, as the player list is always visible).
-   `!exit`: (This command is not available in the UI version. To stop the server, press `Ctrl+C` in the terminal where it is running).