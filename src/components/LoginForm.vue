<template>
    <form @submit.prevent="login">
        <div v-if="error" class="error">{{ error }}</div>
        <label>
            Username:
            <input type="username" v-model="username" required autocomplete="username">
        </label>
        <label>
            Password:
            <input type="password" v-model="password" required autocomplete="current-password">
        </label>
        <!-- Show login button, if isLogginIn is true, show a spinner and disable the button -->
        <button type="submit" :disabled="isMakingRequest" :class="{ 'disabled': isMakingRequest }">
            <span v-if="isMakingRequest">
                <i class="fa-solid fa-spinner fa-spin"></i>
            </span>
            <span v-else>Login</span>
        </button>
    </form>
</template>
  
<script>
import controller from '@/controller';
export default {
    data() {
        return {
            username: '',
            password: '',
            error: '',
            isMakingRequest: false
        }
    },
    methods: {
        login() {
            this.error = '';
            this.isMakingRequest = true;
            controller.login(this.username, this.password)
                .then(response => {
                    this.$store.dispatch('login', response.data);
                })
                .catch(error => {
                    const defaultError = 'An error occurred while logging in. Please try again later.';
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