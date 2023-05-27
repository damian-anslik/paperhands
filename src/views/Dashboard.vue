<template>
    <div v-if="activePortfolio" class="dashboard-container">
        <div class="portfolio-container">
            <Chart />
            <Portfolio v-if="activePortfolio" :portfolio="activePortfolio" />
        </div>
        <div class="sidebar-container">
            <OrderForm :portfolioId="activePortfolio.id" :availableSymbols="availableSymbols" />
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