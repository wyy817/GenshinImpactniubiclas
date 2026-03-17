<template>
  <div class="competitors-page">
    <div class="page-header">
      <h1>Competitor Analysis</h1>
      <p>Dingdong Maicai vs Freshippo (Hema) — China Fresh Food Market Leaders 2024</p>
    </div>

    <!-- KPI Banner -->
    <el-row :gutter="16" class="kpi-row">
      <el-col :span="6">
        <el-card class="kpi-card kpi-blue">
          <div class="kpi-icon">💰</div>
          <div class="kpi-val">¥98.07B</div>
          <div class="kpi-lbl">Combined Revenue 2024</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="kpi-card kpi-green">
          <div class="kpi-icon">👥</div>
          <div class="kpi-val">~18.5M</div>
          <div class="kpi-lbl">Combined MAU</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="kpi-card kpi-orange">
          <div class="kpi-icon">🏪</div>
          <div class="kpi-val">1,430+</div>
          <div class="kpi-lbl">Total Stores / Warehouses</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="kpi-card kpi-purple">
          <div class="kpi-icon">🚚</div>
          <div class="kpi-val">~20%</div>
          <div class="kpi-lbl">Avg Fulfillment Cost Rate</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Competitor summary cards -->
    <el-row :gutter="20" class="competitor-cards">
      <el-col :span="12" v-for="c in twoCompetitors" :key="c.Competitor || c.competitor">
        <el-card class="competitor-card" :class="isDingdong(c) ? 'card-dingdong' : 'card-freshippo'">
          <template #header>
            <div class="card-header-row">
              <span class="card-title">{{ c.Competitor || c.competitor }}</span>
              <el-tag :type="isDingdong(c) ? 'primary' : 'success'" size="small">
                {{ isDingdong(c) ? 'Warehouse-led' : 'Store-led' }}
              </el-tag>
            </div>
          </template>
          <div class="metrics-grid">
            <div class="metric">
              <span class="label">Revenue (2024)</span>
              <span class="value">¥{{ c.Revenue_CNY_B || c.revenue_cny_b }}B</span>
            </div>
            <div class="metric">
              <span class="label">GMV</span>
              <span class="value">¥{{ c.GMV_CNY_B || c.gmv_cny_b }}B</span>
            </div>
            <div class="metric">
              <span class="label">Net Profit</span>
              <span class="value net-profit">{{ isDingdong(c) ? '¥295M' : 'FY2025 ✓' }}</span>
            </div>
            <div class="metric">
              <span class="label">MAU</span>
              <span class="value">{{ c.MAU_M || c.mau_m || (isDingdong(c) ? '8.22' : '~10') }}M</span>
            </div>
            <div class="metric">
              <span class="label">Avg Basket</span>
              <span class="value">¥{{ c.Avg_Basket_CNY || c.avg_basket_cny }}</span>
            </div>
            <div class="metric">
              <span class="label">Stores / Warehouses</span>
              <span class="value">{{ c.Store_Count || c.store_count || (isDingdong(c) ? '1,000+' : '430') }}</span>
            </div>
            <div class="metric">
              <span class="label">Fulfillment Cost Rate</span>
              <span class="value" :style="{ color: isDingdong(c) ? '#E6A23C' : '#67C23A' }">
                {{ isDingdong(c) ? '21.7%' : '~19%' }}
              </span>
            </div>
            <div class="metric">
              <span class="label">Founded</span>
              <span class="value">{{ isDingdong(c) ? '2017' : '2016' }}</span>
            </div>
          </div>
          <div class="card-footer-tag">
            <el-tag size="small" effect="plain" :type="isDingdong(c) ? 'primary' : 'success'">
              {{ isDingdong(c) ? '30-min delivery · SKU 5,000+' : 'Offline-online · SKU 8,000+' }}
            </el-tag>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Charts Row 1: Bar + Radar -->
    <el-row :gutter="20" class="charts-row">
      <el-col :span="14">
        <el-card>
          <template #header><span>Revenue vs GMV (CNY Billion, 2024)</span></template>
          <v-chart :option="barOption" style="height:300px;" autoresize />
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card>
          <template #header><span>Multi-Dimension Benchmarking</span></template>
          <v-chart :option="radarOption" style="height:300px;" autoresize />
        </el-card>
      </el-col>
    </el-row>

    <!-- Charts Row 2: Fulfillment Cost + Avg Basket Gauge -->
    <el-row :gutter="20" class="charts-row">
      <el-col :span="12">
        <el-card>
          <template #header><span>Fulfillment Cost Rate Comparison (%)</span></template>
          <v-chart :option="fulfillmentBarOption" style="height:260px;" autoresize />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header><span>Avg Basket Size vs MAU</span></template>
          <v-chart :option="bubbleOption" style="height:260px;" autoresize />
        </el-card>
      </el-col>
    </el-row>

    <!-- Strategic Advantage Table -->
    <el-card class="table-card">
      <template #header><span>Strategic Positioning Summary</span></template>
      <el-table :data="strategyTable" border>
        <el-table-column prop="dimension" label="Dimension" width="200" />
        <el-table-column prop="dingdong" label="Dingdong Maicai">
          <template #default="{ row }">
            <span :class="row.winner === 'dingdong' ? 'winner-text' : ''">{{ row.dingdong }}</span>
            <el-tag v-if="row.winner === 'dingdong'" size="small" type="success" style="margin-left:6px;">✓ Lead</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="freshippo" label="Freshippo (Hema)">
          <template #default="{ row }">
            <span :class="row.winner === 'freshippo' ? 'winner-text' : ''">{{ row.freshippo }}</span>
            <el-tag v-if="row.winner === 'freshippo'" size="small" type="success" style="margin-left:6px;">✓ Lead</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="cpOpportunity" label="CP Group Opportunity" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, ScatterChart, RadarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent, RadarComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, BarChart, ScatterChart, RadarChart, GridComponent, TooltipComponent, LegendComponent, RadarComponent])

