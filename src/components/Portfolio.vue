<template>
    <div class="portfolio-container">
        <div>
            <h2>Place an order</h2>
            <OrderForm :portfolioId="portfolio.id" :availableSymbols="availableSymbols" />
        </div>
        <div>
            <h2>Active orders</h2>
            <div class="orders-list">
                <Order v-if="portfolio.orders && portfolio.orders.length > 0" v-for="order in portfolio.orders" :key="order.id" :order="order" />
                <p v-else>You do not currently have any active orders</p>
            </div>
        </div>
        <div>
            <h2>Positions</h2>
            <div class="positions-list">
                <Position v-if="portfolio.positions && portfolio.positions.length > 0" v-for="position in portfolio.positions" :key="position.id"  :position="position" /> 
                <p v-else>You do not currently have any positions</p>
            </div>
        </div>
    </div>
</template>

<script>
import OrderForm from '@/components/OrderForm.vue'
import Order from '@/components/Order.vue'
import Position from '@/components/Position.vue'
export default {
    name: "Portfolio",
    props: {
        portfolio: {
            type: Object,
            required: true
        }
    },
    components: {
        OrderForm,
        Order,
        Position
    },
    computed: {
        availableSymbols() {
            return this.$store.getters.availableSymbols
        }
    }
}
</script>
        
<style scoped>
.positions-list, .orders-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-gap: 20px;
}
</style>