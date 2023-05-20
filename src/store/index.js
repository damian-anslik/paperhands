import { createStore } from 'vuex'
import router from '@/router/index'
import controller from '@/controller'

const routeToPush = 'Dashboard'

// TODO Handle expired tokens

const localStoragePlugin = store => {
  store.subscribe((_, state) => {
    localStorage.setItem('store', JSON.stringify(state))
  })
}

const activePortfolioPlugin = store => {
  let interval = null
  store.subscribe((_, state) => {
    if (state.activePortfolio) {
      if (interval) {
        clearInterval(interval)
      }
      interval = setInterval(async () => {
        const portfolio = await controller.portfolioData(state.activePortfolio.id)
        store.commit('setPortfolio', portfolio.data)
      }, 5000)
    }
  })
}

const store = createStore({
  state: localStorage.getItem('store') ? JSON.parse(localStorage.getItem('store')) : {
    loading: false,
    user: null,
    token: null,
    tokenExpiry: null,
    activePortfolio: null,
    availableSymbols: null,
  },
  mutations: {
    setLoading(state, loading) {
      state.loading = loading
    },
    setUser(state, user) {
      state.user = user
    },
    setToken(state, token) {
      state.token = token
    },
    setTokenExpiry(state, expiry) {
      state.tokenExpiry = expiry
    },
    setPortfolio(state, portfolio) {
      state.activePortfolio = portfolio
    },
    setAvailableSymbols(state, symbols) {
      state.availableSymbols = symbols
    },
  },
  getters: {
    isLoading(state) {
      return state.loading
    },
    isAuthenticated(state) {
      return !!state.token
    },
    user(state) {
      return state.user
    },
    token(state) {
      return state.token
    },
    activePortfolio(state) {
      return state.activePortfolio
    },
    availableSymbols(state) {
      return state.availableSymbols
    },
    tokenExpiryTime(state) {
      return state.tokenExpiry
    }
  },
  actions: {
    async login({ commit }, { access_token, access_token_expires }) {
      commit('setLoading', true)
      commit('setToken', access_token)
      commit('setTokenExpiry', access_token_expires)
      const user = await controller.userData()
      let userData = user.data
      if (userData.portfolios.length > 0) {
        const portfolio = await controller.portfolioData(userData.portfolios[0].id)
        commit('setPortfolio', portfolio.data)
      }
      commit('setUser', userData)
      commit('setLoading', false)
      router.push({ name: routeToPush })
    },
    async logout({ commit }) {
      commit('setTokenExpiry', null)
      commit('setToken', null)
      commit('setUser', null)
      commit('setPortfolio', null)
      router.push({ name: 'Home' })
    },
    async refreshSessionToken({ commit }) {
      const tokenData = await controller.refreshToken()
      commit('setToken', tokenData.data.access_token)
      commit('setTokenExpiry', tokenData.data.access_token_expires)
    },
    async addPortfolio({ commit }, { id, name }) {
      let user = this.getters.user
      user.portfolios.push({ id, name })
      commit('setUser', user)
      this.dispatch('setActivePortfolio', { id })
      router.push({ name: 'Dashboard' })
    },
    async setActivePortfolio({ commit }, portfolio) {
      commit('setPortfolio', portfolio)
    },
    async addOrder({ commit }, orderData) {
      let portfolio = this.getters.activePortfolio
      portfolio.orders.push(orderData)
      commit('setPortfolio', portfolio)
    },
    async cancelOrder({ commit }, orderId) {
      let portfolio = this.getters.activePortfolio
      portfolio.orders = portfolio.orders.filter(order => order.id !== orderId)
      commit('setPortfolio', portfolio)
    }
  },
  plugins: [
    localStoragePlugin,
    activePortfolioPlugin
  ]
})

export default store;