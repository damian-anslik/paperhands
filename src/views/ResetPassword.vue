<template>
    <div class="single-component-view-container">
        <h2>Reset Password</h2>
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