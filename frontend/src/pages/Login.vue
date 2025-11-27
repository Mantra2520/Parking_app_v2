<template>
  <div class="body">
    <div class="login-box">
      <!-- TAB SWITCH -->
      <div class="tabs">
        <span :class="{ active: activeTab === 'login' }" @click="activeTab = 'login'">
          LOG IN
        </span>

        <span :class="{ active: activeTab === 'signup' }" @click="activeTab = 'signup'">
          SIGN UP
        </span>
      </div>

      <!-- LOGIN FORM -->
      <form class="ls-form" v-if="activeTab === 'login'" @submit.prevent="handleLogin">
        <input type="text" v-model="login.userid" placeholder="User ID" required />

        <input type="password" v-model="login.password" placeholder="Password" required />

        <button type="submit" :disabled="loadingLogin">
          {{ loadingLogin ? "Signing In..." : "SIGN IN" }}
        </button>

        <p class="error" v-if="loginError">{{ loginError }}</p>
      </form>

      <!-- SIGNUP FORM -->
      <form class="ls-form" v-if="activeTab === 'signup'" @submit.prevent="handleSignup">
        <input type="text" v-model="signup.username" placeholder="User ID" required />

        <input type="text" v-model="signup.name" placeholder="Full Name" required />

        <input type="text" v-model="signup.email" placeholder="Email" required />

        <input type="text" v-model="signup.address" placeholder="Address" required />

        <input type="text" v-model="signup.pincode" placeholder="Pincode" required />


        <br>

        <input type="password" v-model="signup.password" placeholder="Create Password" required />

        <input type="password" v-model="signup.confirm" placeholder="Confirm Password" required />

        <button type="submit" :disabled="loadingSignup">
          {{ loadingSignup ? "Creating Account..." : "SIGN UP" }}
        </button>

        <p class="error" v-if="signupError">{{ signupError }}</p>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginSignup",

  data() {
    return {
      activeTab: "login",

      login: {
        userid: "",
        password: ""
      },

      signup: {
        username: "",
        name: "",
        email: "",
        address: "",
        pincode: "",
        password: "",
        confirm: ""
      },

      loadingLogin: false,
      loadingSignup: false,

      loginError: null,
      signupError: null
    };
  },
  mounted() {
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");
    const userid = localStorage.getItem("userid");

    // If already logged in → redirect accordingly
    if (token && role) {
      if (role === "admin") {
        this.$router.push("/admin/home");
      }
      else if (role === "user" && userid) {
        this.$router.push(`/user/home/${userid}`);
      }
    }
  },
  methods: {
    /* ===========================
       LOGIN
    ============================ */
    async handleLogin() {
      this.loginError = null;

      if (!this.login.userid || !this.login.password) {
        this.loginError = "Please fill all fields.";
        return;
      }

      this.loadingLogin = true;

      try {
        const res = await fetch("http://127.0.0.1:5000/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.login)
        });

        const data = await res.json();

        if (!res.ok || data.error) {
          this.loginError = data.error || "Login failed.";
          return;
        }

        // Save session
        localStorage.setItem("token", data.token);
        localStorage.setItem("userid", data.userid);
        localStorage.setItem("role", data.role);

        // Redirect
        if (data.role === "admin") this.$router.push("/admin/home");
        else this.$router.push(`/user/home/${data.userid}`);

      } catch (err) {
        this.loginError = "Network error.";
      }finally{
        this.loadingLogin = false;
      }

    },

    /* ===========================
       SIGN UP
    ============================ */
    async handleSignup() {
      this.signupError = null;

      if (this.signup.password !== this.signup.confirm) {
        this.signupError = "Passwords do not match.";
        return;
      }

      this.loadingSignup = true;

      try {
        const res = await fetch("http://127.0.0.1:5000/singup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            userid: this.signup.username,
            fullname: this.signup.name,
            email: this.signup.email,
            address: this.signup.address,
            pincode: this.signup.pincode,
            password: this.signup.password
          })
        });

        const data = await res.json();

        if (!res.ok || data.error) {
          this.signupError = data.error || "Signup failed.";
          return;
        }

        alert("Account created successfully! Please log in.");
        this.activeTab = "login";

      } catch (err) {
        this.signupError = "Network error.";
      }

      this.loadingSignup = false;
    }
  }
};
</script>

<style>
/* --- GLOBAL FIX (required for full-page background) --- */
html,
body,
#app {
  height: 91%;
  width: 100%;
  margin: 0;
  padding: 0;
}

/* --- PAGE BACKGROUND --- */
.body {
  height: 100vh;
  width: 100%;
  background: url("/login_bg.png") center center no-repeat;
  background-size: cover;
  font-family: 'Segoe UI', sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
}


/* --- LOGIN BOX (Glassmorphism) --- */
.login-box {
  width: 300px;
  padding: 40px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(15px);
  color: white;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}


/* --- TABS --- */
.tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

.tabs span {
  font-weight: 600;
  font-size: 18px;
  margin: 0 14px;
  cursor: pointer;
  padding-bottom: 6px;
  color: #ccc;
}

.tabs .active {
  color: white;
  border-bottom: 2px solid #00c8ff;
}


/* --- FORMS --- */
.login-box form {
  all: unset;
  display: flex;
  flex-direction: column;
}


/* --- INPUTS --- */
/* IMPORTANT: these !important rules override Bootstrap/Tailwind resets */
.login-box input {
  background-color: rgba(0, 0, 0, 0.4);
  color: white;
  padding: 12px 14px;
  border: none;
  border-radius: 8px;
  margin: 10px 0;
  font-size: 15px;
}


.login-box input::placeholder {
  color: #bfbfbf !important;
}


/* --- BUTTON --- */
.login-box button {
  width: 100%;
  padding: 14px;
  border-radius: 10px;
  border: none;

  font-size: 17px;
  font-weight: 600;

  background: linear-gradient(135deg, #4facfe, #00f2fe);
  color: white;
  cursor: pointer;

  margin-top: 18px;
  transition: transform 0.2s ease;
}

.login-box button:hover {
  transform: scale(1.03);
}


/* --- ERROR MESSAGE --- */
.error {
  color: #ff6b6b;
  margin-top: 10px;
  font-size: 14px;
  text-align: center;
}
</style>
