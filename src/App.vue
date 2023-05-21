<template>
  <Navbar />
  <div class="content">
    <router-view />
  </div>
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
body {
  margin: 0;
  background-color: #0d1117;
  overflow-y: scroll;
}

/* Style the scrollbar */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: #0d1117;
}

::-webkit-scrollbar-thumb {
  background: #30363d;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}
</style>
