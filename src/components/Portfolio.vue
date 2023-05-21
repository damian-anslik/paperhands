<template>
    <div class="portfolio-container">
        <div class="tab-selector">
            <div :class="{ active: activeTab === 'Positions' }" @click="() => activeTabChanged('Positions')">Positions</div>
            <div :class="{ active: activeTab === 'Orders' }" @click="() => activeTabChanged('Orders')">Orders</div>
        </div>
        <div v-if="activeTab === 'Positions'">
            <Positions :positions="portfolio.positions" />
        </div>
        <div v-else>
            <Orders :orders="portfolio.orders" />
        </div>
    </div>
</template>

<script>
import Orders from '@/components/Orders.vue'
import Positions from '@/components/Positions.vue'
import Chart from '@/components/Chart.vue'
export default {
    name: "Portfolio",
    props: {
        portfolio: {
            type: Object,
            required: true
        }
    },
    components: {
        Orders,
        Positions,
        Chart
    },
    computed: {
        availableSymbols() {
            return this.$store.getters.availableSymbols
        },
        activeTab() {
            return this.$store.getters.activeTab
        }
    },
    methods: {
        activeTabChanged(tab) {
            this.$store.commit('setActiveTab', tab)
        }
    },
    data() {
        return {
            tabs: ['Positions', 'Orders']
        }
    }
}
</script>
        
<style scoped>
.positions-list,
.orders-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-gap: 20px;
}

.tab-selector {
    display: flex;
}

.tab-selector div {
    cursor: pointer;
    padding: 0.5rem 1rem;
    border-bottom: none;
    color: #c9d1d9;
    user-select: none;
}

.tab-selector div.active {
    background-color: #161b22;
    border-bottom: 2px solid #c9d1d9;
}
</style>