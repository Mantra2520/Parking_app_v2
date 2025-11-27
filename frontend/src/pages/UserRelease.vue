<template>
    <div class="content">
        <h1>Release</h1>
        <div v-if="loading" class="loading">Loading...</div>

        <!-- Error -->
        <div v-if="error" class="error">{{ error }}</div>

        <form v-if="!loading && !error" style="margin-top: 30px;" @submit.prevent="payment">
            <div class="input-group">
                <input required type="text" v-model="data.resid" class="input" disabled />
                <label class="user-label">Reservation ID</label>
            </div>

            <div class="input-group">
                <input required type="text" v-model="data.lotid" class="input" disabled />
                <label class="user-label">Lot ID</label>
            </div>

            <div class="input-group">
                <input required type="text" v-model="data.spotid" class="input" disabled />
                <label class="user-label">Spot ID</label>
            </div>

            <div class="input-group">
                <input required type="text" v-model="data.userid" class="input" disabled />
                <label class="user-label">User ID</label>
            </div>

            <div class="input-group">
                <input required type="text" v-model="data.vno" disabled class="input" />
                <label class="user-label">Vehicle No.</label>
            </div>

            <div class="input-group">
                <input required type="text" v-model="data.loc" class="input" disabled />
                <label class="user-label">Address</label>
            </div>

            <div class="input-group">
                <input required type="number" v-model="data.price" class="input" disabled />
                <label class="user-label">Price (/hour)</label>
            </div>

            <div>
                <input class="form-button" type="submit" value="Release" />
            </div>
        </form>
    </div>
</template>
<script>
export default {
    name: 'UserRelease',
    data() {
        return {
            userid: this.$route.params.id,
            resid: this.$route.params.rid,
            data: {
                "lotid": null,
                "spotid": null,
                "userid": null,
                "location": null,
                "price": null,
                "vno":null,
            },
            error: null,
            loading: false,
        }
    },
    mounted() {
        const token = localStorage.getItem("token");
        const role = localStorage.getItem("role");

        if (token && role === "user") {
            this.fetchData();
        } else {
            this.$router.push("/");
        }
    },
    methods: {
        async fetchData() {
            this.loading = true;
            this.error = null;

            try {
                const res = await fetch(`http://127.0.0.1:5000/user/release/${this.userid}/${this.resid}`, {
                    method: "GET",
                    headers: {
                        "Authorization": localStorage.getItem("token")
                    }
                });

                if (!res.ok) {
                    throw new Error("Unable to fetch booking details.");
                }

                const json = await res.json();

                // Backend: {error: "..."} case
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
            console.log(this.data);
        },
        payment(){
            this.$router.push(`/user/payment/${this.userid}/${this.resid}`);
        }
    }
}
</script>