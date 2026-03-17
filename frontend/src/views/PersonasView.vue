<template>
  <div class="personas-page">
    <div class="page-header">
      <h1>Customer Personas</h1>
      <p>5 target consumer segments for CP Group's China market entry strategy</p>
    </div>

    <!-- Summary KPI -->
    <el-row :gutter="16" class="kpi-row">
      <el-col :span="6">
        <el-card class="kpi-card kpi-blue">
          <div class="kpi-icon">👤</div>
          <div class="kpi-val">5</div>
          <div class="kpi-lbl">Defined Personas</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="kpi-card kpi-green">
          <div class="kpi-icon">🏙️</div>
          <div class="kpi-val">Tier 1–3</div>
          <div class="kpi-lbl">City Coverage</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="kpi-card kpi-orange">
          <div class="kpi-icon">💵</div>
          <div class="kpi-val">¥80K–500K+</div>
          <div class="kpi-lbl">Annual Income Range</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="kpi-card kpi-purple">
          <div class="kpi-icon">🎂</div>
          <div class="kpi-val">25–55</div>
          <div class="kpi-lbl">Age Range Covered</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Charts Row: Income Bar + Persona Radar -->
    <el-row :gutter="20" class="charts-row">
      <el-col :span="14">
        <el-card>
          <template #header><span>Annual Income by Persona (CNY '000)</span></template>
          <v-chart :option="incomeBarOption" style="height:280px;" autoresize />
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card>
          <template #header><span>City Tier Distribution</span></template>
          <v-chart :option="tierDonutOption" style="height:280px;" autoresize />
        </el-card>
      </el-col>
    </el-row>

    <!-- Persona Priority Matrix -->
    <el-card class="chart-card">
      <template #header><span>Persona Priority & Spending Power Matrix</span></template>
      <v-chart :option="bubbleOption" style="height:300px;" autoresize />
    </el-card>

    <!-- Persona Cards -->
    <el-row :gutter="20">
      <el-col :span="8" v-for="(p, i) in personas" :key="p.Persona_ID || i" style="margin-bottom:20px;">
        <el-card class="persona-card" :style="{ borderTop: `4px solid ${personaColors[i % personaColors.length]}` }">
          <div class="persona-avatar" :style="{ background: personaColors[i % personaColors.length] }">
            {{ initials(p.Name || p.name) }}
          </div>
          <div class="persona-name">{{ p.Name || p.name }}</div>
          <div class="persona-id">{{ p.Persona_ID || p.persona_id }}</div>
          <el-divider />
          <div class="persona-details">
            <div class="detail-row">
              <span class="detail-label">Age Range</span>
              <span class="detail-value">{{ p.Age_Range || p.age_range }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">City Tier</span>
              <span class="detail-value">{{ p.City_Tier || p.city_tier }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Annual Income</span>
              <span class="detail-value" :style="{ color: personaColors[i % personaColors.length] }">
                ¥{{ p.Annual_Income_CNY_K || p.annual_income_cny_k }}K
              </span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Priority</span>
              <el-tag size="small" effect="dark" :color="personaColors[i % personaColors.length]" style="border:none;">
                {{ p.Priority || p.priority }}
              </el-tag>
            </div>
          </div>
          <div class="persona-desc">{{ p.Description || p.description }}</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, PieChart, ScatterChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, BarChart, PieChart, ScatterChart, GridComponent, TooltipComponent, LegendComponent])

const personas = ref([])
const personaColors = ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#9747FF']

function initials(name) {
  if (!name) return '?'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
}

// Income bar chart
const incomeBarOption = computed(() => ({
  tooltip: { trigger: 'axis', formatter: '{b}: ¥{c}K' },
  grid: { left: '3%', right: '5%', bottom: '3%', containLabel: true },
  xAxis: {
    type: 'category',
    data: personas.value.map(p => (p.Name || p.name || '').split(' ').slice(0, 2).join(' ')),
    axisLabel: { fontSize: 11 }
  },
  yAxis: { type: 'value', name: 'Annual Income (¥K)', max: 600 },
  series: [{
    type: 'bar',
    data: personas.value.map((p, i) => ({
      value: parseFloat(p.Annual_Income_CNY_K || p.annual_income_cny_k) || 0,
      itemStyle: { color: personaColors[i % personaColors.length], borderRadius: [4, 4, 0, 0] }
    })),
    label: {
      show: true,
      position: 'top',
      formatter: v => `¥${v.value}K`,
      fontWeight: 600
    }
  }]
}))

// City tier donut
const tierDonutOption = computed(() => {
  const tierMap = {}
  personas.value.forEach(p => {
    const tier = p.City_Tier || p.city_tier || 'Unknown'
    tierMap[tier] = (tierMap[tier] || 0) + 1
  })
  return {
    tooltip: { trigger: 'item', formatter: '{b}: {c} persona(s) ({d}%)' },
    legend: { orient: 'vertical', right: '5%', top: 'center' },
    series: [{
      type: 'pie',
      radius: ['40%', '68%'],
      center: ['40%', '50%'],
      data: Object.entries(tierMap).map(([name, value]) => ({ name, value })),
      label: { show: false },
      itemStyle: { borderRadius: 4 }
    }]
  }
})

