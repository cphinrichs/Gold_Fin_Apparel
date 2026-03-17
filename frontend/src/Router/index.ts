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
      path: '/cart',
      name: 'Cart',
      component: () => import('../Views/CartView.vue')
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
    },
    {
      path: '/contactus',
      name: 'ContactUs',
      component: () => import('../Views/ContactUsView.vue')
    },
    {
      path: '/returnpolicy',
      name: 'ReturnPolicy',
      component: () => import('../Views/ReturnPolicyView.vue')
    },
    {
      path: '/shippinginformation',
      name: 'ShippingInformation',
      component: () => import('../Views/ShippingInformationView.vue')
    },
    {
      path: '/sizecharts',
      name: 'SizeCharts',
      component: () => import('../Views/SizeChartsView.vue')
    },
    {
      path: '/inspect',
      name: 'Inspect',
      component: () => import('../Views/InspectView.vue')
    },
    {
      path: '/tshirts',
      name: 'T-Shirts',
      component: () => import('../ProductViewPages/TShirtsView.vue')
    },
    {
      path: '/longsleeves',
      name: 'Long Sleeves',
      component: () => import('../ProductViewPages/LongSleevesView.vue')
    },
    {
      path: '/hoodies',
      name: 'Hoodies',
      component: () => import('../ProductViewPages/HoodiesView.vue')
    },
    {
      path: '/tanktops',
      name: 'Tank Tops',
      component: () => import('../ProductViewPages/TankTopsView.vue')
    },
    {
      path: '/vests',
      name: 'Vests',
      component: () => import('../ProductViewPages/VestsView.vue')
    },
    {
      path: '/kimonos',
      name: 'Kimonos',
      component: () => import('../ProductViewPages/KimonosView.vue')
    },
    {
      path: '/orderconfirmation',
      name: 'OrderConfirmation',
      component: () => import('../Views/OrderConfirmationView.vue')
    }

  ],
})

export default router