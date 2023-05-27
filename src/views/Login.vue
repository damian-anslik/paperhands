<template>
    <div class="single-component-view-container">
        <h2>Login</h2>
        <LoginForm />
        <span>
            Forgot your password? <router-link to="/reset-password">Reset Password</router-link>
        </span>
    </div>
</template>
  
<script>
import LoginForm from '@/components/LoginForm.vue'

export default {
    components: {
        LoginForm
    }
}
</script>

<style scoped>
span {
    width: 100%;
    margin: 0 auto;
    background-color: #161b22;
    padding-block: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    text-align: center;
}

span a {
    color: #c9d1d9;
    font-weight: bold;
    text-decoration: none;
}

span a:hover {
    color: #4CAF50;
}
</style>