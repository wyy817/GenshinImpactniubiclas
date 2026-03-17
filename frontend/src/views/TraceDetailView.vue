<template>
  <div class="trace-detail-view">
    <el-button text type="primary" @click="$router.back()" style="margin-bottom:16px">
      <el-icon><ArrowLeft /></el-icon>
      Back to Traceability
    </el-button>

    <div v-if="loading">
      <el-skeleton :rows="8" animated />
    </div>

    <div v-else>
      <!-- Header -->
      <div class="detail-header">
        <div class="product-badge">
          <el-icon :size="48" color="#67c23a"><Goods /></el-icon>
        </div>
        <div>
          <h1 class="page-title">{{ productName }}</h1>
          <p class="page-subtitle" style="margin-bottom:0">
            Product ID: <strong>{{ productId }}</strong> &nbsp;·&nbsp;
            <el-tag type="success" round>{{ traceNodes.length }} Trace Steps</el-tag>
          </p>
        </div>
      </div>

      <el-empty
        v-if="!traceNodes.length"
        description="No traceability data available for this product"
      />

      <div v-else>
        <!-- Transport Route Map -->
        <el-card shadow="never" class="map-card">
          <template #header>
            <div class="map-header">
              <el-icon color="#409eff" :size="18"><Position /></el-icon>
              <span style="font-weight:700;font-size:16px">Transport Route Map</span>
              <el-tag type="info" size="small" style="margin-left:auto">
                Interactive · {{ mappableNodes.length }} stops mapped
              </el-tag>
            </div>
          </template>

          <div v-if="mapLoadError" class="map-fallback">
            <el-icon :size="36" color="#c0c4cc"><Location /></el-icon>
            <p style="color:#909399;margin:8px 0 4px">Map unavailable (offline mode)</p>
            <p style="color:#c0c4cc;font-size:12px">Route: {{ routeTextSummary }}</p>
          </div>
          <div v-else ref="mapRef" class="route-map"></div>

          <div class="map-legend">
            <span class="legend-item"><span class="dot dot-start"></span>Origin</span>
            <span class="legend-item"><span class="dot dot-mid"></span>Transit Point</span>
            <span class="legend-item"><span class="dot dot-end"></span>Destination</span>
            <span class="legend-route">— Cold Chain Route</span>
          </div>
        </el-card>

        <el-row :gutter="24">
          <!-- Timeline -->
          <el-col :xs="24" :md="15">
            <el-card shadow="never" style="border-radius:14px">
              <template #header>
                <span style="font-weight:700;font-size:16px">
                  <el-icon><LocationFilled /></el-icon>
                  Supply Chain Journey
                </span>
              </template>

              <el-timeline>
                <el-timeline-item
                  v-for="(node, index) in sortedNodes"
                  :key="index"
                  :timestamp="formatDate(node.Date || node.date)"
                  :color="timelineColor(index, sortedNodes.length)"
                  placement="top"
                  size="large"
                >
                  <el-card class="timeline-card" shadow="hover">
                    <!-- Node header -->
                    <div class="node-header">
                      <div style="display:flex;align-items:center;gap:8px">
                        <span class="stage-icon">{{ stageIcon(node.Stage || node.stage) }}</span>
                        <strong class="node-stage">{{ node.Stage || node.stage || `Step ${index + 1}` }}</strong>
                      </div>
                      <el-tag :type="stepTagType(index, sortedNodes.length)" size="small">
                        Step {{ node.Step_Order || node.step_order || index + 1 }}
                      </el-tag>
                    </div>

                    <!-- Location -->
                    <div class="node-location" v-if="node.Location || node.location">
                      <el-icon size="13"><LocationFilled /></el-icon>
                      {{ node.Location || node.location }}
                    </div>

                    <!-- Description -->
                    <p class="node-desc">
                      {{ node.Description || node.description || getDefaultDesc(node.Stage || node.stage) }}
                    </p>

                    <!-- Meta chips -->
                    <div class="node-meta" v-if="(node.Temperature || node.temperature) || (node.Duration || node.duration) || (node.Vehicle || node.vehicle)">
                      <span v-if="node.Temperature || node.temperature" class="meta-chip temp">
                        🌡️ {{ node.Temperature || node.temperature }}
                      </span>
                      <span v-if="node.Duration || node.duration" class="meta-chip duration">
                        ⏱️ {{ node.Duration || node.duration }}
                      </span>
                      <span v-if="node.Vehicle || node.vehicle" class="meta-chip vehicle">
                        🚛 {{ node.Vehicle || node.vehicle }}
                      </span>
                    </div>

                    <!-- Certifications -->
                    <div class="node-certs" v-if="getCerts(node)">
                      <el-tag
                        v-for="cert in getCerts(node).split(',')"
                        :key="cert"
                        type="success"
                        size="small"
                        round
                        style="margin:2px"
                      >✓ {{ cert.trim() }}</el-tag>
                    </div>
                  </el-card>
                </el-timeline-item>
              </el-timeline>
            </el-card>
          </el-col>

          <!-- Right Panel -->
          <el-col :xs="24" :md="9">
            <!-- Journey Summary -->
            <el-card shadow="never" style="border-radius:14px;margin-bottom:16px">
              <template #header>
                <span style="font-weight:700;font-size:16px">Journey Summary</span>
              </template>
              <div class="summary-row" v-for="item in summaryItems" :key="item.label">
                <span class="summary-label">{{ item.label }}</span>
                <span class="summary-value">{{ item.value }}</span>
              </div>
            </el-card>

            <!-- Cold Chain Stats -->
            <el-card shadow="never" style="border-radius:14px;margin-bottom:16px">
              <template #header>
                <span style="font-weight:700;font-size:16px">❄️ Cold Chain Stats</span>
              </template>
              <div class="stat-grid">
                <div class="stat-item">
                  <div class="stat-num">{{ coldChainSteps }}</div>
                  <div class="stat-label">Cold Steps</div>
                </div>
                <div class="stat-item">
                  <div class="stat-num">{{ journeyDays }}</div>
                  <div class="stat-label">Journey Days</div>
                </div>
                <div class="stat-item">
                  <div class="stat-num">{{ allCertifications.length }}</div>
                  <div class="stat-label">Certifications</div>
                </div>
              </div>
            </el-card>

            <!-- All Certifications -->
            <el-card shadow="never" style="border-radius:14px">
              <template #header>
                <span style="font-weight:700;font-size:16px">Certifications</span>
              </template>
              <div v-if="allCertifications.length">
                <el-tag
                  v-for="cert in allCertifications"
                  :key="cert"
                  type="success"
                  round
                  style="margin:4px"
                >✓ {{ cert }}</el-tag>
              </div>
              <el-empty v-else description="No certifications recorded" :image-size="60" />
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft, LocationFilled, Goods, Position, Location } from '@element-plus/icons-vue'
import api from '../api/index.js'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
// Fix default marker icon paths broken by Vite bundling
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({ iconUrl: markerIcon, iconRetinaUrl: markerIcon2x, shadowUrl: markerShadow })

