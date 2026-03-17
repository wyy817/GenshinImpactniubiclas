<template>
  <!-- Floating Cart Bubble -->
  <div class="cart-bubble" @click="drawerOpen = true">
    <el-icon :size="26" color="#fff"><ShoppingCart /></el-icon>
    <span v-if="cart.totalItems > 0" class="cart-badge">{{ cart.totalItems }}</span>
  </div>

  <!-- Cart Drawer -->
  <el-drawer
    v-model="drawerOpen"
    title="Shopping Cart"
    direction="rtl"
    size="380px"
    :append-to-body="true"
  >
    <template #header>
      <div class="drawer-header">
        <el-icon size="20" color="#67c23a"><ShoppingCart /></el-icon>
        <span style="font-weight:700;font-size:17px;margin-left:8px">Shopping Cart</span>
        <el-tag type="success" size="small" round style="margin-left:8px">
          {{ cart.totalItems }} items
        </el-tag>
      </div>
    </template>

    <div v-if="cart.items.length === 0" class="empty-cart">
      <el-empty description="Your cart is empty" :image-size="100" />
      <p class="empty-hint">Browse the Product Catalogue and add items!</p>
    </div>

    <div v-else class="cart-items">
      <div
        v-for="item in cart.items"
        :key="item.id"
        class="cart-item"
      >
        <div class="item-info">
          <div class="item-name">{{ item.name }}</div>
          <div class="item-meta">
            <el-tag type="info" size="small" round>{{ item.category }}</el-tag>
            <span class="item-id">{{ item.id }}</span>
          </div>
          <div class="item-price">¥{{ item.price.toFixed(2) }} / {{ item.unit }}</div>
        </div>
        <div class="item-controls">
          <el-input-number
            v-model="item.qty"
            :min="1"
            :max="99"
            size="small"
            controls-position="right"
            style="width:100px"
            @change="val => cart.updateQty(item.id, val)"
          />
          <el-button
            type="danger"
            :icon="Delete"
            circle
            size="small"
            plain
            @click="cart.removeItem(item.id)"
          />
        </div>
        <div class="item-subtotal">¥{{ (item.price * item.qty).toFixed(2) }}</div>
      </div>
    </div>

    <template #footer>
      <div v-if="cart.items.length > 0" class="drawer-footer">
        <div class="total-row">
          <span class="total-label">Total</span>
          <span class="total-value">¥{{ cart.totalPrice.toFixed(2) }}</span>
        </div>
        <div class="footer-buttons">
          <el-button plain @click="cart.clearCart()">Clear Cart</el-button>
          <el-button type="primary" @click="goCheckout" style="flex:1">
            <el-icon><CreditCard /></el-icon>
            Proceed to Checkout
          </el-button>
        </div>
      </div>
    </template>
  </el-drawer>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ShoppingCart, Delete, CreditCard } from '@element-plus/icons-vue'
import { useCartStore } from '../stores/cart.js'

const cart = useCartStore()
const router = useRouter()
const drawerOpen = ref(false)

function goCheckout() {
  drawerOpen.value = false
  router.push('/checkout')
}
</script>

<style scoped>
.cart-bubble {
  position: fixed;
  bottom: 40px;
  right: 40px;
  width: 62px;
  height: 62px;
  border-radius: 50%;
  background: linear-gradient(135deg, #67c23a, #3a8e00);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(103, 194, 58, 0.5);
  transition: transform 0.2s, box-shadow 0.2s;
  z-index: 999;
  user-select: none;
}

.cart-bubble:hover {
  transform: scale(1.1);
  box-shadow: 0 8px 28px rgba(103, 194, 58, 0.65);
}

.cart-bubble:active {
  transform: scale(0.96);
}

.cart-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  background: #f56c6c;
  color: #fff;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #fff;
}

.drawer-header {
  display: flex;
  align-items: center;
}

.empty-cart {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 40px;
}

.empty-hint {
  color: #909399;
  font-size: 13px;
  margin-top: 8px;
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.cart-item {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.item-info {
  flex: 1;
}

.item-name {
  font-weight: 600;
  font-size: 15px;
  color: #1a1a2e;
  margin-bottom: 4px;
}

.item-meta {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-bottom: 4px;
}

.item-id {
  font-size: 11px;
  color: #c0c4cc;
}

.item-price {
  font-size: 13px;
  color: #909399;
}

.item-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.item-subtotal {
  font-size: 16px;
  font-weight: 700;
  color: #f56c6c;
  text-align: right;
}

.drawer-footer {
  padding: 0;
}

.total-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-top: 1px solid #ebeef5;
  margin-bottom: 12px;
}

.total-label {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.total-value {
  font-size: 22px;
  font-weight: 700;
  color: #f56c6c;
}

.footer-buttons {
  display: flex;
  gap: 10px;
}
</style>
