<template>
  <div>
    <div class="login-box">
      <div class="tabs">
        <span id="login-tab" class="active">LOG IN</span>
      </div>

      <form @submit.prevent="handleLogin">
        <input
          type="text"
          v-model="userid"
          placeholder="User ID"
          required
        />
        <input
          type="password"
          v-model="password"
          placeholder="Password"
          required
        />

        <button type="submit" :disabled="loading">
          {{ loading ? "Signing In..." : "SIGN IN" }}
        </button>

        <!-- Error / Success Message -->
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      userid: "",
      password: "",
      responseData: null,
      errorMessage: null,
      loading: false
    };
  },
//   mounted() {
//     // If already logged in, redirect directly
//     const token = localStorage.getItem("token");
//     const role = localStorage.getItem("role");
//     if (token && role) {
//       if (role === "admin") this.$router.push("/admin/home");
//       else if (role === "user") this.$router.push("/user/home");
//     }
//   },
  methods: {
    async handleLogin() {
      // Prevent double-clicks
      if (this.loading) return;

      // Frontend validation
      if (!this.userid.trim() || !this.password.trim()) {
        this.errorMessage = "Please enter both User ID and Password.";
        return;
      }

      this.loading = true;
      this.errorMessage = null;
      this.responseData = null;

      const url = "http://127.0.0.1:5000/login";
      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          userid: this.userid,
          password: this.password
        })
      };

      try {
        const response = await fetch(url, requestOptions);

        let data;
        try {
          data = await response.json();
        } catch {
          throw new Error("Invalid response from server.");
        }

        if (!response.ok || data.error) {
          this.errorMessage = data.error || `Error ${response.status}`;
          return;
        }

        // ✅ Everything is fine
        this.responseData = data;
        localStorage.setItem("token", data.token);
        localStorage.setItem("userid", data.userid);
        localStorage.setItem("role", data.role);

        if (data.role === "admin") {
          console.log("✅ Logged in as Admin");
          this.$router.push("/admin/home");
        } else if (data.role === "user") {
          console.log("✅ Logged in as User");
          this.$router.push("/user/home");
        }

      } catch (error) {
        this.errorMessage = "Network error: " + error.message;
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.login-box {
  width: 300px;
  margin: 100px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  text-align: center;
}

input {
  display: block;
  width: 90%;
  margin: 10px auto;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #aaa;
}

button {
  padding: 8px 16px;
  border: none;
  background-color: #4caf50;
  color: white;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 10px;
}

button:disabled {
  background-color: #9e9e9e;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #45a049;
}

.error {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}
</style>