const route = useRoute()
const productId = computed(() => route.params.productId)
const loading = ref(true)
const traceNodes = ref([])
const productName = ref('')
const mapRef = ref(null)
const mapLoadError = ref(false)
let leafletMap = null

// ─── Sorting ───────────────────────────────────────────────────────────────
const sortedNodes = computed(() =>
  [...traceNodes.value].sort((a, b) => {
    const ao = Number(a.Step_Order || a.step_order || 0)
    const bo = Number(b.Step_Order || b.step_order || 0)
    return ao - bo
  })
)

// ─── Stage Icons ────────────────────────────────────────────────────────────
function stageIcon(stage) {
  if (!stage) return '📍'
  const s = stage.toLowerCase()
  if (s.includes('farm') || s.includes('origin')) return '🌱'
  if (s.includes('harvest') || s.includes('grading')) return '🌾'
  if (s.includes('pre-cool') || s.includes('cooling') || s.includes('refriger')) return '❄️'
  if (s.includes('transit') || s.includes('transport')) return '🚛'
  if (s.includes('cold chain')) return '🚛'
  if (s.includes('distribution') || s.includes('warehouse')) return '🏭'
  if (s.includes('quality') || s.includes('inspection') || s.includes('qc')) return '🔍'
  if (s.includes('packaging') || s.includes('pack')) return '📦'
  if (s.includes('import') || s.includes('customs') || s.includes('port')) return '🛳️'
  if (s.includes('processing') || s.includes('slaughter')) return '⚙️'
  if (s.includes('delivery') || s.includes('last mile')) return '🏠'
  if (s.includes('retail') || s.includes('store')) return '🏪'
  if (s.includes('slaughter') || s.includes('abattoir')) return '🥩'
  return '📍'
}

