<template>
    <div class="content">
        <h1>Booking</h1>

        <!-- Loading -->
        <div v-if="loading" class="loading">Loading...</div>

        <!-- Error -->
        <div v-if="error" class="error">{{ error }}</div>

        <form v-if="!loading && !error" style="margin-top: 30px;" @submit.prevent="book">
            <div class="input-group">
                <input required type="text" v-model="data.lotid" class="input" disabled />
                <label class="user-label">Lot ID</label>
            </div>

            <div class="input-group">
                <input required type="text" v-model="data.spotid" class="input" disabled />
                <label class="user-label">Spot ID</label>
            </div>

            <div class="input-group">
                <input required type="text" v-model="data.userid" class="input" disabled />
                <label class="user-label">User ID</label>
            </div>

            <div class="input-group">
                <input required type="text" v-model="vno" placeholder=" " @input="vno = vno.toUpperCase()"
                    class="input" />
                <label class="user-label">Vehicle No.</label>
            </div>

            <div class="input-group">
                <input required type="date" v-model="indate" class="input" />
                <label class="user-label">date</label>
            </div>

            <div class="input-group">
                <input required type="time" v-model="intime" class="input" />
                <label class="user-label">date</label>
            </div>

            <div class="input-group">
                <input required type="text" v-model="data.location" class="input" disabled />
                <label class="user-label">Address</label>
            </div>

            <div class="input-group">
                <input required type="number" v-model="data.price" class="input" disabled />
                <label class="user-label">Price (/hour)</label>
            </div>


            <div>
                <input class="form-button" type="submit" value="Book" />
            </div>
        </form>
    </div>
</template>
<script>
export default {
    name: 'UserBooking',
    data() {
        return {
            userid: this.$route.params.id,
            lotid: this.$route.params.lid,
            vno: null,
            indate: null,
            intime: null,
            data: {
                "lotid": null,
                "spotid": null,
                "userid": null,
                "location": null,
                "price": null
            },
            error: null,
            loading: false,
        }
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
        // -----------------------------
        // Fetch booking details
        // -----------------------------
        async fetchData() {
            this.loading = true;
            this.error = null;

            try {
                const res = await fetch(`http://127.0.0.1:5000/user/booking/${this.userid}/${this.lotid}`, {
                    method: "GET",
                    headers: {
                        "Authorization": localStorage.getItem("token")
                    }
                });

                if (!res.ok) {
                    throw new Error("Unable to fetch booking details.");
                }

                const json = await res.json();

                // Backend: {error: "..."} case
                if (json.error) {
                    this.error = json.error;
                    return;
                }

                this.data = json;

            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
        },

        // -----------------------------
        // Book parking
        // -----------------------------
        async book() {
            console.log(String(this.indate))
            console.log(String(this.intime))
            const pattern = /^[A-Za-z]{2}\d{2}[A-Za-z]{2}\d{4}$/;


            if (!pattern.test(this.vno)) {
                alert("Invalid vehicle number format. Example: GJ01AB1234")
                return;
            }

            if (!this.checkDateTime(this.indate, this.intime)) {
                return;
            }

            this.loading = true;
            this.error = null;



            try {
                const res = await fetch(`http://127.0.0.1:5000/user/booking/${this.userid}/${this.lotid}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "Authorization": localStorage.getItem("token")
                    },
                    body: JSON.stringify({
                        vno: this.vno,
                        indate: this.indate,
                        intime: String(this.intime),
                        spotid: String(this.data.spotid)
                    })
                });

                if (!res.ok) {
                    throw new Error("Booking failed. Please try again.");
                }

                const json = await res.json();

                alert(json.message || "Reservation completed successfully!");
                this.$router.push(`/user/home/${this.userid}`);

            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
        },
        checkDateTime(indate, intime) {
            if (!indate || !intime) {
                alert("Please select both date and time.");
                return false;
            }

            // Full datetime from user input (already IST)
            const fullInput = new Date(`${indate}T${intime}:00`);

            // Current IST time
            const now = new Date();

            // Create 2 months later date
            const twoMonthsLater = new Date();
            twoMonthsLater.setMonth(twoMonthsLater.getMonth() + 2);

            // --- VALIDATIONS ---
            if (fullInput < now) {
                alert("Selected date & time is in the past.");
                return false;
            }

            if (fullInput > twoMonthsLater) {
                alert("Bookings allowed only within the next 2 months.");
                return false;
            }

            return true;
        }
    }
}
</script>