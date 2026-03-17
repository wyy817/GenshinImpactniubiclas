<template>
  <div class="checkout-view">

    <!-- Success State -->
    <div v-if="orderPlaced" class="success-state">
      <el-result
        icon="success"
        title="Payment Successful!"
        :sub-title="`Order ${confirmedOrder.id} has been placed. Your products are now traceable.`"
      >
        <template #extra>
          <el-button type="primary" @click="$router.push('/traceability')">
            <el-icon><Search /></el-icon>
            View Traceable Products
          </el-button>
          <el-button @click="$router.push('/products')">Continue Shopping</el-button>
        </template>
      </el-result>

      <el-card class="order-summary-card" shadow="never">
        <h3 style="margin-bottom:16px;font-weight:700">Order Summary — {{ confirmedOrder.id }}</h3>
        <el-table :data="confirmedOrder.items" size="small" stripe>
          <el-table-column prop="name" label="Product" />
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column label="Price" width="110">
            <template #default="{ row }">¥{{ row.price.toFixed(2) }}/{{ row.unit }}</template>
          </el-table-column>
          <el-table-column prop="qty" label="Qty" width="60" />
          <el-table-column label="Subtotal" width="110">
            <template #default="{ row }">¥{{ (row.price * row.qty).toFixed(2) }}</template>
          </el-table-column>
        </el-table>
        <div class="order-total-row">
          <span>Total Paid</span>
          <span class="order-total">¥{{ confirmedOrder.total.toFixed(2) }}</span>
        </div>
      </el-card>
    </div>

    <!-- Checkout Form -->
    <div v-else>
      <div class="page-header">
        <h1 class="page-title">Checkout</h1>
        <p class="page-subtitle">Review your order and complete payment</p>
      </div>

      <!-- Empty cart guard -->
      <div v-if="cart.items.length === 0" class="empty-cart-notice">
        <el-empty description="Your cart is empty">
          <el-button type="primary" @click="$router.push('/products')">Browse Products</el-button>
        </el-empty>
      </div>

      <div v-else class="checkout-layout">
        <!-- Order Items -->
        <div class="checkout-left">
          <el-card shadow="never" class="checkout-card">
            <template #header>
              <div class="card-header-title">
                <el-icon color="#67c23a"><ShoppingBag /></el-icon>
                <span>Order Items ({{ cart.totalItems }})</span>
              </div>
            </template>

            <div class="order-items">
              <div v-for="item in cart.items" :key="item.id" class="order-item">
                <div class="oi-icon">
                  <el-icon size="28" color="#67c23a"><Goods /></el-icon>
                </div>
                <div class="oi-info">
                  <div class="oi-name">{{ item.name }}</div>
                  <div class="oi-meta">
                    <el-tag type="info" size="small" round>{{ item.category }}</el-tag>
                    <span class="oi-id">{{ item.id }}</span>
                  </div>
                  <div class="oi-price">¥{{ item.price.toFixed(2) }} × {{ item.qty }} {{ item.unit }}</div>
                </div>
                <div class="oi-subtotal">¥{{ (item.price * item.qty).toFixed(2) }}</div>
              </div>
            </div>

            <el-divider />
            <div class="cart-total-row">
              <span class="ct-label">Order Total</span>
              <span class="ct-value">¥{{ cart.totalPrice.toFixed(2) }}</span>
            </div>
          </el-card>

          <!-- Traceability Notice -->
          <el-alert
            title="After payment, all purchased products will appear in your Traceable Products list"
            description="You can then track the full farm-to-table supply chain journey for each item."
            type="success"
            show-icon
            :closable="false"
            style="border-radius:10px;margin-top:16px"
          />
        </div>

        <!-- Payment Form -->
        <div class="checkout-right">
          <el-card shadow="never" class="checkout-card">
            <template #header>
              <div class="card-header-title">
                <el-icon color="#409eff"><CreditCard /></el-icon>
                <span>Payment Details</span>
              </div>
            </template>

            <el-form
              ref="formRef"
              :model="form"
              :rules="rules"
              label-position="top"
              size="large"
            >
              <el-form-item label="Cardholder Name" prop="name">
                <el-input v-model="form.name" placeholder="Zhang Wei" prefix-icon="User" />
              </el-form-item>

              <el-form-item label="Card Number" prop="cardNumber">
                <el-input
                  v-model="form.cardNumber"
                  placeholder="1234 5678 9012 3456"
                  maxlength="19"
                  @input="formatCardNumber"
                >
                  <template #suffix>
                    <el-icon color="#409eff"><CreditCard /></el-icon>
                  </template>
                </el-input>
              </el-form-item>

              <div class="form-row">
                <el-form-item label="Expiry Date" prop="expiry" style="flex:1">
                  <el-input
                    v-model="form.expiry"
                    placeholder="MM/YY"
                    maxlength="5"
                    @input="formatExpiry"
                  />
                </el-form-item>
                <el-form-item label="CVV" prop="cvv" style="flex:1">
                  <el-input
                    v-model="form.cvv"
                    placeholder="123"
                    maxlength="3"
                    type="password"
                    show-password
                  />
                </el-form-item>
              </div>

              <el-form-item label="Delivery Address" prop="address">
                <el-input
                  v-model="form.address"
                  placeholder="e.g. 123 Nanjing Road, Shanghai"
                  type="textarea"
                  :rows="2"
                />
              </el-form-item>

              <el-divider>
                <el-tag type="success" size="small">Secured by CP Pay</el-tag>
              </el-divider>

              <div class="pay-summary">
                <span class="pay-label">Amount Due</span>
                <span class="pay-amount">¥{{ cart.totalPrice.toFixed(2) }}</span>
              </div>

              <el-button
                type="success"
                size="large"
                :loading="paying"
                style="width:100%;margin-top:16px;border-radius:8px;font-size:16px;font-weight:700"
                @click="submitPayment"
              >
                <el-icon v-if="!paying"><Lock /></el-icon>
                {{ paying ? 'Processing...' : `Pay ¥${cart.totalPrice.toFixed(2)}` }}
              </el-button>

              <p class="secure-note">
                <el-icon size="12"><Lock /></el-icon>
                This is a demo — no real payment is processed
              </p>
            </el-form>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ShoppingBag, CreditCard, Goods, Lock, Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useCartStore } from '../stores/cart.js'

