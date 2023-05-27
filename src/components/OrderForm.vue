<template>
    <form class="order-form">
        <div v-if="error" class="error">{{ error }}</div>
        <label id="symbol">
            Symbol
            <input type="text" :value="activeSymbol" list="symbols" :onblur="(e) => onBlurHandler(e.target.value)" required>
            <datalist id="symbols">
                <option v-for="symbol in availableSymbols" :key="symbol" :value="symbol.ticker">{{ symbol.ticker }} ({{
                    symbol.name }})</option>
            </datalist>
        </label>
        <label id="quantity">
            Quantity
            <input type="number" v-model="quantity" list="quantities" min="1" required>
        </label>
        <label id="order-type">
            Order Type
            <select v-model="orderType" required>
                <option value="MKT">MKT</option>
                <option value="LMT">LMT</option>
            </select>
        </label>
        <label id="limit-price" v-if="orderType === 'LMT'">
            Limit Price
            <input type="number" v-model="limitPrice" min="0" required>
        </label>
        <div class="buttons">
            <button id="sell-order" @click.prevent="submitSellOrder" :disabled="isMakingRequest"
                :class="{ 'disabled': isMakingRequest }">
                <span v-if="isMakingRequest">
                    <i class="fa-solid fa-spinner fa-spin"></i>
                </span>
                <span v-else>Sell</span>
            </button>
            <button id="buy-order" @click.prevent="submitBuyOrder" :disabled="isMakingRequest"
                :class="{ 'disabled': isMakingRequest }">
                <span v-if="isMakingRequest">
                    <i class="fa-solid fa-spinner fa-spin"></i>
                </span>
                <span v-else>Buy</span>
            </button>
        </div>
    </form>
</template>

<script>
import controller from '@/controller'
export default {
    name: "OrderForm",
    props: {
        portfolioId: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            quantity: null,
            limitPrice: null,
            orderType: "MKT",
            error: "",
            availableSymbols: this.$store.getters.availableSymbols,
            isMakingRequest: false
        }
    },
    computed: {
        activeSymbol() {
            return this.$store.getters.activeSymbol
        }
    },
    methods: {
        onBlurHandler(symbol) {
            this.$store.commit("setActiveSymbol", symbol)
        },
        submitBuyOrder() {
            this.submitOrder("BUY")
        },
        submitSellOrder() {
            this.submitOrder("SELL")
        },
        submitOrder(side) {
            let symbol = this.$store.getters.activeSymbol
            this.error = ""
            this.isMakingRequest = true
            if (symbol === "") {
                this.error = "Symbol cannot be empty"
            }
            if (!this.availableSymbols.some(s => s.ticker === symbol)) {
                this.error = "Symbol is not available"
            }
            if (this.quantity <= 0) {
                this.error = "Quantity must be greater than 0"
            }
            if (this.orderType === "LMT" && this.limitPrice === null) {
                this.error = "Limit price cannot be empty"
            }
            if (this.error !== "") {
                this.isMakingRequest = false
                return
            }
            this.error = ""
            controller.placeOrder(this.portfolioId, symbol, this.quantity, side, this.orderType, this.limitPrice)
                .then(response => {
                    this.$store.dispatch("addOrder", response.data)
                })
                .catch(error => {
                    console.log(error)
                })
                .finally(() => {
                    this.isMakingRequest = false
                    this.error = ""
                })
        }
    }
}
</script>