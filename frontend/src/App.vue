<template>
  <div id="app">
    <!-- <Navbar v-if="showNavbar" /> -->
     <p>Navbar</p>
    <router-view />
  </div>
</template>

<script>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import Navbar from './components/navbar.vue';

export default {
  components: { Navbar },
  setup() {
    const route = useRoute();

    // ✅ Define which routes should hide the navbar
    const noNavbarRoutes = ['/', '/login', '/signup'];

    // Compute visibility dynamically
    const showNavbar = computed(() => !noNavbarRoutes.includes(route.path));

    return { showNavbar };
  }
};
</script>
