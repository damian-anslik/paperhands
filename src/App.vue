<template>
  <Navbar />
  <router-view />
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import controller from '@/controller'

export default {
  name: 'App',
  components: {
    Navbar
  },
  created() {
    if (this.$store.getters.availableSymbols) {
      return
    }
    controller.getSymbols()
      .then(response => {
        this.$store.commit('setAvailableSymbols', response.data)
      })
      .catch(error => {
        console.error(error)
      })
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  max-width: 1024px;
}

body {
  margin: 1rem;
}
</style>