// ─── Default Descriptions ───────────────────────────────────────────────────
function getDefaultDesc(stage) {
  if (!stage) return 'Quality-controlled processing at this stage of the supply chain.'
  const s = stage.toLowerCase()
  if (s.includes('farm') || s.includes('origin'))
    return 'Grown under organic certification standards with full field-level traceability. Soil health and pesticide-free practices verified by third-party auditors.'
  if (s.includes('harvest') || s.includes('grading'))
    return 'Hand-harvested and graded by trained staff. Only produce meeting CP\'s premium quality specifications (size, colour, Brix level) is selected for onward shipment.'
  if (s.includes('pre-cool') || s.includes('cooling'))
    return 'Field heat removed within 2 hours of harvest using forced-air pre-cooling tunnels. Core temperature reduced to ≤4 °C to extend shelf life and maintain nutritional quality.'
  if (s.includes('cold chain') || s.includes('transit') || s.includes('transport'))
    return 'GPS-tracked refrigerated vehicle maintains 0–4 °C throughout transit. Real-time temperature logs uploaded every 15 minutes to CP\'s traceability platform.'
  if (s.includes('distribution') || s.includes('warehouse'))
    return 'Received at CP\'s temperature-controlled regional distribution centre. Lot-level scanning, FIFO rotation, and same-day dispatch to fulfilment hubs.'
  if (s.includes('quality') || s.includes('inspection') || s.includes('qc'))
    return 'Multi-point quality inspection: microbiological sampling, sensory evaluation, weight verification, and cold-chain log review before clearance for consumer sale.'
  if (s.includes('packaging') || s.includes('pack'))
    return 'Packed in modified-atmosphere, recyclable trays. Each unit bears a unique QR code linking to the full traceability record visible to consumers via CP app.'
  if (s.includes('import') || s.includes('customs') || s.includes('port'))
    return 'GACC-registered facility inspection, veterinary health certificate verification, and customs clearance at designated port of entry. All import permits archived.'
  if (s.includes('processing') || s.includes('slaughter'))
    return 'Processed at HACCP-certified abattoir. Carcass identification maintained from lairage through to primal cuts, with each lot assigned a traceable batch code.'
  if (s.includes('delivery') || s.includes('last mile'))
    return 'Same-day cold-chain delivery to consumer door. Temperature maintained via insulated packaging and ice gel packs. Delivery confirmation photo uploaded to order record.'
  return 'Rigorous standards applied at this stage to ensure product safety, quality, and full supply chain transparency in line with CP Group protocols.'
}

// ─── Certifications ─────────────────────────────────────────────────────────
function getCerts(node) {
  return node.Certifications || node.certifications || ''
}

const allCertifications = computed(() => {
  const set = new Set()
  traceNodes.value.forEach(n => {
    const c = getCerts(n)
    if (c) c.split(',').forEach(x => set.add(x.trim()))
  })
  return Array.from(set).filter(Boolean)
})

// ─── Timeline Colours ───────────────────────────────────────────────────────
const PALETTE = ['#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#9c27b0', '#17a2b8']
function timelineColor(i) { return PALETTE[i % PALETTE.length] }
function stepTagType(i, total) {
  if (i === 0) return 'success'
  if (i === total - 1) return 'danger'
  return 'warning'
}

