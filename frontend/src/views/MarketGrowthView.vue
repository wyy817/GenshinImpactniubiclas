<template>
  <div class="market-growth-page">
    <div class="page-header">
      <h1>Market Growth Trends</h1>
      <p>China Fresh Food E-commerce Market Size 2014–2028 — Historical & Forecast</p>
    </div>

    <!-- KPI Banner -->
    <el-row :gutter="16" class="stats-row">
      <el-col :span="4">
        <el-card class="stat-card stat-blue">
          <div class="stat-icon">📦</div>
          <div class="stat-val">¥736.8B</div>
          <div class="stat-lbl">2024 Market Size</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card stat-green">
          <div class="stat-icon">📈</div>
          <div class="stat-val">~22%</div>
          <div class="stat-lbl">CAGR 2021–2028</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card stat-orange">
          <div class="stat-icon">🎯</div>
          <div class="stat-val">9.8%</div>
          <div class="stat-lbl">2024 Penetration</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card stat-red">
          <div class="stat-icon">🚀</div>
          <div class="stat-val">2026</div>
          <div class="stat-lbl">CP Group Entry</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card stat-purple">
          <div class="stat-icon">🔮</div>
          <div class="stat-val">¥1,587B</div>
          <div class="stat-lbl">2028 Forecast</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card stat-cyan">
          <div class="stat-icon">🌏</div>
          <div class="stat-val">18.2%</div>
          <div class="stat-lbl">2028 Est. Penetration</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Main Dual-Axis Chart -->
    <el-card class="chart-card">
      <template #header>
        <div class="chart-header-row">
          <span>Market Size & Penetration Rate (2014–2028)</span>
          <div class="legend-badges">
            <span class="badge badge-blue">━ Historical Market Size</span>
            <span class="badge badge-orange">┅ Forecast Market Size</span>
            <span class="badge badge-green">━ Penetration Rate</span>
            <span class="badge badge-red">┆ CP Entry 2026</span>
          </div>
        </div>
      </template>
      <v-chart :option="dualAxisOption" style="height:420px;" autoresize />
    </el-card>

    <!-- Growth Rate Bar Chart -->
    <el-row :gutter="20" class="charts-row">
      <el-col :span="14">
        <el-card>
          <template #header><span>Year-over-Year Growth Rate (%)</span></template>
          <v-chart :option="growthBarOption" style="height:280px;" autoresize />
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card>
          <template #header><span>Market Size Breakdown 2024 vs 2028</span></template>
          <v-chart :option="comparisonDonut" style="height:280px;" autoresize />
        </el-card>
      </el-col>
    </el-row>

    <!-- Data Table -->
    <el-card class="table-card">
      <template #header><span>Year-by-Year Data</span></template>
      <el-table :data="marketData" border stripe>
        <el-table-column prop="Year" label="Year" width="90" />
        <el-table-column label="Market Size (CNY B)" width="200">
          <template #default="{ row }">¥{{ row.Market_Size_CNY_B || row.market_size_cny_b }}B</template>
        </el-table-column>
        <el-table-column label="Penetration Rate" width="160">
          <template #default="{ row }">{{ row.Penetration_Rate || row.penetration_rate }}%</template>
        </el-table-column>
        <el-table-column label="YoY Growth" width="130">
          <template #default="{ row }">
            <span v-if="yoyGrowth(row)" :style="{ color: '#67C23A', fontWeight: 600 }">+{{ yoyGrowth(row) }}%</span>
            <span v-else>—</span>
          </template>
        </el-table-column>
        <el-table-column label="Type" width="110">
          <template #default="{ row }">
            <el-tag :type="(row.Is_Forecast || row.is_forecast) ? 'warning' : 'success'" size="small">
              {{ (row.Is_Forecast || row.is_forecast) ? 'Forecast' : 'Historical' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="CP Milestone">
          <template #default="{ row }">
            <el-tag v-if="(row.Year || row.year) == 2026" type="danger" size="small" effect="dark">
              🚀 CP Group Market Entry
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart, PieChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent, MarkLineComponent, MarkPointComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, LineChart, BarChart, PieChart, GridComponent, TooltipComponent, LegendComponent, MarkLineComponent, MarkPointComponent])

const marketData = ref([])

const allYears = computed(() => marketData.value.map(d => d.Year || d.year))
const getSize = d => parseFloat(d.Market_Size_CNY_B || d.market_size_cny_b) || 0
const getPen = d => parseFloat(d.Penetration_Rate || d.penetration_rate) || 0

