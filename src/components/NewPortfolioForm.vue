<template>
    <div>
        <form @submit.prevent="createPortfolio">
            <label for="name">
                Portfolio Name
                <input type="text" id="name" v-model="name" />
            </label>
            <button type="submit" :disabled="isMakingRequest" :class="{ 'disabled': isMakingRequest }">
                <span v-if="isMakingRequest">
                    <i class="fa-solid fa-spinner fa-spin"></i>
                </span>
                <span v-else>Create</span>
            </button>
        </form>
    </div>
</template>

<script>
import controller from '@/controller';
export default {
    name: "NewPortfolioForm",
    data() {
        return {
            name: "",
            is_public: false,
            error: "",
            isMakingRequest: false
        }
    },
    methods: {
        createPortfolio() {
            this.error = ""
            this.isMakingRequest = true
            controller.createPortfolio(this.name, false)
                .then(response => {
                    this.$store.dispatch('addPortfolio', response.data)
                    this.name = ""
                    this.is_public = false
                })
                .catch(error => {
                    this.error = error.response.data.detail;
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