<template>
    <div>
        <div v-if="portfolio">
            <h2>Portfolio Settings</h2>
            <PortfolioSettingsForm :portfolio="portfolio" />
        </div>
        <h2>User Settings</h2>
        <UserSettingsForm />
    </div>
</template>
  
<script>
import PortfolioSettingsForm from '@/components/PortfolioSettingsForm.vue'
import UserSettingsForm from '@/components/UserSettingsForm.vue'
export default {
    components: {
        PortfolioSettingsForm,
        UserSettingsForm
    },
    computed: {
        portfolio() {
            return this.$store.getters.activePortfolio
        }
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
    padding-bottom: 1rem;
}

span {
    width: 100%;
    margin: 0 auto;
    background-color: #161b22;
    padding-block: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    text-align: center;
}

span a {
    color: #c9d1d9;
    font-weight: bold;
    text-decoration: none;
}

span a:hover {
    color: #4CAF50;
}
</style>