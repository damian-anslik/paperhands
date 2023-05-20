<template>
    <div class="dashboard-container">
        <div class="portfolio-container">
            <Portfolio v-if="activePortfolio" :portfolio="activePortfolio" />
            <div v-else>
                <h2>You don't have any portfolios yet.</h2>
                <router-link to="/portfolio/new">Create a new portfolio</router-link>
            </div>
        </div>
        <div class="sidebar-container">
        </div>
    </div>
</template>
  
<script>
import Portfolio from '@/components/Portfolio.vue'
import NewPortfolioForm from '@/components/NewPortfolioForm.vue'
export default {
    components: {
        Portfolio,
        NewPortfolioForm
    },
    computed: {
        user() {
            return this.$store.getters.user
        },
        activePortfolio() {
            return this.$store.getters.activePortfolio
        }
    }
}
</script>
  
<style scoped>
.dashboard-container {
    display: flex;
    margin-top: 1rem;
    gap: 1rem;
    flex: 1;
}

.portfolio-container {
    text-align: left;
    flex: 2;
}

.sidebar-container {
    background-color: #F2F2F2;
    padding: 0;
    flex: 1;
}

/* On small and medium devices show the sidebar container below the portfolio */
@media screen and (max-width: 900px) {
    .dashboard-container {
        flex-direction: column;
    }
}
</style>