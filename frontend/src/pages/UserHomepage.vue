<template>
    <div class="content">
        <div class="search">
            <form @submit.prevent="search">
                <h1>Search Parking Lot by</h1>
                <h2>Pincode/Location</h2>
                <div class="input-container">
                    <input name="search" v-model="s" placeholder="Enter pincode or location..." type="text" />
                    <button type="submit" class="button" :disabled="sloading">
                        {{ sloading ? "Searching..." : "Search" }}
                    </button>
                </div>
            </form>
        </div>
        <div v-if="searchData && searchData.search_results && searchData.search_results.length">
            <table>
                <thead>
                    <tr>
                        <th>LOT ID</th>
                        <th>Location</th>
                        <th>Address</th>
                        <th>Pincode</th>
                        <th>Price</th>
                        <th>Availability</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>

                    <tr v-for="lot in searchData.search_results" :key="lot.lot_id">
                        <td>{{ lot.lot_id }}</td>
                        <td>{{ lot.prime_location_name }}</td>
                        <td>{{ lot.address }}</td>
                        <td>{{ lot.pin_code }}</td>
                        <td>{{ lot.price }}</td>
                        <td>{{ lot.available ? "Available" : "Booked Out" }}</td>
                        <td>
                            <a v-if="lot.available" :href="`/user/booking/${userid}/${lot.lot_id}`"
                                class="green">Book</a>
                            <span v-else class="red">Not Available</span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <h4 v-else-if="searchData && searchData.search_results && !searchData.search_results.length">No Result</h4>

        <!-- Reservation History -->
        <div class="res">
            <h1 class="above">Recent Parking History</h1>

            <!-- Active Reservations -->
            <div v-if="reservatios && (reservatios.active_reservations.length || reservatios.last_reservation)">
                <table>
                    <thead>

                        <tr>
                            <th>ID</th>
                            <th>Location</th>
                            <th>Vehicle No.</th>
                            <th>Entry Date</th>
                            <th>Entry Time</th>
                            <th>Exit Date</th>
                            <th>Exit Time</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>

                        <!-- Active reservations -->
                        <tr v-for="r in reservatios.active_reservations" :key="r.res_id">
                            <td>{{ r.res_id }}</td>
                            <td>{{ r.address }}</td>
                            <td>{{ r.vehicle_no }}</td>
                            <td>{{ formatDate(r.entry_date) }}</td>
                            <td>{{ formatTime(r.entry_time) }}</td>
                            <td>{{ r.exit_date ? formatDate(r.exit_date) : "N/A" }}</td>
                            <td>{{ r.exit_time ? formatTime(r.exit_time) : "N/A" }}</td>
                            <td>
                                <a class="blue" @click.prevent="relese(r.res_id,r.entry_date,r.entry_time)" href="#">
                                    Release
                                </a>
                            </td>
                        </tr>
                        <!-- /user/release/${userid}/${r.res_id} -->
                        <!-- Last Reservation -->
                        <tr v-if="reservatios.last_reservation">
                            <td>{{ reservatios.last_reservation.res_id }}</td>
                            <td>{{ reservatios.last_reservation.address }}</td>
                            <td>{{ reservatios.last_reservation.vehicle_no }}</td>
                            <td>{{ formatDate(reservatios.last_reservation.entry_date) }}</td>
                            <td>{{ formatTime(reservatios.last_reservation.entry_time) }}</td>
                            <td>{{ formatDate(reservatios.last_reservation.exit_date) }}</td>
                            <td>{{ formatTime(reservatios.last_reservation.exit_time) }}</td>
                            <td><a href="#" class="red">Parked Out</a></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- No bookings -->
            <div v-else-if="resError" class="error">{{ resError }}</div>
            <h4 v-else class="no">No Bookings</h4>
        </div>
    </div>
</template>

<script>
export default {
    name: "UserHomePage",
    data() {
        return {
            userid: this.$route.params.id,
            s: "",
            reservatios: null,
            resError: null,
            searchData: null,
            serchError: null,
            rloading: false,
            sloading: false,
        };
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
            this.rloading = true;
            try {
                const response = await fetch(`http://127.0.0.1:5000/user/home/${this.userid}`, {
                    method: "GET",
                    headers: {
                        "Authorization": localStorage.getItem("token")
                    }
                });
                console.log(response)
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                this.reservatios = await response.json();
            } catch (err) {
                this.resError = err.message;
            } finally {
                this.rloading = false;
            }
        },
        async search() {
            this.sloading = true;
            try {
                const response = await fetch(`http://127.0.0.1:5000/user/home/search`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json", "Authorization": localStorage.getItem("token") },
                    body: JSON.stringify({ s: this.s }),
                });
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                this.searchData = await response.json();
            } catch (err) {
                this.serchError = err.message;
            } finally {
                this.sloading = false;
            }
        },
        formatDate(dateStr) {
            if (!dateStr) return "N/A";
            const date = new Date(dateStr);
            if (isNaN(date)) return dateStr; // fallback if parsing fails
            const day = String(date.getDate()).padStart(2, "0");
            const month = String(date.getMonth() + 1).padStart(2, "0");
            const year = date.getFullYear();
            return `${day}-${month}-${year}`;
        },
        formatTime(time) {
            if (!time) return "N/A";
            try {
                return time.length >= 5 ? time.slice(0, 5) : time;
            } catch {
                return time;
            }
        },
        relese(resid,date,time) {
            const dt = `${date}T${time}`;
            const targetDate = new Date(dt);
            const now = new Date();
            if (targetDate > now) {
                alert("Reservatiosn is in future can not relese now")
            } else if (targetDate <= now) {
                this.$router.push(`/user/release/${this.userid}/${resid}`);
            } 
        },
    },
};
</script>
