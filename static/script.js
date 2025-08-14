document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const playerNameInput = document.getElementById('player-name');
    const commandMessageInput = document.getElementById('command-message');
    const commandForm = document.getElementById('command-form');
    const playerList = document.getElementById('player-list');
    const messageLog = document.getElementById('message-log');
    const gameBoard = document.getElementById('game-board');

    // State
    let lastLog = [];
    let lastBoardSize = 0;
    const playerColors = ['#ff4136', '#0074d9', '#2ecc40', '#ffdc00', '#b10dc9', '#ff851b', '#7fdbff', '#f012be'];

    // --- Initialization ---
    fetchGameState();
    setInterval(fetchGameState, 2000);

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
        if (!playerName || !message) { alert('Player Name and Command are required.'); return; }
        try {
            const response = await fetch('/api/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ player: playerName, message: message }),
            });
            const newState = await (response.ok ? response.json() : Promise.reject('Command submission failed'));
            renderGame(newState);
            commandMessageInput.value = '';
        } catch (error) { console.error('Error sending command:', error); }
    }

    // --- Rendering Functions ---
    function renderGame(state) {
        if (state.board.length !== lastBoardSize) {
            createBoard(state.board);
            lastBoardSize = state.board.length;
        }
        updateBoard(state.board, state.players);
        renderPlayerList(state.players, state.currentPlayerName);
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
            if (player.name === currentPlayerName) li.classList.add('current-player');
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

    function getPosition(index, sideLength) {
        if (index < sideLength) return { row: sideLength, col: index + 1 }; // Bottom
        if (index < 2 * sideLength) return { row: sideLength - (index - sideLength), col: sideLength }; // Right
        if (index < 3 * sideLength) return { row: 1, col: sideLength - (index - 2 * sideLength) }; // Top
        return { row: index - 3 * sideLength + 1, col: 1 }; // Left
    }

    function createBoard(boardData) {
        gameBoard.innerHTML = '';
        const boardSize = boardData.length;
        if (boardSize === 0) return;

        const sideLength = (boardSize / 4) + 1;
        gameBoard.style.gridTemplateColumns = `100px repeat(${sideLength - 2}, 1fr) 100px`;
        gameBoard.style.gridTemplateRows = `100px repeat(${sideLength - 2}, 1fr) 100px`;

        for (let i = 0; i < boardSize; i++) {
            const space = boardData[i];
            const spaceDiv = document.createElement('div');
            spaceDiv.id = `space-${i}`;
            spaceDiv.className = 'space';

            const pos = getPosition(i, sideLength);
            spaceDiv.style.gridRow = `${pos.row} / span 1`;
            spaceDiv.style.gridColumn = `${pos.col} / span 1`;

            if (space.image_url) {
                spaceDiv.style.backgroundImage = `url('${space.image_url}')`;
            }

            spaceDiv.innerHTML = `<div class="space-name">${space.name}</div><div class="players-on-space"></div>`;
            gameBoard.appendChild(spaceDiv);
        }

        const centerDiv = document.createElement('div');
        centerDiv.className = 'center';
        centerDiv.style.gridArea = `2 / 2 / ${sideLength} / ${sideLength}`;
        centerDiv.innerHTML = '<h2>Mini Monopoly</h2>';
        gameBoard.appendChild(centerDiv);
    }

    function updateBoard(boardData, players) {
        document.querySelectorAll('.player-marker-on-board').forEach(marker => marker.remove());
        boardData.forEach((space, i) => {
            const spaceDiv = document.getElementById(`space-${i}`);
            if (space.type === 'PROPERTY' && space.owner) {
                let ownerDiv = spaceDiv.querySelector('.space-owner');
                if (!ownerDiv) {
                    ownerDiv = document.createElement('div');
                    ownerDiv.className = 'space-owner';
                    spaceDiv.appendChild(ownerDiv);
                }
                ownerDiv.textContent = `Owner: ${space.owner}`;
            } else {
                 let ownerDiv = spaceDiv.querySelector('.space-owner');
                 if(ownerDiv) ownerDiv.remove();
            }
        });

        players.forEach((player, index) => {
            const spaceDiv = document.getElementById(`space-${player.position}`);
            if (spaceDiv) {
                const playersOnSpaceDiv = spaceDiv.querySelector('.players-on-space');
                if (playersOnSpaceDiv) {
                    const marker = document.createElement('div');
                    marker.className = 'player-marker-on-board';
                    marker.style.backgroundColor = playerColors[index % playerColors.length];
                    marker.title = player.name;
                    playersOnSpaceDiv.appendChild(marker);
                }
            }
        });
    }
});
