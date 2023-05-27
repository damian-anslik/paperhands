<template>
    <div class="table-container">
        <table v-if="orders && orders.length > 0">
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