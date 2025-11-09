<template>
    <div class="content">
        <h1>Parking Lot #{{ lotid }}</h1>

        <div v-if="loading" class="loading">Loading...</div>
        <div v-else-if="errorMessage" class="error">{{ errorMessage }}</div>

        <div v-else>
            <form @submit.prevent="editLot">
                <div class="input-group">
                    <input required type="text" v-model="details.prime_location_name" autocomplete="off" class="input"
                        placeholder=" " />
                    <label class="user-label">Prime Location</label>
                </div>

                <div class="input-group">
                    <input required type="text" v-model="details.address" autocomplete="off" class="input"
                        placeholder=" " />
                    <label class="user-label">Address</label>
                </div>

                <div class="input-group">
                    <input required type="text" v-model="details.pin_code" autocomplete="off" class="input"
                        placeholder=" " />
                    <label class="user-label">Pin code</label>
                </div>

                <div class="input-group">
                    <input required type="number" v-model="details.price" autocomplete="off" class="input"
                        placeholder=" " />
                    <label class="user-label">Price per Hour</label>
                </div>

                <div class="input-group">
                    <input disabled type="number" v-model="details.max_spots" autocomplete="off" class="input"
                        placeholder=" " />
                    <label class="user-label">Max Spots</label>
                </div>

                <div>
                    <input type="submit" value="Update" />
                </div>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    name: "adminEditLot",
    data() {
        return {
            lotid: this.$route.params.id,
            lotDetails: null,
            errorMessage: null,
            details: {
                prime_location_name: "",
                address: "",
                pin_code: "",
                price: "",
                max_spots: "",
            },
            loading: false,
        }
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
                const response = await fetch(`http://127.0.0.1:5000/admin/lot_details/${this.lotid}`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                this.lotDetails = await response.json();
                this.details.prime_location_name = this.lotDetails.prime_location_name
                this.details.price = this.lotDetails.price
                this.details.pin_code = this.lotDetails.pin_code
                this.details.address = this.lotDetails.address
                this.details.max_spots = this.lotDetails.max_spots

            } catch (err) {
                this.errorMessage = err.message;
            } finally {
                this.loading = false;
            }

        },
        async editLot() {
            this.loading = true;
            this.errorMessage = null;
            try {
                const response = await fetch(
                    `http://127.0.0.1:5000/admin/edit_parking/${this.lotid}`,
                    {
                        method: "PUT",
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": `Bearer ${localStorage.getItem("token")}`,
                        },
                        body: JSON.stringify(this.details),
                    }
                );

                if (!response.ok) throw new Error(`Update failed! Status: ${response.status}`);

                alert("Parking Lot updated successfully!");
                this.$router.push("/admin/home");
            } catch (err) {
                this.errorMessage = err.message;
            } finally {
                this.loading = false;
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

/* body {} */

.content {
    padding: 20px;
    background-color: #f2f2f2;
    /* padding-top: 60px; */
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
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

.input:focus~label,
input:valid~label {
    transform: translateY(-50%) scale(0.8);
    background-color: #ffffff;
    padding: 0 0.2em;
    color: black;
}

.input:not(:placeholder-shown)~.user-label {
    transform: translateY(-50%) scale(0.8);
    background-color: #ffffff;
    padding: 0 0.2em;
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

input[disabled] {
    cursor: not-allowed;
}

/* Add optional loading and error styling */
.loading {
    text-align: center;
    font-weight: bold;
    font-size: 1.2rem;
    color: #4facfe;
    animation: pulse 1.5s ease-in-out infinite;
}

.error {
    text-align: center;
    background: #ffe5e5;
    color: #a10000;
    border: 1px solid #ffb3b3;
    padding: 10px 16px;
    border-radius: 8px;
    margin: 20px auto;
    width: fit-content;
}

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