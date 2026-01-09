/**
 * Main application module.
 */
const App = {
    currentPage: 'play',

    /**
     * Initialize the application.
     */
    async init() {
        // Load user if logged in
        await Auth.loadUser();
        Auth.updateUI();

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
        // Login form
        document.getElementById('login-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleLogin();
        });

        // Register form
        document.getElementById('register-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleRegister();
        });

        // Logout button
        document.getElementById('nav-logout').addEventListener('click', async () => {
            await Auth.logout();
            this.showToast('Logged out successfully', 'success');
        });

        // Game controls
        document.getElementById('btn-check').addEventListener('click', () => Crossword.check());
        document.getElementById('btn-reveal').addEventListener('click', () => Crossword.reveal());
        document.getElementById('btn-clear').addEventListener('click', () => Crossword.clear());

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

        // Add friend button
        document.getElementById('btn-add-friend').addEventListener('click', () => this.handleAddFriend());

        // Tab switching
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => this.switchTab(tab));
        });
    },

    /**
     * Navigate to a page.
     */
    async navigate(page) {
        // Check auth for protected pages
        if (['friends', 'profile'].includes(page) && !Auth.isLoggedIn()) {
            this.navigate('login');
            return;
        }

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
            case 'friends':
                await this.loadFriends();
                break;
            case 'profile':
                await this.loadProfile();
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

            Crossword.init(puzzle);

            // Check if user has already solved
            if (Auth.isLoggedIn()) {
                const solve = await API.puzzles.getMySolve(puzzle.id);
                if (solve.solved) {
                    this.showToast(`You've already solved this! Time: ${this.formatTime(solve.time_ms)}`, 'info');
                }
            }
        } catch (e) {
            console.error('Error loading puzzle:', e);
            document.getElementById('puzzle-title').textContent = 'No puzzle available';
            document.getElementById('puzzle-meta').textContent = 'Check back later';
        }
    },

    /**
     * Load leaderboard.
     */
    async loadLeaderboard() {
        try {
            const data = await API.leaderboard.getToday();

            // Render global leaderboard
            const globalTbody = document.getElementById('leaderboard-global');
            globalTbody.innerHTML = '';

            data.entries.forEach(entry => {
                const tr = document.createElement('tr');
                if (entry.is_current_user) tr.classList.add('current-user');
                if (entry.is_friend) tr.classList.add('friend');

                tr.innerHTML = `
                    <td><span class="rank-badge rank-${entry.rank <= 3 ? entry.rank : ''}">${entry.rank}</span></td>
                    <td>${entry.username}${entry.is_current_user ? ' (you)' : ''}</td>
                    <td>${this.formatTime(entry.time_ms)}</td>
                `;
                globalTbody.appendChild(tr);
            });

            // Render friends leaderboard
            const friendsTbody = document.getElementById('leaderboard-friends');
            friendsTbody.innerHTML = '';

            if (Auth.isLoggedIn()) {
                document.getElementById('friends-leaderboard-login').classList.add('hidden');

                data.friends_entries.forEach(entry => {
                    const tr = document.createElement('tr');
                    if (entry.is_current_user) tr.classList.add('current-user');

                    tr.innerHTML = `
                        <td><span class="rank-badge rank-${entry.rank <= 3 ? entry.rank : ''}">${entry.rank}</span></td>
                        <td>${entry.username}${entry.is_current_user ? ' (you)' : ''}</td>
                        <td>${this.formatTime(entry.time_ms)}</td>
                    `;
                    friendsTbody.appendChild(tr);
                });

                if (data.friends_entries.length === 0) {
                    friendsTbody.innerHTML = '<tr><td colspan="3">No friends have solved today\'s puzzle yet.</td></tr>';
                }
            } else {
                document.getElementById('friends-leaderboard-login').classList.remove('hidden');
            }
        } catch (e) {
            console.error('Error loading leaderboard:', e);
            this.showToast('Error loading leaderboard', 'error');
        }
    },

    /**
     * Load friends list.
     */
    async loadFriends() {
        try {
            const data = await API.friends.getList();

            // Render friends list
            const friendsList = document.getElementById('friends-list');
            friendsList.innerHTML = '';

            if (data.friends.length === 0) {
                friendsList.innerHTML = '<li class="friend-item">No friends yet. Add some!</li>';
            } else {
                data.friends.forEach(friend => {
                    const li = document.createElement('li');
                    li.className = 'friend-item';
                    li.innerHTML = `
                        <div class="friend-info">
                            <div class="friend-avatar">${friend.username[0].toUpperCase()}</div>
                            <div>
                                <div class="friend-name">${friend.username}</div>
                                <div class="friend-stats">
                                    ${friend.total_solves} puzzles solved
                                    ${friend.average_time_ms ? ` • Avg: ${this.formatTime(friend.average_time_ms)}` : ''}
                                </div>
                            </div>
                        </div>
                        <button class="btn btn-secondary btn-sm" onclick="App.removeFriend(${friend.id})">Remove</button>
                    `;
                    friendsList.appendChild(li);
                });
            }

            // Render received requests
            const receivedList = document.getElementById('received-requests');
            receivedList.innerHTML = '';

            if (data.pending_received.length === 0) {
                receivedList.innerHTML = '<li class="friend-item">No pending requests</li>';
            } else {
                data.pending_received.forEach(req => {
                    const li = document.createElement('li');
                    li.className = 'friend-item';
                    li.innerHTML = `
                        <div class="friend-info">
                            <div class="friend-avatar">${req.sender_username[0].toUpperCase()}</div>
                            <div class="friend-name">${req.sender_username}</div>
                        </div>
                        <div>
                            <button class="btn btn-success btn-sm" onclick="App.acceptRequest(${req.id})">Accept</button>
                            <button class="btn btn-secondary btn-sm" onclick="App.rejectRequest(${req.id})">Reject</button>
                        </div>
                    `;
                    receivedList.appendChild(li);
                });
            }

            // Render sent requests
            const sentList = document.getElementById('sent-requests');
            sentList.innerHTML = '';

            if (data.pending_sent.length === 0) {
                sentList.innerHTML = '<li class="friend-item">No pending sent requests</li>';
            } else {
                data.pending_sent.forEach(req => {
                    const li = document.createElement('li');
                    li.className = 'friend-item';
                    li.innerHTML = `
                        <div class="friend-info">
                            <div class="friend-avatar">${req.receiver_username[0].toUpperCase()}</div>
                            <div class="friend-name">${req.receiver_username}</div>
                        </div>
                        <span style="color: var(--text-secondary);">Pending</span>
                    `;
                    sentList.appendChild(li);
                });
            }

            // Update badge
            const badge = document.getElementById('requests-badge');
            if (data.pending_received.length > 0) {
                badge.textContent = `(${data.pending_received.length})`;
            } else {
                badge.textContent = '';
            }
        } catch (e) {
            console.error('Error loading friends:', e);
            this.showToast('Error loading friends', 'error');
        }
    },

    /**
     * Load user profile.
     */
    async loadProfile() {
        try {
            const profile = await Auth.getProfile();

            document.getElementById('profile-avatar').textContent = profile.username[0].toUpperCase();
            document.getElementById('profile-username').textContent = profile.username;
            document.getElementById('profile-email').textContent = profile.email;
            document.getElementById('profile-joined').textContent =
                `Joined ${new Date(profile.created_at).toLocaleDateString()}`;

            document.getElementById('stat-solves').textContent = profile.total_solves;
            document.getElementById('stat-avg-time').textContent =
                profile.average_time_ms ? this.formatTime(profile.average_time_ms) : '--:--';
            document.getElementById('stat-best-time').textContent =
                profile.best_time_ms ? this.formatTime(profile.best_time_ms) : '--:--';
            document.getElementById('stat-friends').textContent = profile.friends_count;
        } catch (e) {
            console.error('Error loading profile:', e);
            this.showToast('Error loading profile', 'error');
        }
    },

    /**
     * Handle login form submission.
     */
    async handleLogin() {
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        const errorEl = document.getElementById('login-error');

        errorEl.classList.add('hidden');

        try {
            await Auth.login(username, password);
            this.showToast('Logged in successfully!', 'success');
            this.navigate('play');
        } catch (e) {
            errorEl.textContent = e.message;
            errorEl.classList.remove('hidden');
        }
    },

    /**
     * Handle register form submission.
     */
    async handleRegister() {
        const username = document.getElementById('register-username').value;
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
        const errorEl = document.getElementById('register-error');

        errorEl.classList.add('hidden');

        try {
            await Auth.register(username, email, password);
            this.showToast('Account created successfully!', 'success');
            this.navigate('play');
        } catch (e) {
            errorEl.textContent = e.message;
            errorEl.classList.remove('hidden');
        }
    },

    /**
     * Handle add friend button click.
     */
    async handleAddFriend() {
        const username = document.getElementById('friend-username').value.trim();

        if (!username) {
            this.showToast('Please enter a username', 'error');
            return;
        }

        try {
            await API.friends.sendRequest(username);
            this.showToast('Friend request sent!', 'success');
            document.getElementById('friend-username').value = '';
            await this.loadFriends();
        } catch (e) {
            this.showToast(e.message, 'error');
        }
    },

    /**
     * Accept a friend request.
     */
    async acceptRequest(requestId) {
        try {
            await API.friends.acceptRequest(requestId);
            this.showToast('Friend request accepted!', 'success');
            await this.loadFriends();
        } catch (e) {
            this.showToast(e.message, 'error');
        }
    },

    /**
     * Reject a friend request.
     */
    async rejectRequest(requestId) {
        try {
            await API.friends.rejectRequest(requestId);
            this.showToast('Friend request rejected', 'success');
            await this.loadFriends();
        } catch (e) {
            this.showToast(e.message, 'error');
        }
    },

    /**
     * Remove a friend.
     */
    async removeFriend(friendId) {
        if (!confirm('Are you sure you want to remove this friend?')) {
            return;
        }

        try {
            await API.friends.remove(friendId);
            this.showToast('Friend removed', 'success');
            await this.loadFriends();
        } catch (e) {
            this.showToast(e.message, 'error');
        }
    },

    /**
     * Switch tab.
     */
    switchTab(tab) {
        const tabId = tab.dataset.tab;
        const container = tab.closest('.card');

        // Update tab buttons
        container.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        // Update tab content
        container.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        container.querySelector(`#tab-${tabId}`).classList.add('active');
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
};

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => App.init());
