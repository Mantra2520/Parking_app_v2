import { createRouter, createWebHistory } from 'vue-router'

import AdminHomePage from '@/pages/AdminHomepage.vue'
import AdminEditLot from '@/pages/AdminEditLot.vue'
import AdminLotDetails from '@/pages/AdminLotDetails.vue'
import AdminAddLot from '@/pages/AdminAddLot.vue'
import UserHomePage from '@/pages/UserHomepage.vue'
import Login from '@/pages/Login.vue'
import Summary from '@/pages/Summary.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: '/',component: Login},
    {path: '/admin/home',component: AdminHomePage},
    {path: '/admin/edit/:id',component: AdminEditLot},
    {path: '/admin/lot/:id',component: AdminLotDetails},
    {path: '/admin/addLot',component: AdminAddLot},
    {path: '/user/home',component: UserHomePage},
    {path: '/summary',component: Summary},
  ],
})

export default router
