<template>
    <div class="table-container">
        <table v-if="positions && positions.length > 0">
            <thead>
                <tr>
                    <th>Symbol</th>
                    <th>Quantity</th>
                    <th>Price</th>
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
                    <td>{{ position.price }}</td>
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

<style scoped>
.table-container {
    width: 100%;
    overflow-x: auto;
}

table {
    width: 100%;
}

table thead {
    background-color: #161b22;
    color: #c9d1d9;
}

table thead th {
    padding: 0.5rem 1rem;
    white-space: nowrap;
}

table tbody tr:nth-child(even) {
    background-color: #161b22;
}

table tbody tr:nth-child(odd) {
    background-color: #0d1117;
}

table tbody td {
    padding: 0.75rem 1rem;
}

a {
    cursor: pointer;
    color: #c9d1d9;
    font-weight: bold;
    text-decoration: none;
}

a:hover {
    color: #4CAF50;
    text-decoration: underline;
}

.empty {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    color: #2c3e50;;
    padding-block: 1rem;
    user-select: none;
}
</style>