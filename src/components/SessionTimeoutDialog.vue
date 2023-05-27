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
                } else {
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