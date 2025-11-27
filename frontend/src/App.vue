<template>
  <div id="app">
    <AdminNavbar v-if="isAdmin" />
    <UserNavbar v-else-if="isUser" />
    <!-- <p>Navbar</p> -->
    <router-view />
  </div>
</template>

<script>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import AdminNavbar from './components/AdminNavbar.vue';
import UserNavbar from './components/UserNavbar.vue';

export default {
  components: { AdminNavbar, UserNavbar },
  computed: {
    isAdmin() {
      return this.$route.path.includes('/admin');
    },
    isUser() {
      return this.$route.path.includes('/user');
    }
  }
};
</script>

<style>
body {
  background-color: #f9f9f9;
}

.content {
  font-family: 'Segoe UI', sans-serif;
  margin-top: 80px;
}

h1 {
  margin: 0px;
  font-size: 32px;
  font-weight: 800;
  text-align: center;
  color: #2c3e50;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
  letter-spacing: 1px;
}

.lot-h3 {
  text-align: center;
  margin-bottom: 10px;
  margin-top: 0px;
  font-size: 22px;
  color: #2c3e50;
}

.lots-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
  padding-left: 20px;
  padding-right: 20px;
}

.lot {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  max-width: 240px;
  box-shadow: 0 7px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.lot:hover {
  transform: scale(1.02);
}

.blue {
  padding-bottom: 0px;
  margin-right: 10px;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  -webkit-text-fill-color: transparent;
  -webkit-background-clip: text;
  text-decoration: none;
}

.blue:hover {
  border-bottom: 1px solid #00f2fe;
}

.green {
  padding-bottom: 0px;
  margin-right: 10px;
  background: linear-gradient(to right, rgba(50, 220, 100, 0.95), rgba(30, 180, 70, 0.95));
  -webkit-text-fill-color: transparent;
  -webkit-background-clip: text;
  text-decoration: none;
}

.green:hover {
  border-bottom: 1px solid rgba(50, 220, 100, 0.95);
}

.red {
  padding-bottom: 0px;
  margin-right: 10px;
  background: linear-gradient(to right, rgba(255, 99, 132, 1), rgba(255, 70, 100, 0.95), rgba(200, 30, 70, 0.95));
  -webkit-text-fill-color: transparent;
  -webkit-background-clip: text;
  text-decoration: none;
}

.red:hover {
  border-bottom: 1px solid rgba(255, 70, 100, 0.95);
}

.occupancy {
  margin: 10px 0;
  font-weight: bold;
}

.occupancy.low {
  color: rgb(2, 178, 2);
}

.occupancy.mid {
  color: orange;
}

.occupancy.full {
  color: red;
}

.add-lot a {
  margin: 40px 20px 20px 0px;
  display: inline-block;
  padding: 12px 20px;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  color: white;
  text-decoration: none;
  font-weight: bold;
  border-radius: 6px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
  transition: 0.2s ease-in-out;
  margin-left: 20px;
  margin-right: 20px;
}

.add-lot a:hover {
  background: linear-gradient(135deg, #4fb6ff, #28f8ff);
  transform: scale(1.02);
}

/* h3 {
  text-align: center;
  margin-bottom: 40px;
  font-size: 28px;
  color: #2c3e50;
} */

/* Loading text */
.loading {
  /* text-align: center; */
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  margin-top: 20px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 0.5px;
  animation: pulse 1.5s ease-in-out infinite;
}

/* Error message */
.error {
  text-align: center;
  font-size: 1rem;
  font-weight: 600;
  color: #b00020;
  background-color: #ffe5e5;
  border: 1px solid #ffb3b3;
  border-radius: 8px;
  padding: 12px 16px;
  width: fit-content;
  margin: 20px auto;
  box-shadow: 0 2px 8px rgba(255, 0, 0, 0.1);
}

/* Subtle pulsing animation for "Loading..." */
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



table {
  width: 90%;
  margin: auto;
  border-collapse: collapse;
  background-color: #ffffff;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  border-radius: 10px;
  margin-bottom: 30px;
  margin-top: 20px;
}

table th,
table td {
  padding: 12px 15px;
  text-align: center;
  border-bottom: 1px solid #ddd;
}

table th {
  /* background: #00f2fe; */
  /* background-color: #2c3e50;  */
  color: white;
  text-transform: uppercase;
  font-size: 16px;
}

table thead tr:first-child {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
}

table tr:hover {
  background-color: #f1f1f1;
}

table tr:last-child td {
  border-bottom: none;
}

.grey {
  text-align: center;
  color: #555;
  margin-top: 0px;
  margin-bottom: 40px;
}

form {
  width: 37%;
  max-width: 600px;
  margin: 110px auto;
  background-color: white;
  padding: 20px 24px;
  padding-top: 30px;
  border-radius: 17px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 40px;
}


.input-container {
  width: 100%;
  display: flex;
  background: white;
  border-radius: 1rem;
  background: linear-gradient(45deg, #c5c5c5 0%, #ffffff 100%);
  padding: 0.3rem;
  gap: 0.3rem;
}

.input-container input[type="text"] {
  border-radius: 0.75rem 0 0 0.75rem;
  background: #e8e8e8;
  width: 100%;
  padding: 0.4rem 0.8rem;
  font-size: 0.95rem;
  border: none;
  color: #333;
  height: 25px;
}

.input-container input:focus {
  outline: none;
  box-shadow: inset 13px 13px 10px #BFF0FA, inset -13px -13px 10px #f4f4f4;
}

.input-container button[type="submit"] {
  border-radius: 0 0.75rem 0.75rem 0;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  padding: 0.4rem 1rem;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  color: white;
  border: none;
  cursor: pointer;
  height: 38px;
}

h3 {
  font-size: 20px;
  font-weight: 800;
  text-align: center;
  margin-top: 20px;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 40px;
  letter-spacing: 1px;
}

.input-container button[type="submit"]:hover {
  background: linear-gradient(135deg, #4fb6ff, #28f8ff)
}

h2 {
  margin: 0px;
  font-size: 28px;
  font-weight: 800;
  text-align: center;
  color: #2c3e50;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 40px;
  letter-spacing: 1px;
}

.no {
    font-size: 15px;
    font-weight: 800;
    text-align: center;
    margin-top: 20px;
    width: fit-content;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 40px;
    letter-spacing: 1px;
}

.input-group {
  display: flex;
  flex-direction: column;
  position: relative;
  margin: 20px;
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
  padding: 0 .2em;
  color: black;
}

.input:not(:placeholder-shown)~.user-label {
  transform: translateY(-50%) scale(0.8);
  background-color: #ffffff;
  padding: 0 .2em;
  color: black;
}

.form-button {
  display: block;
  width: 180px;
  margin: 10px auto 0 auto;
  padding: 12px;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.form-button:hover {
  background: linear-gradient(135deg, #4fb6ff, #28f8ff);
  transform: scale(1.03);
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1);
}


input[disabled] {
  cursor: not-allowed;
}

.parent {
  margin-top: 100px;
  text-align: center;
  padding: 0 20px;
}

.div1 h2 {
  font-size: 28px;
  margin-bottom: 20px;
  color: #2c3e50;
}

.details-box {
  display: flex;
  align-items: stretch;
  background-color: white;
  border: 2px solid #ccc;
  border-radius: 12px;
  padding: 20px;
  margin: 20px 520px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.div2,
.div3 {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}


.vertical-line {
  width: 2px;
  background-color: #ccc;
  height: auto;
  margin: 0 10px;
}


.div2 p,
.div3 p {
  margin: 8px 0;
  font-size: 16px;
  text-align: center;
  word-wrap: break-word;
  word-break: break-word;
}

.div4 {
  padding-bottom: 20px;
}

.div4 h3 {
  font-size: 28px;
  margin-bottom: 15px;
  color: #34495e;
}

.div5 {
  background-color: #2f2f2f;
  padding: 30px;
  margin-bottom: 20px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  border-radius: 12px;
  box-shadow: inset 0 0 10px rgba(255, 255, 0, 0.1);
}


.spot {
  margin: 15px 0;
  width: 100px;
  height: 130px;
  border: 3px solid yellow;
  border-radius: 3px;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  padding-bottom: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
  color: white;
}

.spot.spot.available::before {
  content: 'P';
  position: absolute;
  top: 10px;
  font-size: 40px;
  font-family: Helvetica;
  color: yellow;
}

.road-midline {
  width: 100%;
  height: 15px;
  background: repeating-linear-gradient(to right,
      white,
      white 60px,
      transparent 20px,
      transparent 105px);
  margin: 20px 0;
  border-radius: 2px;
}

.road-sideline {
  content: "";
  width: 100%;
  height: 15px;
  background-color: white;
}

.occupied .car-img {
  position: relative;
  top: 4px;
  width: 120px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}


.spot.available p:last-child {
  color: limegreen;
  font-weight: bold;
}

.spot p {
  margin: 4px 0 0;
  z-index: 1;
}

.spot-wrap {
  display: contents;
}

.road-group {
  flex: 0 0 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 20px 0;
}

.paybox {
  height: 80vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
}


.card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  width: 400px;
}

.details {
  margin: 20px 0;
}

.details p {
  margin: 8px 0;
}

.pay-btn {
  width: 100%;
  padding: 12px;
  background-color: #4BB543;
  color: white;
  border: none;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
}

.pay-btn:hover {
  background-color: #3ea43a;
}

.success-popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  animation: fadeIn 0.3s ease;
  z-index: 9999;
}

.success-circle {
  width: 120px;
  height: 120px;
  background: #4CAF50;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: popIn 0.4s ease;
}

.tick {
  width: 40px;
  height: 20px;
  border-left: 5px solid white;
  border-bottom: 5px solid white;
  transform: rotate(-45deg);
  animation: tickDraw 0.5s ease forwards;
}

.success-text {
  margin-top: 20px;
  font-size: 22px;
  font-weight: bold;
  color: #fff;
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes popIn {
  0% {
    transform: scale(0.2);
    opacity: 0;
  }

  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes tickDraw {
  0% {
    stroke-dashoffset: 50;
  }

  100% {
    stroke-dashoffset: 0;
  }
}
</style>