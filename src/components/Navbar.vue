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
                    <PortfolioSelector :portfolios="user.portfolios"
                        :activePortfolio="this.$store.getters.activePortfolio" />
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