// ─── Date Formatter ──────────────────────────────────────────────────────────
function formatDate(val) {
  if (!val) return '—'
  if (typeof val === 'string') return val
  try {
    return new Date(val).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
  } catch { return String(val) }
}

// ─── Summary ─────────────────────────────────────────────────────────────────
const coldChainSteps = computed(() =>
  sortedNodes.value.filter(n => {
    const s = (n.Stage || n.stage || '').toLowerCase()
    return s.includes('cool') || s.includes('cold') || s.includes('refriger') || s.includes('transit')
  }).length
)

const journeyDays = computed(() => {
  const dates = sortedNodes.value
    .map(n => {
      const v = n.Date || n.date
      if (!v) return null
      const d = typeof v === 'string' ? new Date(v) : v
      return isNaN(d) ? null : d.getTime()
    })
    .filter(Boolean)
  if (dates.length < 2) return '—'
  const diff = Math.round((Math.max(...dates) - Math.min(...dates)) / 86400000)
  return diff === 0 ? '< 1' : diff
})

const summaryItems = computed(() => [
  { label: 'Product ID',  value: productId.value },
  { label: 'Total Steps', value: sortedNodes.value.length },
  { label: 'Origin',      value: sortedNodes.value[0]?.Location || sortedNodes.value[0]?.location || '—' },
  { label: 'Destination', value: sortedNodes.value[sortedNodes.value.length - 1]?.Location || sortedNodes.value[sortedNodes.value.length - 1]?.location || '—' },
  { label: 'Final Stage', value: sortedNodes.value[sortedNodes.value.length - 1]?.Stage || '—' },
  { label: 'Journey Days', value: journeyDays.value },
])

// ─── Map: coordinate lookup ──────────────────────────────────────────────────
const LOCATION_COORDS = {
  // Shandong
  'shouguang': [36.88, 118.74],
  'weifang': [36.70, 119.10],
  'shandong': [36.67, 117.00],
  'qingdao': [36.07, 120.38],
  'jinan': [36.65, 117.12],
  // North China
  'tianjin': [39.13, 117.20],
  'beijing': [39.90, 116.41],
  'hebei': [38.04, 114.51],
  // East China / Shanghai
  'shanghai': [31.23, 121.47],
  'pudong': [31.22, 121.54],
  'baoshan': [31.40, 121.49],
  'waigaoqiao': [31.36, 121.56],
  'yangshan': [30.63, 122.07],
  // South China
  'guangzhou': [23.13, 113.26],
  'shenzhen': [22.54, 114.06],
  'dongguan': [23.04, 113.75],
  // Southwest
  'chengdu': [30.57, 104.07],
  'chongqing': [29.56, 106.55],
  // Australia
  'australia': [-33.87, 151.21],
  'sydney': [-33.87, 151.21],
  'melbourne': [-37.81, 144.96],
  'brisbane': [-27.47, 153.02],
  'victoria': [-37.81, 144.96],
  'queensland': [-27.47, 153.02],
  'new south wales': [-33.87, 151.21],
  'perth': [-31.95, 115.86],
  'adelaide': [-34.93, 138.60],
  // Japan
  'japan': [34.69, 135.50],
  'tokyo': [35.68, 139.69],
  'osaka': [34.69, 135.50],
  'kyoto': [35.01, 135.77],
  'miyazaki': [31.91, 131.42],
  'kagoshima': [31.60, 130.56],
  'hokkaido': [43.06, 141.35],
  'kyushu': [32.80, 131.00],
  'nagoya': [35.18, 136.91],
  // Other Asia / Oceania
  'new zealand': [-41.29, 174.78],
  'auckland': [-36.87, 174.76],
  'christchurch': [-43.53, 172.62],
  'thailand': [13.75, 100.52],
  'bangkok': [13.75, 100.52],
  'vietnam': [21.03, 105.83],
  'hanoi': [21.03, 105.83],
  'singapore': [1.35, 103.82],
  // Northeast China
  'jilin': [43.84, 126.55],
  'changchun': [43.84, 125.32],
  'liaoning': [41.83, 123.43],
  'shenyang': [41.83, 123.43],
  'dandong': [40.12, 124.39],
  // Central / Southwest China
  'yunnan': [25.07, 102.68],
  'kunming': [25.07, 102.68],
  'guizhou': [26.60, 106.71],
  'guiyang': [26.60, 106.71],
  'henan': [34.75, 113.65],
  'zhengzhou': [34.75, 113.65],
  // South China (additional)
  'hainan': [20.02, 110.34],
  'haikou': [20.02, 110.34],
  'zhanjiang': [21.27, 110.35],
  'guangxi': [22.82, 108.33],
  'nanning': [22.82, 108.33],
  // Northeast / Northwest China
  'heilongjiang': [45.74, 126.66],
  'harbin': [45.74, 126.66],
  'inner mongolia': [40.82, 111.76],
  'hohhot': [40.82, 111.76],
  // Japan (additional)
  'yamanashi': [35.66, 138.57],
  'sapporo': [43.06, 141.35],
  'fukuoka': [33.60, 130.40],
  'sendai': [38.27, 140.87],
  // Norway
  'norway': [59.91, 10.75],
  'oslo': [59.91, 10.75],
  'bergen': [60.39, 5.32],
}

