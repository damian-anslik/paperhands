<template>
    <SessionTimeoutDialog />
    <div class="dashboard-container">
        <div class="portfolio-container">
            <Chart />
            <Portfolio v-if="activePortfolio" :portfolio="activePortfolio" />
            <div v-else>
                <h2>You don't have any portfolios yet.</h2>
                <router-link to="/portfolio/new">Create a new portfolio</router-link>
            </div>
        </div>
        <div class="sidebar-container">
            <OrderForm :portfolioId="activePortfolio.id" :availableSymbols="availableSymbols" />
        </div>
    </div>
</template>
  
<script>
import Portfolio from '@/components/Portfolio.vue'
import NewPortfolioForm from '@/components/NewPortfolioForm.vue'
import OrderForm from '@/components/OrderForm.vue'
import Chart from '@/components/Chart.vue'
import SessionTimeoutDialog from '@/components/SessionTimeoutDialog.vue'
export default {
    components: {
        Portfolio,
        NewPortfolioForm,
        OrderForm,
        Chart,
        SessionTimeoutDialog
    },
    data() {
        return {
            availableSymbols: []
        }
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
/* TODO portfolio-container and sidebar-container should scroll independently */
.dashboard-container {
    display: flex;
    flex: 1;
    z-index: -1;
}

.portfolio-container {
    flex: 1;
}

.sidebar-container {
    flex: 0 0 290px;
}

@media screen and (max-width: 1024px) {
    .dashboard-container {
        flex-direction: column;
    }

    .sidebar-container {
        display: none;
    }
}
</style>