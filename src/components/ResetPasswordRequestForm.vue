<template>
    <form @submit.prevent="resetPassword">
        <!-- Success message -->
        <div v-if="success" class="success">{{ success }}</div>
        <div v-if="error" class="error">{{ error }}</div>
        <label>
            Username
            <input type="username" v-model="username" required autocomplete="username">
        </label>
        <button type="submit" :disabled="isMakingRequest" :class="{ 'disabled': isMakingRequest }">
            <span v-if="isMakingRequest">
                <i class="fa-solid fa-spinner fa-spin"></i>
            </span>
            <span v-else>Reset Password</span>
        </button>
    </form>
</template>
  
<script>
import controller from '@/controller';
export default {
    name: 'ResetPasswordRequestForm',
    data() {
        return {
            username: '',
            error: '',
            success: '',
            isMakingRequest: false
        }
    },
    methods: {
        resetPassword() {
            this.error = '';
            this.success = '';
            this.isMakingRequest = true;
            controller.requestPasswordReset(this.username)
                .then(_ => {
                    const successMessage = 'If an account with that username exists, a password reset link has been sent to the associated email.';
                    this.success = successMessage;
                })
                .catch(error => {
                    const defaultError = 'An error occurred while resetting your password. Please try again later.';
                    try {
                        this.error = error.response.data.detail;
                    } catch (e) {
                        this.error = defaultError;
                    }
                })
                .finally(_ => {
                    this.isMakingRequest = false;
                })
        }
    }
}
</script>