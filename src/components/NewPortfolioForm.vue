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