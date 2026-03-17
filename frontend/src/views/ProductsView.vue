<template>
  <div class="products-view">
    <CartBubble />

    <div class="page-header">
      <h1 class="page-title">Product Catalogue</h1>
      <p class="page-subtitle">Fresh, traceable products sourced directly from CP Group's integrated supply chain</p>
    </div>

    <!-- Filters -->
    <el-card class="filter-bar" shadow="never">
      <div class="filter-row">
        <el-input
          v-model="searchText"
          placeholder="Search products..."
          prefix-icon="Search"
          clearable
          style="width:260px"
        />
        <el-select
          v-model="selectedCategory"
          placeholder="All Categories"
          clearable
          style="width:200px"
        >
          <el-option
            v-for="cat in categories"
            :key="cat"
            :label="cat"
            :value="cat"
          />
        </el-select>
        <el-select v-model="stockFilter" placeholder="All Stock" clearable style="width:160px">
          <el-option label="In Stock" value="In Stock" />
          <el-option label="Out of Stock" value="Out of Stock" />
        </el-select>
        <el-tag type="info" round>{{ filteredProducts.length }} items</el-tag>
      </div>
    </el-card>

    <!-- Loading -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="3" animated />
    </div>

    <!-- Product Grid -->
    <div v-else-if="filteredProducts.length" class="products-grid">
      <el-card
        v-for="product in filteredProducts"
        :key="product.Product_ID"
        class="product-card"
        shadow="hover"
      >
        <div class="product-badges">
          <el-tag
            :type="isInStock(product) ? 'success' : 'danger'"
            size="small"
            round
          >
            {{ isInStock(product) ? 'In Stock' : 'Out of Stock' }}
          </el-tag>
          <el-tag
            v-if="isCPSelect(product)"
            type="warning"
            size="small"
            round
          >
            CP Select
          </el-tag>
        </div>

        <div class="product-icon">
          <el-icon :size="40" color="#67c23a"><Goods /></el-icon>
        </div>

        <div class="product-name">{{ product.Product_Name || product.Name_EN || product.product_name || '—' }}</div>
        <div class="product-category">
          <el-tag type="info" size="small">{{ product.Category || product.category || '—' }}</el-tag>
        </div>

        <div class="product-price">
          <span class="price-value">¥{{ formatPrice(product.Price_CNY || product.price_cny) }}</span>
          <span class="price-unit"> / {{ product.Unit || product.unit || 'unit' }}</span>
        </div>

        <div v-if="product.Origin || product.origin" class="product-origin">
          <el-icon size="12"><LocationFilled /></el-icon>
          {{ product.Origin || product.origin }}
        </div>

        <el-divider style="margin:12px 0" />

        <div class="product-actions">
          <el-button
            text
            type="primary"
            size="small"
            @click="$router.push(`/traceability/${product.Product_ID || product.product_id}`)"
          >
            <el-icon><LocationFilled /></el-icon>
            Traceability
          </el-button>
          <el-button
            type="success"
            size="small"
            :disabled="!isInStock(product)"
            @click.stop="addToCart(product)"
          >
            <el-icon><ShoppingCart /></el-icon>
            Add to Cart
          </el-button>
        </div>
      </el-card>
    </div>

    <el-empty v-else description="No products found" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Goods, LocationFilled, ShoppingCart } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import api from '../api/index.js'
import CartBubble from '../components/CartBubble.vue'
import { useCartStore } from '../stores/cart.js'

const cart = useCartStore()

function addToCart(product) {
  cart.addItem(product)
  ElMessage({ message: `Added "${product.Product_Name || product.product_name}" to cart`, type: 'success', duration: 1500 })
}

const loading = ref(true)
const products = ref([])
const searchText = ref('')
const selectedCategory = ref('')
const stockFilter = ref('')

function isInStock(p) {
  const val = p.Stock_Status || p.stock_status || ''
  return val.toString().toLowerCase().includes('in')
}

function isCPSelect(p) {
  const val = p.CP_Select || p.cp_select
  return val === true || val === 1 || val === 'Yes' || val === 'yes'
}

function formatPrice(val) {
  if (val === null || val === undefined) return '—'
  return Number(val).toFixed(2)
}

const categories = computed(() => {
  const cats = new Set(
    products.value.map(p => p.Category || p.category).filter(Boolean)
  )
  return Array.from(cats).sort()
})

const filteredProducts = computed(() => {
  return products.value.filter(p => {
    const name = (p.Product_Name || p.product_name || '').toLowerCase()
    const cat = p.Category || p.category || ''
    const matchSearch = !searchText.value || name.includes(searchText.value.toLowerCase())
    const matchCat = !selectedCategory.value || cat === selectedCategory.value
    const matchStock = !stockFilter.value || (
      stockFilter.value === 'In Stock' ? isInStock(p) : !isInStock(p)
    )
    return matchSearch && matchCat && matchStock
  })
})

onMounted(async () => {
  try {
    const data = await api.get('/products')
    products.value = Array.isArray(data) ? data : []
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.products-view {
  padding-bottom: 40px;
}

.page-header {
  margin-bottom: 24px;
}

.filter-bar {
  margin-bottom: 24px;
  border-radius: 12px;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.loading-container {
  margin-top: 24px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}

.product-card {
  border-radius: 14px;
  position: relative;
  transition: transform 0.2s;
}

.product-card:hover {
  transform: translateY(-4px);
}

.product-badges {
  display: flex;
  gap: 6px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.product-icon {
  display: flex;
  justify-content: center;
  margin-bottom: 12px;
}

.product-name {
  font-size: 15px;
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 8px;
  text-align: center;
}

.product-category {
  text-align: center;
  margin-bottom: 12px;
}

.product-price {
  text-align: center;
  margin-bottom: 8px;
}

.price-value {
  font-size: 22px;
  font-weight: 700;
  color: #f56c6c;
}

.price-unit {
  font-size: 13px;
  color: #909399;
}

.product-origin {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.product-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}
</style>
