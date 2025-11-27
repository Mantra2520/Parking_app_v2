<template>
    <div class="content">
        <h1>Parking Lot Revenue Summary</h1>

        <div v-if="loading" class="status-box">Loading summary data...</div>
        <div v-else-if="error" class="status-box error">⚠️ {{ error }}</div>

        <div v-else-if="Data" class="cont">

            <div class="revenue-card">
                <h3>Total Revenue</h3>
                <p>₹{{ Data.total_rev.toFixed(2) }}</p>
            </div>

            <div class="charts-container">

                <div class="chart-box">
                    <h3>Revenue by Each Lots</h3>
                    <canvas ref="revenueChart"></canvas>
                </div>

                <div class="chart-box">
                    <h3>Available vs Occupied Parking Slots</h3>
                    <canvas ref="slotChart"></canvas>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
const Chart = window.Chart;

export default {
    name: "AdminSummary",

    data() {
        return {
            Data: null,
            error: null,
            loading: false,

            revChartInstance: null,
            slotChartInstance: null,
        };
    },

    mounted() {
        const token = localStorage.getItem("token");
        const role = localStorage.getItem("role");

        if (token && role === "admin") {
            this.fetchData();
        } else {
            window.location.href = "/";
        }
    },

    watch: {
        Data(newVal) {
            if (newVal) {
                this.$nextTick(() => {
                    setTimeout(() => this.renderCharts(), 80);
                });
            }
        }
    },

    methods: {
        async fetchData() {
            this.loading = true;
            try {
                const res = await fetch("http://127.0.0.1:5000/admin/summary", {
                    method: "GET",
                    headers: {
                        "Authorization": localStorage.getItem("token")
                    }});
                if (!res.ok) throw new Error("HTTP error " + res.status);
                this.Data = await res.json();
            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
        },

        renderCharts() {
            const lots = this.Data.lots;

            const labels = Object.values(lots).map(l => l.lot_label);
            const revenues = Object.values(lots).map(l => l.rev);
            const available = Object.values(lots).map(l => l.ava_count);
            const occupied = Object.values(lots).map(l => l.occ_count);

            /* ====== REVENUE CHART ====== */

            const ctx = this.$refs.revenueChart.getContext("2d");
            if (this.revChartInstance) this.revChartInstance.destroy();

            const gradient = ctx.createLinearGradient(0, 0, 0, 400);
            gradient.addColorStop(0, "rgba(54, 162, 235, 1)");
            gradient.addColorStop(1, "rgba(75, 192, 192, 0.5)");

            const maxRevenue = Math.max(...revenues) || 0;
            const yMax = maxRevenue === 0 ? 10 : Math.ceil(maxRevenue * 1.1);
            const yStep = maxRevenue === 0
                ? 2
                : Math.max(1, Math.round(maxRevenue / 5));

            this.revChartInstance = new Chart(ctx, {
                type: "bar",
                data: {
                    labels,
                    datasets: [
                        {
                            label: "Revenue (₹)",
                            data: revenues,
                            backgroundColor: gradient,
                            borderColor: "rgba(54,162,235,1)",
                            borderWidth: 1,
                            borderRadius: 5,
                            maxBarThickness: 120,
                            minBarLength: 5
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,

                    layout: {
                        padding: { top: 10, right: 10, bottom: 70, left: 10 }
                    },

                    animation: {
                        duration: 1000,
                        easing: "easeOutBounce"
                    },

                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true,
                                suggestedMax: Math.ceil(maxRevenue * 1.1),
                                stepSize: Math.max(1, Math.round(maxRevenue / 5)),
                                callback: function (value) {
                                    return value.toFixed(0);   // eliminate decimals
                                }
                            },
                            scaleLabel: {
                                display: true,
                                labelString: "Revenue in ₹"
                            }
                        }],
                        xAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: "Parking Lots"
                            }
                        }]
                    },

                    plugins: {
                        legend: {
                            display: true,
                            position: "top"
                        },
                        tooltip: {
                            callbacks: {
                                label: ctx => "₹" + ctx.parsed.y.toFixed(2)
                            }
                        }
                    }
                }
            });

            /* ====== SLOT CHART ====== */

            const sd = this.$refs.slotChart.getContext("2d");
            if (this.slotChartInstance) this.slotChartInstance.destroy();

            const gradientAvailable = sd.createLinearGradient(0, 0, 0, 400);
            gradientAvailable.addColorStop(0, "rgba(75,192,192,1)");
            gradientAvailable.addColorStop(1, "rgba(75,192,192,0.5)");

            const gradientOccupied = sd.createLinearGradient(0, 0, 0, 400);
            gradientOccupied.addColorStop(0, "rgba(255,99,132,1)");
            gradientOccupied.addColorStop(1, "rgba(255,99,132,0.5)");

            const maxSlots = Math.max(...available, ...occupied) || 0;
            const yMaxSlots = maxSlots === 0 ? 10 : Math.ceil(maxSlots * 1.1);
            const yStepSlots = maxSlots === 0
                ? 2
                : Math.max(1, Math.round(maxSlots / 5));

            this.slotChartInstance = new Chart(sd, {
                type: "bar",
                data: {
                    labels,
                    datasets: [
                        {
                            label: "Available",
                            stack: "slots",
                            data: available,
                            backgroundColor: gradientAvailable,
                            borderRadius: 5,
                            borderSkipped: false,
                            maxBarThickness: 120,
                            minBarLength: 5
                        },
                        {
                            label: "Occupied",
                            stack: "slots",
                            data: occupied,
                            backgroundColor: gradientOccupied,
                            borderRadius: 5,
                            borderSkipped: false,
                            maxBarThickness: 120,
                            minBarLength: 5
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,

                    layout: {
                        padding: { top: 10, right: 10, bottom: 70, left: 10 }
                    },

                    animation: {
                        duration: 1200,
                        easing: "easeOutBounce"
                    },

                    scales: {
                        yAxes: [{
                            stacked: true,
                            ticks: {
                                beginAtZero: true,
                                suggestedMax: Math.ceil(maxSlots * 1.1),
                                stepSize: Math.max(1, Math.round(maxSlots / 5))
                            },
                            scaleLabel: {
                                display: true,
                                labelString: "Number of Slots"
                            }
                        }],
                        xAxes: [{
                            stacked: true,
                            scaleLabel: {
                                display: true,
                                labelString: "Parking Lot"
                            }
                        }]
                    },

                    plugins: {
                        legend: { position: "top" },
                        tooltip: {
                            callbacks: {
                                label: ctx => `${ctx.dataset.label}: ${ctx.parsed.y}`
                            }
                        }
                    }
                }
            });
        }
    }
};
</script>

<style scoped>
.content {
    font-family: 'Segoe UI', sans-serif;
}

.revenue-card {
    background: linear-gradient(135deg, #4facfe, #00f2fe);
    color: white;
    padding: 1.5rem;
    border-radius: 12px;
    width: fit-content;
    margin: 24px auto 24px auto;
    text-align: center;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
    animation: pop-in 0.6s ease-out;
}

.revenue-card h3 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 500;
    color: black;
}

.revenue-card p {
    margin: 0.5rem 0 0;
    font-size: 2rem;
    font-weight: bold;
}

@keyframes pop-in {
    0% {
        transform: scale(0.8);
        opacity: 0;
    }

    100% {
        transform: scale(1);
        opacity: 1;
    }
}

.charts-container {
    display: flex;
    justify-content: center;
    gap: 40px;
    flex-wrap: wrap;
}

.chart-box {
    width: 670px;
    height: 450px;
    /* a bit taller to give more room */
    background-color: #fff;
    padding: 20px;
    border: 2px solid #ddd;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

canvas {
    width: 100% !important;
    height: 100% !important;
}
</style>
