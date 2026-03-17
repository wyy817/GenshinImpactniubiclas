<template>
  <div class="trace-view">
    <div class="page-header">
      <h1 class="page-title">Supply Chain Traceability</h1>
      <p class="page-subtitle">
        CP Group's farm-to-table transparency system. Track each product's journey from origin
        through cold chain logistics to your door — certified at every step.
      </p>
    </div>

    <!-- Info Banner -->
    <el-alert
      title="All 15 products are fully traceable — click any card to view its step-by-step supply chain timeline"
      type="success"
      :closable="false"
      show-icon
      style="margin-bottom:24px;border-radius:10px"
    />

    <!-- How It Works -->
    <el-card class="how-it-works" shadow="never">
      <h3 style="margin-bottom:16px;font-size:16px;font-weight:700">How Traceability Works</h3>
      <el-steps :active="4" finish-status="success" align-center>
        <el-step title="Farm Origin" description="Certified growing conditions & soil quality" icon="Sunrise" />
        <el-step title="Processing" description="Hygienic processing & quality grading" icon="Operation" />
        <el-step title="Cold Chain" description="Temperature-controlled logistics" icon="Van" />
        <el-step title="Distribution" description="Last-mile delivery to consumer" icon="House" />
      </el-steps>
    </el-card>

    <!-- My Purchased Products -->
    <div v-if="purchasedProducts.length > 0" class="section-gap">
      <h2 style="font-size:18px;font-weight:700;margin-bottom:8px;color:#1a1a2e">
        My Purchased Products
      </h2>
      <p style="font-size:13px;color:#909399;margin-bottom:16px">
        Products you've ordered — click any to view its full supply chain traceability timeline.
      </p>

      <div class="products-grid">
        <el-card
          v-for="product in purchasedProducts"
          :key="product.id + product.orderId"
          class="trace-product-card purchased-card"
          shadow="hover"
          @click="$router.push(`/traceability/${product.id}`)"
        >
          <div class="purchased-badge">
            <el-tag type="success" size="small" round>
              <el-icon><ShoppingBag /></el-icon>
              Purchased
            </el-tag>
          </div>
          <div class="trace-card-icon">
            <el-icon :size="36" color="#67c23a"><Goods /></el-icon>
          </div>
          <div class="trace-card-id">{{ product.id }}</div>
          <div class="trace-card-name">{{ product.name }}</div>
          <div class="trace-card-meta">
            <el-tag size="small" type="success">{{ product.category }}</el-tag>
            <el-tag size="small" type="warning">Qty: {{ product.qty }}</el-tag>
          </div>
          <div class="trace-card-order">Order: {{ product.orderId }}</div>
          <div class="trace-card-action">
            <el-icon><ArrowRight /></el-icon>
            View Full Timeline
          </div>
        </el-card>
      </div>
    </div>

    <!-- Product Cards -->
    <div class="section-gap">
      <h2 style="font-size:18px;font-weight:700;margin-bottom:16px;color:#1a1a2e">
        Traceable Products
        <el-tag type="success" size="small" round style="margin-left:8px;vertical-align:middle">All 15 Products</el-tag>
      </h2>

      <div v-if="loading" class="products-grid">
        <el-skeleton v-for="n in 3" :key="n" :rows="2" animated style="background:#fff;border-radius:12px;padding:20px" />
      </div>

      <div v-else class="products-grid">
        <el-card
          v-for="product in traceableProducts"
          :key="product.id"
          class="trace-product-card"
          shadow="hover"
          @click="$router.push(`/traceability/${product.id}`)"
        >
          <div class="trace-card-icon">
            <el-icon :size="36" :color="product.color"><Goods /></el-icon>
          </div>
          <div class="trace-card-id">{{ product.id }}</div>
          <div class="trace-card-name">{{ product.name }}</div>
          <div class="trace-card-meta">
            <el-tag size="small" :color="product.color" style="color:#fff;border:none">{{ product.category }}</el-tag>
            <el-tag size="small" type="info">{{ product.nodes }} steps</el-tag>
          </div>
          <div class="trace-card-action">
            <el-icon><ArrowRight /></el-icon>
            View Full Timeline
          </div>
        </el-card>
      </div>
    </div>

    <!-- Certifications -->
    <el-card class="cert-section section-gap" shadow="never">
      <h3 style="margin-bottom:16px;font-size:16px;font-weight:700">Certifications & Standards</h3>
      <div class="cert-grid">
        <div class="cert-item" v-for="cert in certifications" :key="cert.name">
          <el-icon :size="24" :color="cert.color"><component :is="cert.icon" /></el-icon>
          <div>
            <div class="cert-name">{{ cert.name }}</div>
            <div class="cert-desc">{{ cert.desc }}</div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ArrowRight, ShoppingBag, Goods } from '@element-plus/icons-vue'
