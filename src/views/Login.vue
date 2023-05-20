<template>
    <div>
        <h1>Login</h1>
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
div {
    width: 100%;
    max-width: 700px;
    margin: 0 auto;
    text-align: left;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}


span {
    width: 100%;
    margin: 0 auto;
    background-color: #fff;
    padding-block: 1rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    text-align: center;
}

span a {
    color: #000;
}

span a:hover {
    color: #4CAF50;
}
</style>