function getCoords(location) {
  if (!location) return null
  const loc = location.toLowerCase()
  let best = null, bestLen = 0
  for (const [key, coords] of Object.entries(LOCATION_COORDS)) {
    if (loc.includes(key) && key.length > bestLen) {
      best = coords; bestLen = key.length
    }
  }
  return best
}

const mappableNodes = computed(() =>
  sortedNodes.value
    .map(n => ({ ...n, coords: getCoords(n.Location || n.location) }))
    .filter(n => n.coords)
)

const routeTextSummary = computed(() =>
  sortedNodes.value.map(n => n.Location || n.location || n.Stage || n.stage).filter(Boolean).join(' → ')
)

// ─── Leaflet Map Init ────────────────────────────────────────────────────────
async function initMap() {
  if (!mapRef.value || mappableNodes.value.length === 0) {
    mapLoadError.value = true
    return
  }
  try {
    const nodes = mappableNodes.value

    if (leafletMap) { leafletMap.remove(); leafletMap = null }

    leafletMap = L.map(mapRef.value, { zoomControl: true, scrollWheelZoom: false })

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 18,
    }).addTo(leafletMap)

    const coords = nodes.map(n => n.coords)

    // Dashed polyline for route
    L.polyline(coords, { color: '#409eff', weight: 3, dashArray: '10 7', opacity: 0.85 }).addTo(leafletMap)

    // Markers
    nodes.forEach((node, i) => {
      const isFirst = i === 0
      const isLast  = i === nodes.length - 1
      const bg = isFirst ? '#67c23a' : isLast ? '#f56c6c' : '#e6a23c'
      const size = isFirst || isLast ? 20 : 14

      const icon = L.divIcon({
        html: `<div style="background:${bg};width:${size}px;height:${size}px;border-radius:50%;border:3px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,0.3);"></div>`,
        iconSize: [size + 6, size + 6],
        iconAnchor: [(size + 6) / 2, (size + 6) / 2],
        className: '',
      })

      const stage  = node.Stage  || node.stage  || `Step ${i + 1}`
      const loc    = node.Location || node.location || ''
      const date   = formatDate(node.Date || node.date)
      const desc   = node.Description || node.description || ''
      const certs  = getCerts(node)

      L.marker(node.coords, { icon })
        .addTo(leafletMap)
        .bindPopup(`
          <div style="min-width:180px;font-size:13px;line-height:1.6">
            <div style="font-weight:700;font-size:14px;margin-bottom:4px">
              ${stageIcon(stage)} Step ${node.Step_Order || node.step_order || i + 1}: ${stage}
            </div>
            <div style="color:#666;margin-bottom:3px">📍 ${loc}</div>
            <div style="color:#999;font-size:12px;margin-bottom:${desc ? '6px' : '0'}">📅 ${date}</div>
            ${desc ? `<div style="color:#444;font-size:12px;border-top:1px solid #eee;padding-top:5px">${desc}</div>` : ''}
            ${certs ? `<div style="margin-top:5px;font-size:11px;color:#67c23a">✓ ${certs}</div>` : ''}
          </div>
        `, { maxWidth: 260 })
    })

    // Fit bounds with padding
    leafletMap.fitBounds(L.latLngBounds(coords), { padding: [40, 40] })

  } catch (err) {
    console.warn('[TraceMap] Failed to load:', err.message)
    mapLoadError.value = true
  }
}

