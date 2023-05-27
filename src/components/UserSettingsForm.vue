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
