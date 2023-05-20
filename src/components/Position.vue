<template>
    <div class="position-container">
        <span>{{ position.symbol }}</span>
        <span>{{ position.quantity }}</span>
        <span>{{ position.price }}</span>
        <span>{{ position.side }}</span>
    </div>
</template>

<script>
export default {
    name: "Position",
    props: {
        position: {
            type: Object,
            required: true
        }
    }
}
</script>

<style scoped>
.position-container {
    border: 1px solid #ccc;
    border-radius: 5px;
    display: flex;
    flex-direction: column;
}
</style>