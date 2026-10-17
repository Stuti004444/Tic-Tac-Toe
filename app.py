
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Tic-Tac-Toe</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #10152f, #253b70);
            color: white;
        }

        .game {
            width: 350px;
            max-width: 94vw;
            padding: 25px;
            text-align: center;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 22px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        }

        h1 {
            margin: 0 0 8px;
            color: #65e6ff;
            font-size: 30px;
        }

        .subtitle {
            color: #cbd5f0;
            margin-bottom: 22px;
        }

        .scores {
            display: flex;
            justify-content: space-between;
            gap: 8px;
            margin-bottom: 20px;
        }

        .score {
            flex: 1;
            padding: 10px 5px;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.09);
        }

        .score strong {
            display: block;
            margin-top: 6px;
            font-size: 23px;
            color: #65e6ff;
        }

        #status {
            min-height: 26px;
            margin: 12px 0 16px;
            font-weight: bold;
            color: #ffffff;
        }

        .board {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 9px;
        }

        .cell {
            aspect-ratio: 1;
            border: none;
            border-radius: 13px;
            background: #e9f1ff;
            color: #182344;
            font-size: 43px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
        }

        .cell:hover:enabled {
            background: #c9f5ff;
            transform: scale(1.04);
        }

        .cell:disabled {
            cursor: default;
        }

        .cell.x {
            color: #1769d2;
        }

        .cell.o {
            color: #df438a;
        }

        .cell.winner {
            background: #8cf5b5;
            color: #123c2b;
        }

        button:focus-visible {
            outline: 3px solid #65e6ff;
            outline-offset: 3px;
        }

        .restart {
            width: 100%;
            margin-top: 22px;
            padding: 13px;
            border: none;
            border-radius: 12px;
            background: #65e6ff;
            color: #10152f;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }

        .restart:hover {
            background: #a0f0ff;
        }

        .hint {
            margin: 16px 0 0;
            color: #cbd5f0;
            font-size: 12px;
        }
    </style>
</head>

<body>
    <main class="game">
        <h1>AI Tic-Tac-Toe</h1>
        <p class="subtitle">Can you beat the machine?</p>

        <div class="scores">
            <div class="score">
                You (X)
                <strong id="playerScore">0</strong>
            </div>
            <div class="score">
                Draws
                <strong id="drawScore">0</strong>
            </div>
            <div class="score">
                AI (O)
                <strong id="aiScore">0</strong>
            </div>
        </div>

        <div id="status" role="status" aria-live="polite">
            Your turn! Choose a square.
        </div>

        <div class="board" id="board" role="group"
             aria-label="Tic-Tac-Toe board">
            <button class="cell" data-index="0"
                    aria-label="Top left square"></button>
            <button class="cell" data-index="1"
                    aria-label="Top middle square"></button>
            <button class="cell" data-index="2"
                    aria-label="Top right square"></button>
            <button class="cell" data-index="3"
                    aria-label="Middle left square"></button>
            <button class="cell" data-index="4"
                    aria-label="Center square"></button>
            <button class="cell" data-index="5"
                    aria-label="Middle right square"></button>
            <button class="cell" data-index="6"
                    aria-label="Bottom left square"></button>
            <button class="cell" data-index="7"
                    aria-label="Bottom middle square"></button>
            <button class="cell" data-index="8"
                    aria-label="Bottom right square"></button>
        </div>

        <button class="restart" id="restart">
            Restart Game
        </button>

        <p class="hint">Powered by the Minimax AI algorithm</p>
    </main>

    <script>
        const cells = [...document.querySelectorAll(".cell")];
        const statusText = document.getElementById("status");

        const playerScoreText = document.getElementById("playerScore");
        const aiScoreText = document.getElementById("aiScore");
        const drawScoreText = document.getElementById("drawScore");

        const WINNING_COMBINATIONS = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ];

        let board = Array(9).fill("");
        let gameOver = false;
        let playerTurn = true;

        let playerScore = 0;
        let aiScore = 0;
        let drawScore = 0;

        // Check whether a player has won.
        function getWinner(state) {
            for (const combination of WINNING_COMBINATIONS) {
                const [a, b, c] = combination;

                if (
                    state[a] &&
                    state[a] === state[b] &&
                    state[a] === state[c]
                ) {
                    return {
                        player: state[a],
                        combination
                    };
                }
            }

            return null;
        }

        // Minimax evaluates all possible future moves.
        // AI tries to maximize its score; the player minimizes it.
        function minimax(state, isMaximizing, depth = 0) {
            const result = getWinner(state);

            if (result) {
                return result.player === "O"
                    ? 10 - depth
                    : depth - 10;
            }

            const available = state
                .map((value, index) => value === "" ? index : -1)
                .filter(index => index !== -1);

            if (available.length === 0) {
                return 0;
            }

            if (isMaximizing) {
                let bestScore = -Infinity;

                for (const index of available) {
                    state[index] = "O";

                    const score = minimax(
                        state, false, depth + 1
                    );

                    state[index] = "";
                    bestScore = Math.max(bestScore, score);
                }

                return bestScore;
            } else {
                let bestScore = Infinity;

                for (const index of available) {
                    state[index] = "X";

                    const score = minimax(
                        state, true, depth + 1
                    );

                    state[index] = "";
                    bestScore = Math.min(bestScore, score);
                }

                return bestScore;
            }
        }

        // Find the best possible move for the AI.
        function getBestMove() {
            let bestScore = -Infinity;
            let bestMove = -1;

            for (let i = 0; i < 9; i++) {
                if (board[i] === "") {
                    board[i] = "O";

                    const score = minimax(board, false, 0);

                    board[i] = "";

                    if (score > bestScore) {
                        bestScore = score;
                        bestMove = i;
                    }
                }
            }

            return bestMove;
        }

        // Update the visible board.
        function renderBoard() {
            cells.forEach((cell, index) => {
                cell.textContent = board[index];
                cell.classList.toggle("x", board[index] === "X");
                cell.classList.toggle("o", board[index] === "O");

                cell.disabled =
                    gameOver ||
                    board[index] !== "" ||
                    !playerTurn;

                cell.setAttribute(
                    "aria-label",
                    `Square ${index + 1}: ${
                        board[index] || "empty"
                    }`
                );
            });
        }

        // Check for a win or a draw.
        function checkGameEnd() {
            const result = getWinner(board);

            if (result) {
                gameOver = true;

                result.combination.forEach(index => {
                    cells[index].classList.add("winner");
                });

                if (result.player === "X") {
                    playerScore++;
                    playerScoreText.textContent = playerScore;
                    statusText.textContent = "🎉 You win!";
                } else {
                    aiScore++;
                    aiScoreText.textContent = aiScore;
                    statusText.textContent = "🤖 AI wins! Try again.";
                }

                renderBoard();
                return true;
            }

            if (board.every(cell => cell !== "")) {
                gameOver = true;
                drawScore++;
                drawScoreText.textContent = drawScore;
                statusText.textContent = "🤝 It's a draw!";
                renderBoard();
                return true;
            }

            return false;
        }

        // Handle a human move.
        function playerMove(index) {
            if (
                gameOver ||
                !playerTurn ||
                board[index] !== ""
            ) {
                return;
            }

            board[index] = "X";
            renderBoard();

            if (checkGameEnd()) {
                return;
            }

            playerTurn = false;
            statusText.textContent = "AI is thinking...";
            renderBoard();

            // A short pause makes the AI turn feel natural.
            setTimeout(aiMove, 350);
        }

        // Let the AI choose its best move.
        function aiMove() {
            if (gameOver) {
                return;
            }

            const move = getBestMove();

            if (move !== -1) {
                board[move] = "O";
            }

            if (checkGameEnd()) {
                return;
            }

            playerTurn = true;
            statusText.textContent = "Your turn! Choose a square.";
            renderBoard();
        }

        // Start a new round without resetting the scores.
        function restartGame() {
            board = Array(9).fill("");
            gameOver = false;
            playerTurn = true;

            cells.forEach(cell => {
                cell.classList.remove("winner");
            });

            statusText.textContent = "Your turn! Choose a square.";
            renderBoard();
        }

        cells.forEach(cell => {
            cell.addEventListener("click", () => {
                playerMove(Number(cell.dataset.index));
            });
        });

        document.getElementById("restart")
            .addEventListener("click", restartGame);

        renderBoard();
    </script>
</body>
</html>
