<template>
    <nav>
        <div class="left">
            <router-link :to="isLoggedIn ? '/dashboard' : '/'">
                paperhands.io
            </router-link>
        </div>
        <div class="right" v-if="!isLoading && !isLoggedIn">
            <router-link to="/login">Login</router-link>
            <router-link to="/signup">Signup</router-link>
        </div>
        <div class="right" v-if="!isLoading && isLoggedIn">
            <PortfolioSelector :portfolios="user.portfolios" :activePortfolio="this.$store.getters.activePortfolio" />
            <router-link to="/portfolio/new">New Portfolio</router-link>
            <router-link to="/settings">Settings</router-link>
            <button @click="logout">Logout</button>
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
    position: sticky;
}

.right {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.left a,
.right a,
.right button {
    background-color: #4CAF50;
    border: none;
    color: white;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    font-weight: bold;
    border-radius: 5px;
}
</style>