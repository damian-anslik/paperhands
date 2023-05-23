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

<style scoped>

form {
    width: 100%;
    margin: 0 auto;
    background-color: #161b22;
    border: 1px solid rgba(255, 255, 255, 0.1);
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
    background-color: #c9d1d9; 
    border: 1px solid #ccc;
}

button {
    padding: 1rem;
    border: 1px solid #ccc;
    background-color: #4CAF50;
    border: 1px solid rgba(255, 255, 255, 0.1);
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
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin: 0 1rem;
    padding: 1rem;
}

.success {
    background-color: #007bff;
    color: #fff;
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin: 0 1rem;
    padding: 1rem;
}
</style>