// ─── Lifecycle ────────────────────────────────────────────────────────────────
onMounted(async () => {
  try {
    const data = await api.get(`/products/${productId.value}/traceability`)
    traceNodes.value = Array.isArray(data) ? data : []

    const products = await api.get('/products')
    if (Array.isArray(products)) {
      const found = products.find(p =>
        (p.Product_ID || p.product_id || '').toString().trim().toUpperCase() ===
        productId.value.toString().trim().toUpperCase()
      )
      productName.value = found
        ? (found.Product_Name || found.product_name || productId.value)
        : productId.value
    }
  } finally {
    loading.value = false
    await nextTick()
    await initMap()
  }
})

onUnmounted(() => {
  if (leafletMap) { leafletMap.remove(); leafletMap = null }
})
</script>

<style scoped>
.trace-detail-view {
  padding-bottom: 40px;
}

/* ── Header ── */
.detail-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
  padding: 24px;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

.product-badge {
  background: #f0f9eb;
  width: 80px;
  height: 80px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* ── Map Card ── */
.map-card {
  border-radius: 14px;
  margin-bottom: 20px;
}

.map-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.route-map {
  height: 320px;
  border-radius: 10px;
  overflow: hidden;
  background: #f5f7fa;
}

.map-fallback {
  height: 180px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: #f5f7fa;
}

.map-legend {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 10px;
  flex-wrap: wrap;
  font-size: 12px;
  color: #606266;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}
.dot-start  { background: #67c23a; }
.dot-mid    { background: #e6a23c; }
.dot-end    { background: #f56c6c; }
.legend-route {
  color: #409eff;
  font-weight: 500;
  letter-spacing: .5px;
}

/* ── Timeline Cards ── */
.timeline-card {
  border-radius: 10px;
  margin-bottom: 4px;
}

.node-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}

.stage-icon {
  font-size: 18px;
  line-height: 1;
}

.node-stage {
  font-size: 15px;
  color: #1a1a2e;
}

.node-location {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #909399;
  margin-bottom: 6px;
}

.node-desc {
  font-size: 13px;
  color: #606266;
  line-height: 1.65;
  margin-bottom: 8px;
}

.node-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 8px;
}

.meta-chip {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 20px;
  font-weight: 500;
}

.meta-chip.temp     { background: #ecf5ff; color: #409eff; }
.meta-chip.duration { background: #fdf6ec; color: #e6a23c; }
.meta-chip.vehicle  { background: #f0f9eb; color: #67c23a; }

.node-certs {
  margin-top: 4px;
}

/* ── Summary / Stats ── */
.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 10px 0;
  border-bottom: 1px solid #f5f5f5;
  font-size: 13px;
  gap: 12px;
}
.summary-row:last-child { border-bottom: none; }

.summary-label {
  color: #909399;
  flex-shrink: 0;
}
.summary-value {
  font-weight: 600;
  color: #303133;
  text-align: right;
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  text-align: center;
}

.stat-item {
  padding: 12px 8px;
  background: #f5f7fa;
  border-radius: 10px;
}

.stat-num {
  font-size: 26px;
  font-weight: 700;
  color: #409eff;
  line-height: 1.2;
}

.stat-label {
  font-size: 11px;
  color: #909399;
  margin-top: 4px;
}
</style>
