<template>
    <form @submit.prevent="resetPassword">
        <div v-if="success" class="success">{{ success }}</div>
        <div v-if="error" class="error">{{ error }}</div>
        <label>
            New Password
            <input type="password" v-model="password" required autocomplete="new-password">
        </label>
        <label>
            Confirm Password
            <input type="password" v-model="confirmPassword" required autocomplete="new-password">
        </label>
        <button type="submit" :disabled="isMakingRequest" :class="{ 'disabled': isMakingRequest }">
            <span v-if="isMakingRequest">
                <i class="fa-solid fa-spinner fa-spin"></i>
            </span>
            <span v-else>Confirm Password Reset</span>
        </button>
    </form>
</template>

<script>
import controller from '@/controller';
export default {
    name: 'ResetPasswordForm',
    data() {
        return {
            password: '',
            confirmPassword: '',
            error: '',
            success: '',
            isMakingRequest: false
        }
    },
    props: {
        token: {
            type: String,
            required: true
        }
    },
    methods: {
        resetPassword() {
            this.error = '';
            this.success = '';
            if (this.password !== this.confirmPassword) {
                this.error = 'Passwords do not match'
                return
            }
            this.isMakingRequest = true;
            controller.resetPassword(this.token, this.password)
                .then(_ => {
                    const successMessage = "Password reset successful. You can now login with your new password"
                    this.success = successMessage;
                    this.error = '';
                    this.password = '';
                    this.confirmPassword = '';
                })
                .catch(err => {
                    const defaultError = 'An error occurred while resetting your password. Please try again later.';
                    if (err.response.status === 400) {
                        this.error = 'Password reset request is invalid or has expired. Please request a new one.';
                    }
                    else {
                        this.error = defaultError;
                    }
                })
                .finally(() => {
                    this.isMakingRequest = false;
                })
        }
    }
}
</script>