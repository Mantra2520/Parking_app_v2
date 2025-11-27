<template>
    <div class="content">
        <h1>Profile Page</h1>
        <form @submit.prevent="UpdUser()" style="margin-top: 30px;" method="post">
            <div class="input-group">
                <input required type="text" name="userid" v-model="UserData.userid" placeholder=" " autocomplete="off"
                    class="input" disabled>
                <label class="user-label">User ID</label>
            </div>

            <div class="input-group">
                <input required type="text" name="fullname" v-model="UserData.fullname" placeholder=" "
                    autocomplete="off" class="input">
                <label class="user-label">Fullname</label>
            </div>

            <div class="input-group">
                <input required type="text" name="email" v-model="UserData.email" placeholder=" " autocomplete="off"
                    class="input">
                <label class="user-label">Email</label>
            </div>

            <div class="input-group">
                <input required type="text" name="address" v-model="UserData.address" placeholder=" " autocomplete="off"
                    class="input">
                <label class="user-label">Address</label>
            </div>

            <div class="input-group">
                <input required type="text" name="pincode" v-model="UserData.pincode" placeholder=" " autocomplete="off"
                    class="input">
                <label class="user-label">Pincode</label>
            </div>

            <div>
                <input class="form-button" type="submit" value="Update">
            </div>
        </form>
    </div>
</template>

<script>
export default {
    name: "UserProfile",
    data() {
        return {
            userid: this.$route.params.id,
            UserData: {
                "userid": null,
                "fullname": null,
                "email": null,
                "address": null,
                "pincode": null
            },
            UpdUserData: {
                "fullname": null,
                "email": null,
                "address": null,
                "pincode": null
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
        async fetchData() {
            this.loading = true;
            try {
                const response = await fetch(`http://127.0.0.1:5000/user/profile/${this.userid}`, {
                    method: "GET",
                    headers: {
                        "Authorization": localStorage.getItem("token")
                    }
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                this.UserData = await response.json();

            } catch (err) {
                this.errorMessage = err.message;
            } finally {
                this.loading = false;
            }
            console.log(this.UserData)
        },
        async UpdUser() {
            this.loading = true;
            this.errorMessage = null;
            this.UpdUserData={
                "fullname": this.UserData.fullname,
                "email": this.UserData.email,
                "address": this.UserData.address,
                "pincode": this.UserData.pincode
            }
            try {
                const response = await fetch(
                    `http://127.0.0.1:5000/user/profile/${this.userid}`,
                    {
                        method: "PUT",
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": localStorage.getItem("token")
                        },
                        body: JSON.stringify(this.UpdUserData),
                    }
                );

                if (!response.ok) throw new Error(`Update failed! Status: ${response.status}`);

                alert("Profile Data updated successfully!");
            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
        }

    }

}

</script>