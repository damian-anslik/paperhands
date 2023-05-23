import axios from 'axios'

const controller = {
    authHeader() {
        return {
            Authorization: `Bearer ${localStorage.getItem('store') ? JSON.parse(localStorage.getItem('store')).token : null}`
        }
    },
    async getSymbols() {
        return axios.get('/symbols')
    },
    async login(username, password) {
        return axios.post(
            '/token',
            {
                username,
                password
            },
            {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }
        )
    },
    async refreshToken() {
        return axios.post(
            '/token/refresh',
            {},
            {
                headers: this.authHeader()
            }
        )
    },
    async signup(email, username, password) {
        return axios.post(
            '/signup',
            {
                email,
                username,
                password
            },
            {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }
        )
    },
    async createPortfolio(portfolio_name, is_public) {
        return axios.post(
            '/portfolio',
            {
                portfolio_name,
                is_public
            },
            {
                headers: {
                    ...this.authHeader(),
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }
        )
    },
    async userData() {
        return axios.get(
            '/users/me/',
            {
                headers: this.authHeader()
            }
        )
    },
    async portfolioData(id) {
        return axios.get(
            '/portfolio',
            {
                params: {
                    id
                },
                headers: this.authHeader()
            }
        )
    },
    async placeOrder(portfolioId, symbol, quantity, side, orderType, limitPrice = null) {
        return axios.post(
            `/order?id=${portfolioId}`,
            {
                symbol,
                quantity,
                side,
                order_type: orderType,
                limit_price: limitPrice
            },
            {
                headers: {
                    ...this.authHeader(),
                    "Content-Type": "application/x-www-form-urlencoded",
                }
            }
        )
    },
    async cancelOrder(orderId) {
        return axios.delete(
            '/order',
            {
                params: {
                    id: orderId
                },
                headers: this.authHeader()
            }
        )
    },
    async requestPasswordReset(username) {
        return axios.post('/request-password-reset',
            {
                username
            },
            {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            })
    },
    async resetPassword(token, password) {
        return axios.post('/reset-password',
            {
                token,
                password
            },
            {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            })
    },
    async getHistoricalData(symbol) {
        return axios.get('/symbols/hmds',
            {
                params: {
                    symbol
                },
                headers: this.authHeader()
            }
        )
    },
    async updatePortfolio(portfolioId, portfolioName) {
        console.log(portfolioName)
        return axios.put(`/portfolio?id=${portfolioId}`,
            {
                portfolio_name: portfolioName,
                is_public: false
            },
            {
                headers: {
                    ...this.authHeader(),
                    "Content-Type": "application/x-www-form-urlencoded",
                }
            }
        )
    },
    async deletePortfolio(portfolioId) {
        return axios.delete(`/portfolio?id=${portfolioId}`,
            {
                headers: this.authHeader()
            }
        )
    }
}

export default controller