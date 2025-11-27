<template>
    <nav>
        <span>Welcome Admin</span>
        <router-link to="/admin/home">Home</router-link>
        <router-link to="/admin/users">Users</router-link>
        <router-link to="/admin/search">Search</router-link>
        <router-link to="/admin/summary">Summary</router-link>
        <a @click.prevent="logout" href="#">Logout</a>
    </nav>
</template>

<script>
export default {
    name: "UserNavbar",
    methods: {
        logout() {
            localStorage.removeItem("role");
            localStorage.removeItem("userid");

            this.$router.push("/");
        }
    }
};

</script>

<style>
nav {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    background-image: url("/Nav_background.png");
    background-size: cover;
    background-repeat: no-repeat;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: space-around;
    color: white;
    font-weight: bold;
    font-family: sans-serif;
    z-index: 3;
}

nav span {
    font-size: 20px;
    margin: -55px;
}

nav a {
    color: #2c3e50;
    text-decoration: none;
    padding: 3px 20px;
    border-radius: 4px;
    background-color: white;
}

nav a:hover {
    background-color: rgba(255, 255, 255, 0.3);
    color: white;
    transition: 0.3s;
}
</style>