// YoY growth helper
function yoyGrowth(row) {
  const yr = row.Year || row.year
  const prev = marketData.value.find(d => (d.Year || d.year) == yr - 1)
  if (!prev) return null
  const curr = getSize(row)
  const prevV = getSize(prev)
  if (!prevV) return null
  return ((curr - prevV) / prevV * 100).toFixed(1)
}

// Dual-axis line chart
const dualAxisOption = computed(() => {
  const historical = marketData.value.filter(d => !(d.Is_Forecast || d.is_forecast))
  const forecast = marketData.value.filter(d => d.Is_Forecast || d.is_forecast)
  return {
    tooltip: {
      trigger: 'axis',
      formatter: params => params.map(p =>
        p.seriesName.includes('Penetration')
          ? `${p.seriesName}: ${p.value}%`
          : `${p.seriesName}: ¥${p.value}B`
      ).join('<br/>')
    },
    legend: { data: ['Historical (Market Size)', 'Forecast (Market Size)', 'Penetration Rate'], top: 0 },
    grid: { left: '3%', right: '5%', bottom: '3%', top: '12%', containLabel: true },
    xAxis: { type: 'category', data: allYears.value, axisLabel: { rotate: 30 } },
    yAxis: [
      { type: 'value', name: 'CNY Billion', position: 'left', axisLabel: { formatter: '¥{value}B' } },
      { type: 'value', name: 'Penetration %', position: 'right', max: 25, axisLabel: { formatter: '{value}%' } }
    ],
    series: [
      {
        name: 'Historical (Market Size)',
        type: 'line',
        yAxisIndex: 0,
        data: allYears.value.map(y => {
          const d = historical.find(h => (h.Year || h.year) == y)
          return d ? getSize(d) : null
        }),
        itemStyle: { color: '#409EFF' },
        lineStyle: { width: 3 },
        symbol: 'circle', symbolSize: 7,
        connectNulls: false
      },
      {
        name: 'Forecast (Market Size)',
        type: 'line',
        yAxisIndex: 0,
        data: allYears.value.map(y => {
          const d = forecast.find(f => (f.Year || f.year) == y)
          return d ? getSize(d) : null
        }),
        itemStyle: { color: '#E6A23C' },
        lineStyle: { type: 'dashed', width: 3 },
        symbol: 'circle', symbolSize: 7,
        connectNulls: false,
        markLine: {
          data: [{ xAxis: '2026', label: { formatter: 'CP Entry', color: '#F56C6C', fontWeight: 700 }, lineStyle: { color: '#F56C6C', type: 'solid', width: 2 } }]
        }
      },
      {
        name: 'Penetration Rate',
        type: 'line',
        yAxisIndex: 1,
        data: allYears.value.map(y => {
          const d = marketData.value.find(h => (h.Year || h.year) == y)
          return d ? getPen(d) : null
        }),
        itemStyle: { color: '#67C23A' },
        lineStyle: { width: 2, type: 'dotted' },
        symbol: 'diamond', symbolSize: 6
      }
    ]
  }
})

