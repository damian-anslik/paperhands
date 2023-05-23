<template>
    <form @submit.prevent="updatePortfolio">
        <div v-if="error" class="error">{{ error }}</div>
        <div v-if="success" class="success">{{ success }}</div>
        <label>
            Portfolio Name:
            <input type="text" v-model="portfolioName" required>
        </label>
        <button type="submit" :disabled="isMakingRequest" :class="{ 'disabled': isMakingRequest }">
            <span v-if="isMakingRequest">
                <i class="fa-solid fa-spinner fa-spin"></i>
            </span>
            <span v-else>Update Portfolio</span>
        </button>
        <!-- TODO Add delete button -->
    </form>
</template>
  
<script>
import controller from '@/controller';
export default {
    props: {
        portfolio: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            portfolioName: this.portfolio.name,
            isMakingRequest: false,
            error: "",
            success: ""
        }
    },
    methods: {
        updatePortfolio() {
            this.error = ""
            this.success = ""
            this.isMakingRequest = true
            controller.updatePortfolio(this.portfolio.id, this.portfolioName)
                .then((response) => {
                    this.success = "Portfolio updated successfully"
                    let updatedPortfolio = response.data
                    this.$store.dispatch('updatePortfolioDetails', {
                        oldPortfolio: this.portfolio,
                        newPortfolio: updatedPortfolio
                    })
                })
                .catch((error) => {
                    this.error = error.message
                })
                .finally(() => {
                    this.isMakingRequest = false
                })
        }
    }
}
</script>


<style scoped>
form {
    width: 100%;
    margin: 0 auto;
    background-color: #161b22;
    border: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding-block: 1rem;
}

label {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    text-align: left;
    margin: 0 1rem;
}

input {
    padding: 1rem;
    background-color: #c9d1d9;
    border: 1px solid #ccc;
}

button {
    padding: 1rem;
    border: 1px solid #ccc;
    background-color: #4CAF50;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #fff;
    cursor: pointer;
    margin: 0 1rem;
}


button.disabled {
    background-color: #ccc;
    color: #fff;
    cursor: not-allowed;
}

.error {
    background-color: #f44336;
    color: #fff;
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin: 0 1rem;
    padding: 1rem;
}

.success {
    background-color: #007bff;
    color: #fff;
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin: 0 1rem;
    padding: 1rem;
}
</style>