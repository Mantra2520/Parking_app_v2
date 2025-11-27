<template>
    <div class="content">
        <h1>Registered Users</h1>
        <div v-if="Data.length > 0">
            <table style="margin-top: 50px;">
                <thead>
                    <tr>
                        <th>Sr.No.</th>
                        <th>Full Name</th>
                        <th>User ID</th>
                        <th>Email ID</th>
                        <th>Address</th>
                        <th>pincode</th>
                        <th>Total reservations</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(user, i) in Data" :key="i">
                        <td>{{ i + 1 }}</td>
                        <td>{{ user.fname }}</td>
                        <td>{{ user.user_id }}</td>
                        <td>{{ user.email }}</td>
                        <td>{{ user.address }}</td>
                        <td>{{ user.pincode }}</td>
                        <td>{{ user.res_count }}</td>
                        <td><router-link class="blue" :to="`/admin/user/${user.user_id}`">View Reservations</router-link></td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else-if="Data.length === 0" >No Users</div>
        <div v-else-if="error" class="error">{{ errorMessage }}</div>
        <div v-else-if="loading" class="loading">Loading Data...</div>
    </div>
</template>

<script>
import { looseIndexOf } from '@vue/shared';

export default {
    name: "AdminUserDetails",
    data() {
        return {
            Data: [],
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
                const response = await fetch('http://127.0.0.1:5000/admin/users', {
                    method: "GET",
                    headers: {
                        "Authorization": localStorage.getItem("token")
                    }})
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                this.Data = await response.json()

            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
        }
    }
}

</script>