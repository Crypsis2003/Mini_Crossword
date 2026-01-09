/**
 * Authentication module.
 */
const Auth = {
    currentUser: null,

    /**
     * Check if user is logged in.
     */
    isLoggedIn() {
        return !!API.getToken();
    },

    /**
     * Load current user.
     */
    async loadUser() {
        if (!this.isLoggedIn()) {
            this.currentUser = null;
            return null;
        }

        try {
            this.currentUser = await API.auth.getMe();
            return this.currentUser;
        } catch (e) {
            console.error('Failed to load user:', e);
            this.currentUser = null;
            return null;
        }
    },

    /**
     * Register a new user.
     */
    async register(username, email, password) {
        const user = await API.auth.register(username, email, password);
        // Auto-login after registration
        await this.login(username, password);
        return user;
    },

    /**
     * Login user.
     */
    async login(username, password) {
        const data = await API.auth.login(username, password);
        await this.loadUser();
        window.dispatchEvent(new Event('auth:login'));
        return data;
    },

    /**
     * Logout user.
     */
    async logout() {
        try {
            await API.auth.logout();
        } catch (e) {
            console.error('Logout error:', e);
        }
        this.currentUser = null;
        window.dispatchEvent(new Event('auth:logout'));
    },

    /**
     * Get user profile with stats.
     */
    async getProfile() {
        return API.auth.getProfile();
    },

    /**
     * Update UI based on auth state.
     */
    updateUI() {
        const isLoggedIn = this.isLoggedIn();

        // Show/hide nav items
        document.getElementById('nav-login').classList.toggle('hidden', isLoggedIn);
        document.getElementById('nav-register').classList.toggle('hidden', isLoggedIn);
        document.getElementById('nav-logout').classList.toggle('hidden', !isLoggedIn);
        document.getElementById('nav-profile').classList.toggle('hidden', !isLoggedIn);
        document.getElementById('nav-friends').classList.toggle('hidden', !isLoggedIn);
    },
};

// Listen for auth events
window.addEventListener('auth:login', () => Auth.updateUI());
window.addEventListener('auth:logout', () => {
    Auth.updateUI();
    App.navigate('play');
});
