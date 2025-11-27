<template>
    <div class="content">
        <div class="spot-details-container">
            <div v-if="loading" class="loading">Loading details...</div>
            <div v-else-if="error" class="error">{{ error }}</div>
            <div v-else-if="Data">
                <h1>Parking Spot #{{ Data.spotid }}</h1>

                <table class="details-table">
                    <thead>
                        <tr>
                            <th>Spot ID</th>
                            <th>Lot ID</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{{ Data.spotid }}</td>
                            <td>{{ Data.lotid }}</td>
                            <td>{{ Data.status === 'A' ? 'Available' : 'Occupied' }}</td>
                        </tr>
                    </tbody>
                </table>

                <h2>Reservation Details</h2>
                <table class="details-table">
                    <thead>
                        <tr>
                            <th>Reservation ID</th>
                            <th>User ID</th>
                            <th>Spot ID</th>
                            <th>Vehicle No</th>
                            <th>Entry Date</th>
                            <th>In Time</th>
                            <th>Cost per Hour</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{{ Data.res_id }}</td>
                            <td>{{ Data.userid }}</td>
                            <td>{{ Data.spotid }}</td>
                            <td>{{ Data.vehicle_no }}</td>
                            <td>{{ formatDate(Data.entry_date) }}</td>
                            <td>{{ formatTime(Data.entry_time) }}</td>
                            <td>{{ Data.cost }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

</template>

<script>
export default {
    name: 'AdminSpotDetails',
    data() {
        return {
            spotid: this.$route.params.id,
            Data: null,
            error: null,
            loading: false
        }
    },
    mounted() {
        const token = localStorage.getItem("token");
        const role = localStorage.getItem("role");

        if (token && role === "admin") {
            this.fetchData();
        } else {
            this.$router.push("/");
        }
    },
    methods: {
        async fetchData() {
            this.loading = true;
            try {
                const response = await fetch(`http://127.0.0.1:5000/admin/spot_details/${this.spotid}`, {
                    method: "GET",
                    headers: {
                        "Authorization": localStorage.getItem("token")
                    }});
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                this.Data = await response.json();
            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
            console.log(this.Data);
        },
        formatDate(dateStr) {
            if (!dateStr) return '-';
            const date = new Date(dateStr);
            return date.toISOString().split('T')[0];
        },
        formatTime(timeStr) {
            if (!timeStr) return '-';
            // handle string like "11:00:00" or "11:00"
            return timeStr.slice(0, 5);
        }
    }
}
</script>