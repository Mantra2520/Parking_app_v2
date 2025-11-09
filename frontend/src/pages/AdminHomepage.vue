<template>
    <div class="content">
        <h1>Parking lots</h1>

        <div v-if="loading" class="loading">Loading Data...</div>

        <div v-else-if="errorMessage" class="error">{{ errorMessage }}</div>

        <div v-else-if="!lots || lots.length === 0">
            You don't have any parking lots. Please add one.
        </div>

        <div v-else class="lots-container">
            <div v-for="lot in lots" :key="lot.id" class="lot">
                <h3>Parking #{{ lot.id }}</h3>
                <div class="occupancy" :class="getOccupancy(lot)">
                    Occupied: {{ lot.os }}/{{ lot.ms }}
                </div>
                <div class="actions">
                    <!-- <a href="">Edit</a> -->
                    <router-link :to="`/admin/edit/${lot.id}`">Edit</router-link>
                    <a href="#" @click.prevent="deleteLot(lot)">Delete</a>
                    <router-link :to="`/admin/lot/${lot.id}`">See Details</router-link>
                </div>
            </div>
        </div>
        <div class="add-lot">
            <router-link :to="`/admin/addLot`">➕ Add a new Lot</router-link>
        </div>
    </div>
</template>

<script>
export default {
    name: "adminHomepage",
    data() {
        return {
            lots: null,
            errorMessage: null,
            loading: false
        };
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
                const response = await fetch('http://127.0.0.1:5000/admin/home');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                this.lots = await response.json();
            } catch (err) {
                this.errorMessage = err.message;
            } finally {
                this.loading = false;
            }
        },
        getOccupancy(lot) {
            if (lot.os === 0) {
                return "low"
            }

            const p = (lot.os / lot.ms) * 100;

            if (p === 100) return "full";
            if (p >= 60) return "mid";
            return "low";
        },
        async deleteLot(lot) {
            if (!confirm("Are you sure you want to delete this parking lot?")) {
                return;
            }
            if (lot.os > 0) {
                alert("There are Reservations in the Lot")
                return;
            }

            try {
                const token = localStorage.getItem("token");
                const response = await fetch(`http://127.0.0.1:5000/admin/delete_parking/${lot.id}`, {
                    method: "DELETE"
                });
                if (!response.ok) {
                    throw new Error(`Failed to delete. Status: ${response.status}`);
                }

                alert("Parking Lot deleted successfully!");
                // Refresh the lot list
                await this.fetchData();
            } catch (err) {
                alert(err.message);
            }

        }
    }

}
</script>

<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.content {
    font-family: 'Segoe UI', sans-serif;
    background-color: #f9f9f9;
    padding: 20px;
    height: 100vh;
}

h1 {
    font-size: 32px;
    font-weight: 800;
    text-align: center;
    color: #2c3e50;
    margin-top: 30px;
    width: fit-content;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 40px;
    letter-spacing: 1px;
}

.lots-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.lot {
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
}

.lot:hover {
    transform: scale(1.02);
}

.lot h3 {
    margin-bottom: 10px;
    font-size: 22px;
    color: #2c3e50;
}

.lot .actions a {
    padding-bottom: 0px;
    margin-right: 10px;
    background: linear-gradient(135deg, #4facfe, #00f2fe);
    -webkit-text-fill-color: transparent;
    -webkit-background-clip: text;
    text-decoration: none;
}

.lot .actions a:hover {
    border-bottom: 1px solid #00f2fe;
}

.occupancy {
    margin: 10px 0;
    font-weight: bold;
}

.occupancy.low {
    color: rgb(2, 178, 2);
}

.occupancy.mid {
    color: orange;
}

.occupancy.full {
    color: red;
}

.add-lot a {
    margin: 40px 20px 20px 0px;
    display: inline-block;
    padding: 12px 20px;
    background: linear-gradient(135deg, #4facfe, #00f2fe);
    color: white;
    text-decoration: none;
    font-weight: bold;
    border-radius: 6px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
    transition: 0.2s ease-in-out;
}

.add-lot a:hover {
    background: linear-gradient(135deg, #4fb6ff, #28f8ff);
    transform: scale(1.02);
}

h3 {
    text-align: center;
    margin-bottom: 40px;
    font-size: 28px;
    color: #2c3e50;
}

/* Loading text */
.loading {
    /* text-align: center; */
    font-size: 1.2rem;
    font-weight: 600;
    color: #2c3e50;
    margin-top: 20px;
    padding: 12px 20px;
    background: linear-gradient(135deg, #4facfe, #00f2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 0.5px;
    animation: pulse 1.5s ease-in-out infinite;
}

/* Error message */
.error {
    text-align: center;
    font-size: 1rem;
    font-weight: 600;
    color: #b00020;
    background-color: #ffe5e5;
    border: 1px solid #ffb3b3;
    border-radius: 8px;
    padding: 12px 16px;
    width: fit-content;
    margin: 20px auto;
    box-shadow: 0 2px 8px rgba(255, 0, 0, 0.1);
}

/* Subtle pulsing animation for "Loading..." */
@keyframes pulse {
    0% {
        opacity: 0.6;
    }

    50% {
        opacity: 1;
    }

    100% {
        opacity: 0.6;
    }
}
</style>