/**
 * Crossword game module.
 */
const Crossword = {
    puzzle: null,
    solution: null,
    grid: [],
    selectedCell: null,
    direction: 'across',
    timerInterval: null,
    startTime: null,
    elapsedMs: 0,
    isCompleted: false,
    hasStarted: false,
    isRevealed: false,
    hintsUsed: 0,

    /**
     * Initialize the crossword with a puzzle.
     */
    init(puzzle) {
        this.puzzle = puzzle;
        this.solution = null;
        this.grid = [];
        this.selectedCell = null;
        this.direction = 'across';
        this.isCompleted = false;
        this.hasStarted = false;
        this.isRevealed = false;
        this.hintsUsed = 0;
        this.elapsedMs = 0;
        this.stopTimer();

        // Initialize grid state
        for (let row = 0; row < puzzle.size; row++) {
            this.grid[row] = [];
            for (let col = 0; col < puzzle.size; col++) {
                this.grid[row][col] = puzzle.grid[row][col] === '.' ? '.' : '';
            }
        }

        this.render();
        this.renderClues();
        this.updateTimer();
        this.showStartScreen();
        this.disableControls();
    },

    /**
     * Show the start screen overlay.
     */
    showStartScreen() {
        document.getElementById('start-screen').classList.remove('hidden');
        document.getElementById('crossword-grid').classList.add('blurred');
    },

    /**
     * Hide the start screen and begin the game.
     */
    startGame() {
        document.getElementById('start-screen').classList.add('hidden');
        document.getElementById('crossword-grid').classList.remove('blurred');
        this.enableControls();
        this.startTimer();

        // Focus first cell
        const firstClue = this.puzzle.clues_across[0];
        if (firstClue) {
            this.selectCell(firstClue.row, firstClue.col);
            this.focusCell(firstClue.row, firstClue.col);
        }
    },

    /**
     * Enable game control buttons.
     */
    enableControls() {
        document.getElementById('btn-hint').disabled = false;
        document.getElementById('btn-check').disabled = false;
        document.getElementById('btn-reveal').disabled = false;
        document.getElementById('btn-clear').disabled = false;
    },

    /**
     * Disable game control buttons.
     */
    disableControls() {
        document.getElementById('btn-hint').disabled = true;
        document.getElementById('btn-check').disabled = true;
        document.getElementById('btn-reveal').disabled = true;
        document.getElementById('btn-clear').disabled = true;
    },

    /**
     * Render the crossword grid.
     */
    render() {
        const container = document.getElementById('crossword-grid');
        container.innerHTML = '';
        container.style.gridTemplateColumns = `repeat(${this.puzzle.size}, 48px)`;

        const cellNumbers = this.buildCellNumbers();

        for (let row = 0; row < this.puzzle.size; row++) {
            for (let col = 0; col < this.puzzle.size; col++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.dataset.row = row;
                cell.dataset.col = col;

                if (this.puzzle.grid[row][col] === '.') {
                    cell.classList.add('block');
                } else {
                    const number = cellNumbers[`${row}-${col}`];
                    if (number) {
                        const numSpan = document.createElement('span');
                        numSpan.className = 'cell-number';
                        numSpan.textContent = number;
                        cell.appendChild(numSpan);
                    }

                    const input = document.createElement('input');
                    input.type = 'text';
                    input.className = 'cell-input';
                    input.maxLength = 1;
                    input.value = this.grid[row][col];
                    input.dataset.row = row;
                    input.dataset.col = col;

                    input.addEventListener('click', (e) => this.handleCellClick(row, col, e));
                    input.addEventListener('input', (e) => this.handleInput(row, col, e));
                    input.addEventListener('keydown', (e) => this.handleKeyDown(row, col, e));
                    input.addEventListener('focus', () => this.selectCell(row, col));

                    cell.appendChild(input);
                }

                container.appendChild(cell);
            }
        }

        this.updateHighlight();
    },

    /**
     * Build cell numbers from clues.
     */
    buildCellNumbers() {
        const numbers = {};
        const allClues = [...this.puzzle.clues_across, ...this.puzzle.clues_down];

        allClues.forEach(clue => {
            const key = `${clue.row}-${clue.col}`;
            if (!numbers[key]) {
                numbers[key] = clue.number;
            }
        });

        return numbers;
    },

    /**
     * Render the clues.
     */
    renderClues() {
        const acrossContainer = document.getElementById('clues-across');
        const downContainer = document.getElementById('clues-down');

        acrossContainer.innerHTML = '';
        downContainer.innerHTML = '';

        this.puzzle.clues_across.forEach(clue => {
            const li = document.createElement('li');
            li.className = 'clue-item';
            li.dataset.direction = 'across';
            li.dataset.number = clue.number;
            li.dataset.row = clue.row;
            li.dataset.col = clue.col;
            li.innerHTML = `<span class="clue-number">${clue.number}.</span>${clue.clue}`;
            li.addEventListener('click', () => this.handleClueClick(clue, 'across'));
            acrossContainer.appendChild(li);
        });

        this.puzzle.clues_down.forEach(clue => {
            const li = document.createElement('li');
            li.className = 'clue-item';
            li.dataset.direction = 'down';
            li.dataset.number = clue.number;
            li.dataset.row = clue.row;
            li.dataset.col = clue.col;
            li.innerHTML = `<span class="clue-number">${clue.number}.</span>${clue.clue}`;
            li.addEventListener('click', () => this.handleClueClick(clue, 'down'));
            downContainer.appendChild(li);
        });
    },

    /**
     * Handle cell click.
     */
    handleCellClick(row, col, event) {
        if (!this.hasStarted) return;

        if (this.selectedCell && this.selectedCell.row === row && this.selectedCell.col === col) {
            this.direction = this.direction === 'across' ? 'down' : 'across';
        }
        this.selectCell(row, col);
    },

    /**
     * Handle clue click.
     */
    handleClueClick(clue, direction) {
        if (!this.hasStarted) return;

        this.direction = direction;
        this.selectCell(clue.row, clue.col);
        this.focusCell(clue.row, clue.col);
    },

    /**
     * Select a cell.
     */
    selectCell(row, col) {
        this.selectedCell = { row, col };
        this.updateHighlight();
        this.updateSelectedClue();
    },

    /**
     * Focus a cell's input.
     */
    focusCell(row, col) {
        const input = document.querySelector(`.cell-input[data-row="${row}"][data-col="${col}"]`);
        if (input) {
            input.focus();
            input.select();
        }
    },

    /**
     * Update cell highlighting.
     */
    updateHighlight() {
        document.querySelectorAll('.cell').forEach(cell => {
            cell.classList.remove('selected', 'highlighted');
        });

        if (!this.selectedCell) return;

        const { row, col } = this.selectedCell;

        const selectedCell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
        if (selectedCell) {
            selectedCell.classList.add('selected');
        }

        const wordCells = this.getWordCells(row, col, this.direction);
        wordCells.forEach(({ r, c }) => {
            const cell = document.querySelector(`.cell[data-row="${r}"][data-col="${c}"]`);
            if (cell && !(r === row && c === col)) {
                cell.classList.add('highlighted');
            }
        });
    },

    /**
     * Update selected clue highlighting.
     */
    updateSelectedClue() {
        document.querySelectorAll('.clue-item').forEach(item => {
            item.classList.remove('selected');
        });

        if (!this.selectedCell) return;

        const clue = this.getCurrentClue();
        if (clue) {
            const clueItem = document.querySelector(
                `.clue-item[data-direction="${this.direction}"][data-number="${clue.number}"]`
            );
            if (clueItem) {
                clueItem.classList.add('selected');
                clueItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }
    },

    /**
     * Get cells in the current word.
     */
    getWordCells(row, col, direction) {
        const cells = [];

        if (direction === 'across') {
            let startCol = col;
            while (startCol > 0 && this.puzzle.grid[row][startCol - 1] !== '.') {
                startCol--;
            }
            for (let c = startCol; c < this.puzzle.size && this.puzzle.grid[row][c] !== '.'; c++) {
                cells.push({ r: row, c });
            }
        } else {
            let startRow = row;
            while (startRow > 0 && this.puzzle.grid[startRow - 1][col] !== '.') {
                startRow--;
            }
            for (let r = startRow; r < this.puzzle.size && this.puzzle.grid[r][col] !== '.'; r++) {
                cells.push({ r, c: col });
            }
        }

        return cells;
    },

    /**
     * Get the current clue based on selected cell and direction.
     */
    getCurrentClue() {
        if (!this.selectedCell) return null;

        const { row, col } = this.selectedCell;
        const clues = this.direction === 'across' ? this.puzzle.clues_across : this.puzzle.clues_down;

        for (const clue of clues) {
            const cells = this.getWordCells(clue.row, clue.col, this.direction);
            if (cells.some(c => c.r === row && c.c === col)) {
                return clue;
            }
        }

        return null;
    },

    /**
     * Handle input in a cell.
     */
    handleInput(row, col, event) {
        if (!this.hasStarted || this.isCompleted) return;

        const value = event.target.value.toUpperCase();
        event.target.value = value;
        this.grid[row][col] = value;

        if (value) {
            this.moveToNextCell(row, col);
        }

        this.checkCompletion();
    },

    /**
     * Handle keyboard navigation.
     */
    handleKeyDown(row, col, event) {
        if (!this.hasStarted) return;

        switch (event.key) {
            case 'ArrowUp':
                event.preventDefault();
                this.moveCell(row, col, -1, 0);
                break;
            case 'ArrowDown':
                event.preventDefault();
                this.moveCell(row, col, 1, 0);
                break;
            case 'ArrowLeft':
                event.preventDefault();
                this.moveCell(row, col, 0, -1);
                break;
            case 'ArrowRight':
                event.preventDefault();
                this.moveCell(row, col, 0, 1);
                break;
            case 'Backspace':
                if (!event.target.value) {
                    event.preventDefault();
                    this.moveToPrevCell(row, col);
                }
                break;
            case 'Tab':
                event.preventDefault();
                if (event.shiftKey) {
                    this.moveToPrevWord();
                } else {
                    this.moveToNextWord();
                }
                break;
            case ' ':
                event.preventDefault();
                this.direction = this.direction === 'across' ? 'down' : 'across';
                this.updateHighlight();
                this.updateSelectedClue();
                break;
        }
    },

    /**
     * Move to a cell in a direction.
     */
    moveCell(row, col, dRow, dCol) {
        let newRow = row + dRow;
        let newCol = col + dCol;

        while (
            newRow >= 0 && newRow < this.puzzle.size &&
            newCol >= 0 && newCol < this.puzzle.size
        ) {
            if (this.puzzle.grid[newRow][newCol] !== '.') {
                this.selectCell(newRow, newCol);
                this.focusCell(newRow, newCol);
                return;
            }
            newRow += dRow;
            newCol += dCol;
        }
    },

    /**
     * Move to the next cell in current word.
     */
    moveToNextCell(row, col) {
        if (this.direction === 'across') {
            this.moveCell(row, col, 0, 1);
        } else {
            this.moveCell(row, col, 1, 0);
        }
    },

    /**
     * Move to the previous cell in current word.
     */
    moveToPrevCell(row, col) {
        if (this.direction === 'across') {
            this.moveCell(row, col, 0, -1);
        } else {
            this.moveCell(row, col, -1, 0);
        }
    },

    /**
     * Move to the next word.
     */
    moveToNextWord() {
        const clues = this.direction === 'across' ? this.puzzle.clues_across : this.puzzle.clues_down;
        const currentClue = this.getCurrentClue();

        if (!currentClue) return;

        const currentIndex = clues.findIndex(c => c.number === currentClue.number);
        let nextIndex = currentIndex + 1;

        if (nextIndex >= clues.length) {
            this.direction = this.direction === 'across' ? 'down' : 'across';
            const newClues = this.direction === 'across' ? this.puzzle.clues_across : this.puzzle.clues_down;
            nextIndex = 0;
            this.selectCell(newClues[0].row, newClues[0].col);
            this.focusCell(newClues[0].row, newClues[0].col);
        } else {
            this.selectCell(clues[nextIndex].row, clues[nextIndex].col);
            this.focusCell(clues[nextIndex].row, clues[nextIndex].col);
        }
    },

    /**
     * Move to the previous word.
     */
    moveToPrevWord() {
        const clues = this.direction === 'across' ? this.puzzle.clues_across : this.puzzle.clues_down;
        const currentClue = this.getCurrentClue();

        if (!currentClue) return;

        const currentIndex = clues.findIndex(c => c.number === currentClue.number);
        let prevIndex = currentIndex - 1;

        if (prevIndex < 0) {
            this.direction = this.direction === 'across' ? 'down' : 'across';
            const newClues = this.direction === 'across' ? this.puzzle.clues_across : this.puzzle.clues_down;
            prevIndex = newClues.length - 1;
            this.selectCell(newClues[prevIndex].row, newClues[prevIndex].col);
            this.focusCell(newClues[prevIndex].row, newClues[prevIndex].col);
        } else {
            this.selectCell(clues[prevIndex].row, clues[prevIndex].col);
            this.focusCell(clues[prevIndex].row, clues[prevIndex].col);
        }
    },

    /**
     * Start the timer.
     */
    startTimer() {
        if (this.hasStarted) return;
        this.hasStarted = true;
        this.startTime = Date.now();

        this.timerInterval = setInterval(() => {
            this.elapsedMs = Date.now() - this.startTime;
            this.updateTimer();
        }, 100);

        document.getElementById('timer').classList.add('running');
    },

    /**
     * Stop the timer.
     */
    stopTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
        document.getElementById('timer').classList.remove('running');
    },

    /**
     * Update timer display.
     */
    updateTimer() {
        const minutes = Math.floor(this.elapsedMs / 60000);
        const seconds = Math.floor((this.elapsedMs % 60000) / 1000);
        document.getElementById('timer').textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    },

    /**
     * Check if puzzle is complete.
     */
    checkCompletion() {
        for (let row = 0; row < this.puzzle.size; row++) {
            for (let col = 0; col < this.puzzle.size; col++) {
                if (this.puzzle.grid[row][col] !== '.' && !this.grid[row][col]) {
                    return false;
                }
            }
        }

        this.verifyCompletion();
        return true;
    },

    /**
     * Verify completion with server.
     */
    async verifyCompletion() {
        try {
            const result = await API.puzzles.check(this.puzzle.id, this.grid);

            if (result.is_correct) {
                this.handleCompletion();
            }
        } catch (e) {
            console.error('Error checking puzzle:', e);
        }
    },

    /**
     * Handle puzzle completion.
     */
    async handleCompletion() {
        this.isCompleted = true;
        this.stopTimer();

        if (this.isRevealed) {
            document.getElementById('timer').classList.add('invalidated');
            this.showCompletionModal({ time_ms: this.elapsedMs, revealed: true });
        } else {
            document.getElementById('timer').classList.add('completed');

            if (Auth.isLoggedIn()) {
                try {
                    const result = await API.puzzles.solve(this.puzzle.id, this.elapsedMs, this.grid);
                    this.showCompletionModal(result);
                } catch (e) {
                    console.error('Error submitting solve:', e);
                    this.showCompletionModal({ time_ms: this.elapsedMs });
                }
            } else {
                this.showCompletionModal({ time_ms: this.elapsedMs });
            }
        }
    },

    /**
     * Show completion modal.
     */
    showCompletionModal(result) {
        const minutes = Math.floor(this.elapsedMs / 60000);
        const seconds = Math.floor((this.elapsedMs % 60000) / 1000);

        const timeEl = document.getElementById('completion-time');
        timeEl.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;

        const titleEl = document.getElementById('completion-title-text');
        const iconEl = document.getElementById('completion-icon');
        const rankEl = document.getElementById('completion-rank');

        if (result.revealed || this.isRevealed) {
            titleEl.textContent = 'Puzzle Revealed';
            iconEl.textContent = '👁';
            timeEl.classList.add('invalidated');
            rankEl.textContent = 'Time not recorded (reveal used)';
        } else {
            titleEl.textContent = 'Puzzle Complete!';
            iconEl.textContent = '🎉';
            timeEl.classList.remove('invalidated');

            if (result.rank) {
                rankEl.textContent = `You ranked #${result.rank}!`;
            } else if (!Auth.isLoggedIn()) {
                rankEl.textContent = 'Login to save your time!';
            } else {
                rankEl.textContent = '';
            }
        }

        if (result.share_text) {
            document.getElementById('share-text').textContent = result.share_text;
        }

        document.getElementById('completion-modal').classList.add('active');
    },

    /**
     * Check the puzzle - show correct/incorrect cells.
     */
    async check() {
        try {
            const result = await API.puzzles.check(this.puzzle.id, this.grid);

            document.querySelectorAll('.cell').forEach(cell => {
                cell.classList.remove('correct', 'incorrect');
            });

            let allCorrect = true;
            for (let row = 0; row < this.puzzle.size; row++) {
                for (let col = 0; col < this.puzzle.size; col++) {
                    if (this.puzzle.grid[row][col] === '.') continue;

                    const cell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
                    if (this.grid[row][col]) {
                        const isIncorrect = result.incorrect_cells.some(([r, c]) => r === row && c === col);
                        cell.classList.add(isIncorrect ? 'incorrect' : 'correct');
                        if (isIncorrect) allCorrect = false;
                    }
                }
            }

            if (allCorrect && result.is_correct) {
                App.showToast('All correct! Great job!', 'success');
            } else if (result.incorrect_cells.length > 0) {
                App.showToast(`${result.incorrect_cells.length} cell(s) incorrect`, 'error');
            } else {
                App.showToast('Looking good so far!', 'info');
            }

            setTimeout(() => {
                document.querySelectorAll('.cell').forEach(cell => {
                    cell.classList.remove('correct', 'incorrect');
                });
            }, 3000);
        } catch (e) {
            App.showToast('Error checking puzzle', 'error');
        }
    },

    /**
     * Give a hint - reveal one letter in the current word.
     */
    async hint() {
        if (!this.selectedCell) {
            App.showToast('Select a cell first', 'info');
            return;
        }

        // Fetch solution if we don't have it
        if (!this.solution) {
            try {
                const result = await API.puzzles.check(this.puzzle.id, this.grid);
                // We need to get the solution from the server
                // For hints, we'll check each cell individually
            } catch (e) {
                App.showToast('Error getting hint', 'error');
                return;
            }
        }

        const wordCells = this.getWordCells(this.selectedCell.row, this.selectedCell.col, this.direction);

        // Find an empty or incorrect cell in the current word
        for (const { r, c } of wordCells) {
            if (!this.grid[r][c]) {
                // Try to get the correct letter by checking with server
                await this.revealCell(r, c);
                this.hintsUsed++;
                App.showToast('Hint revealed!', 'info');
                return;
            }
        }

        // If all cells are filled, check for incorrect ones
        try {
            const result = await API.puzzles.check(this.puzzle.id, this.grid);
            for (const { r, c } of wordCells) {
                if (result.incorrect_cells.some(([ir, ic]) => ir === r && ic === c)) {
                    await this.revealCell(r, c);
                    this.hintsUsed++;
                    App.showToast('Hint: corrected a letter!', 'info');
                    return;
                }
            }
            App.showToast('This word is already correct!', 'success');
        } catch (e) {
            App.showToast('Error getting hint', 'error');
        }
    },

    /**
     * Reveal a single cell by finding its correct letter.
     */
    async revealCell(row, col) {
        // Try each letter until we find the correct one
        const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        const originalValue = this.grid[row][col];

        for (const letter of letters) {
            this.grid[row][col] = letter;
            try {
                const result = await API.puzzles.check(this.puzzle.id, this.grid);
                const isIncorrect = result.incorrect_cells.some(([r, c]) => r === row && c === col);
                if (!isIncorrect) {
                    // Found the correct letter
                    const input = document.querySelector(`.cell-input[data-row="${row}"][data-col="${col}"]`);
                    if (input) {
                        input.value = letter;
                    }
                    const cell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
                    if (cell) {
                        cell.classList.add('revealed');
                    }
                    this.checkCompletion();
                    return;
                }
            } catch (e) {
                // Continue trying
            }
        }

        // Restore original if nothing found
        this.grid[row][col] = originalValue;
    },

    /**
     * Reveal the entire puzzle solution.
     */
    async reveal() {
        if (!confirm('Revealing the solution will invalidate your time. Are you sure?')) {
            return;
        }

        this.isRevealed = true;
        document.getElementById('timer').classList.add('invalidated');

        // Reveal all cells by trying each one
        App.showToast('Revealing solution...', 'info');

        for (let row = 0; row < this.puzzle.size; row++) {
            for (let col = 0; col < this.puzzle.size; col++) {
                if (this.puzzle.grid[row][col] !== '.') {
                    await this.revealCell(row, col);
                }
            }
        }

        this.isCompleted = true;
        this.stopTimer();
        this.showCompletionModal({ revealed: true, time_ms: this.elapsedMs });
    },

    /**
     * Clear the puzzle.
     */
    clear() {
        if (!confirm('Are you sure you want to clear all your answers?')) {
            return;
        }

        for (let row = 0; row < this.puzzle.size; row++) {
            for (let col = 0; col < this.puzzle.size; col++) {
                if (this.puzzle.grid[row][col] !== '.') {
                    this.grid[row][col] = '';
                }
            }
        }

        document.querySelectorAll('.cell').forEach(cell => {
            cell.classList.remove('revealed', 'correct', 'incorrect');
        });

        this.render();
    },

    /**
     * Get current grid state.
     */
    getGrid() {
        return this.grid;
    },
};
