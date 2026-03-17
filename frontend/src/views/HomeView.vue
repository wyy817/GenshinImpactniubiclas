<template>
  <div class="home-view">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <div class="hero-badge">
          <el-tag type="success" size="large" round>Fresh Food E-Commerce Platform</el-tag>
        </div>
        <h1 class="hero-title">CP Group Fresh Food Platform</h1>
        <p class="hero-subtitle">
          Entering China's ¥736.8B fresh food e-commerce market with a differentiated
          farm-to-table supply chain, powered by CP Group's vertically integrated agriculture
          and logistics network.
        </p>
        <div class="hero-actions">
          <el-button type="primary" size="large" @click="$router.push('/products')" round>
            <el-icon><ShoppingCart /></el-icon>
            Browse Products
          </el-button>
          <el-button type="default" size="large" @click="$router.push('/login')" round>
            <el-icon><DataAnalysis /></el-icon>
            View Dashboard
          </el-button>
        </div>
      </div>
      <div class="hero-visual">
        <div class="hero-icon-grid">
          <div class="icon-cell" v-for="item in heroIcons" :key="item.label">
            <el-icon :size="36" :color="item.color"><component :is="item.icon" /></el-icon>
            <span>{{ item.label }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Market Stats -->
    <section class="stats-section">
      <h2 class="section-heading">Market Opportunity</h2>
      <div class="stats-grid">
        <el-card
          v-for="stat in marketStats"
          :key="stat.label"
          class="stat-card"
          shadow="hover"
        >
          <div class="stat-icon" :style="{ background: stat.bg }">
            <el-icon :size="28" color="#fff"><component :is="stat.icon" /></el-icon>
          </div>
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
          <div class="stat-note">{{ stat.note }}</div>
        </el-card>
      </div>
    </section>

    <!-- Features -->
    <section class="features-section">
      <h2 class="section-heading">Platform Capabilities</h2>
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="8" v-for="feat in features" :key="feat.title">
          <el-card class="feature-card" shadow="hover">
            <div class="feature-header">
              <el-icon :size="24" :color="feat.color"><component :is="feat.icon" /></el-icon>
              <strong>{{ feat.title }}</strong>
            </div>
            <p>{{ feat.desc }}</p>
            <el-button text type="primary" @click="$router.push(feat.link)">
              Explore →
            </el-button>
          </el-card>
        </el-col>
      </el-row>
    </section>
  </div>
</template>

<script setup>
import {
  ShoppingCart, DataAnalysis, TrendCharts, LocationFilled,
  Trophy, Promotion, User, Goods, PieChart
} from '@element-plus/icons-vue'

const heroIcons = [
  { icon: 'Goods', label: 'Fresh Products', color: '#67c23a' },
  { icon: 'LocationFilled', label: 'Traceability', color: '#409eff' },
  { icon: 'TrendCharts', label: 'Market Data', color: '#e6a23c' },
  { icon: 'Trophy', label: 'Competitive Edge', color: '#f56c6c' },
  { icon: 'User', label: 'Consumer Insights', color: '#909399' },
  { icon: 'Promotion', label: 'Opportunities', color: '#7c3aed' },
]

const marketStats = [
  {
    value: '¥736.8B',
    label: 'Market Size (2026E)',
    note: 'China fresh food e-commerce TAM',
    icon: 'PieChart',
    bg: 'linear-gradient(135deg,#409eff,#0066cc)',
  },
  {
    value: '22% CAGR',
    label: 'Annual Growth Rate',
    note: '2022-2026 projected growth',
    icon: 'TrendCharts',
    bg: 'linear-gradient(135deg,#67c23a,#3a8e00)',
  },
  {
    value: '2026',
    label: 'CP Market Entry',
    note: 'Strategic platform launch year',
    icon: 'Promotion',
    bg: 'linear-gradient(135deg,#e6a23c,#b57600)',
  },
  {
    value: '2',
    label: 'Key Competitors',
    note: 'Dingdong Maicai & Freshippo',
    icon: 'Trophy',
    bg: 'linear-gradient(135deg,#f56c6c,#c0392b)',
  },
]

const features = [
  {
    title: 'Product Catalogue',
    desc: 'Browse CP Group\'s curated selection of fresh produce, protein, and premium food products with real-time stock status.',
    icon: 'ShoppingCart',
    color: '#409eff',
    link: '/products',
  },
  {
    title: 'Supply Chain Traceability',
    desc: 'Track every product from farm origin through processing, cold chain, and delivery. Full transparency for consumers.',
    icon: 'LocationFilled',
    color: '#67c23a',
    link: '/traceability',
  },
  {
    title: 'Competitor Analysis',
    desc: 'Detailed benchmarking against Dingdong Maicai and Freshippo across revenue, GMV, MAU, and operational metrics.',
    icon: 'DataAnalysis',
    color: '#e6a23c',
    link: '/login',
  },
  {
    title: 'Market Growth',
    desc: 'Historical and forecast market size data showing China\'s fresh food e-commerce trajectory through 2026 and beyond.',
    icon: 'TrendCharts',
    color: '#9c27b0',
    link: '/login',
  },
  {
    title: 'Strategic Opportunities',
    desc: 'Ranked strategic opportunities scored by market impact and feasibility for CP Group\'s market entry strategy.',
    icon: 'Trophy',
    color: '#f56c6c',
    link: '/login',
  },
  {
    title: 'Consumer Personas',
    desc: 'Detailed profiles of target customer segments — urban professionals, health-conscious families, and premium buyers.',
    icon: 'User',
    color: '#17a2b8',
    link: '/login',
  },
]
</script>

<style scoped>
.home-view {
  padding-bottom: 48px;
}

/* Hero */
.hero {
  display: flex;
  align-items: center;
  gap: 48px;
  padding: 56px 0 48px;
  border-bottom: 1px solid #ebeef5;
  margin-bottom: 40px;
}

.hero-content {
  flex: 1;
}

.hero-badge {
  margin-bottom: 16px;
}

.hero-title {
  font-size: 42px;
  font-weight: 800;
  color: #1a1a2e;
  line-height: 1.2;
  margin-bottom: 16px;
}

.hero-subtitle {
  font-size: 17px;
  color: #606266;
  line-height: 1.7;
  margin-bottom: 32px;
  max-width: 560px;
}

.hero-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.hero-visual {
  flex: 0 0 300px;
}

.hero-icon-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.icon-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  background: #fff;
  border-radius: 12px;
  padding: 20px 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  font-size: 12px;
  color: #606266;
  text-align: center;
  transition: transform 0.2s;
}

.icon-cell:hover {
  transform: translateY(-3px);
}

/* Stats */
.section-heading {
  font-size: 22px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 24px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  text-align: center;
  padding: 8px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
}

.stat-value {
  font-size: 28px;
  font-weight: 800;
  color: #1a1a2e;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.stat-note {
  font-size: 12px;
  color: #909399;
}

/* Features */
.features-section {
  margin-top: 40px;
}

.feature-card {
  margin-bottom: 20px;
  height: calc(100% - 20px);
}

.feature-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
  font-size: 16px;
}

.feature-card p {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  margin-bottom: 12px;
}

@media (max-width: 768px) {
  .hero {
    flex-direction: column;
    padding: 32px 0;
  }
  .hero-visual {
    flex: none;
    width: 100%;
  }
  .hero-title {
    font-size: 28px;
  }
}
</style>
