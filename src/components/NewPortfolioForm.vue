<!-- TODO This does not currently submit the form when the button is clicked. -->
<template>
    <div>
        <form>
            <label for="name">
                Portfolio Name
                <input type="text" id="name" v-model="name" />
            </label>
            <div class="buttons">
                <button id="public" @click.prevent="createPublicPortfolio">Create Public Portfolio</button>
                <button id="private" @click.prevent="createPrivatePortfolio">Create Private Portfolio</button>
            </div>
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
            error: ""
        }
    },
    methods: {
        createPublicPortfolio() {
            this.is_public = true
            this.createPortfolio()
        },
        createPrivatePortfolio() {
            this.is_public = false
            this.createPortfolio()
        },
        createPortfolio() {
            this.error = ""
            controller.createPortfolio(this.name, this.is_public)
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
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 5px;
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
    border: 1px solid #ccc;
    border-radius: 5px;
}

button {
    padding: 1rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #4CAF50;
    color: #fff;
    cursor: pointer;
    margin-inline: 1rem;
    width: 100%;
}

button#public {
    /* Blue */
    background-color: #2196F3;
}

.buttons {
    display: flex;
    justify-content: center;
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