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
                        this.error = error.response.data.message || defaultError;
                    } catch (err) {
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
  