<template>
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
                        <img src="/car-icon.png" alt="Car" class="car-img" />
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
                const response = await fetch(`http://127.0.0.1:5000/admin/lot_details/${this.lotid}`)
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                this.lot = await response.json();
                console.log(this.lot)
            }
            catch (err) {
                this.errorMessage = err.message;
                console.log(this.errorMessage)
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

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f0f2f5;
}


.parent {
    margin-top: 100px;
    text-align: center;
    padding: 0 20px;
}

.div1 h2 {
    font-size: 28px;
    margin-bottom: 20px;
    color: #2c3e50;
}

.details-box {
    display: flex;
    align-items: stretch;
    background-color: white;
    border: 2px solid #ccc;
    border-radius: 12px;
    padding: 20px;
    margin: 20px 520px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.div2,
.div3 {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
}


.vertical-line {
    width: 2px;
    background-color: #ccc;
    height: auto;
    margin: 0 10px;
}


.div2 p,
.div3 p {
    margin: 8px 0;
    font-size: 16px;
    text-align: center;
    word-wrap: break-word;
    word-break: break-word;
}

.div4 {
    padding-bottom: 20px;
}

.div4 h3 {
    font-size: 28px;
    margin-bottom: 15px;
    color: #34495e;
}

.div5 {
    background-color: #2f2f2f;
    padding: 30px;
    margin-bottom: 20px;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    border-radius: 12px;
    box-shadow: inset 0 0 10px rgba(255, 255, 0, 0.1);
}

.spot-wrap {
    display: contents;
}

.spot {
    margin: 15px 0;
    width: 100px;
    height: 130px;
    border: 3px solid yellow;
    border-radius: 3px;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: center;
    padding-bottom: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    color: white;
}

.road-group {
    flex: 0 0 100%;
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin: 20px 0;
}

.spot.spot.available::before {
    content: 'P';
    position: absolute;
    top: 10px;
    font-size: 40px;
    font-family: Helvetica;
    color: yellow;
}

.road-midline {
    width: 100%;
    height: 15px;
    background: repeating-linear-gradient(to right,
            white,
            white 60px,
            transparent 20px,
            transparent 105px);
    margin: 20px 0;
    border-radius: 2px;
}

.road-sideline {
    content: "";
    width: 100%;
    height: 15px;
    background-color: white;
}

.occupied .car-img {
    position: relative;
    top: 7.5px;
    width: 120px;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}


.spot.available p:last-child {
    color: limegreen;
    font-weight: bold;
}

.spot p {
    margin: 4px 0 0;
    z-index: 1;
}
</style>