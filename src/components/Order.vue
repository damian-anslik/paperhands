<template>
    <div class="order-container">
        <span>{{ order.symbol }}</span>
        <span>{{ order.quantity }}</span>
        <span>{{ order.order_type }}</span>
        <span>{{ order.side }}</span>
        <span :v-if="order.limit_price">{{ order.limit_price }}</span>
        <!-- Cancel button -->
        <button @click="cancel(order.id)">Cancel</button>
    </div>
</template>

<script>
import controller from "@/controller";
export default {
    name: "Order",
    props: {
        order: {
            type: Object,
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
        }
    }
}
</script>

<style scoped>
.order-container {
    border: 1px solid #ccc;
    border-radius: 5px;
    display: flex;
    flex-direction: column;
}
</style>