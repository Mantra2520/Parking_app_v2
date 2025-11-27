<template>
    <div class="content">
        <div class="parent" v-if="lot">
            <div class="div1">
                <h2>Parking LOT #{{ lot.lot_id }}</h2>
            </div>

            <div class="details-box">
                <div class="div2">
                    <p><strong>Location:</strong> {{ lot.prime_location_name }}</p>
                    <p><strong>Address:</strong> {{ lot.address }}</p>
                    <p><strong>Pincode:</strong> {{ lot.pin_code }}</p>
                </div>

                <div class="vertical-line"></div>

                <div class="div3">
                    <p><strong>Price/unit time:</strong> ₹{{ lot.price }}</p>
                    <p><strong>Total Spots:</strong> {{ lot.max_spots }}</p>
                    <p><strong>Occupied Spots:</strong> {{ lot.occupidespot }}</p>
                </div>
            </div>

            <div class="div4">
                <h3>Parking Spots</h3>
            </div>

            <div class="div5">
                <div v-for="(spot, index) in lot.spots" :key="index" class="spot-wrap">
                    <!-- full-width road block every 13 spots -->
                    <div v-if="index > 0 && index % 13 === 0" class="road-group">
                        <div class="road-sideline"></div>
                        <div class="road-midline"></div>
                        <div class="road-sideline"></div>
                    </div>

                    <!-- Spot box -->
                    <div class="spot" :class="getSpotStatus(spot)">
                        <template v-if="isOccupied(spot)">
                            <router-link :to="`/admin/spotDetails/${getSpotId(spot)}`"><img src="/car-icon.png"
                                    alt="Car" class="car-img" /></router-link>
                        </template>
                        <template v-else>
                            <p>{{ getSpotId(spot) }}</p>
                            <p>Available</p>
                        </template>
                    </div>
                </div>
            </div>
        </div>

        <div v-else class="loading">Loading lot details...</div>
    </div>
</template>


<script>
export default {
    name: "Adminlot",
    data() {
        return {
            lotid: this.$route.params.id,
            lot: null,
            error: null,
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
                    }})
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                this.lot = await response.json();
                console.log(this.lot)
            }
            catch (err) {
                this.errorMessage = err.message;
            } finally {
                this.loading = false;
            }
        },
        getSpotId(spot) {
            return Object.keys(spot)[0];
        },
        getSpotStatus(spot) {
            const key = Object.keys(spot)[0];
            return spot[key] === "O" ? "occupied" : "available";
        },
        isOccupied(spot) {
            const key = Object.keys(spot)[0];
            return spot[key] === "O";
        },

    }
}
</script>