import api from '../api/index.js'
import { useCartStore } from '../stores/cart.js'

const cartStore = useCartStore()

// Derive unique purchased products from all orders
const purchasedProducts = computed(() => {
  const seen = new Set()
  const result = []
  for (const order of cartStore.orders) {
    for (const item of order.items) {
      const key = item.id + '|' + order.id
      if (!seen.has(key)) {
        seen.add(key)
        result.push({ ...item, orderId: order.id })
      }
    }
  }
  return result
})

const loading = ref(true)

const traceableProducts = ref([])

// Node counts per product (matches hardcoded _TRACE_DATA in backend)
const TRACE_NODE_COUNTS = {
  P001: 7, P002: 6, P003: 6, P004: 6, P005: 7,
  P006: 7, P007: 6, P008: 7, P009: 7, P010: 7,
  P011: 8, P012: 6, P013: 6, P014: 8, P015: 8,
}

// Color per category
const CATEGORY_COLOR = {
  'Vegetables':   '#67c23a',
  'Fruits':       '#ff9800',
  'Seafood':      '#17a2b8',
  'Dairy & Eggs': '#9c27b0',
  'Meat':         '#f56c6c',
}

// Skeleton placeholders while loading
const SKELETON_IDS = ['P001','P002','P003','P004','P005','P006','P007','P008','P009','P010','P011','P012','P013','P014','P015']
traceableProducts.value = SKELETON_IDS.map(id => ({
  id, name: 'Loading...', category: '—', nodes: TRACE_NODE_COUNTS[id] ?? '—', icon: 'Goods', color: '#c0c4cc',
}))

onMounted(async () => {
  try {
    const products = await api.get('/products')
    if (Array.isArray(products) && products.length) {
      traceableProducts.value = SKELETON_IDS.map(id => {
        const found = products.find(p =>
          (p.Product_ID || p.product_id || '').toString().trim().toUpperCase() === id
        )
        const cat = found ? (found.Category || found.category || '—') : '—'
        return {
          id,
          name: found ? (found.Product_Name || found.Name_EN || id) : id,
          category: cat,
          nodes: TRACE_NODE_COUNTS[id] ?? '—',
          icon: 'Goods',
          color: CATEGORY_COLOR[cat] ?? '#409eff',
        }
      })
    }
  } finally {
    loading.value = false
  }
})

const certifications = [
  { name: 'ISO 22000', desc: 'Food safety management system', icon: 'CircleCheck', color: '#67c23a' },
  { name: 'GAP Certified', desc: 'Good Agricultural Practices', icon: 'Sunrise', color: '#409eff' },
  { name: 'HACCP', desc: 'Hazard Analysis Critical Control Points', icon: 'Warning', color: '#e6a23c' },
  { name: 'Green Food', desc: 'China Green Food certification', icon: 'Leaf', color: '#3a8e00' },
]
</script>

<style scoped>
.trace-view {
  padding-bottom: 40px;
}

.page-header {
  margin-bottom: 24px;
}

.how-it-works {
  border-radius: 12px;
  margin-bottom: 8px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
}

.trace-product-card {
  border-radius: 14px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  text-align: center;
}

.trace-product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.trace-card-icon {
  margin-bottom: 12px;
}

.trace-card-id {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.trace-card-name {
  font-size: 17px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 10px;
}

.trace-card-meta {
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.trace-card-action {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 13px;
  color: #409eff;
  font-weight: 500;
}

.cert-section {
  border-radius: 12px;
}

.cert-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.cert-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 10px;
}

.cert-name {
  font-weight: 600;
  font-size: 14px;
  color: #303133;
}

.cert-desc {
  font-size: 12px;
  color: #909399;
  margin-top: 2px;
}

.purchased-card {
  border: 2px solid #e1f3d8;
  background: linear-gradient(145deg, #ffffff, #f0f9eb);
}

.purchased-badge {
  position: absolute;
  top: 12px;
  right: 12px;
}

.trace-card-order {
  font-size: 11px;
  color: #c0c4cc;
  margin-bottom: 10px;
}
</style>
