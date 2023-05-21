<template>
    <div class="chart-container">
        <div class="instrument-chart">
            <div class="chart" ref="chart">
                <span v-if="this.activeSymbol">This is the chart for {{ this.activeSymbol }}</span>
                <span v-else>Select a symbol to see the chart</span>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    computed: {
        activeSymbol() {
            return this.$store.getters.activeSymbol
        }
    }
}
</script>

<style scoped>
.chart-container {
    height: 50vh;
    min-height: 400px;
    overflow: auto;
    resize: vertical;
    background-color: #000;
}

.instrument-chart {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

@media screen and (max-width: 1024px) {
    .chart-container {
        resize: none;
    }
}
</style>