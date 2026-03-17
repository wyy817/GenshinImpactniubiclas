import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  const items = ref(JSON.parse(localStorage.getItem('cp_cart') || '[]'))
  const orders = ref(JSON.parse(localStorage.getItem('cp_orders') || '[]'))

  const totalItems = computed(() => items.value.reduce((sum, i) => sum + i.qty, 0))
  const totalPrice = computed(() => items.value.reduce((sum, i) => sum + i.price * i.qty, 0))

  function addItem(product) {
    const id = product.Product_ID || product.product_id
    const existing = items.value.find(i => i.id === id)
    if (existing) {
      existing.qty++
    } else {
      items.value.push({
        id,
        name: product.Product_Name || product.product_name || id,
        price: Number(product.Price_CNY || product.price_cny || 0),
        unit: product.Unit || product.unit || 'unit',
        category: product.Category || product.category || '',
        qty: 1,
      })
    }
    _save()
  }

  function removeItem(id) {
    items.value = items.value.filter(i => i.id !== id)
    _save()
  }

  function updateQty(id, qty) {
    const item = items.value.find(i => i.id === id)
    if (!item) return
    if (qty <= 0) removeItem(id)
    else { item.qty = qty; _save() }
  }

  function clearCart() {
    items.value = []
    _save()
  }

  function placeOrder(paymentInfo) {
    const order = {
      id: 'ORD-' + Date.now(),
      items: items.value.map(i => ({ ...i })),
      total: totalPrice.value,
      paymentInfo,
      createdAt: new Date().toISOString(),
    }
    orders.value.unshift(order)
    localStorage.setItem('cp_orders', JSON.stringify(orders.value))
    clearCart()
    return order
  }

  function _save() {
    localStorage.setItem('cp_cart', JSON.stringify(items.value))
  }

  return { items, orders, totalItems, totalPrice, addItem, removeItem, updateQty, clearCart, placeOrder }
})
