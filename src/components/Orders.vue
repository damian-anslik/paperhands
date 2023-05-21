<template>
    <div class="table-container">
        <table v-if="orders.length">
            <thead>
                <tr>
                    <th>Symbol</th>
                    <th>Quantity</th>
                    <th>Order type</th>
                    <th>Price</th>
                    <th>Side</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="order in orders" :key="order.id">
                    <td>
                        <a href="#" @click.prevent="setActiveSymbol(order.symbol)">
                            {{ order.symbol }}
                        </a>
                    </td>
                    <td>{{ order.quantity }}</td>
                    <td>{{ order.order_type }}</td>
                    <td>{{ order.limit_price ? order.limit_price.toFixed(2) : "" }}</td>
                    <td>{{ order.side }}</td>
                    <td><button @click="cancel(order.id)">Cancel</button></td>
                </tr>
            </tbody>
        </table>
        <div v-else>
            <div class="empty">
                <i class="fa-solid fa-cart-shopping"></i>
                <p>No active orders</p>
            </div>
        </div>
    </div>
</template>

<script>
import controller from "@/controller";
export default {
    name: "Order",
    props: {
        orders: {
            type: Array,
            required: true
        }
    },
    methods: {
        cancel(orderId) {
            controller.cancelOrder(orderId)
                .then(response => {
                    this.$store.dispatch("cancelOrder", orderId)
                })
                .catch(error => {
                    console.log(error)
                })
        },
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
    padding: 0.5rem 1rem;
}

button {
    background-color: red;
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 0.25rem 0.5rem;
    cursor: pointer;
}

a {
    cursor: pointer;
    color: #2c3e50;
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