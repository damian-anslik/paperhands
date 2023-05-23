<template>
    <form>
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

<style scoped>
form {
    margin: 0 auto;
    background-color: #0d1117;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 1rem;
}

form label {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
    text-align: left;
}

form label input,
select {
    padding: 0.25rem 0.5rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    background-color: #161b22;
    color: #ccc;
    font-size: 1rem;
}

button {
    padding: 0.25rem 0.5rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    background-color: #4CAF50;
    color: #fff;
    cursor: pointer;
    flex: 1;
    font-weight: bold;
    font-size: 1rem;
}

.buttons {
    display: flex;
    justify-content: center;
    gap: 1rem;
}

button#sell-order {
    background-color: #f44336;
}

button#buy-order {
    background-color: #4CAF50;
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
    padding: 0.5rem 1rem;
    text-align: left;
}

@media screen and (max-width: 1024px) {
    form {
        display: none;
    }
}
</style>