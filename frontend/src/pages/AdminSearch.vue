<template>
    <div class="content">
        <div class="search">
            <form @submit.prevent="search">
                <h1 style="margin-bottom: 25px;">Search</h1>
                <div class="input-container">
                    <input v-model="query" placeholder="Search..." type="text" />
                    <button type="submit" class="button" :disabled="loading">
                        {{ loading ? "Searching..." : "Search" }}
                    </button>
                </div>
            </form>
        </div>

        <div v-if="Data">

            <!-- No Result -->
            <h3 v-if="Data.type === 'none'">{{ Data.message }}</h3>

            <!-- USER RESULT -->
            <div v-if="Data.type === 'user'">
                <h2>User Details</h2>
                <table>
                    <thead>
                        <tr>
                            <th>User ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Address</th>
                            <th>Pincode</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{{ Data.user.userid }}</td>
                            <td>{{ Data.user.fullname }}</td>
                            <td>{{ Data.user.email }}</td>
                            <td>{{ Data.user.address }}</td>
                            <td>{{ Data.user.pincode }}</td>
                        </tr>
                    </tbody>
                </table>

                <h2>Reservations</h2>
                <table v-if="Data.reservations.length > 0">
                    <thead>
                        <tr>
                            <th>Reservation ID</th>
                            <th>User ID</th>
                            <th>Spot ID</th>
                            <th>Vehicle No</th>
                            <th>Entry Date</th>
                            <th>Exit Date</th>
                            <th>In Time</th>
                            <th>Out Time</th>
                            <th>Cost</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="r in Data.reservations" :key="r.res_id">
                            <td>{{ r.res_id }}</td>
                            <td>{{ r.user_id }}</td>
                            <td>{{ r.spot_id }}</td>
                            <td>{{ r.vehicle_no }}</td>
                            <td>{{ r.in_date }}</td>
                            <td>{{ r.out_date }}</td>
                            <td>{{ r.in_time }}</td>
                            <td>{{ r.out_time }}</td>
                            <td>{{ r.cost_unit_time }}</td>
                        </tr>
                    </tbody>
                </table>

                <p v-else>No reservations</p>
            </div>

            <!-- LOT RESULT -->
            <div v-if="Data.type === 'lot'">
                <h2>Parking Lot Details</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Lot ID</th>
                            <th>Location</th>
                            <th>Address</th>
                            <th>Pincode</th>
                            <th>Price</th>
                            <th>Max Spots</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{{ Data.lot.lot_id }}</td>
                            <td>{{ Data.lot.prime_location_name }}</td>
                            <td>{{ Data.lot.address }}</td>
                            <td>{{ Data.lot.pin_code }}</td>
                            <td>{{ Data.lot.price }}</td>
                            <td>{{ Data.lot.max_spots }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- SPOT RESULT -->
            <div v-if="Data.type === 'spot'">
                <h2>Parking Spot</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Spot ID</th>
                            <th>Lot ID</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{{ Data.spot.spot_id }}</td>
                            <td>{{ Data.spot.lot_id }}</td>
                            <td>{{ Data.spot.status === 'A' ? 'Available' : 'Occupied' }}</td>
                        </tr>
                    </tbody>
                </table>

                <div v-if="Data.current_reservation">
                    <h2>Current Reservation</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Reservation ID</th>
                                <th>User ID</th>
                                <th>Vehicle</th>
                                <th>In</th>
                                <th>Out</th>
                            </tr>
                        </thead>
                        <tbody>

                            <tr>
                                <td>{{ Data.current_reservation.res_id }}</td>
                                <td>{{ Data.current_reservation.user_id }}</td>
                                <td>{{ Data.current_reservation.vehicle_no }}</td>
                                <td>{{ Data.current_reservation.in_time }}</td>
                                <td>{{ Data.current_reservation.out_time }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- RESERVATION RESULT -->
            <div v-if="Data.type === 'reservation'">
                <h2>Reservation Details</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Reservation ID</th>
                            <th>User ID</th>
                            <th>Spot ID</th>
                            <th>Vehicle</th>
                            <th>In</th>
                            <th>Out</th>
                        </tr>
                    </thead>
                    <tbody>

                        <tr>
                            <td>{{ Data.reservation.res_id }}</td>
                            <td>{{ Data.reservation.user_id }}</td>
                            <td>{{ Data.reservation.spot_id }}</td>
                            <td>{{ Data.reservation.vehicle_no }}</td>
                            <td>{{ Data.reservation.in_time }}</td>
                            <td>{{ Data.reservation.out_time }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- VEHICLE RESULT (NEW) -->
            <div v-if="Data.type === 'vehicle'">
                <h2>Vehicle Reservations</h2>
                <table v-if="Data.reservations.length > 0">
                    <thead>
                        <tr>
                            <th>Reservation ID</th>
                            <th>User ID</th>
                            <th>Spot ID</th>
                            <th>Vehicle No</th>
                            <th>Entry Date</th>
                            <th>Exit Date</th>
                            <th>In Time</th>
                            <th>Out Time</th>
                            <th>Cost</th>
                        </tr>
                    </thead>
                    <tbody>

                        <tr v-for="r in Data.reservations" :key="r.res_id">
                            <td>{{ r.res_id }}</td>
                            <td>{{ r.user_id }}</td>
                            <td>{{ r.spot_id }}</td>
                            <td>{{ r.vehicle_no }}</td>
                            <td>{{ r.in_date }}</td>
                            <td>{{ r.out_date }}</td>
                            <td>{{ r.in_time }}</td>
                            <td>{{ r.out_time }}</td>
                            <td>{{ r.cost_unit_time }}</td>
                        </tr>
                    </tbody>
                </table>

                <p v-else>No reservations found for this vehicle.</p>
            </div>

            <!-- LOCATION RESULT -->
            <div v-if="Data.type === 'location'">
                <table>
                    <thead>
                        <tr>
                            <th>Lot ID</th>
                            <th>Prime Location</th>
                            <th>Address</th>
                            <th>Pincode</th>
                            <th>Price</th>
                            <th>Max Spots</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="lot in Data.lots" :key="lot.lot_id">
                            <td>{{ lot.lot_id }}</td>
                            <td>{{ lot.prime_location_name }}</td>
                            <td>{{ lot.address }}</td>
                            <td>{{ lot.pin_code }}</td>
                            <td>{{ lot.price }}</td>
                            <td>{{ lot.max_spots }}</td>
                        </tr>
                    </tbody>
                </table>

                <p v-if="Data.lots.length === 0">No lots found in this location.</p>
            </div>

        </div>

    </div>
</template>


<script>
export default {
    name: 'AdminSearch',
    data() {
        return {
            query: null,
            Data: null,
            error: null,
            loading: false,
        }
    },
    mounted() {
        const token = localStorage.getItem("token");
        const role = localStorage.getItem("role");

        if (token && role === "admin") {
            this.null();
        } else {
            this.$router.push("/");
        }

    },
    methods: {
        async search() {
            this.loading = true;
            try {
                const response = await fetch('http://127.0.0.1:5000/admin/search', {
                    method: "POST",
                    headers: { 
                        "Content-Type": "application/json",
                        "Authorization": localStorage.getItem("token")
                     },
                    body: JSON.stringify({ "query": this.query }),
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                this.Data = await response.json();
            } catch (err) {
                this.errorMessage = err.message;
            } finally {
                this.loading = false;
            }
            console.log(this.Data)
        },
        null() {

        }
    }
}
</script>