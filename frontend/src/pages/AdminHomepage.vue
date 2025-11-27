<template>
    <div class="content lot-content">
        <h1>Parking lots</h1>

        <div v-if="loading" class="loading">Loading Data...</div>

        <div v-else-if="errorMessage" class="error">{{ errorMessage }}</div>

        <div v-else-if="!lots || lots.length === 0">
            You don't have any parking lots. Please add one.
        </div>

        <div v-else class="lots-container">
            <div v-for="lot in lots" :key="lot.id" class="lot">
                <h3 class="lot-h3">Parking #{{ lot.id }}</h3>
                <div class="occupancy" :class="getOccupancy(lot)">
                    Occupied: {{ lot.os }}/{{ lot.ms }}
                </div>
                <div class="actions">
                    <!-- <a href="">Edit</a> -->
                    <router-link class="blue" :to="`/admin/edit/${lot.id}`">Edit</router-link>
                    <a class="blue" href="#" @click.prevent="deleteLot(lot)">Delete</a>
                    <router-link class="blue" :to="`/admin/lot/${lot.id}`">See Details</router-link>
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
            this.$router.push("/");
        }

    },
    methods: {
        async fetchData() {
            this.loading = true;
            try {
                const response = await fetch('http://127.0.0.1:5000/admin/home', {
                    method: "GET",
                    headers: {
                        "Authorization": localStorage.getItem("token")
                    }
                });
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
                    method: "DELETE",
                    headers: {
                        "Authorization": localStorage.getItem("token")
                    }
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
