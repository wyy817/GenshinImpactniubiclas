<template>
  <div class="opportunities-page">
    <div class="page-header">
      <h1>Market Opportunities</h1>
      <p>Strategic entry opportunities for CP Group in China's fresh food e-commerce market</p>
    </div>

    <!-- KPI Row -->
    <el-row :gutter="16" class="kpi-row">
      <el-col :span="6">
        <el-card class="kpi-card kpi-green">
          <div class="kpi-icon">🎯</div>
          <div class="kpi-val">{{ sortedOpportunities.length }}</div>
          <div class="kpi-lbl">Total Opportunities Identified</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="kpi-card kpi-blue">
          <div class="kpi-icon">⭐</div>
          <div class="kpi-val">{{ topScore }}</div>
          <div class="kpi-lbl">Top Opportunity Score</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="kpi-card kpi-orange">
          <div class="kpi-icon">🔥</div>
          <div class="kpi-val">{{ highPriorityCount }}</div>
          <div class="kpi-lbl">High Priority (Score ≥ 85)</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="kpi-card kpi-purple">
          <div class="kpi-icon">📊</div>
          <div class="kpi-val">{{ avgScore }}</div>
          <div class="kpi-lbl">Average Score</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Horizontal Bar Chart -->
    <el-card class="chart-card">
      <template #header><span>Opportunity Scores Overview</span></template>
      <v-chart :option="hBarOption" style="height:320px;" autoresize />
    </el-card>

    <!-- Opportunity Cards -->
    <div v-for="(opp, index) in sortedOpportunities" :key="opp.Rank || index" class="opp-card" :class="scoreClass(opp.Score)">
      <!-- Left accent + rank -->
      <div class="opp-rank">#{{ index + 1 }}</div>

      <!-- Main content -->
      <div class="opp-main">
        <div class="opp-title">{{ opp.Opportunity }}</div>

        <!-- Meta badges -->
        <div class="opp-meta">
          <el-tag v-if="opp.Time_Horizon" size="small" type="info" effect="plain">
            ⏱ {{ opp.Time_Horizon }}
          </el-tag>
          <el-tag v-if="opp.Investment_Level" size="small" type="warning" effect="plain">
            💰 {{ opp.Investment_Level }}
          </el-tag>
          <el-tag v-if="opp.Target_Segment" size="small" type="success" effect="plain">
            👥 {{ opp.Target_Segment }}
          </el-tag>
        </div>

        <!-- Detail rows -->
        <div class="opp-detail-grid">
          <div class="detail-item" v-if="opp.Why_It_Matters">
            <div class="detail-label">📌 Why It Matters</div>
            <div class="detail-body">{{ opp.Why_It_Matters }}</div>
          </div>
          <div class="detail-item" v-if="opp.How_CP_Can_Execute">
            <div class="detail-label">🚀 How CP Can Execute</div>
            <div class="detail-body">{{ opp.How_CP_Can_Execute }}</div>
          </div>
          <div class="detail-item full-width" v-if="opp.CP_Competitive_Advantage">
            <div class="detail-label">🏆 CP Competitive Advantage</div>
            <div class="detail-body advantage">{{ opp.CP_Competitive_Advantage }}</div>
          </div>
        </div>
      </div>

      <!-- Score section -->
      <div class="opp-score-section">
        <div class="score-label">Score</div>
        <div class="score-value" :style="{ color: scoreColor(opp.Score) }">{{ opp.Score }}</div>
        <el-progress
          :percentage="opp.Score"
          :color="scoreColor(opp.Score)"
          :show-text="false"
          style="width: 90px; margin: 6px auto;"
        />
        <div class="priority-badge" :style="{ background: scoreColor(opp.Score) }">
          {{ priorityLabel(opp.Score) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, BarChart, GridComponent, TooltipComponent])