// YoY growth bar
const growthBarOption = computed(() => {
  const years = allYears.value.slice(1)
  const growthData = years.map(y => {
    const curr = marketData.value.find(d => (d.Year || d.year) == y)
    const prev = marketData.value.find(d => (d.Year || d.year) == y - 1)
    if (!curr || !prev) return null
    return parseFloat(((getSize(curr) - getSize(prev)) / getSize(prev) * 100).toFixed(1))
  })
  return {
    tooltip: { trigger: 'axis', formatter: '{b}: +{c}%' },
    grid: { left: '3%', right: '5%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: years, axisLabel: { rotate: 30, fontSize: 10 } },
    yAxis: { type: 'value', name: 'YoY Growth (%)', axisLabel: { formatter: '{value}%' } },
    series: [{
      type: 'bar',
      data: growthData.map((v, i) => ({
        value: v,
        itemStyle: {
          color: years[i] >= 2025 ? '#E6A23C' : '#409EFF',
          borderRadius: [4, 4, 0, 0],
          opacity: v === null ? 0 : 1
        }
      })),
      label: { show: true, position: 'top', formatter: v => v.value ? `+${v.value}%` : '', fontSize: 10 }
    }]
  }
})

// Comparison donut (2024 vs 2028 relative market share context)
const comparisonDonut = {
  tooltip: { trigger: 'item', formatter: '{b}: ¥{c}B ({d}%)' },
  legend: { orient: 'vertical', right: '5%', top: 'center' },
  series: [{
    type: 'pie',
    radius: ['35%', '65%'],
    center: ['40%', '50%'],
    data: [
      { name: '2024 Actual', value: 736.8, itemStyle: { color: '#409EFF' } },
      { name: '2025 Forecast', value: 892 - 736.8, itemStyle: { color: '#67C23A' } },
      { name: '2026 (CP Entry)', value: 1081 - 892, itemStyle: { color: '#E6A23C' } },
      { name: '2027–2028 Growth', value: 1587 - 1081, itemStyle: { color: '#F56C6C' } }
    ],
    label: { show: false },
    itemStyle: { borderRadius: 4 }
  }]
}

onMounted(async () => {
  try {
    const base = (import.meta.env.VITE_API_BASE_URL || '') + '/api/v1'
    const res = await fetch(`${base}/market-data`)
    const json = await res.json()
    marketData.value = json.data || []
  } catch (e) {
    ElMessage.error('Failed to load market data')
    marketData.value = [
      { Year: 2014, Market_Size_CNY_B: 68.9, Penetration_Rate: 1.1, Is_Forecast: false },
      { Year: 2015, Market_Size_CNY_B: 102.7, Penetration_Rate: 1.6, Is_Forecast: false },
      { Year: 2016, Market_Size_CNY_B: 157.3, Penetration_Rate: 2.3, Is_Forecast: false },
      { Year: 2017, Market_Size_CNY_B: 202.6, Penetration_Rate: 2.9, Is_Forecast: false },
      { Year: 2018, Market_Size_CNY_B: 261.0, Penetration_Rate: 3.6, Is_Forecast: false },
      { Year: 2019, Market_Size_CNY_B: 325.6, Penetration_Rate: 4.5, Is_Forecast: false },
      { Year: 2020, Market_Size_CNY_B: 442.2, Penetration_Rate: 6.1, Is_Forecast: false },
      { Year: 2021, Market_Size_CNY_B: 500.4, Penetration_Rate: 6.8, Is_Forecast: false },
      { Year: 2022, Market_Size_CNY_B: 578.0, Penetration_Rate: 7.8, Is_Forecast: false },
      { Year: 2023, Market_Size_CNY_B: 656.8, Penetration_Rate: 8.8, Is_Forecast: false },
      { Year: 2024, Market_Size_CNY_B: 736.8, Penetration_Rate: 9.8, Is_Forecast: false },
      { Year: 2025, Market_Size_CNY_B: 892, Penetration_Rate: 11.5, Is_Forecast: true },
      { Year: 2026, Market_Size_CNY_B: 1081, Penetration_Rate: 13.5, Is_Forecast: true },
      { Year: 2027, Market_Size_CNY_B: 1310, Penetration_Rate: 15.8, Is_Forecast: true },
      { Year: 2028, Market_Size_CNY_B: 1587, Penetration_Rate: 18.2, Is_Forecast: true }
    ]
  }
})
</script>

<style scoped>
.market-growth-page { padding: 24px; max-width: 1200px; margin: 0 auto; }
.page-header { margin-bottom: 24px; }
.page-header h1 { font-size: 28px; margin: 0 0 8px; }
.page-header p { color: #666; margin: 0; }

.stats-row { margin-bottom: 24px; }
.stat-card { text-align: center; padding: 6px; }
.stat-icon { font-size: 22px; margin-bottom: 2px; }
.stat-val { font-size: 22px; font-weight: 800; color: #303133; }
.stat-lbl { font-size: 11px; color: #909399; margin-top: 2px; }
.stat-blue { border-top: 3px solid #409EFF; }
.stat-green { border-top: 3px solid #67C23A; }
.stat-orange { border-top: 3px solid #E6A23C; }
.stat-red { border-top: 3px solid #F56C6C; }
.stat-purple { border-top: 3px solid #9747FF; }
.stat-cyan { border-top: 3px solid #00BCD4; }

.chart-card { margin-bottom: 20px; }
.charts-row { margin-bottom: 20px; }
.table-card { margin-bottom: 24px; }

.chart-header-row { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; }
.legend-badges { display: flex; gap: 12px; flex-wrap: wrap; }
.badge { font-size: 12px; color: #606266; }
.badge-blue { color: #409EFF; }
.badge-orange { color: #E6A23C; }
.badge-green { color: #67C23A; }
.badge-red { color: #F56C6C; }
</style>
