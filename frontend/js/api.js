/**
 * API module for communicating with the backend.
 */
const API = {
    baseUrl: '/api',

    /**
     * Make an API request.
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;

        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        const response = await fetch(url, {
            ...options,
            headers,
        });

        return this.handleResponse(response);
    },

    /**
     * Handle API response.
     */
    async handleResponse(response) {
        const data = await response.json().catch(() => null);

        if (!response.ok) {
            const error = new Error(data?.detail || 'An error occurred');
            error.status = response.status;
            error.data = data;
            throw error;
        }

        return data;
    },

    // Puzzle endpoints
    puzzles: {
        async getToday() {
            return API.request('/puzzles/today');
        },

        async getById(id) {
            return API.request(`/puzzles/${id}`);
        },

        async getByDate(date) {
            return API.request(`/puzzles/date/${date}`);
        },

        async check(puzzleId, grid) {
            return API.request(`/puzzles/${puzzleId}/check`, {
                method: 'POST',
                body: JSON.stringify(grid),
            });
        },

        async getSolution(puzzleId) {
            return API.request(`/puzzles/${puzzleId}/solution`);
        },

        async getPractice(excludeId = null) {
            const url = excludeId ? `/puzzles/practice/random?exclude=${excludeId}` : '/puzzles/practice/random';
            return API.request(url);
        },
    },

    // Leaderboard endpoints
    leaderboard: {
        async getToday() {
            return API.request('/leaderboard/today');
        },

        async submit(name, timeMs, puzzleDate = null) {
            const body = {
                name: name || 'Anonymous',
                time_ms: timeMs,
            };
            if (puzzleDate) {
                body.puzzle_date = puzzleDate;
            }
            return API.request('/leaderboard/submit', {
                method: 'POST',
                body: JSON.stringify(body),
            });
        },
    },
};
