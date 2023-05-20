<template>
    <form @submit.prevent="signup">
        <div v-if="error" class="error">{{ error }}</div>
        <div v-if="success" class="success">{{ success }}</div>
        <label>
            Email:
            <input type="email" v-model="email" required autocomplete="email">
        </label>
        <label>
            Username:
            <input type="username" v-model="username" required autocomplete="username">
        </label>
        <label>
            Password:
            <input type="password" v-model="password" required autocomplete="new-password">
        </label>
        <label>
            Confirm Password:
            <input type="password" v-model="confirmPassword" required autocomplete="new-password">
        </label>
        <button type="submit" :disabled="isMakingRequest" :class="{ 'disabled': isMakingRequest }">
            <span v-if="isMakingRequest">
                <i class="fa-solid fa-spinner fa-spin"></i>
            </span>
            <span v-else>Create New Account</span>
        </button>
    </form>
</template>
  
<script>
import controller from '@/controller';
export default {
    data() {
        return {
            email: '',
            username: '',
            password: '',
            confirmPassword: '',
            error: '',
            success: '',
            isMakingRequest: false
        }
    },
    methods: {
        signup() {
            this.error = '';
            if (this.password !== this.confirmPassword) {
                // Check that the passwords match
                this.error = 'Passwords do not match';
                return;
            }
            this.isMakingRequest = true;
            controller.signup(this.email, this.username, this.password)
                .then(_ => {
                    this.success = 'Signup successful. Please login.'
                })
                .catch(error => {
                    const defaultError = 'An error occurred while signing up. Please try again later.';
                    try {
                        this.error = error.response.data.detail;
                    } catch (e) {
                        this.error = defaultError;
                    }
                })
                .finally(() => {
                    this.isMakingRequest = false;
                });
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
    border-radius: 5px;
    border: 1px solid #ccc;
    margin: 0 1rem;
    padding: 1rem;
}

.success {
    background-color: #007bff;
    color: #fff;
    border-radius: 5px;
    border: 1px solid #ccc;
    margin: 0 1rem;
    padding: 1rem;
}
</style>