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
    padding: 10px 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    cursor: pointer;
    width: 200px;
}
</style>