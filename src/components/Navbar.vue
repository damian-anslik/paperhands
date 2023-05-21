<template>
    <nav>
        <div class="left">
            <router-link :to="isLoggedIn ? '/dashboard' : '/'">
                <span>
                    <i class="fa-solid fa-hand-peace"></i>
                    paperhands.io
                </span>
            </router-link>
        </div>
        <div class="right">
            <i class="fa-solid fa-bars" @click="toggleSidebar"></i>
            <div class="links">
                <div v-if="!isLoading && !isLoggedIn">
                    <router-link to="/login">
                        Login
                    </router-link>
                    <router-link to="/signup">
                        Signup
                    </router-link>
                </div>
                <div v-if="!isLoading && isLoggedIn">
                    <PortfolioSelector :portfolios="user.portfolios" :activePortfolio="this.$store.getters.activePortfolio" />
                    <router-link to="/portfolio/new">
                        Create Portfolio
                    </router-link>
                    <router-link to="/settings">
                        Settings
                    </router-link>
                    <button @click="logout">
                        Logout
                    </button>
                </div>
            </div>
        </div>
    </nav>
</template>

<script>
import PortfolioSelector from '@/components/PortfolioSelector.vue'
export default {
    name: 'Navbar',
    computed: {
        isLoggedIn() {
            return this.$store.getters.isAuthenticated
        },
        isLoading() {
            return this.$store.getters.isLoading
        },
        user() {
            return this.$store.getters.user
        }
    },
    methods: {
        logout() {
            this.$store.dispatch('logout')
        },
        toggleSidebar() {
            const links = document.querySelector('.links')
            links.classList.toggle('show')
            const icon = document.querySelector('.fa-bars')
            icon.classList.toggle('fa-times')

            // Close sidebar when clicking outside of it
            const app = document.querySelector('#app')
            app.addEventListener('click', (e) => {
                // If the click is on anything but the child or grandchild of the right div, close the sidebar
                if (!e.target.closest('.right')) {
                    links.classList.remove('show')
                    icon.classList.remove('fa-times')
                }
                // If the user clicks on an item in the sidebar, except the portfolio selector, close the sidebar
                if (e.target.closest('.links') && !e.target.closest('.portfolio-selector')) {
                    links.classList.remove('show')
                    icon.classList.remove('fa-times')
                }
            })
        }
    },
    components: {
        PortfolioSelector
    }
}
</script>

<style scoped>
nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1rem;
    position: sticky;
    top: 0;
    box-shadow: 0 1px 0 0 rgba(255, 255, 255, 0.1);
    background-color: rgba(13, 17, 23, 0.95);
    user-select: none;
    z-index: 1;
}

.links > div {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.left a,
.links a,
.links div button {
    background-color: transparent;
    border: none;
    color: #c9d1d9;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    padding: 0.25rem;
    font-size: 1rem;
    cursor: pointer;
    font-weight: bold;
}

.left a span {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.left a:hover,
.links a:hover,
.links button:hover {
    color: #4CAF50;
}

.right i {
    display: none;
    color: #c9d1d9;
    cursor: pointer;
}

@media (max-width: 768px) {
    .right i {
        display: block;
    }

    .links {
        display: none;
    }

    .links.show {
        display: flex;
        flex-direction: column;
        position: absolute;
        top: 3.5rem;
        right: 0.25rem;
        background-color: rgba(13, 17, 23, 1);
        padding: 0.5rem;
        box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1);
        z-index: 1;
        text-align: right;
        width: 50vw;
        max-width: 300px;
    }

    .links.show div {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        width: 100%;
    }

    .links.show div > * {
        width: 100%;
    }

    .links.show div button {
        padding-inline: 0;
    }

    /* Align any text to the left */
    .links.show div a, .links.show div button {
        text-align: left;
    }

    i {
        display: block;
    }
}
</style>