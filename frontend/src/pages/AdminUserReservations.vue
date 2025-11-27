<template>
    <div class="content">
        <h1>User Reservations</h1>
        <h4 class="grey">User ID : {{ Data.userid }} | Email: {{ Data.email }}</h4>
        <div v-if="Data.reservations.length > 0">
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
                        <th>Cost/Hour</th>
                    </tr>
                </thead>
                <tbody>

                    <!-- Active reservations -->
                    <tr v-for="r in Data.reservations" :key="r.res_id">
                        <td>{{ r.res_id }}</td>
                        <td>{{ r.address }}</td>
                        <td>{{ r.vehicle_no }}</td>
                        <td>{{ formatDate(r.entry_date) }}</td>
                        <td>{{ formatTime(r.entry_time) }}</td>
                        <td>{{ r.exit_date ? formatDate(r.exit_date) : "N/A" }}</td>
                        <td>{{ r.exit_time ? formatTime(r.exit_time) : "N/A" }}</td>
                        <td>₹{{ r.cost }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
export default {
    name: 'AdminUserReservation',
    data() {
        return {
            userid: this.$route.params.id,
            Data: { reservations: [] },
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
            this.$router.push("/");
        }
    },
    methods: {
        async fetchData() {
            this.loading = true;

            try {
                const response = await fetch(`http://127.0.0.1:5000/admin/user/${this.userid}`, {
                    method: "GET",
                    headers: {
                        "Authorization": localStorage.getItem("token")
                    }})
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                this.Data = await response.json();
            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
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

    }
}
</script>