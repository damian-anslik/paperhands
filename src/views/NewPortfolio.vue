<template>
    <div>
        <h2>Create new portfolio</h2>
        <NewPortfolioForm />
    </div>
</template>

<script>
import NewPortfolioForm from '@/components/NewPortfolioForm.vue'
export default {
    components: {
        NewPortfolioForm
    }
}
</script>

<style scoped>
div {
    width: 100%;
    max-width: 700px;
    margin: 0 auto;
    text-align: left;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}
</style>