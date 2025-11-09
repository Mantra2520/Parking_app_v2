<template>
    <div class="content">
        <h1>Add New Parking Lot</h1>

        <div v-if="error" class="error">{{ error }}</div>

        <form @submit.prevent="addLot">
            <div class="input-group">
                <input required type="text" v-model="lotDetails.lot_id" autocomplete="off" class="input" />
                <label class="user-label">Lot ID</label>
            </div>

            <div class="input-group">
                <input required type="text" v-model="lotDetails.pl" autocomplete="off" class="input" />
                <label class="user-label">Prime Location</label>
            </div>

            <div class="input-group">
                <input required type="text" v-model="lotDetails.address" autocomplete="off" class="input" />
                <label class="user-label">Address</label>
            </div>

            <div class="input-group">
                <input required type="text" v-model="lotDetails.pin_code" autocomplete="off" class="input" />
                <label class="user-label">Pin Code</label>
            </div>

            <div class="input-group">
                <input required type="number" v-model="lotDetails.price" autocomplete="off" class="input" />
                <label class="user-label">Price</label>
            </div>

            <div class="input-group">
                <input required type="number" v-model="lotDetails.max_spots" autocomplete="off" class="input" />
                <label class="user-label">Max Spots</label>
            </div>

            <div>
                <input type="submit" value="Add" />
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
                        ...(token ? { "Authorization": `Bearer ${token}` } : {}),
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



<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background-color: #f2f2f2;
    padding-top: 60px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.content {
    padding: 20px;
}

h1 {
    font-size: 32px;
    font-weight: 800;
    text-align: center;
    color: #2c3e50;
    margin: 40px auto 30px auto;
    letter-spacing: 1px;
}

form {
    width: 90%;
    max-width: 600px;
    margin: 20px auto;
    background-color: #ffffff;
    padding: 30px 28px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    display: flex;
    flex-direction: column;
    gap: 18px;
}

form div {
    display: flex;
    flex-direction: column;
}

.input-group {
    position: relative;
}

.input {
    border: solid 1.5px #9e9e9e;
    border-radius: 10px;
    background: none;
    padding: 1rem;
    font-size: 1rem;
    color: black;
    transition: border 150ms cubic-bezier(0.4, 0, 0.2, 1);
}

.user-label {
    position: absolute;
    left: 15px;
    color: black;
    pointer-events: none;
    transform: translateY(1rem);
    transition: 150ms cubic-bezier(0.4, 0, 0.2, 1);
}

.input:focus,
input:valid {
    outline: none;
    border: 1.5px solid #4facfe;
}

.input:focus~.user-label,
input:valid~.user-label {
    transform: translateY(-50%) scale(0.8);
    background-color: #ffffff;
    padding: 0 .2em;
    color: black;
}

input[type="submit"] {
    margin: 10px 200px 0 200px;
    padding: 12px;
    background: linear-gradient(135deg, #4facfe, #00f2fe);
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
}

input[type="submit"]:hover {
    background: linear-gradient(135deg, #4fb6ff, #28f8ff);
    transform: scale(1.03);
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1);
}

.error {
    color: red;
    text-align: center;
    margin-top: 15px;
}
</style>