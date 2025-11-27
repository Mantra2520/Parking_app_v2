<template>
    <div class="content">
        <h1>Summary</h1>

        <div v-if="loading" class="loading">Loading user summary...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else>
            <div class="details-box">
                <div class="div2">
                    <p><strong>No. of bookings:</strong> {{ Data.stats.total_completed }}</p>
                    <p><strong>Total money spent:</strong> ₹{{ Data.stats.total_money }}</p>
                    <p><strong>Total parked time:</strong> {{ Data.stats.total_hours }} hrs</p>
                </div>

                <div class="vertical-line"></div>

                <div class="div3">
                    <p><strong>Most used Lot:</strong> {{ Data.stats.most_used_lot || 'N/A' }}</p>
                    <p v-if="Data.stats.total_completed > 0">
                        <strong>Avg. money spent:</strong>
                        ₹{{ (Data.stats.total_money / Data.stats.total_completed).toFixed(2) }}
                    </p>
                    <p v-else>
                        <strong>Avg. money spent:</strong>
                        N/A
                    </p>
                    <p v-if="Data.stats.total_completed > 0">
                        <strong>Avg. time spent:</strong>
                        {{ (Data.stats.total_hours / Data.stats.total_completed).toFixed(1) }} hrs
                    </p>
                    <p v-else>
                        <strong>Avg. time spent:</strong>
                        N/A
                    </p>
                </div>
            </div>
            <h1>Parked vehicle</h1>
            <div v-if="Data.active_reservations.length > 0">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Location</th>
                            <th>Vehicle No.</th>
                            <th>Entry Date</th>
                            <th>Entry Time</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="r in Data.active_reservations" :key="r.res_id">
                            <td>{{ r.res_id }}</td>
                            <td>{{ r.address }}</td>
                            <td>{{ r.vno }}</td>
                            <td>{{ formatDate(r.entry_date) }}</td>
                            <td>{{ formatTime(r.entry_time) }}</td>
                            <td>
                                <a class="blue" :href="`/user/release/${userid}/${r.res_id}`">
                                    Release
                                </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div v-else>
                <p class="no">No active parked vehicles.</p>
            </div>
            <h1>Last 10 Resarvations</h1>
            <div v-if="Data.past_reservations.length > 0">
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
                            <th>Cost</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="r in Data.past_reservations.slice(0, 10)" :key="r.res_id">
                            <td>{{ r.res_id }}</td>
                            <td>{{ r.address }}</td>
                            <td>{{ r.vno }}</td>
                            <td>{{ formatDate(r.in_date) }}</td>
                            <td>{{ formatTime(r.in_time) }}</td>
                            <td>{{ formatDate(r.out_date) }}</td>
                            <td>{{ formatTime(r.out_time) }}</td>
                            <td>₹{{ r.cost }}</td>
                            <td>
                                <!-- ✅ Book Again / Booked Logic -->
                                <a :href="`/user/booking/${userid}/${r.lot_id}`" v-if="r.available_spots" class="green"
                                    @click="">
                                    Book Again
                                </a>

                                <a href="#" v-else class="red" disabled>
                                    Booked
                                </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div v-else>
                <p class="no">No reservation history yet.</p>
            </div>
            <div class="export-section">
                <button class="export-btn" @click.prevent="Export()" :disabled="isExporting">
                    <span v-if="!isExporting && !exportDone">⬇ Export CSV</span>
                    <span v-if="isExporting" class="loader"></span>
                    <span v-if="exportDone">✔ Download Ready!</span>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "UserSummary",
    data() {
        return {
            isExporting: false,
            exportDone: false,
            userid: this.$route.params.id,
            Data: {
                active_reservations: [],
                past_reservations: [],
                stats: {
                    total_hours: 0,
                    total_money: 0,
                    most_used_lot: null,
                    total_completed: 0
                }
            },
            error: null,
            loading: false,
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
            this.loading = true;
            try {
                const response = await fetch(`http://127.0.0.1:5000/user/summary/${this.userid}`, {
                    method: "GET",
                    headers: {
                        "Authorization": localStorage.getItem("token")
                    }
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! stats: ${response.stats}`);
                }

                this.Data = await response.json();
            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
            console.log(this.Data)
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
        async Export() {
            this.isExporting = true;
            this.exportDone = false;

            let response;

            try {
                response = await fetch(`http://127.0.0.1:5000/user/export/csv/${this.userid}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": localStorage.getItem("token")
                    },
                    body: JSON.stringify({})
                });

                const data = await response.json();
                this.startPollingExport(data.task_id);

            } catch (err) {
                alert("Error exporting: " + err.message);
                this.isExporting = false;
            }
        },

        async startPollingExport(task_id) {
            const poll = setInterval(async () => {
                const res = await fetch(`http://127.0.0.1:5000/user/export/csv/status/${task_id}`);
                const data = await res.json();

                if (data.state === "SUCCESS") {
                    clearInterval(poll);

                    this.isExporting = false;
                    this.exportDone = true;

                    // Auto-download
                    window.open(data.file_url, "_blank");

                    // Reset after 4 sec
                    setTimeout(() => {
                        this.exportDone = false;
                    }, 4000);
                }
            }, 1500);
        }
    }
}
</script>
<style>
.export-section {
    margin: 20px;
    text-align: right;
    padding-bottom: 20px;
}

.export-btn {
    background: linear-gradient(135deg, #4facfe, #00f2fe);
    border: none;
    padding: 10px 18px;
    font-size: 16px;
    color: white;
    border-radius: 6px;
    cursor: pointer;
    transition: 0.3s ease;
}

.export-btn:hover {
    background: linear-gradient(135deg, #4fb6ff, #28f8ff);
}

.export-btn:disabled {
    background-color: #b5b5b5;
    cursor: not-allowed;
}

.loader {
    border: 3px solid #f3f3f3;
    border-top: 3px solid white;
    border-radius: 50%;
    width: 16px;
    height: 16px;
    animation: spin 0.7s linear infinite;
    display: inline-block;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
