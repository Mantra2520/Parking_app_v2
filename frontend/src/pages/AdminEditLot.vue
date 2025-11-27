<template>
    <div class="content">
        <h1 style="margin-top: 110px;">Parking Lot #{{ lotid }}</h1>

        <div v-if="loading" class="loading">Loading...</div>
        <div v-else-if="errorMessage" class="error">{{ errorMessage }}</div>

        <div v-else>
            <form style="margin-top: 60px;" @submit.prevent="editLot">
                <div class="input-group">
                    <input required type="text" v-model="details.prime_location_name" autocomplete="off" class="input"
                        placeholder=" " />
                    <label class="user-label">Prime Location</label>
                </div>

                <div class="input-group">
                    <input required type="text" v-model="details.address" autocomplete="off" class="input"
                        placeholder=" " />
                    <label class="user-label">Address</label>
                </div>

                <div class="input-group">
                    <input required type="text" v-model="details.pin_code" autocomplete="off" class="input"
                        placeholder=" " />
                    <label class="user-label">Pin code</label>
                </div>

                <div class="input-group">
                    <input required type="number" v-model="details.price" autocomplete="off" class="input"
                        placeholder=" " />
                    <label class="user-label">Price per Hour</label>
                </div>

                <div class="input-group">
                    <input disabled type="number" v-model="details.max_spots" autocomplete="off" class="input"
                        placeholder=" " />
                    <label class="user-label">Max Spots</label>
                </div>

                <div>
                    <input class="form-button" type="submit" value="Update" />
                </div>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    name: "adminEditLot",
    data() {
        return {
            lotid: this.$route.params.id,
            lotDetails: null,
            errorMessage: null,
            details: {
                prime_location_name: "",
                address: "",
                pin_code: "",
                price: "",
                max_spots: "",
            },
            loading: false,
        }
    },
    mounted() {
        const token = localStorage.getItem("token");
        const role = localStorage.getItem("role");

        if (token && role === "admin") {
            this.fetchData();
        } else {
            this.$router.push("/login");
        }
    },
    methods: {
        async fetchData() {
            this.loading = true;
            try {
                const response = await fetch(`http://127.0.0.1:5000/admin/lot_details/${this.lotid}`, {
                    method: "GET",
                    headers: {
                        "Authorization": localStorage.getItem("token")
                    }});
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                this.lotDetails = await response.json();
                this.details.prime_location_name = this.lotDetails.prime_location_name
                this.details.price = this.lotDetails.price
                this.details.pin_code = this.lotDetails.pin_code
                this.details.address = this.lotDetails.address
                this.details.max_spots = this.lotDetails.max_spots

            } catch (err) {
                this.errorMessage = err.message;
            } finally {
                this.loading = false;
            }

        },
        async editLot() {
            this.loading = true;
            this.errorMessage = null;
            try {
                const response = await fetch(
                    `http://127.0.0.1:5000/admin/edit_parking/${this.lotid}`,
                    {
                        method: "PUT",
                        headers: {
                            "Content-Type": "application/json",
                             "Authorization": localStorage.getItem("token")
                        },
                        body: JSON.stringify(this.details),
                    }
                );

                if (!response.ok) throw new Error(`Update failed! Status: ${response.status}`);

                alert("Parking Lot updated successfully!");
                this.$router.push("/admin/home");
            } catch (err) {
                this.errorMessage = err.message;
            } finally {
                this.loading = false;
            }
        }

    }

}
</script>

