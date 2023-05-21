<template>
    <div v-if="showDialog" class="dialog">
        <div class="dialog-content">
            <h3>Your session is about to expire!</h3>
            <p>Do you want to continue? Your session will expire in {{ timeRemaining }} seconds.</p>
            <div class="buttons">
                <button id="logout-button" @click="logout">No</button>
                <button id="extend-button" @click="extendSession">Yes</button>
            </div>
        </div>
    </div>
</template>
  
<script>
import controller from '@/controller';
export default {
    data() {
        return {
            showDialog: false,
            timeRemaining: null,
            interval: null
        };
    },
    computed: {
        tokenExpiry() {
            return this.$store.getters.tokenExpiry;
        }
    },
    mounted() {
        this.checkSessionTimeout();
    },
    beforeUnmount() {
        // Stop the interval when the component is unmounted
        clearInterval(this.interval)
    },
    methods: {
        checkSessionTimeout() {
            this.interval = setInterval(() => {
                const tokenExpiry = this.tokenExpiry;
                const currentTime = Math.floor(Date.now() / 1000) - 3600; 
                let diff = tokenExpiry - currentTime;
                this.timeRemaining = Math.floor(diff);
                if (diff <= 0) {
                    this.logout();
                }
                if (diff <= 60) {
                    this.showDialog = true;
                }
                else {
                    this.showDialog = false;
                }
            }, 1000);
        },
        extendSession() {
            controller.refreshToken()
                .then((response) => {
                    this.$store.dispatch('extendSession', response.data)
                })
                .catch((error) => {
                    // Logout if the refresh token fails
                    console.error(error);
                    this.logout();
                });
        },
        logout() {
            this.$store.dispatch('logout');
        }
    }
};
</script>

<style scoped>
/* Show in middle of screen */
.dialog {
    position: fixed;
    z-index: 1;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    display: flex;
    flex-direction: column;
    align-items: center;
    top: 0;
}

.dialog-content {
    margin-top: 25vh;
    max-width: 75vw;
    background-color: #161b22;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: left;
    gap: 1rem;
}

.dialog-content h3 {
    width: 100%;
    text-align: left;
    margin: 0;
}

.buttons {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    width: 100%;
    gap: 1rem;
}

button {
    padding: 0.25rem 0.5rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #fff;
    cursor: pointer;
    flex: 1;
    font-weight: bold;
    font-size: 1rem;
}

button#extend-button {
    background-color: #4CAF50;
}

button#logout-button {
    background-color: #f44336;
}
</style>