const competitors = ref([])

// Only show Dingdong and Freshippo
const twoCompetitors = computed(() =>
  competitors.value
    .filter(c => {
      const name = (c.Competitor || c.competitor || '').toLowerCase()
      return name.includes('dingdong') || name.includes('freshippo') || name.includes('hema')
    })
    .slice(0, 2)
)

function isDingdong(c) {
  return (c.Competitor || c.competitor || '').toLowerCase().includes('dingdong')
}

// Bar chart: Revenue vs GMV
const barOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: { data: ['Revenue (¥B)', 'GMV (¥B)'] },
  grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  xAxis: {
    type: 'category',
    data: twoCompetitors.value.map(c => c.Competitor || c.competitor),
    axisLabel: { fontSize: 13, fontWeight: 600 }
  },
  yAxis: { type: 'value', name: 'CNY Billion' },
  series: [
    {
      name: 'Revenue (¥B)',
      type: 'bar',
      barWidth: '30%',
      data: twoCompetitors.value.map(c => parseFloat(c.Revenue_CNY_B || c.revenue_cny_b) || 0),
      itemStyle: { color: '#409EFF', borderRadius: [4, 4, 0, 0] },
      label: { show: true, position: 'top', formatter: v => `¥${v.value}B` }
    },
    {
      name: 'GMV (¥B)',
      type: 'bar',
      barWidth: '30%',
      data: twoCompetitors.value.map(c => parseFloat(c.GMV_CNY_B || c.gmv_cny_b) || 0),
      itemStyle: { color: '#67C23A', borderRadius: [4, 4, 0, 0] },
      label: { show: true, position: 'top', formatter: v => `¥${v.value}B` }
    }
  ]
}))

// Radar chart: multi-dimension (normalized 0-100)
const radarOption = {
  tooltip: {},
  legend: { data: ['Dingdong Maicai', 'Freshippo (Hema)'], bottom: 0 },
  radar: {
    indicator: [
      { name: 'Revenue Scale', max: 100 },
      { name: 'MAU', max: 100 },
      { name: 'Avg Basket', max: 100 },
      { name: 'Physical Reach', max: 100 },
      { name: 'Fulfillment Eff.', max: 100 },
      { name: 'Brand Trust', max: 100 }
    ],
    splitArea: { areaStyle: { color: ['rgba(64,158,255,0.05)', 'rgba(64,158,255,0.1)'] } }
  },
  series: [{
    type: 'radar',
    data: [
      {
        name: 'Dingdong Maicai',
        value: [31, 82, 58, 100, 72, 78],
        itemStyle: { color: '#409EFF' },
        areaStyle: { opacity: 0.2 }
      },
      {
        name: 'Freshippo (Hema)',
        value: [100, 50, 100, 43, 88, 92],
        itemStyle: { color: '#67C23A' },
        areaStyle: { opacity: 0.2 }
      }
    ]
  }]
}

// Fulfillment cost bar
const fulfillmentBarOption = {
  tooltip: { trigger: 'axis', formatter: '{b}: {c}%' },
  grid: { left: '3%', right: '15%', bottom: '3%', containLabel: true },
  xAxis: { type: 'value', max: 30, name: '%', axisLabel: { formatter: '{value}%' } },
  yAxis: { type: 'category', data: ['Freshippo (Hema)', 'Dingdong Maicai'] },
  series: [{
    type: 'bar',
    data: [
      { value: 19, itemStyle: { color: '#67C23A', borderRadius: [0, 4, 4, 0] } },
      { value: 21.7, itemStyle: { color: '#E6A23C', borderRadius: [0, 4, 4, 0] } }
    ],
    label: { show: true, position: 'right', formatter: '{c}%', fontWeight: 600 }
  }]
}

