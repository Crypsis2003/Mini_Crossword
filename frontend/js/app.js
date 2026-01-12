/**
 * Main application module.
 */
const App = {
    currentPage: 'play',

    /**
     * Initialize the application.
     */
    async init() {
        // Set up navigation
        this.setupNavigation();

        // Set up event listeners
        this.setupEventListeners();

        // Load initial page
        this.navigate('play');
    },

    /**
     * Set up navigation links.
     */
    setupNavigation() {
        document.querySelectorAll('[data-page]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.navigate(link.dataset.page);
            });
        });
    },

    /**
     * Set up event listeners.
     */
    setupEventListeners() {
        // Start game button
        document.getElementById('btn-start').addEventListener('click', () => Crossword.startGame());

        // Game controls
        document.getElementById('btn-hint').addEventListener('click', () => Crossword.hint());
        document.getElementById('btn-check').addEventListener('click', () => Crossword.check());
        document.getElementById('btn-reveal').addEventListener('click', () => Crossword.reveal());
        document.getElementById('btn-clear').addEventListener('click', () => Crossword.clear());

        // Theme picker
        this.setupThemePicker();

        // Completion modal
        document.getElementById('close-completion').addEventListener('click', () => {
            document.getElementById('completion-modal').classList.remove('active');
        });

        document.getElementById('btn-copy-share').addEventListener('click', () => {
            const shareText = document.getElementById('share-text').textContent;
            navigator.clipboard.writeText(shareText);
            this.showToast('Copied to clipboard!', 'success');
        });

        document.getElementById('btn-view-leaderboard').addEventListener('click', () => {
            document.getElementById('completion-modal').classList.remove('active');
            this.navigate('leaderboard');
        });

        document.getElementById('btn-play-another').addEventListener('click', () => {
            document.getElementById('completion-modal').classList.remove('active');
            this.loadPracticePuzzle();
        });

        // Name entry modal
        document.getElementById('btn-submit-leaderboard').addEventListener('click', () => {
            Crossword.submitToLeaderboard();
        });

        document.getElementById('btn-skip-leaderboard').addEventListener('click', () => {
            Crossword.skipLeaderboard();
        });

        // Allow Enter key to submit name
        document.getElementById('leaderboard-name').addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                Crossword.submitToLeaderboard();
            }
        });
    },

    /**
     * Navigate to a page.
     */
    async navigate(page) {
        // Hide all pages
        document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));

        // Show target page
        const pageEl = document.getElementById(`page-${page}`);
        if (pageEl) {
            pageEl.classList.remove('hidden');
        }

        this.currentPage = page;

        // Load page data
        switch (page) {
            case 'play':
                await this.loadPuzzle();
                break;
            case 'leaderboard':
                await this.loadLeaderboard();
                break;
        }
    },

    /**
     * Load today's puzzle.
     */
    async loadPuzzle() {
        try {
            const puzzle = await API.puzzles.getToday();

            document.getElementById('puzzle-title').textContent = puzzle.title;
            document.getElementById('puzzle-meta').textContent =
                `${puzzle.size}x${puzzle.size} • ${puzzle.difficulty}`;

            Crossword.init(puzzle, false);
        } catch (e) {
            console.error('Error loading puzzle:', e);
            document.getElementById('puzzle-title').textContent = 'No puzzle available';
            document.getElementById('puzzle-meta').textContent = 'Check back later';
        }
    },

    /**
     * Load a random practice puzzle.
     */
    async loadPracticePuzzle() {
        try {
            // Exclude current puzzle if we have one
            const excludeId = Crossword.puzzle ? Crossword.puzzle.id : null;
            const puzzle = await API.puzzles.getPractice(excludeId);

            document.getElementById('puzzle-title').textContent = puzzle.title;
            document.getElementById('puzzle-meta').textContent =
                `${puzzle.size}x${puzzle.size} • ${puzzle.difficulty} • Practice Mode`;

            Crossword.init(puzzle, true);
            this.showToast('Practice mode - time not recorded on leaderboard', 'info');
        } catch (e) {
            console.error('Error loading practice puzzle:', e);
            this.showToast('No more practice puzzles available', 'error');
        }
    },

    /**
     * Load leaderboard.
     */
    async loadLeaderboard() {
        try {
            const data = await API.leaderboard.getToday();

            // Show puzzle date
            const dateEl = document.getElementById('leaderboard-date');
            if (dateEl && data.puzzle_date) {
                const date = new Date(data.puzzle_date + 'T00:00:00');
                dateEl.textContent = date.toLocaleDateString('en-US', {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                });
            }

            // Render leaderboard
            const tbody = document.getElementById('leaderboard-global');
            const emptyEl = document.getElementById('leaderboard-empty');
            tbody.innerHTML = '';

            if (data.entries && data.entries.length > 0) {
                emptyEl.classList.add('hidden');
                data.entries.forEach(entry => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td><span class="rank-badge rank-${entry.rank <= 3 ? entry.rank : ''}">${entry.rank}</span></td>
                        <td>${this.escapeHtml(entry.name)}</td>
                        <td>${this.formatTime(entry.time_ms)}</td>
                    `;
                    tbody.appendChild(tr);
                });
            } else {
                emptyEl.classList.remove('hidden');
            }
        } catch (e) {
            console.error('Error loading leaderboard:', e);
            this.showToast('Error loading leaderboard', 'error');
        }
    },

    /**
     * Escape HTML to prevent XSS.
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    /**
     * Format time in milliseconds to MM:SS.
     */
    formatTime(ms) {
        const minutes = Math.floor(ms / 60000);
        const seconds = Math.floor((ms % 60000) / 1000);
        return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    },

    /**
     * Show a toast notification.
     */
    showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;

        container.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3000);
    },

    /**
     * Set up theme picker functionality.
     */
    setupThemePicker() {
        // Load saved theme
        const savedTheme = localStorage.getItem('crossword-theme') || 'default';
        this.applyTheme(savedTheme);

        // Add click listeners to theme buttons
        document.querySelectorAll('.theme-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const theme = btn.dataset.theme;
                this.applyTheme(theme);
                localStorage.setItem('crossword-theme', theme);
            });
        });
    },

    /**
     * Apply a theme to the page.
     */
    applyTheme(theme) {
        // Set data-theme attribute on document element
        if (theme === 'default') {
            document.documentElement.removeAttribute('data-theme');
        } else {
            document.documentElement.setAttribute('data-theme', theme);
        }

        // Update active state on buttons
        document.querySelectorAll('.theme-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.theme === theme);
        });
    },
};

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => App.init());
