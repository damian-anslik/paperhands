<template>
        <form>
            <div v-if="error" class="error">{{ error }}</div>
            <div class="order-details">
                <label id="symbol">
                    Symbol
                    <input type="text" list="symbols" v-model="symbol" placeholder="Enter a symbol" required>
                    <datalist id="symbols">
                        <option v-for="symbol in availableSymbols" :key="symbol" :value="symbol.ticker">{{ symbol.ticker }} ({{ symbol.name }})</option>
                    </datalist>
                </label>
                <label id="quantity">
                    Quantity
                    <input type="number" v-model="quantity" min="1" required>
                </label>
            </div>
            <div class="order-details-extra">
                <!-- Select whether the order is a MKT or LMT order, if it's a LMT order show the limit price field -->
                <label id="order-type">
                    Order Type
                    <select v-model="orderType" required>
                        <option value="MKT">MKT</option>
                        <option value="LMT">LMT</option>
                    </select>
                </label>
                <!-- Change the visibility of the limit price field based on the order type -->
                <label id="limit-price" v-if="orderType === 'LMT'">
                    Limit Price
                    <input type="number" v-model="limitPrice" min="0" required>
                </label>
            </div>
            <div class="buttons">
                <button id="sell-order" @click.prevent="submitSellOrder">Sell</button>
                <button id="buy-order" @click.prevent="submitBuyOrder">Buy</button>
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
        },
        availableSymbols: {
            type: Array,
            required: true
        }
    },
    data() {
        return {
            symbol: "",
            quantity: 1,
            limitPrice: null,
            orderType: "MKT",
            error: ""
        }
    },
    methods: {
        submitBuyOrder() {
            this.submitOrder("BUY")
        },
        submitSellOrder() {
            this.submitOrder("SELL")
        },
        submitOrder(side) {
            if (this.symbol === "") {
                this.error = "Symbol cannot be empty"
                return
            }
            if (this.quantity <= 0) {
                this.error = "Quantity must be greater than 0"
                return
            }
            if (!this.availableSymbols.find(symbol => symbol.ticker === this.symbol)) {
                // Validate that the symbol is available
                this.error = "Symbol is not available"
                return
            }
            this.error = ""
            controller.placeOrder(this.portfolioId, this.symbol, this.quantity, side, this.orderType, this.limitPrice)
                .then(response => {
                    this.$store.dispatch("addOrder", response.data)
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}
</script>

<style scoped>
form {
    width: 100%;
    margin: 0 auto;
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 5px;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding-block: 1rem;
}

.order-type {
    display: flex;
    gap: 1rem;
}

.order-details {
    display: flex;
    width: 100%;
    flex: 1;
}

.order-details #symbol {
    flex: 3;
}

.order-details #symbol input {
    width: 100%;
}

/* 
.order-details #symbol {
    flex: 3;
}

.order-details #symbol select {
    width: 100%;
} */

.order-details #quantity {
    flex: 1;
}

.order-details #quantity input {
    width: 100%;
}

.order-details-extra {
    display: flex;
    width: 100%;
    flex: 1;
}

.order-details-extra #order-type {
    flex: 1;
}

.order-details-extra #order-type select {
    width: 100%;
}

.order-details-extra #limit-price {
    /* Dont' make it visible */
    flex: 1;
}

.order-details-extra #limit-price input {
    width: 100%;
}

input, select {
    padding-block: 0.75rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #fff;
    color: #000;
    font-size: 1rem;
}

label {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 100%;
    align-items: flex-start;    
    gap: 1rem;
    margin: 0 1rem;
}

button {
    padding: 0.75rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #4CAF50;
    color: #fff;
    cursor: pointer;
    margin-inline: 1rem;
    flex: 1;
    font-weight: bold;
    font-size: 1rem;
}

.buttons {
    display: flex;
    justify-content: center;
}

button#sell-order {
    background-color: #f44336;
}

button#buy-order {
    background-color: #4CAF50;
}

.error {
    background-color: #f44336;
    color: #fff;
    border-radius: 5px;
    border: 1px solid #ccc;
    margin: 0 1rem;
    padding: 1rem;
}
</style>