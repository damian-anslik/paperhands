<template>
    <div v-if="activePortfolio">
        <div class="dashboard-container">
            <div class="portfolio-container">
                <Chart />
                <Portfolio v-if="activePortfolio" :portfolio="activePortfolio" />
            </div>
            <div class="sidebar-container">
                <OrderForm :portfolioId="activePortfolio.id" :availableSymbols="availableSymbols" />
            </div>
        </div>
    </div>
    <div v-else class="empty-portfolios">
        <h2>You don't have any portfolios yet.</h2>
    </div>
</template>
  
<script>
import Portfolio from '@/components/Portfolio.vue'
import NewPortfolioForm from '@/components/NewPortfolioForm.vue'
import OrderForm from '@/components/OrderForm.vue'
import Chart from '@/components/Chart.vue'
export default {
    components: {
        Portfolio,
        NewPortfolioForm,
        OrderForm,
        Chart,
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
.dashboard-container {
    display: flex;
    flex: 1;
    z-index: -1;
    gap: 1rem;
}

.portfolio-container {
    flex: 1;
    padding-block: 1rem;
}

.sidebar-container {
    flex: 0 0 270px;
    padding-block: 1rem;
}

.empty-portfolios {
    /* Show in middle of screen */
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
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