<template>
    <form>
        <div v-if="error" class="error">{{ error }}</div>
        <div v-if="success" class="success">{{ success }}</div>
        <label>
            Portfolio Name
            <!--The input should initially have the name of the portfolio  -->
            <input type="text" v-model="portfolioName" />
        </label>
        <div class="portfolio-actions">
            <!-- Update Portfolio button -->
            <button type="button" @click="updatePortfolio" :disabled="isMakingRequest"
                :class="{ 'disabled': isMakingRequest }">
                <span v-if="isMakingRequest">
                    <i class="fa-solid fa-spinner fa-spin"></i>
                </span>
                <span v-else>Update Portfolio</span>
            </button>
            <!-- Delete Portfolio button -->
            <button type="button" id="delete" @click="deletePortfolio" :disabled="isMakingRequest"
                :class="{ 'disabled': isMakingRequest }">
                <span v-if="isMakingRequest">
                    <i class="fa-solid fa-spinner fa-spin"></i>
                </span>
                <span v-else>Delete Portfolio</span>
            </button>
        </div>
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
        deletePortfolio() {
            this.error = ""
            this.success = ""
            this.isMakingRequest = true
            controller.deletePortfolio(this.portfolio.id)
                .then(() => {
                    this.$store.dispatch('deletePortfolio', this.portfolio.id)
                    .then(() => {
                        this.success = `Portfolio deleted successfully. Switched to porfolio: ${this.portfolio.name} (id: ${this.portfolio.id})`
                        this.portfolioName = this.portfolio.name
                    })
                })
                .catch((error) => {
                    this.error = error.message
                })
                .finally(() => {
                    this.isMakingRequest = false
                })
        },
        updatePortfolio() {
            this.error = ""
            this.success = ""
            this.isMakingRequest = true
            controller.updatePortfolio(this.portfolio.id, this.portfolioName)
                .then((response) => {
                    let updatedPortfolio = response.data
                    this.$store.dispatch('updatePortfolioDetails', {
                        oldPortfolio: this.portfolio,
                        newPortfolio: updatedPortfolio
                    })
                    this.success = "Portfolio updated successfully"
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