// Bubble: income vs age midpoint, bubble size = priority rank
const ageMid = str => {
  if (!str) return 35
  const m = str.match(/(\d+)[–-](\d+)/)
  return m ? (parseInt(m[1]) + parseInt(m[2])) / 2 : 35
}

const bubbleOption = computed(() => ({
  tooltip: {
    trigger: 'item',
    formatter: params => {
      const d = params.data
      return `${d[3]}<br/>Age midpoint: ${d[0]}<br/>Income: ¥${d[1]}K<br/>Priority: ${d[2]}`
    }
  },
  grid: { left: '5%', right: '5%', bottom: '10%', containLabel: true },
  xAxis: { name: 'Age Midpoint', type: 'value', min: 20, max: 60 },
  yAxis: { name: 'Annual Income (¥K)', type: 'value', min: 0, max: 600 },
  series: [{
    type: 'scatter',
    symbolSize: d => Math.sqrt(d[1]) * 3,
    data: personas.value.map((p, i) => [
      ageMid(p.Age_Range || p.age_range),
      parseFloat(p.Annual_Income_CNY_K || p.annual_income_cny_k) || 100,
      p.Priority || p.priority || 'Medium',
      p.Name || p.name
    ]),
    itemStyle: {
      color: params => personaColors[params.dataIndex % personaColors.length],
      opacity: 0.85
    },
    label: {
      show: true,
      formatter: params => (params.data[3] || '').split(' ')[0],
      position: 'top',
      fontSize: 11,
      fontWeight: 600
    }
  }]
}))

onMounted(async () => {
  try {
    const base = (import.meta.env.VITE_API_BASE_URL || '') + '/api/v1'
    const res = await fetch(`${base}/personas`)
    const json = await res.json()
    personas.value = json.data || []
  } catch (e) {
    ElMessage.error('Failed to load personas')
    personas.value = [
      { Persona_ID: 'PA001', Name: 'Pragmatic Mei', Age_Range: '28-38', City_Tier: 'Tier 1', Annual_Income_CNY_K: 200, Priority: 'Quality/Safety', Description: 'Quality-conscious urban professional, family-oriented.' },
      { Persona_ID: 'PA002', Name: 'Value Victor', Age_Range: '35-50', City_Tier: 'Tier 1-2', Annual_Income_CNY_K: 150, Priority: 'Value', Description: 'Price-performance focused, compares platforms.' },
      { Persona_ID: 'PA003', Name: 'Health Hero', Age_Range: '25-35', City_Tier: 'Tier 1-2', Annual_Income_CNY_K: 120, Priority: 'Health', Description: 'Organic and functional food enthusiast.' },
      { Persona_ID: 'PA004', Name: 'Premium Penny', Age_Range: '40-55', City_Tier: 'Tier 1', Annual_Income_CNY_K: 500, Priority: 'Premium', Description: 'High-net-worth, demands white-glove service.' },
      { Persona_ID: 'PA005', Name: 'Suburban Savvy', Age_Range: '30-45', City_Tier: 'Tier 2-3', Annual_Income_CNY_K: 80, Priority: 'Convenience', Description: 'Convenience-first, low delivery fee sensitive.' }
    ]
  }
})
</script>

<style scoped>
.personas-page { padding: 24px; max-width: 1200px; margin: 0 auto; }
.page-header { margin-bottom: 24px; }
.page-header h1 { font-size: 28px; margin: 0 0 8px; }
.page-header p { color: #666; margin: 0; }

.kpi-row { margin-bottom: 24px; }
.kpi-card { text-align: center; padding: 8px; }
.kpi-icon { font-size: 26px; margin-bottom: 4px; }
.kpi-val { font-size: 22px; font-weight: 800; color: #303133; }
.kpi-lbl { font-size: 12px; color: #909399; margin-top: 4px; }
.kpi-blue { border-top: 3px solid #409EFF; }
.kpi-green { border-top: 3px solid #67C23A; }
.kpi-orange { border-top: 3px solid #E6A23C; }
.kpi-purple { border-top: 3px solid #9747FF; }

.charts-row { margin-bottom: 20px; }
.chart-card { margin-bottom: 24px; }

.persona-card { text-align: center; }
.persona-avatar { width: 64px; height: 64px; border-radius: 50%; margin: 0 auto 12px; display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 700; color: #fff; }
.persona-name { font-size: 18px; font-weight: 700; }
.persona-id { font-size: 12px; color: #909399; margin-top: 2px; }
.persona-details { text-align: left; }
.detail-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.detail-label { font-size: 13px; color: #909399; }
.detail-value { font-size: 13px; font-weight: 600; }
.persona-desc { text-align: left; font-size: 13px; color: #606266; margin-top: 12px; line-height: 1.5; }
</style>
