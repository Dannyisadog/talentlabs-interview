import { createRouter, createWebHistory } from 'vue-router'
import JobListView from '../views/JobListView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'job-list',
      component: JobListView,
    },
    {
      path: '/job/:id',
      name: 'job-details',
      component: JobListView,
    },
  ],
})

export default router
