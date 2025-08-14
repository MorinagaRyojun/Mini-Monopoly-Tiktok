document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const playerNameInput = document.getElementById('player-name');
    const commandMessageInput = document.getElementById('command-message');
    const commandForm = document.getElementById('command-form');
    const playerList = document.getElementById('player-list');
    const messageLog = document.getElementById('message-log');

    // State
    let lastLog = [];
    const playerColors = ['#ff4136', '#0074d9', '#2ecc40', '#ffdc00', '#b10dc9', '#ff851b', '#7fdbff', '#f012be'];

    // --- Initialization ---
    fetchGameState();
    setInterval(fetchGameState, 2000); // Poll every 2 seconds

    // --- Event Listeners ---
    commandForm.addEventListener('submit', handleCommandSubmit);

    // --- Core Functions ---
    function fetchGameState() {
        fetch('/api/game_state')
            .then(response => response.ok ? response.json() : Promise.reject('Network response was not ok'))
            .then(renderGame)
            .catch(error => console.error('Error fetching game state:', error));
    }

    async function handleCommandSubmit(event) {
        event.preventDefault();
        const playerName = playerNameInput.value.trim();
        const message = commandMessageInput.value.trim();

        if (!playerName || !message) {
            alert('Player Name and Command are required.');
            return;
        }

        try {
            const response = await fetch('/api/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ player: playerName, message: message }),
            });
            const newState = await (response.ok ? response.json() : Promise.reject('Command submission failed'));
            renderGame(newState);
            commandMessageInput.value = ''; // Clear input
        } catch (error) {
            console.error('Error sending command:', error);
        }
    }

    // --- Rendering Functions ---
    function renderGame(state) {
        renderPlayerList(state.players, state.currentPlayerName);
        renderBoard(state.board, state.players);
        // Only update log if it has changed to prevent scroll jumping
        if (JSON.stringify(state.log) !== JSON.stringify(lastLog)) {
            renderMessageLog(state.log);
            lastLog = state.log;
        }
    }

    function renderPlayerList(players, currentPlayerName) {
        playerList.innerHTML = '';
        players.forEach((player, index) => {
            const li = document.createElement('li');
            const propList = player.properties.join(', ') || 'None';
            li.innerHTML = `<span class="player-marker" style="background-color: ${playerColors[index % playerColors.length]}"></span> <strong>${player.name}</strong>: $${player.money} <br><small>Properties: ${propList}</small>`;

            if (player.name === currentPlayerName) {
                li.classList.add('current-player');
            }
            playerList.appendChild(li);
        });
    }

    function renderMessageLog(log) {
        messageLog.innerHTML = '';
        log.forEach(message => {
            const li = document.createElement('li');
            li.textContent = message;
            messageLog.appendChild(li);
        });
        messageLog.scrollTop = messageLog.scrollHeight;
    }

    function renderBoard(boardData, players) {
        // Clear existing player markers first
        document.querySelectorAll('.player-marker-on-board').forEach(marker => marker.remove());

        // Update space details (only needs to be done once, but simple to do it every time)
        for (let i = 0; i < 12; i++) {
            const spaceDiv = document.getElementById(`space-${i}`);
            if (spaceDiv && spaceDiv.children.length < 2) { // Avoid re-rendering text content
                const spaceInfo = boardData[i] || "";
                const nameMatch = spaceInfo.match(/\[(.*?)(?:\s\(| -|\])/);
                const ownerMatch = spaceInfo.match(/Owner: (\w+)/);

                let nameContent = nameMatch ? nameMatch[1] : spaceInfo;
                // For properties, just show the name, not price/rent details in the main view
                if(nameContent.includes("Price:")){
                    nameContent = nameContent.split(" - ")[0];
                }

                spaceDiv.innerHTML = `<div class="space-name">${nameContent}</div>`;
                if (ownerMatch) {
                    spaceDiv.innerHTML += `<div class="space-owner">Owner: ${ownerMatch[1]}</div>`;
                }
                spaceDiv.innerHTML += `<div class="players-on-space"></div>`;
            }
        }

        // Place new player markers
        players.forEach((player, index) => {
            const spaceIndex = player.position;
            const spaceDiv = document.getElementById(`space-${spaceIndex}`);
            if (spaceDiv) {
                const playersOnSpaceDiv = spaceDiv.querySelector('.players-on-space');
                if (playersOnSpaceDiv) {
                    const marker = document.createElement('div');
                    marker.className = 'player-marker-on-board';
                    marker.style.backgroundColor = playerColors[index % playerColors.length];
                    marker.title = player.name; // Hover to see name
                    playersOnSpaceDiv.appendChild(marker);
                }
            }
        });
    }
});