const cart = useCartStore()
const router = useRouter()

const formRef = ref(null)
const paying = ref(false)
const orderPlaced = ref(false)
const confirmedOrder = ref(null)

const form = reactive({
  name: '',
  cardNumber: '',
  expiry: '',
  cvv: '',
  address: '',
})

const rules = {
  name: [{ required: true, message: 'Please enter cardholder name', trigger: 'blur' }],
  cardNumber: [
    { required: true, message: 'Please enter card number', trigger: 'blur' },
    { pattern: /^\d{4} \d{4} \d{4} \d{4}$/, message: 'Enter a valid 16-digit card number', trigger: 'blur' },
  ],
  expiry: [
    { required: true, message: 'Please enter expiry date', trigger: 'blur' },
    { pattern: /^\d{2}\/\d{2}$/, message: 'Format: MM/YY', trigger: 'blur' },
  ],
  cvv: [
    { required: true, message: 'Please enter CVV', trigger: 'blur' },
    { pattern: /^\d{3}$/, message: 'CVV must be 3 digits', trigger: 'blur' },
  ],
  address: [{ required: true, message: 'Please enter delivery address', trigger: 'blur' }],
}

function formatCardNumber() {
  let v = form.cardNumber.replace(/\D/g, '').slice(0, 16)
  form.cardNumber = v.replace(/(.{4})/g, '$1 ').trim()
}

function formatExpiry() {
  let v = form.expiry.replace(/\D/g, '').slice(0, 4)
  if (v.length >= 3) v = v.slice(0, 2) + '/' + v.slice(2)
  form.expiry = v
}

async function submitPayment() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  paying.value = true
  // Simulate payment processing delay
  await new Promise(r => setTimeout(r, 1800))

  const order = cart.placeOrder({
    name: form.name,
    cardLast4: form.cardNumber.slice(-4),
    address: form.address,
  })

  confirmedOrder.value = order
  orderPlaced.value = true
  paying.value = false
  ElMessage({ message: 'Payment successful! Your order has been confirmed.', type: 'success', duration: 3000 })
}
</script>

<style scoped>
.checkout-view {
  padding-bottom: 60px;
  max-width: 1100px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 28px;
}

.empty-cart-notice {
  margin-top: 60px;
}

.checkout-layout {
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: 24px;
  align-items: flex-start;
}

@media (max-width: 900px) {
  .checkout-layout {
    grid-template-columns: 1fr;
  }
}

.checkout-card {
  border-radius: 14px;
}

.card-header-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 16px;
}

.order-items {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.order-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 10px;
}

.oi-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  background: #f0f9eb;
  border-radius: 10px;
}

.oi-info {
  flex: 1;
}

.oi-name {
  font-weight: 600;
  font-size: 15px;
  color: #1a1a2e;
  margin-bottom: 4px;
}

.oi-meta {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-bottom: 4px;
}

.oi-id {
  font-size: 11px;
  color: #c0c4cc;
}

.oi-price {
  font-size: 13px;
  color: #909399;
}

.oi-subtotal {
  font-size: 17px;
  font-weight: 700;
  color: #f56c6c;
  white-space: nowrap;
}

.cart-total-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 4px;
}

.ct-label {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.ct-value {
  font-size: 24px;
  font-weight: 700;
  color: #f56c6c;
}

.form-row {
  display: flex;
  gap: 16px;
}

.pay-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f0f9eb;
  border-radius: 8px;
}

.pay-label {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.pay-amount {
  font-size: 26px;
  font-weight: 800;
  color: #67c23a;
}

.secure-note {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  font-size: 12px;
  color: #c0c4cc;
  margin-top: 10px;
}

/* Success state */
.success-state {
  padding-top: 20px;
}

.order-summary-card {
  max-width: 700px;
  margin: 0 auto;
  border-radius: 14px;
}

.order-total-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0 0;
  border-top: 2px solid #ebeef5;
  margin-top: 12px;
  font-weight: 600;
  font-size: 15px;
}

.order-total {
  font-size: 22px;
  font-weight: 800;
  color: #f56c6c;
}
</style>
