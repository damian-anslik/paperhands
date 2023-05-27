<template>
    <div class="table-container">
        <table v-if="positions && positions.length > 0">
            <thead>
                <tr>
                    <th>Symbol</th>
                    <th>Quantity</th>
                    <th>Side</th>
                    <th>Unrealized PnL</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="position in positions" :key="position.id">
                    <td>
                        <a href="#" @click.prevent="setActiveSymbol(position.symbol)">
                            {{ position.symbol }}
                        </a>
                    </td>
                    <td>{{ position.quantity }}</td>
                    <td>{{ position.side }}</td>
                    <td></td>
                </tr>
            </tbody>
        </table>
        <div v-else>
            <div class="empty">
                <i class="fa-solid fa-folder-open"></i>
                <p>No open positions</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "Position",
    props: {
        positions: {
            type: Array,
            required: true
        }
    },
    methods: {
        setActiveSymbol(symbol) {
            this.$store.commit("setActiveSymbol", symbol)
        }
    }
}
</script>