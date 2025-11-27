import { createRouter, createWebHistory } from 'vue-router'

import AdminHomePage from '@/pages/AdminHomepage.vue'
import AdminEditLot from '@/pages/AdminEditLot.vue'
import AdminLotDetails from '@/pages/AdminLotDetails.vue'
import AdminAddLot from '@/pages/AdminAddLot.vue'
import AdminSpotDetails from '@/pages/AdminSpotDetails.vue'
import AdminUserDetails from '@/pages/AdminUserDetails.vue'
import AdminUserReservations from '@/pages/AdminUserReservations.vue'
import AdminSearch from '@/pages/AdminSearch.vue'
import AdminSummary from '@/pages/AdminSummary.vue'
import UserHomePage from '@/pages/UserHomepage.vue'
import UserSummary from '@/pages/UserSummary.vue'
import UserProfile from '@/pages/UserProfile.vue'
import UserBooking from '@/pages/UserBooking.vue'
import UserRelease from '@/pages/UserRelease.vue'
import UserPayment from '@/pages/UserPayment.vue'
import Login from '@/pages/Login.vue'
import Summary from '@/pages/Summary.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: Login },
    { path: '/admin/home', component: AdminHomePage },
    { path: '/admin/edit/:id', component: AdminEditLot },
    { path: '/admin/lot/:id', component: AdminLotDetails },
    { path: '/admin/addLot', component: AdminAddLot },
    { path: '/admin/spotDetails/:id', component: AdminSpotDetails },
    { path: '/admin/users', component: AdminUserDetails },
    { path: '/admin/user/:id', component: AdminUserReservations },
    { path: '/admin/search', component: AdminSearch },
    { path: '/admin/summary', component: AdminSummary },
    { path: '/user/home/:id', component: UserHomePage },
    { path: '/user/summary/:id', component: UserSummary },
    { path: '/user/profile/:id', component: UserProfile },
    { path: '/user/booking/:id/:lid', component: UserBooking },
    { path: '/user/release/:id/:rid', component: UserRelease },
    { path: '/user/payment/:id/:rid', component: UserPayment },
    { path: '/summary', component: Summary },
  ],
})

export default router
