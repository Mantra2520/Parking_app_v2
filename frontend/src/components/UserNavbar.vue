<template>
    <nav>
        <span style="margin-left: -80px;">Wellcome {{ userid }}</span>
        <router-link :to="`/user/home/${userid}`">Home</router-link>
        <router-link :to="`/user/summary/${userid}`">Summary</router-link>
        <router-link :to="`/user/profile/${userid}`">Profile</router-link>
        <a @click.prevent="logout" href="#">Logout</a>
    </nav>
</template>

<script>
export default {
    data() {
        return {
            userid: this.$route.params.id
        }
    },
    methods: {
        logout() {
            localStorage.removeItem("role");
            localStorage.removeItem("userid");

            this.$router.push("/");
        }
    }
}
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