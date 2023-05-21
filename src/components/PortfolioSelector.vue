<template>
    <select v-if="portfolios.length > 0" @change="setActivePortfolio($event.target.value)" class="portfolio-selector">
        <option v-for="portfolio in portfolios" :key="portfolio.id" :value="portfolio.id" :selected="portfolio.id === activePortfolio.id">
            {{ portfolio.name }}
        </option>
    </select>
</template>

<script>
import controller from '@/controller';
export default {
    name: 'PortfolioSelector',
    props: {
        portfolios: {
            type: Array,
            required: true
        },
        activePortfolio: {
            type: Object,
            required: true
        }
    },
    methods: {
        setActivePortfolio(portfolioId) {
            controller.portfolioData(portfolioId)
                .then(response => {
                    this.$store.dispatch('setActivePortfolio', response.data)
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}
</script>

<style scoped>
.portfolio-selector {
    border: 1px solid rgba(255, 255, 255, 0.1);
    cursor: pointer;
    width: 200px;
    padding: 0.25rem 0.5rem;
    background-color: #161b22;
    color: #c9d1d9;
    font-size: 1rem;
}
</style>