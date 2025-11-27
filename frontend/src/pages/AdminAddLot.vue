<template>
    <div class="content">
        <h1 style="margin-top: 100px;">Add New Parking Lot</h1>

        <div v-if="error" class="error">{{ error }}</div>

        <form style="margin-top: 30px;" @submit.prevent="addLot">
            <div class="input-group">
                <input required type="text" v-model="lotDetails.lot_id" autocomplete="off" class="input" placeholder=" "/>
                <label class="user-label">Lot ID</label>
            </div>

            <div class="input-group">
                <input required type="text" v-model="lotDetails.pl" autocomplete="off" class="input" placeholder=" "/>
                <label class="user-label">Prime Location</label>
            </div>

            <div class="input-group">
                <input required type="text" v-model="lotDetails.address" autocomplete="off" class="input" placeholder=" "/>
                <label class="user-label">Address</label>
            </div>

            <div class="input-group">
                <input required type="text" v-model="lotDetails.pin_code" autocomplete="off" class="input" placeholder=" "/>
                <label class="user-label">Pin Code</label>
            </div>

            <div class="input-group">
                <input required type="number" v-model="lotDetails.price" autocomplete="off" class="input" placeholder=" "/>
                <label class="user-label">Price</label>
            </div>

            <div class="input-group">
                <input required type="number" v-model="lotDetails.max_spots" autocomplete="off" class="input" placeholder=" "/>
                <label class="user-label">Max Spots</label>
            </div>

            <div>
                <input class="form-button" type="submit" value="Add" />
            </div>
        </form>

        
    </div>
</template>

<script>
export default {
    name: "AdminAddLot",
    data() {
        return {
            lotDetails: {
                lot_id: "",
                pl: "",
                address: "",
                pin_code: "",
                price: "",
                max_spots: ""
            },
            error: null,
            loading: false
        };
    },
    mounted() {
        const token = localStorage.getItem("token");
        const role = localStorage.getItem("role");
        if (!token || role !== "admin") {
            this.$router.push("/login");
            return;
        }
    },
    methods: {
        sanitize(details) {
            // trim strings and coerce numbers
            return {
                lot_id: (details.lot_id || "").trim(),
                pl: (details.pl || "").trim(),
                address: (details.address || "").trim(),
                pin_code: (details.pin_code || "").trim(),
                price: details.price === "" ? null : Number(details.price),
                max_spots: details.max_spots === "" ? null : Number(details.max_spots),
            };
        },

        async addLot() {
            if (this.loading) return;
            this.error = null;
            this.loading = true;

            try {
                const token = localStorage.getItem("token");
                const payload = this.sanitize(this.lotDetails);

                // simple client-side checks (optional)
                if (!payload.lot_id || !payload.pl || !payload.address || !payload.pin_code) {
                    throw new Error("Please fill all required fields.");
                }
                if (!Number.isFinite(payload.price) || payload.price < 0) {
                    throw new Error("Price must be a valid non-negative number.");
                }
                if (!Number.isInteger(payload.max_spots) || payload.max_spots <= 0) {
                    throw new Error("Max Spots must be a positive integer.");
                }

                const response = await fetch("http://127.0.0.1:5000/admin/add_parkinglot", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": localStorage.getItem("token"),
                        "Accept": "application/json"
                    },
                    body: JSON.stringify(payload)
                });

                if (!response.ok) {
                    // try to read error message from server
                    let serverMsg = "";
                    try {
                        const errJson = await response.json();
                        serverMsg = errJson?.message || errJson?.error || "";
                    } catch { }
                    throw new Error(serverMsg || `HTTP error! Status: ${response.status}`);
                }

                // success: optional reset
                this.lotDetails = {
                    lot_id: "",
                    pl: "",
                    address: "",
                    pin_code: "",
                    price: "",
                    max_spots: ""
                };

                alert("New parking lot added successfully!");
                this.$router.push("/admin/home");
            } catch (err) {
                this.error = err.message || "Something went wrong.";
            } finally {
                this.loading = false;
            }
        }
    }
};
</script>