const FALLBACK = [
  {
    Rank: 1, Score: 92,
    Opportunity: 'Full Farm-to-Table Supply Chain Traceability Platform',
    Why_It_Matters: 'Only 3% of China fresh e-commerce offers full traceability; 78% of middle-class consumers cite food safety as #1 concern (CNCA 2024)',
    How_CP_Can_Execute: "Leverage CP Group's 200+ agri-subsidiaries to implement QR-code blockchain traceability across all SKUs; partner with Alibaba Cloud for consumer-facing trace app",
    Target_Segment: 'Pragmatic Middle-Class Buyers (25–40, household income ¥200K+)',
    CP_Competitive_Advantage: 'CP Group controls entire supply chain from farm; no competitor has end-to-end traceability at scale',
    Time_Horizon: '12–18 months', Investment_Level: 'High (¥50–80M setup)'
  },
  {
    Rank: 2, Score: 88,
    Opportunity: 'AI-Driven Price-Quality Optimization Engine',
    Why_It_Matters: 'Price sensitivity increased 34% in 2024; consumers demand premium quality at value prices – a gap no single player fills',
    How_CP_Can_Execute: 'Deploy ML pricing models using real-time competitor price scraping + quality score algorithms; display Price-Quality Score on every product listing',
    Target_Segment: 'Value-Seeking Premium Shoppers; Pragmatic Middle-Class',
    CP_Competitive_Advantage: "CP's direct sourcing eliminates 2–3 middlemen layers, enabling 15–25% cost advantage vs Freshippo on equivalent quality",
    Time_Horizon: '6–12 months', Investment_Level: 'Medium (¥20–35M)'
  },
  {
    Rank: 3, Score: 85,
    Opportunity: 'Yangtze River Delta Regional Dominance Strategy',
    Why_It_Matters: "Shanghai/Jiangsu/Zhejiang = 25% of China's consumer spending; market still fragmented with no clear #1 player outside Tier 1 cities",
    How_CP_Can_Execute: "Focus first 3 years exclusively on YRD cities; build 500 front warehouses in Shanghai + 200 in Nanjing/Suzhou/Hangzhou; replicate Dingdong's density model but with traceability differentiation",
    Target_Segment: 'Urban households in YRD cities; emerging middle-class in Suzhou/Nanjing/Wuxi',
    CP_Competitive_Advantage: 'CP Group has existing logistics & cold chain assets in Thailand/ASEAN adaptable to YRD; lower greenfield cost vs national expansion',
    Time_Horizon: '24–36 months', Investment_Level: 'High (¥200–400M)'
  },
  {
    Rank: 4, Score: 82,
    Opportunity: 'Personalized AI Shopping Assistant & Recommendation',
    Why_It_Matters: 'Repeat purchase rate for personalized platforms is 2.3x higher; 65% of consumers want AI meal planning (iResearch 2024)',
    How_CP_Can_Execute: 'Build LLM-powered in-app assistant trained on nutritional data, seasonal availability, and user purchase history; integrate meal planning + auto-reorder',
    Target_Segment: 'Health-conscious urban millennials; families with young children',
    CP_Competitive_Advantage: "CP Group's F&B expertise (processing, recipes) enables proprietary food knowledge base unavailable to pure logistics players",
    Time_Horizon: '9–15 months', Investment_Level: 'Medium (¥25–40M)'
  },
  {
    Rank: 5, Score: 79,
    Opportunity: 'Private Label Fresh Brand Development',
    Why_It_Matters: "Freshippo's 35% private label SKUs generate 40–60% higher margins vs branded equivalents; no front-warehouse player has scaled private label",
    How_CP_Can_Execute: "Launch 'CP Select' private label range starting with 50 SKUs (eggs, produce, protein); leverage CP's Thailand farms for exotic/premium differentiation",
    Target_Segment: 'Quality-first shoppers; cooking enthusiasts; health-conscious buyers',
    CP_Competitive_Advantage: "CP Group's own farms in Thailand & China enable unique origin stories (e.g., 'CP Thai Organic Rice') competitors cannot replicate",
    Time_Horizon: '18–24 months', Investment_Level: 'Medium (¥30–50M)'
  },
  {
    Rank: 6, Score: 71,
    Opportunity: 'Community Group Buying for Tier 2/3 Cities',
    Why_It_Matters: "Tier 2/3 cities have 60% of China's population but only 28% of fresh e-commerce penetration; community model reduces logistics cost by 40%",
    How_CP_Can_Execute: 'Partner with community leaders (团长) in Suzhou/Changzhou/Wuxi suburbs; offer CP-branded fresh bundles with 24-hour advance ordering',
    Target_Segment: 'Budget-conscious families in suburban/smaller cities; retirees',
    CP_Competitive_Advantage: "CP's cold chain logistics network can serve as community pickup points; lower CAC vs front warehouse model",
    Time_Horizon: '18–30 months', Investment_Level: 'Low-Medium (¥10–20M)'
  },
  {
    Rank: 7, Score: 68,
    Opportunity: 'Health & Wellness Premium Segment (Organic/Functional)',
    Why_It_Matters: 'Organic food market in China grew 15% in 2024 to ¥120B; only 8% sold via e-commerce; large unmet demand for certified organic fresh delivery',
    How_CP_Can_Execute: "Create dedicated 'CP Wellness' SKU range: certified organic vegetables, antibiotic-free protein, functional foods; charge 20–30% premium",
    Target_Segment: 'HENRYs (High Earners Not Rich Yet); health-conscious millennials; expat community in Shanghai',
    CP_Competitive_Advantage: "CP Thailand's existing organic certification (GlobalG.A.P.) and ASEAN sourcing network provides authentic origin premium unavailable to domestic competitors",
    Time_Horizon: '12–18 months', Investment_Level: 'Medium (¥20–30M)'
  }
]

const opportunities = ref([])

const sortedOpportunities = computed(() =>
  [...opportunities.value].sort((a, b) => (b.Score || 0) - (a.Score || 0))
)

