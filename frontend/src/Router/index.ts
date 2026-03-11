// This file will manage the routing for our Vue application,
// defining the different routes and their corresponding components.

import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../Views/HomeView.vue'
const router = createRouter({
  history: createWebHistory('/'),
  routes: [
    {
        path: '/',
        name: 'Home',
        component: HomeView
    },
    {
      path: '/about',
      name: 'About',
      component: () => import('../Views/AboutView.vue')
    },
    {
      path: '/browse',
      name: 'Browse',
      component: () => import('../Views/BrowseView.vue')
    },
    {
      path: '/checkout',
      name: 'Checkout',
      component: () => import('../Views/CheckOutView.vue')
    },
    {
      path: '/help',
      name: 'Help',
      component: () => import('../Views/HelpView.vue')
    }
  ],
})

export default router