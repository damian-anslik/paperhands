<template>
    <div>
        <h2>Signup</h2>
        <SignupForm />
    </div>
</template>
  
<script>
import SignupForm from '@/components/SignupForm.vue'
export default {
    components: {
        SignupForm
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