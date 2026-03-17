import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import ProductsView from '../views/ProductsView.vue'
import TraceabilityView from '../views/TraceabilityView.vue'
import TraceDetailView from '../views/TraceDetailView.vue'
import CheckoutView from '../views/CheckoutView.vue'
import CompetitorsView from '../views/CompetitorsView.vue'
import OpportunitiesView from '../views/OpportunitiesView.vue'
import MarketGrowthView from '../views/MarketGrowthView.vue'
import PersonasView from '../views/PersonasView.vue'
import InventoryView from '../views/InventoryView.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView, meta: { requiresAuth: false } },
  { path: '/login', name: 'Login', component: LoginView, meta: { requiresAuth: false } },
  { path: '/products', name: 'Products', component: ProductsView, meta: { requiresAuth: false } },
  { path: '/traceability', name: 'Traceability', component: TraceabilityView, meta: { requiresAuth: false } },
  { path: '/traceability/:productId', name: 'TraceDetail', component: TraceDetailView, meta: { requiresAuth: false } },
  { path: '/checkout', name: 'Checkout', component: CheckoutView, meta: { requiresAuth: false } },
  {
    path: '/competitors',
    name: 'Competitors',
    component: CompetitorsView,
    meta: { requiresAuth: true, roles: ['ADMIN', 'ANALYST'] }
  },
  {
    path: '/opportunities',
    name: 'Opportunities',
    component: OpportunitiesView,
    meta: { requiresAuth: true }
  },
  {
    path: '/market-growth',
    name: 'MarketGrowth',
    component: MarketGrowthView,
    meta: { requiresAuth: true }
  },
  {
    path: '/personas',
    name: 'Personas',
    component: PersonasView,
    meta: { requiresAuth: true }
  },
  {
    path: '/inventory',
    name: 'Inventory',
    component: InventoryView,
    meta: { requiresAuth: true, roles: ['ADMIN', 'ANALYST'] }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('cp_token')
  const role = localStorage.getItem('cp_role')

  if (to.meta.requiresAuth) {
    if (!token) {
      return next({ path: '/login', query: { redirect: to.fullPath } })
    }
    if (to.meta.roles && !to.meta.roles.includes(role)) {
      return next({ path: '/' })
    }
  }
  next()
})

export default router