// Avg Basket vs MAU scatter
const bubbleOption = {
  tooltip: {
    trigger: 'item',
    formatter: params => `${params.data[3]}<br/>MAU: ${params.data[0]}M<br/>Avg Basket: ¥${params.data[1]}<br/>Revenue: ¥${params.data[2]}B`
  },
  grid: { left: '3%', right: '10%', bottom: '10%', containLabel: true },
  xAxis: { name: 'MAU (M)', type: 'value', min: 0, max: 15 },
  yAxis: { name: 'Avg Basket (¥)', type: 'value', min: 0, max: 150 },
  series: [{
    type: 'scatter',
    symbolSize: d => Math.sqrt(d[2]) * 8,
    data: [
      [8.22, 70, 23.07, 'Dingdong Maicai'],
      [10, 120, 75, 'Freshippo (Hema)']
    ],
    itemStyle: { color: (params) => params.data[3].includes('Dingdong') ? '#409EFF' : '#67C23A', opacity: 0.85 },
    label: {
      show: true,
      formatter: params => params.data[3].split(' ')[0],
      position: 'top',
      fontWeight: 600
    }
  }]
}

// Strategy table
const strategyTable = [
  { dimension: 'Business Model', dingdong: 'Dark store (warehouse-led)', freshippo: 'Store + online hybrid', winner: 'freshippo', cpOpportunity: 'Hybrid dark store + showroom' },
  { dimension: 'Revenue 2024', dingdong: '¥23.07B', freshippo: '¥75B', winner: 'freshippo', cpOpportunity: 'Underserved premium segment' },
  { dimension: 'Monthly Active Users', dingdong: '8.22M', freshippo: '~10M', winner: 'freshippo', cpOpportunity: 'Loyalty via traceability' },
  { dimension: 'Avg Basket Size', dingdong: '¥70', freshippo: '¥120', winner: 'freshippo', cpOpportunity: 'Target ¥150+ premium tier' },
  { dimension: 'Physical Reach', dingdong: '1,000+ warehouses', freshippo: '430 stores', winner: 'dingdong', cpOpportunity: 'Yangtze Delta focus first' },
  { dimension: 'Fulfillment Cost Rate', dingdong: '21.7%', freshippo: '~19%', winner: 'freshippo', cpOpportunity: 'CP supply chain advantage' },
  { dimension: 'Key Differentiator', dingdong: '30-min delivery', freshippo: 'In-store experience', winner: null, cpOpportunity: 'Farm-to-table traceability' }
]

onMounted(async () => {
  try {
    const base = (import.meta.env.VITE_API_BASE_URL || '') + '/api/v1'
    const res = await fetch(`${base}/competitors`)
    const json = await res.json()
    competitors.value = (json.data || []).filter(c => {
      const name = (c.Competitor || c.competitor || '').toLowerCase()
      return name.includes('dingdong') || name.includes('freshippo') || name.includes('hema')
    })
  } catch (e) {
    ElMessage.error('Failed to load competitor data')
    // Fallback hardcoded data
    competitors.value = [
      { Competitor: 'Dingdong Maicai', Revenue_CNY_B: 23.07, GMV_CNY_B: 26.5, MAU_M: 8.22, Avg_Basket_CNY: 70, Store_Count: '1,000+' },
      { Competitor: 'Freshippo (Hema)', Revenue_CNY_B: 75, GMV_CNY_B: 75, MAU_M: 10, Avg_Basket_CNY: 120, Store_Count: 430 }
    ]
  }
})
</script>

<style scoped>
.competitors-page { padding: 24px; max-width: 1200px; margin: 0 auto; }
.page-header { margin-bottom: 24px; }
.page-header h1 { font-size: 28px; margin: 0 0 8px; }
.page-header p { color: #666; margin: 0; }

/* KPI Row */
.kpi-row { margin-bottom: 24px; }
.kpi-card { text-align: center; padding: 8px; position: relative; overflow: hidden; }
.kpi-icon { font-size: 28px; margin-bottom: 4px; }
.kpi-val { font-size: 26px; font-weight: 800; color: #303133; }
.kpi-lbl { font-size: 12px; color: #909399; margin-top: 4px; }
.kpi-blue { border-top: 3px solid #409EFF; }
.kpi-green { border-top: 3px solid #67C23A; }
.kpi-orange { border-top: 3px solid #E6A23C; }
.kpi-purple { border-top: 3px solid #9747FF; }

/* Competitor Cards */
.competitor-cards { margin-bottom: 24px; }
.competitor-card { height: 100%; }
.card-dingdong { border-top: 4px solid #409EFF; }
.card-freshippo { border-top: 4px solid #67C23A; }
.card-header-row { display: flex; align-items: center; justify-content: space-between; }
.card-title { font-size: 18px; font-weight: 700; }
.metrics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.metric { display: flex; flex-direction: column; }
.label { font-size: 12px; color: #909399; margin-bottom: 2px; }
.value { font-size: 20px; font-weight: 700; color: #303133; }
.net-profit { font-size: 16px; color: #67C23A; }
.card-footer-tag { margin-top: 14px; }

/* Charts */
.charts-row { margin-bottom: 20px; }
.table-card { margin-bottom: 24px; }
.winner-text { font-weight: 700; color: #303133; }
</style>
