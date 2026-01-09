/**
 * Crossword game module.
 */
const Crossword = {
    puzzle: null,
    grid: [],
    selectedCell: null,
    direction: 'across', // 'across' or 'down'
    timerInterval: null,
    startTime: null,
    elapsedMs: 0,
    isCompleted: false,
    hasStarted: false,

    /**
     * Initialize the crossword with a puzzle.
     */
    init(puzzle) {
        this.puzzle = puzzle;
        this.grid = [];
        this.selectedCell = null;
        this.direction = 'across';
        this.isCompleted = false;
        this.hasStarted = false;
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
    },

    /**
     * Render the crossword grid.
     */
    render() {
        const container = document.getElementById('crossword-grid');
        container.innerHTML = '';
        container.style.gridTemplateColumns = `repeat(${this.puzzle.size}, 48px)`;

        // Build cell number map
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
                    // Add cell number if exists
                    const number = cellNumbers[`${row}-${col}`];
                    if (number) {
                        const numSpan = document.createElement('span');
                        numSpan.className = 'cell-number';
                        numSpan.textContent = number;
                        cell.appendChild(numSpan);
                    }

                    // Add input for letter
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
        if (this.selectedCell && this.selectedCell.row === row && this.selectedCell.col === col) {
            // Toggle direction if clicking same cell
            this.direction = this.direction === 'across' ? 'down' : 'across';
        }
        this.selectCell(row, col);
    },

    /**
     * Handle clue click.
     */
    handleClueClick(clue, direction) {
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
        // Clear all highlights
        document.querySelectorAll('.cell').forEach(cell => {
            cell.classList.remove('selected', 'highlighted');
        });

        if (!this.selectedCell) return;

        const { row, col } = this.selectedCell;

        // Highlight selected cell
        const selectedCell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
        if (selectedCell) {
            selectedCell.classList.add('selected');
        }

        // Highlight word cells
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
            // Find start of word
            let startCol = col;
            while (startCol > 0 && this.puzzle.grid[row][startCol - 1] !== '.') {
                startCol--;
            }
            // Collect word cells
            for (let c = startCol; c < this.puzzle.size && this.puzzle.grid[row][c] !== '.'; c++) {
                cells.push({ r: row, c });
            }
        } else {
            // Find start of word
            let startRow = row;
            while (startRow > 0 && this.puzzle.grid[startRow - 1][col] !== '.') {
                startRow--;
            }
            // Collect word cells
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

        // Find the clue that contains this cell
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
        if (!this.hasStarted) {
            this.startTimer();
        }

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
            // Switch direction and go to first clue
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
            // Switch direction and go to last clue
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
        // Check if all cells are filled
        for (let row = 0; row < this.puzzle.size; row++) {
            for (let col = 0; col < this.puzzle.size; col++) {
                if (this.puzzle.grid[row][col] !== '.' && !this.grid[row][col]) {
                    return false;
                }
            }
        }

        // All cells filled, verify with server
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
        document.getElementById('timer').classList.add('completed');

        // Submit solve if logged in
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
    },

    /**
     * Show completion modal.
     */
    showCompletionModal(result) {
        const minutes = Math.floor(this.elapsedMs / 60000);
        const seconds = Math.floor((this.elapsedMs % 60000) / 1000);

        document.getElementById('completion-time').textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;

        if (result.rank) {
            document.getElementById('completion-rank').textContent = `You ranked #${result.rank}!`;
        } else if (!Auth.isLoggedIn()) {
            document.getElementById('completion-rank').textContent = 'Login to save your time!';
        }

        if (result.share_text) {
            document.getElementById('share-text').textContent = result.share_text;
        }

        document.getElementById('completion-modal').classList.add('active');
    },

    /**
     * Check the puzzle (highlight incorrect cells).
     */
    async check() {
        try {
            const result = await API.puzzles.check(this.puzzle.id, this.grid);

            // Clear previous check highlights
            document.querySelectorAll('.cell').forEach(cell => {
                cell.classList.remove('correct', 'incorrect');
            });

            // Highlight cells
            for (let row = 0; row < this.puzzle.size; row++) {
                for (let col = 0; col < this.puzzle.size; col++) {
                    if (this.puzzle.grid[row][col] === '.') continue;

                    const cell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
                    if (this.grid[row][col]) {
                        const isIncorrect = result.incorrect_cells.some(([r, c]) => r === row && c === col);
                        cell.classList.add(isIncorrect ? 'incorrect' : 'correct');
                    }
                }
            }

            // Clear highlights after 2 seconds
            setTimeout(() => {
                document.querySelectorAll('.cell').forEach(cell => {
                    cell.classList.remove('correct', 'incorrect');
                });
            }, 2000);
        } catch (e) {
            App.showToast('Error checking puzzle', 'error');
        }
    },

    /**
     * Reveal the puzzle solution.
     */
    reveal() {
        if (!confirm('Are you sure you want to reveal the solution? This will stop the timer.')) {
            return;
        }

        this.stopTimer();
        // Note: In a real app, we'd fetch the solution from the server
        // For now, we just show a message
        App.showToast('Solution reveal not implemented for security', 'info');
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

        this.render();
    },

    /**
     * Get current grid state.
     */
    getGrid() {
        return this.grid;
    },
};
