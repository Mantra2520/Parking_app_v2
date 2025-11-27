<template>
    <div class="content paybox">

        <!-- Loading -->
        <div v-if="loading" class="status-box">Loading...</div>

        <!-- Error -->
        <div v-if="error" class="status-box error">{{ error }}</div>

        <!-- SUCCESS POPUP -->
        <div v-if="showSuccess" class="success-popup">
            <div class="success-circle">
                <div class="tick"></div>
            </div>
            <p class="success-text">Payment Successful</p>
        </div>


        <div v-if="data && !loading" class="card">

            <h2>Booking Summary</h2>

            <div class="details">
                <p><strong>Reservation ID:</strong> {{ data.resid }}</p>
                <p><strong>Vehicle No:</strong> {{ data.vno }}</p>
                <p><strong>Date:</strong> {{ data.in_date }} - {{ data.out_date }}</p>
                <p><strong>Time:</strong> {{ data.in_time }} - {{ data.out_time }}</p>
                <p><strong>Duration:</strong> {{ data.dur.toFixed(2) }} hour(s)</p>
                <p><strong>Cost:</strong> ₹{{ data.cost.toFixed(2) }}</p>
            </div>

            <button class="pay-btn" @click="payed">
                Pay ₹{{ data.cost.toFixed(2) }}
            </button>

        </div>

    </div>
</template>

<script>
export default {
    name: 'Summary',
    data() {
        return {
            userid: this.$route.params.id,
            resid: this.$route.params.rid,
            data: null,
            error: null,
            loading: false,
            showSuccess: false,
        }
    },
    mounted() {
        const token = localStorage.getItem("token");
        const role = localStorage.getItem("role");

        if (token && role === "user") {
            this.pay();
        } else {
            this.$router.push("/");
        }
    },
    methods: {
        async pay() {
            this.loading = true;
            this.error = null;

            try {
                const res = await fetch(`http://127.0.0.1:5000/user/payment/${this.userid}/${this.resid}`, {
                    method: "GET",
                    headers: {
                        "Authorization": localStorage.getItem("token")
                    }
                });

                if (!res.ok) {
                    throw new Error("Unable to fetch booking details.");
                }

                const json = await res.json();

                if (json.error) {
                    this.error = json.error;
                    return;
                }

                this.data = json;

            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
        },

        async payed() {
            this.showSuccess = true;

            setTimeout(() => {
                this.$router.push(`/user/home/${this.userid}`);
            }, 2000);
        }
    }
}
</script>
