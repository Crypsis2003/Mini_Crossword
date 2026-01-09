/**
 * API module for communicating with the backend.
 */
const API = {
    baseUrl: '/api',

    /**
     * Get stored auth token.
     */
    getToken() {
        return localStorage.getItem('access_token');
    },

    /**
     * Set auth token.
     */
    setToken(token) {
        localStorage.setItem('access_token', token);
    },

    /**
     * Remove auth token.
     */
    removeToken() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    },

    /**
     * Make an API request.
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const token = this.getToken();

        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(url, {
            ...options,
            headers,
        });

        if (response.status === 401) {
            // Token expired, try to refresh
            const refreshed = await this.refreshToken();
            if (refreshed) {
                // Retry the request
                headers['Authorization'] = `Bearer ${this.getToken()}`;
                const retryResponse = await fetch(url, {
                    ...options,
                    headers,
                });
                return this.handleResponse(retryResponse);
            } else {
                // Refresh failed, clear tokens
                this.removeToken();
                window.dispatchEvent(new Event('auth:logout'));
                throw new Error('Session expired. Please login again.');
            }
        }

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

    /**
     * Refresh access token.
     */
    async refreshToken() {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) return false;

        try {
            const response = await fetch(`${this.baseUrl}/auth/refresh`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh_token: refreshToken }),
            });

            if (response.ok) {
                const data = await response.json();
                this.setToken(data.access_token);
                localStorage.setItem('refresh_token', data.refresh_token);
                return true;
            }
        } catch (e) {
            console.error('Token refresh failed:', e);
        }

        return false;
    },

    // Auth endpoints
    auth: {
        async register(username, email, password) {
            return API.request('/auth/register', {
                method: 'POST',
                body: JSON.stringify({ username, email, password }),
            });
        },

        async login(username, password) {
            const data = await API.request('/auth/login', {
                method: 'POST',
                body: JSON.stringify({ username, password }),
            });
            API.setToken(data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
            return data;
        },

        async logout() {
            try {
                await API.request('/auth/logout', { method: 'POST' });
            } finally {
                API.removeToken();
            }
        },

        async getMe() {
            return API.request('/auth/me');
        },

        async getProfile() {
            return API.request('/auth/profile');
        },
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

        async solve(puzzleId, timeMs, grid) {
            return API.request(`/puzzles/${puzzleId}/solve`, {
                method: 'POST',
                body: JSON.stringify({
                    puzzle_id: puzzleId,
                    time_ms: timeMs,
                    grid: grid,
                }),
            });
        },

        async getMySolve(puzzleId) {
            return API.request(`/puzzles/${puzzleId}/my-solve`);
        },
    },

    // Friends endpoints
    friends: {
        async getList() {
            return API.request('/friends');
        },

        async sendRequest(username) {
            return API.request('/friends/request', {
                method: 'POST',
                body: JSON.stringify({ username }),
            });
        },

        async acceptRequest(requestId) {
            return API.request(`/friends/request/${requestId}/accept`, {
                method: 'POST',
            });
        },

        async rejectRequest(requestId) {
            return API.request(`/friends/request/${requestId}/reject`, {
                method: 'POST',
            });
        },

        async remove(friendId) {
            return API.request(`/friends/${friendId}`, {
                method: 'DELETE',
            });
        },

        async search(query) {
            return API.request(`/friends/search?q=${encodeURIComponent(query)}`);
        },
    },

    // Leaderboard endpoints
    leaderboard: {
        async getToday() {
            return API.request('/leaderboard/today');
        },

        async getForPuzzle(puzzleId) {
            return API.request(`/leaderboard/puzzle/${puzzleId}`);
        },

        async getFriendsToday() {
            return API.request('/leaderboard/friends/today');
        },
    },
};
