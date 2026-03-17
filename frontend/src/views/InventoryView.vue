<template>
  <div class="inventory-page">
    <div class="page-header">
      <h1>Inventory &amp; Sales Dashboard</h1>
      <p class="sub">Real-time stock levels and 30-day sales performance across all SKUs</p>
    </div>

    <!-- KPI Banner -->
    <el-row :gutter="16" class="kpi-row">
      <el-col :span="6" v-for="k in kpis" :key="k.label">
        <el-card class="kpi-card" shadow="never">
          <div class="kpi-value" :style="{ color: k.color }">{{ k.value }}</div>
          <div class="kpi-label">{{ k.label }}</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Charts Row -->
    <el-row :gutter="16" class="charts-row">
      <!-- Stock Status Donut -->
      <el-col :span="8">
        <el-card shadow="never">
          <template #header><span class="card-title">Stock Status Distribution</span></template>
          <v-chart :option="stockStatusChart" style="height:260px" autoresize />
        </el-card>
      </el-col>

      <!-- Stock Qty by Category Bar -->
      <el-col :span="16">
        <el-card shadow="never">
          <template #header><span class="card-title">Stock Quantity by Category</span></template>
          <v-chart :option="stockByCategoryChart" style="height:260px" autoresize />
        </el-card>
      </el-col>
    </el-row>

    <!-- Sales Charts Row -->
    <el-row :gutter="16" class="charts-row">
      <!-- Top Sales Bar -->
      <el-col :span="12">
        <el-card shadow="never">
          <template #header><span class="card-title">Top Products — 30-Day Sales (Units)</span></template>
          <v-chart :option="topSalesChart" style="height:300px" autoresize />
        </el-card>
      </el-col>

      <!-- Revenue Bar -->
      <el-col :span="12">
        <el-card shadow="never">
          <template #header><span class="card-title">Top Products — 30-Day Revenue (CNY)</span></template>
          <v-chart :option="revenueChart" style="height:300px" autoresize />
        </el-card>
      </el-col>
    </el-row>

    <!-- Inventory Table -->
    <el-card shadow="never" class="table-card">
      <template #header>
        <div class="table-header">
          <span class="card-title">Inventory Detail</span>
          <div class="filters">
            <el-select v-model="filterStatus" placeholder="Stock Status" clearable size="small" style="width:140px;margin-right:8px">
              <el-option label="In Stock" value="In Stock" />
              <el-option label="Out of Stock" value="Out of Stock" />
            </el-select>
            <el-select v-model="filterCategory" placeholder="Category" clearable size="small" style="width:140px">
              <el-option v-for="c in categories" :key="c" :label="c" :value="c" />
            </el-select>
          </div>
        </div>
      </template>

      <el-table :data="filteredInventory" stripe border size="small" v-loading="loading">
        <el-table-column prop="Product_ID" label="ID" width="72" />
        <el-table-column prop="Product_Name" label="Product" min-width="160" />
        <el-table-column prop="Category" label="Category" width="110" />
        <el-table-column prop="Unit" label="Unit" width="110" />
        <el-table-column prop="Price_CNY" label="Price (¥)" width="90" align="right">
          <template #default="{ row }">¥{{ row.Price_CNY }}</template>
        </el-table-column>
        <el-table-column prop="Stock_Status" label="Status" width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="row.Stock_Status === 'In Stock' ? 'success' : 'danger'" size="small">
              {{ row.Stock_Status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="Stock_Qty" label="Qty" width="80" align="right" />
        <el-table-column prop="Sales_7D" label="Sold 7D" width="84" align="right">
          <template #default="{ row }">
            <span :class="row.Sales_7D > 0 ? 'pos' : 'zero'">{{ row.Sales_7D }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="Sales_30D" label="Sold 30D" width="88" align="right">
          <template #default="{ row }">
            <span :class="row.Sales_30D > 0 ? 'pos' : 'zero'">{{ row.Sales_30D }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="Revenue_30D" label="Revenue 30D (¥)" width="130" align="right">
          <template #default="{ row }">¥{{ row.Revenue_30D.toLocaleString() }}</template>
        </el-table-column>
        <el-table-column prop="Last_Restocked" label="Last Restocked" width="130" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, PieChart } from 'echarts/charts'
import {
  GridComponent, TooltipComponent, LegendComponent, TitleComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import api from '../api/index.js'

use([CanvasRenderer, BarChart, PieChart, GridComponent, TooltipComponent, LegendComponent, TitleComponent])

const inventory = ref([])
const loading = ref(false)
const filterStatus = ref('')
const filterCategory = ref('')

onMounted(async () => {
  loading.value = true
  try {
    const data = await api.get('/inventory')
    inventory.value = Array.isArray(data) ? data : []
  } catch (e) {
    // error already shown by api interceptor
  } finally {
    loading.value = false
  }
})

const categories = computed(() => [...new Set(inventory.value.map(i => i.Category).filter(Boolean))])

const filteredInventory = computed(() => {
  return inventory.value.filter(i => {
    if (filterStatus.value && i.Stock_Status !== filterStatus.value) return false
    if (filterCategory.value && i.Category !== filterCategory.value) return false
    return true
  })
})

// KPIs
const kpis = computed(() => {
  const total = inventory.value.length
  const inStock = inventory.value.filter(i => i.Stock_Status === 'In Stock').length
  const outStock = inventory.value.filter(i => i.Stock_Status === 'Out of Stock').length
  const totalRevenue = inventory.value.reduce((s, i) => s + (i.Revenue_30D || 0), 0)
  return [
    { label: 'Total SKUs',       value: total,                                color: '#409EFF' },
    { label: 'In Stock',         value: inStock,                              color: '#67C23A' },
    { label: 'Out of Stock',     value: outStock,                             color: '#F56C6C' },
    { label: '30D Revenue (¥)', value: '¥' + totalRevenue.toLocaleString(), color: '#E6A23C' },
  ]
})

// Stock Status Donut
const stockStatusChart = computed(() => ({
  tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
  legend: { bottom: 0 },
  color: ['#67C23A', '#F56C6C'],
  series: [{
    type: 'pie',
    radius: ['45%', '70%'],
    center: ['50%', '45%'],
    data: [
      { name: 'In Stock',     value: inventory.value.filter(i => i.Stock_Status === 'In Stock').length },
      { name: 'Out of Stock', value: inventory.value.filter(i => i.Stock_Status === 'Out of Stock').length },
    ],
    label: { formatter: '{b}\n{c}' },
  }]
}))

// Stock Qty by Category
const stockByCategoryChart = computed(() => {
  const byCategory = {}
  inventory.value.forEach(i => {
    if (!i.Category) return
    byCategory[i.Category] = (byCategory[i.Category] || 0) + (i.Stock_Qty || 0)
  })
  const cats = Object.keys(byCategory)
  return {
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: cats, axisLabel: { rotate: 15, fontSize: 11 } },
    yAxis: { type: 'value', name: 'Units' },
    color: ['#409EFF'],
    series: [{ type: 'bar', data: cats.map(c => byCategory[c]), barMaxWidth: 50 }]
  }
})

// Top 8 by Sales_30D
const top8Sales = computed(() =>
  [...inventory.value].sort((a, b) => b.Sales_30D - a.Sales_30D).slice(0, 8)
)

const topSalesChart = computed(() => ({
  tooltip: { trigger: 'axis' },
  grid: { left: 20, right: 20, bottom: 60, containLabel: true },
  xAxis: {
    type: 'category',
    data: top8Sales.value.map(i => i.Product_Name),
    axisLabel: { rotate: 20, fontSize: 10, interval: 0 }
  },
  yAxis: { type: 'value', name: 'Units' },
  color: ['#67C23A'],
  series: [{ type: 'bar', data: top8Sales.value.map(i => i.Sales_30D), barMaxWidth: 40 }]
}))

const revenueChart = computed(() => {
  const top8Rev = [...inventory.value].sort((a, b) => b.Revenue_30D - a.Revenue_30D).slice(0, 8)
  return {
    tooltip: { trigger: 'axis', formatter: p => `${p[0].name}<br/>¥${p[0].value.toLocaleString()}` },
    grid: { left: 20, right: 20, bottom: 60, containLabel: true },
    xAxis: {
      type: 'category',
      data: top8Rev.map(i => i.Product_Name),
      axisLabel: { rotate: 20, fontSize: 10, interval: 0 }
    },
    yAxis: { type: 'value', name: '¥' },
    color: ['#E6A23C'],
    series: [{ type: 'bar', data: top8Rev.map(i => i.Revenue_30D), barMaxWidth: 40 }]
  }
})
</script>

<style scoped>
.inventory-page { max-width: 1280px; margin: 0 auto; padding: 24px 16px; }
.page-header { margin-bottom: 24px; }
.page-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 6px; color: #303133; }
.page-header .sub { color: #909399; font-size: 14px; margin: 0; }

.kpi-row { margin-bottom: 20px; }
.kpi-card { text-align: center; padding: 8px 0; }
.kpi-value { font-size: 30px; font-weight: 700; }
.kpi-label { font-size: 13px; color: #909399; margin-top: 4px; }

.charts-row { margin-bottom: 20px; }
.card-title { font-weight: 600; font-size: 14px; color: #303133; }

.table-card { margin-bottom: 24px; }
.table-header { display: flex; justify-content: space-between; align-items: center; }
.filters { display: flex; align-items: center; }

.pos { color: #67C23A; font-weight: 600; }
.zero { color: #C0C4CC; }
</style>