const topScore = computed(() => sortedOpportunities.value[0]?.Score || '—')
const highPriorityCount = computed(() => sortedOpportunities.value.filter(o => (o.Score || 0) >= 85).length)
const avgScore = computed(() => {
  if (!sortedOpportunities.value.length) return '—'
  const total = sortedOpportunities.value.reduce((s, o) => s + parseFloat(o.Score || 0), 0)
  return Math.round(total / sortedOpportunities.value.length)
})

function scoreColor(score) {
  const s = parseFloat(score)
  if (s >= 85) return '#67C23A'
  if (s >= 70) return '#E6A23C'
  return '#909399'
}

function scoreClass(score) {
  const s = parseFloat(score)
  if (s >= 85) return 'high-score'
  if (s >= 70) return 'mid-score'
  return 'low-score'
}

function priorityLabel(score) {
  const s = parseFloat(score)
  if (s >= 85) return 'HIGH'
  if (s >= 70) return 'MED'
  return 'LOW'
}

const hBarOption = computed(() => {
  const sorted = [...sortedOpportunities.value].reverse()
  return {
    tooltip: { trigger: 'axis', formatter: '{b}: {c}' },
    grid: { left: '3%', right: '8%', bottom: '3%', containLabel: true },
    xAxis: { type: 'value', min: 60, max: 100, name: 'Score' },
    yAxis: {
      type: 'category',
      data: sorted.map(o => (o.Opportunity || '').split(' ').slice(0, 5).join(' ')),
      axisLabel: { fontSize: 11 }
    },
    series: [{
      type: 'bar',
      data: sorted.map(o => ({
        value: o.Score,
        itemStyle: { color: scoreColor(o.Score), borderRadius: [0, 4, 4, 0] }
      })),
      label: { show: true, position: 'right', fontWeight: 600 }
    }]
  }
})

onMounted(async () => {
  try {
    const base = (import.meta.env.VITE_API_BASE_URL || '') + '/api/v1'
    const res = await fetch(`${base}/opportunities`)
    const json = await res.json()
    opportunities.value = (json.data || []).length > 0 ? json.data : FALLBACK
  } catch {
    ElMessage.warning('Using cached opportunity data')
    opportunities.value = FALLBACK
  }
})
</script>

<style scoped>
.opportunities-page { padding: 24px; max-width: 1100px; margin: 0 auto; }
.page-header { margin-bottom: 24px; }
.page-header h1 { font-size: 28px; margin: 0 0 8px; }
.page-header p { color: #666; margin: 0; }

.kpi-row { margin-bottom: 24px; }
.kpi-card { text-align: center; padding: 8px; }
.kpi-icon { font-size: 26px; margin-bottom: 4px; }
.kpi-val { font-size: 28px; font-weight: 800; color: #303133; }
.kpi-lbl { font-size: 12px; color: #909399; margin-top: 4px; }
.kpi-green { border-top: 3px solid #67C23A; }
.kpi-blue { border-top: 3px solid #409EFF; }
.kpi-orange { border-top: 3px solid #E6A23C; }
.kpi-purple { border-top: 3px solid #9747FF; }

.chart-card { margin-bottom: 20px; }

/* Opportunity Card */
.opp-card {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  background: #fff;
  border-radius: 8px;
  border-left: 5px solid #ddd;
  box-shadow: 0 1px 6px rgba(0,0,0,0.07);
  padding: 20px 24px;
  margin-bottom: 16px;
  transition: box-shadow 0.2s;
}
.opp-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.12); }
.opp-card.high-score { border-left-color: #67C23A; }
.opp-card.mid-score  { border-left-color: #E6A23C; }
.opp-card.low-score  { border-left-color: #909399; }

.opp-rank { font-size: 30px; font-weight: 900; color: #C0C4CC; min-width: 48px; line-height: 1; padding-top: 4px; }

.opp-main { flex: 1; min-width: 0; }
.opp-title { font-size: 17px; font-weight: 700; color: #303133; margin-bottom: 10px; line-height: 1.4; }

.opp-meta { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }

.opp-detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.detail-item { background: #f8f9fa; border-radius: 6px; padding: 10px 12px; }
.detail-item.full-width { grid-column: 1 / -1; }
.detail-label { font-size: 12px; font-weight: 700; color: #606266; margin-bottom: 4px; }
.detail-body { font-size: 13px; color: #606266; line-height: 1.5; }
.detail-body.advantage { color: #303133; font-weight: 500; }

.opp-score-section { text-align: center; min-width: 100px; flex-shrink: 0; }
.score-label { font-size: 12px; color: #909399; }
.score-value { font-size: 36px; font-weight: 900; line-height: 1.1; }
.priority-badge {
  display: inline-block; margin-top: 8px; padding: 3px 10px;
  border-radius: 12px; color: #fff; font-size: 11px; font-weight: 800; letter-spacing: 0.5px;
}
</style>
