<template>
    <div>
        <h1>Reset Password</h1>
        <ResetPasswordForm v-if="token" :token="token" />
        <ResetPasswordRequestForm v-else />
    </div>
</template>
  
<script>
import ResetPasswordForm from '@/components/ResetPasswordForm.vue'
import ResetPasswordRequestForm from '@/components/ResetPasswordRequestForm.vue'

export default {
    computed: {
        token() {
            return this.$route.query.token
        }
    },
    components: {
        ResetPasswordForm,
        ResetPasswordRequestForm
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
</style>