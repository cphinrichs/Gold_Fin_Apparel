// This file will manage the routing for our Vue application,
// defining the different routes and their corresponding components.

import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../Views/HomeView.vue'
import BrowseView from '../Views/BrowseView.vue'
import InspectView from '../Views/InspectView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
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
      component: BrowseView
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
      path: '/inspect/:id',
      name: 'Inspect',
      component: InspectView
    }
  ],
})

export default router