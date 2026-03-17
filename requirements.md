# CP Group 鲜食电商平台 软件需求规格说明书（SRS）

**项目名称**：CP Group 中国鲜食电商战略平台
**文档版本**：v1.1
**编写日期**：2026-03-17
**文档状态**：草稿
**技术栈**：Vue 3 + Spring Boot 3.x

---

## 版本记录

| 版本   | 日期       | 修改人   | 修改内容                                                         |
|--------|------------|----------|------------------------------------------------------------------|
| v0.1   | 2026-03-17 | CP Group | 初稿                                                             |
| v1.0   | 2026-03-17 | CP Group | 结构完善，基线版本                                               |
| v1.1   | 2026-03-17 | CP Group | 竞争对手精简为叮咚与盒马；App 改为纯英文；B2B 改称 Dashboard；数据对齐 Master 数据表 |

---

## 目录

1. [项目概述](#一项目概述)
2. [技术架构](#二技术架构)
3. [系统整体结构](#三系统整体结构)
4. [功能需求详述](#四功能需求详述)
   - 4.1 [首页（Home）](#41-首页-home)
   - 4.2 [竞争对手分析（Competitors）](#42-竞争对手分析-competitors)
   - 4.3 [市场机会（Opportunities）](#43-市场机会-opportunities)
   - 4.4 [产品目录（Product Catalog）](#44-产品目录-product-catalog)
   - 4.5 [溯源追踪（Traceability）](#45-溯源追踪-traceability)
   - 4.6 [市场增长趋势（Market Growth Trend）](#46-市场增长趋势-market-growth-trend)
   - 4.7 [用户画像（Personas）](#47-用户画像-personas)
5. [接口规范（API Contract）](#五接口规范api-contract)
6. [数据库设计](#六数据库设计)
7. [权限与角色设计](#七权限与角色设计)
8. [非功能需求](#八非功能需求)
9. [部署与环境要求](#九部署与环境要求)
10. [附录](#十附录)

---

## 一、项目概述

### 1.1 项目背景

CP Group（正大集团）是泰国领先的农业与食品企业集团，在全球多个市场拥有成熟的供应链体系。随着中国生鲜电商市场的快速扩张（2024 年市场规模约 7,368 亿元，CAGR 约 22%），CP Group 拟通过本平台切入中国线上生鲜零售赛道，以其核心优势（冷链物流、品类丰富、品质可溯）与叮咚买菜、盒马鲜生等头部平台差异化竞争。

### 1.2 平台定位

本平台采用 **Dashboard + Consumer App 双轨并行** 策略：

- **Dashboard（战略智能看板）**：面向 CP Group 内部决策层及战略团队，提供竞争格局分析、市场机会识别、用户画像洞察、市场增长趋势等数据支撑，辅助市场进入决策。
- **Consumer App（消费者应用）**：面向中国生鲜电商终端用户，提供产品浏览及全链路溯源查询功能，建立用户信任与品牌认知。**App 全程仅以英文显示。**

### 1.3 目标用户

| 用户类型     | 描述                                              |
|--------------|---------------------------------------------------|
| 战略分析师   | CP Group 内部，使用 Dashboard 做市场研究          |
| 高管决策层   | CP Group 管理层，查看市场概览与关键指标           |
| 终端消费者   | 使用英文界面浏览产品与溯源信息                    |
| 系统管理员   | 维护平台数据、用户权限及内容更新                  |

### 1.4 项目范围

**本期包含（In Scope）：**
- 首页导航与平台入口（英文）
- 竞争对手分析看板（Dashboard）
- 市场机会识别模块（Dashboard）
- 产品目录展示与筛选（Consumer App，英文）
- 产品溯源追踪查询（Consumer App，英文）
- 市场增长趋势可视化（Dashboard）
- 用户画像展示模块（Dashboard）
- 管理后台（数据维护）
- JWT 认证与角色权限控制

**本期不包含（Out of Scope）：**
- 在线支付与订单系统（二期）
- 多语言切换（App 固定英文，二期可扩展）
- 第三方 ERP/WMS 系统集成（二期）

---

## 二、技术架构

### 2.1 技术选型

| 层级         | 技术选型                       | 说明                         |
|--------------|--------------------------------|------------------------------|
| 前端框架     | Vue 3.4 + Vite 5               | Composition API，性能优先    |
| UI 组件库    | Element Plus 2.x               | 企业级组件，按需引入         |
| 图表库       | ECharts 5 + vue-echarts        | 折线图、柱状图、雷达图等     |
| 状态管理     | Pinia 2                        | 替代 Vuex，轻量易用          |
| 路由         | Vue Router 4                   | History 模式                 |
| HTTP 客户端  | Axios                          | 统一请求封装，拦截器处理     |
| 后端框架     | Spring Boot 3.2                | RESTful API，模块化设计      |
| ORM          | MyBatis-Plus 3.5               | 简化 CRUD，支持分页          |
| 数据库       | MySQL 8.0                      | 主数据库                     |
| 缓存         | Redis 7.0                      | 热点数据缓存、Token 存储     |
| 认证方案     | JWT + Spring Security 6        | 无状态认证                   |
| 文件存储     | 阿里云 OSS / MinIO             | 产品图片、溯源报告存储       |
| 接口文档     | Apifox                         | 前后端接口协作               |
| 构建部署     | Docker + Nginx                 | 容器化部署，前端反向代理     |

### 2.2 系统架构图（文字描述）

```
[Browser / Vue3 SPA — English UI]
        │
        │ HTTPS / REST API
        ▼
[Nginx 反向代理]
        │
        ├──▶ [静态资源 / Vue3 构建产物]
        │
        └──▶ [Spring Boot API Server :8080]
                    │
                    ├──▶ [MySQL 8.0]     主数据存储
                    ├──▶ [Redis 7.0]     缓存 / Token
                    └──▶ [OSS / MinIO]   文件存储
```

---

## 三、系统整体结构

### 3.1 页面结构总览

```
CP Group Platform
│
├── Home                          ← 统一入口，双轨导航（英文）
│
├── Dashboard（战略智能看板）
│   ├── Competitors（竞争对手分析）
│   ├── Opportunities（市场机会）
│   ├── Market Growth Trend（市场增长趋势）
│   └── Personas（用户画像）
│
├── Consumer App（消费者端，纯英文）
│   ├── Product Catalog（产品目录）
│   └── Traceability（溯源追踪）
│
└── Admin（管理后台）             ← 仅管理员可见
    ├── Data Management
    ├── User Management
    └── System Config
```

### 3.2 路由设计

| 路径                       | 页面组件            | 访问权限              |
|----------------------------|---------------------|-----------------------|
| `/`                        | Home                | 公开                  |
| `/competitors`             | Competitors         | 登录后（Dashboard）   |
| `/opportunities`           | Opportunities       | 登录后（Dashboard）   |
| `/market-growth`           | MarketGrowthTrend   | 登录后（Dashboard）   |
| `/personas`                | Personas            | 登录后（Dashboard）   |
| `/products`                | ProductCatalog      | 公开                  |
| `/traceability`            | Traceability        | 公开                  |
| `/traceability/:productId` | TraceabilityDetail  | 公开                  |
| `/admin`                   | AdminDashboard      | 管理员                |
| `/login`                   | Login               | 公开                  |

---

## 四、功能需求详述

---

### 4.1 首页（Home）

#### 功能描述

首页作为平台统一入口，向不同用户展示平台价值主张，并引导其进入对应的功能区域。**页面全程以英文显示。**

#### 页面布局

```
┌────────────────────────────────────────────┐
│  Top Nav: Logo + Navigation + Login Button  │
├────────────────────────────────────────────┤
│  Hero Banner: CP Group tagline + CTA        │
├─────────────────────┬──────────────────────┤
│  Dashboard Entry    │  Consumer App Entry   │
│  Strategic Intel    │  Explore Products /   │
│  Dashboard          │  Trace Your Food      │
├────────────────────────────────────────────┤
│  Key Metrics (Big Numbers):                 │
│  Cities Covered / Product SKUs / Market    │
│  Size / Traceability Nodes                  │
├────────────────────────────────────────────┤
│  Footer: Copyright + Contact               │
└────────────────────────────────────────────┘
```

#### 核心指标展示（Big Numbers）

数据来源：`CP_Glide_Data_Master.xlsx`

| 指标名称          | 参考数值       | 展示格式（英文）            |
|-------------------|----------------|-----------------------------|
| Cities Covered    | 系统配置       | XXX Cities                  |
| Product SKUs      | 产品表统计     | XXX+ Products               |
| Market Size       | 7,368 亿元     | ¥736.8B Market (2024)       |
| Market CAGR       | 22%            | ~22% Annual Growth          |

#### 验收标准（AC）

- [ ] 首页加载时间 < 2 秒（LCP 指标）
- [ ] Dashboard / Consumer App 双入口清晰区分，视觉层级明确
- [ ] 未登录用户点击 Dashboard 功能时跳转至登录页
- [ ] 核心指标数据从后端接口实时获取，非硬编码
- [ ] 顶部导航在页面滚动时固定（sticky）
- [ ] 页面所有文字内容以英文显示

---

### 4.2 竞争对手分析（Competitors）

#### 功能描述

展示中国生鲜电商市场两大主要竞争对手（叮咚买菜、盒马鲜生）的关键数据，辅助 CP Group 战略团队识别竞争格局、定位差异化机会。

#### 覆盖竞争对手

数据来源：`CP_Glide_Data_Master.xlsx` — Competitors Sheet

| 企业名称                | 英文名称              | 商业模式                  | 数据来源                              |
|-------------------------|-----------------------|---------------------------|---------------------------------------|
| 叮咚买菜                | Dingdong Maicai       | Front Warehouse Model     | Dingdong Q4 2024 Earnings, SEC EDGAR  |
| 盒马鲜生                | Freshippo (Hema)      | Omnichannel Store-Warehouse | Alibaba FY2025 Annual Report        |

#### 核心数据字段（来自 Master 数据表）

| 字段名称                 | 叮咚买菜                                 | 盒马鲜生                                    |
|--------------------------|------------------------------------------|---------------------------------------------|
| Business Model           | Front Warehouse (前置仓)                 | Omnichannel Store-Warehouse                 |
| City Focus               | Yangtze River Delta (Shanghai/JS/ZJ)     | 50 cities – Tier 1 & New Tier 1             |
| Revenue 2024 (Billion ¥) | 23.07                                    | 75                                          |
| GMV 2024 (Billion ¥)     | 26.5                                     | 75                                          |
| Net Profit 2024          | ¥295M (first full-year profit)           | First full-year profit FY2025               |
| Stores / Warehouses      | 1,000+ front warehouses                  | 430 Hema Fresh stores                       |
| Online Order %           | N/A (pure online)                        | >60%                                        |
| Monthly Active Users (M) | 8.22                                     | N/A (Alibaba)                               |
| Avg Basket Size (¥)      | 70                                       | 120                                         |
| Traceability Level       | Partial – batch traceability on select SKUs | Partial – QR traceability on premium items |
| SKU Strategy             | Streamlined – fresh & daily necessities  | Broad + 35% private label SKUs              |
| Private Label %          | ~5%                                      | ~35%                                        |
| Fulfillment Cost Rate    | 21.7%                                    | ~18–20% (est.)                              |

#### 页面布局

```
┌──────────────────────────────────────────────────┐
│  Filter Bar: Select Competitor / Metric Toggle    │
├──────────────────────────────────────────────────┤
│  Competitor Overview Cards                        │
│  [Dingdong Maicai]    [Freshippo (Hema)]         │
├─────────────────────┬────────────────────────────┤
│  Revenue Comparison  │  Business Model Contrast   │
│  (Bar Chart)         │  (Radar / Spider Chart)    │
├─────────────────────┼────────────────────────────┤
│  Market Share (Pie)  │  SWOT Summary Cards        │
├──────────────────────────────────────────────────┤
│  Detailed Data Table (sortable, exportable)       │
└──────────────────────────────────────────────────┘
```

#### 用户故事

```
UC-201 Competitor Data Review

As a strategic analyst, I want to compare Dingdong and Freshippo's
key financial and operational metrics, so I can assess the competitive
pressure and identify differentiation opportunities for CP Group.

Main Flow:
1. User enters Competitors page – both competitors shown by default
2. Charts and table load with revenue, GMV, MAU, basket size
3. User can toggle between metric dimensions
4. User can view SWOT breakdown per competitor
5. User can export table data as Excel
```

#### 验收标准（AC）

- [ ] 默认展示叮咚、盒马 2 家竞争对手全量数据
- [ ] 图表支持 Tooltip 悬停显示具体数值
- [ ] 点击图例可显示/隐藏对应数据系列
- [ ] 表格支持按任意列升序/降序排序
- [ ] 数据导出功能生成 .xlsx 文件，文件名含日期时间戳
- [ ] 页面数据支持手动刷新（不刷新整个页面）
- [ ] 所有标签、说明文字以英文显示

---

### 4.3 市场机会（Opportunities）

#### 功能描述

识别并可视化展示 CP Group 在中国生鲜电商市场的核心机会点。数据来源：`CP_Glide_Data_Master.xlsx` — Opportunities Sheet。

#### 机会优先级列表（来自 Master 数据表）

| Rank | Opportunity                                          | Score | Time Horizon   | Investment Level   |
|------|------------------------------------------------------|-------|----------------|--------------------|
| 1    | Full Farm-to-Table Supply Chain Traceability Platform| 92    | 12–18 months   | High (¥50–80M)     |
| 2    | AI-Driven Price-Quality Optimization Engine          | 88    | 6–12 months    | Medium (¥20–35M)   |
| 3    | Yangtze River Delta Regional Dominance Strategy      | 85    | 24–36 months   | High (¥200–400M)   |
| 4    | Personalized AI Shopping Assistant                   | 82    | 9–15 months    | Medium (¥25–40M)   |
| 5    | Private Label Fresh Brand Development                | 79    | 18–24 months   | Medium (¥30–50M)   |
| 6    | Community Group Buying for Tier 2/3 Cities           | 71    | 18–30 months   | Low-Medium         |
| 7    | Health & Wellness Premium Segment (Organic/Functional)| 68   | 12–18 months   | Medium (¥20–30M)   |

#### 页面布局

```
┌──────────────────────────────────────────────────┐
│  TOP 3 Opportunities (Highlight Cards)            │
├──────────────────────────────────────────────────┤
│  Opportunity Score Matrix (Bubble Chart)          │
│  X: Investment Level  Y: Score  Bubble: Time      │
├─────────────────────┬────────────────────────────┤
│  CP Advantage vs     │  Target Segment Coverage   │
│  Competitors         │  (Radar Chart)             │
│  (Radar Chart)       │                            │
├──────────────────────────────────────────────────┤
│  Opportunity List: filterable / sortable by score │
└──────────────────────────────────────────────────┘
```

#### 核心数据字段

| 字段名称             | 类型    | 说明                                         |
|----------------------|---------|----------------------------------------------|
| Rank                 | Integer | 优先级排名                                   |
| Opportunity          | String  | 机会描述                                     |
| Score                | Integer | 综合评分（0-100）                            |
| Why It Matters       | String  | 市场依据                                     |
| How CP Can Execute   | String  | 执行路径                                     |
| Target Segment       | String  | 目标用户群                                   |
| CP Competitive Advantage | String | CP Group 差异化优势                      |
| Time Horizon         | String  | 预计实施周期                                 |
| Investment Level     | String  | 投入规模                                     |

#### 验收标准（AC）

- [ ] 机会气泡图支持点击查看详情弹窗
- [ ] Rank 1（Score 最高）机会用高亮颜色标识
- [ ] 列表支持按 Score、Time Horizon、Investment Level 筛选
- [ ] CP 优势雷达图支持与竞争对手叠加对比
- [ ] 所有文字内容以英文显示

---

### 4.4 产品目录（Product Catalog）

#### 功能描述

面向消费者，展示 CP Group 在售生鲜产品，支持分类浏览、搜索、筛选，并可跳转至溯源详情。**全程英文界面。** 数据来源：`CP_Glide_Data_Master.xlsx` — Products Sheet（15 款产品）。

#### 当前产品数据（来自 Master 数据表）

| Product ID | Name (English)                        | Category        | Origin                   | Price (¥) | Certification              | CP Select |
|------------|---------------------------------------|-----------------|--------------------------|-----------|----------------------------|-----------|
| P001       | Organic Baby Spinach                  | Vegetables      | Shandong, China          | 18.9      | Organic Certified (CNCA)   | No        |
| P002       | Grass-Fed Australian Beef Ribeye      | Meat & Seafood  | Victoria, Australia      | 89.9      | Antibiotic-Free; Grass-Fed | No        |
| P003       | CP Thai Jasmine Rice 5kg              | Pantry          | Chiang Rai, Thailand     | 68        | Thailand GI; CP Select     | Yes       |
| P004       | Heirloom Cherry Tomatoes 500g         | Vegetables      | Yunnan, China            | 24.9      | GAP Certified              | No        |
| P005       | Live Jiangnan Hairy Crab              | Meat & Seafood  | Yangcheng Lake, Jiangsu  | 198       | Yangcheng Lake Authentic   | No        |
| P006       | Free-Range Organic Eggs (30pcs)       | Dairy & Eggs    | Anhui, China             | 58        | Organic Certified; Animal Welfare | No  |
| P007       | Wild Caught Norwegian Salmon 400g     | Meat & Seafood  | Norwegian Sea, Norway    | 128       | MSC Certified Sustainable  | No        |
| P008       | CP Organic Chicken Breast 500g        | Meat & Seafood  | Sichuan, China           | 45        | Organic Certified; CP Select | Yes     |
| P009       | Sichuan Red Kiwi 1kg                  | Fruit           | Ya'an, Sichuan           | 39        | GAP; Geographic Indication | No        |
| P010       | Dongbei Premium Tofu Set              | Dairy & Eggs    | Heilongjiang, China      | 28        | Non-GMO Soy Certified      | No        |
| P011       | French Président Butter 250g          | Dairy & Eggs    | Normandy, France         | 68        | AOC Normandy Certified     | No        |
| P012       | Xinjiang Hami Melon Half              | Fruit           | Turpan, Xinjiang         | 42        | Geographic Indication      | No        |
| P013       | CP Thai Coconut Water 6-pack          | Beverages       | Prachuap Khiri Khan, TH  | 52        | CP Select; No Additive     | Yes       |
| P014       | Yunnan Wild Porcini Mushrooms 200g    | Vegetables      | Diqing, Yunnan           | 88        | Wild Foraged; Altitude 3000m+ | No    |
| P015       | Imported Japanese A5 Wagyu 200g       | Meat & Seafood  | Kagoshima, Japan         | 428       | Japan A5 Grade; BMS 10+   | No        |

#### 页面布局

```
┌──────────────────────────────────────────────────┐
│  Search Bar (product name / keyword)              │
├──────────────────────────────────────────────────┤
│  Category Tabs: All | Vegetables | Meat & Seafood │
│                | Fruit | Dairy & Eggs | Pantry    │
│                | Beverages | CP Select            │
├──────────────────────────────────────────────────┤
│  Sort: Default / Price ↑ / Price ↓ / Quality ↓  │
├──────────────────────────────────────────────────┤
│  Product Card Grid (4 cols):                      │
│  [Image] [Name EN] [Origin] [Spec] [Price]       │
│  [Certification Badge] [Traceability Badge]       │
├──────────────────────────────────────────────────┤
│  Pagination (16 per page)                         │
└──────────────────────────────────────────────────┘
```

#### 产品卡片信息

| 字段             | 类型    | 说明                                     |
|------------------|---------|------------------------------------------|
| Product Image    | URL     | OSS 存储地址                             |
| Name (EN)        | String  | 英文产品名称                             |
| Category         | Enum    | Vegetables / Meat & Seafood / Fruit / Dairy & Eggs / Pantry / Beverages |
| Origin           | String  | 如 "Chiang Rai, Thailand"                |
| Price (¥)        | Decimal | 零售价                                   |
| Quality Score    | Integer | 0-100，来自 Master 数据表                |
| In Stock         | Boolean | 有货 / 售罄                              |
| Traceable        | Boolean | 展示 Traceability 徽章                   |
| Certification    | String  | 认证信息，如 "Organic Certified"         |
| CP Select        | Boolean | 展示 CP Select 私标徽章                  |

#### 用户故事

```
UC-401 Product Browse & Filter

As a consumer, I want to browse CP Group's fresh products by category
and sort by price or quality, so I can quickly find products that match
my needs.

Main Flow:
1. User opens Product Catalog – all products shown in English
2. User clicks a category tab to filter
3. User can search by keyword
4. User can sort by price or quality score
5. User clicks the Traceability badge to view full trace record
```

#### 验收标准（AC）

- [ ] 分类 Tab 切换无页面刷新（前端路由）
- [ ] 搜索结果高亮匹配关键词
- [ ] 售罄产品置灰并展示 "Out of Stock" 标签
- [ ] 可溯源产品显示绿色 "Traceable" 徽章
- [ ] CP Select 产品显示品牌徽章
- [ ] 页面所有文字内容以英文显示

---

### 4.5 溯源追踪（Traceability）

#### 功能描述

提供产品全链路溯源查询功能，用户可通过溯源码查询产品从产地到餐桌的完整流转记录。**全程英文界面。** 数据来源：`CP_Glide_Data_Master.xlsx` — Traceability Sheet（覆盖 P001 有机菠菜、P002 澳洲牛肉、P015 日本和牛）。

#### 溯源链路节点（英文标签）

```
[Farm Origin] → [Harvest & Grading] → [Processing / Pre-Cooling]
    → [Cold Chain Transit] → [Warehouse Inspection]
    → [Front Warehouse] → [Delivery to Consumer]
```

#### 样例数据（P001 Organic Baby Spinach）

| Step | Stage                  | Location                             | Date       | Temperature | Verified By          |
|------|------------------------|--------------------------------------|------------|-------------|----------------------|
| 1    | Farm Origin            | Shouguang Organic Farm, Shandong     | 2025-03-01 | 20°C        | CNCA Inspector       |
| 2    | Harvest & Grading      | Shouguang, Shandong                  | 2025-03-01 | 15°C        | Farm QC Manager      |
| 3    | Pre-Cooling            | Shouguang Cold Facility              | 2025-03-01 | 4°C         | CP Logistics QC      |
| 4    | Cold Chain Transit     | Shandong → Shanghai                  | 2025-03-02 | 4°C         | IoT Sensor #T-00234  |
| 5    | Warehouse Inspection   | CP Shanghai Distribution Centre      | 2025-03-02 | 4°C         | Shanghai QC Lab      |
| 6    | Front Warehouse        | CP Front Warehouse #SH-047, Jing'an  | 2025-03-03 | 4°C         | System Auto          |
| 7    | Delivery to Consumer   | Consumer Address, Shanghai           | 2025-03-03 | 8°C         | Delivery Partner     |

#### 页面布局

```
┌──────────────────────────────────────────────────┐
│  Trace Code Input / QR Scan + Search Button       │
├──────────────────────────────────────────────────┤
│  Product Info Card:                               │
│  Image / Name / Batch No. / Production Date      │
│  Expiry Date / Certifications                     │
├──────────────────────────────────────────────────┤
│  Traceability Timeline (Vertical):                │
│  Each node: Stage / Date / Location / Operator   │
│             / Result / Temperature / Attachment  │
├──────────────────────────────────────────────────┤
│  Origin Map (Leaflet)                             │
├──────────────────────────────────────────────────┤
│  Quality Report Download                         │
└──────────────────────────────────────────────────┘
```

#### 溯源节点数据字段

| 字段名称        | 类型     | 说明                                         |
|-----------------|----------|----------------------------------------------|
| Step Number     | Integer  | 1~N，时间升序                                |
| Stage           | Enum     | Farm Origin / Harvest & Grading / Pre-Cooling / Cold Chain Transit / Warehouse Inspection / Front Warehouse / Delivery to Consumer |
| Location        | String   | 详细地址（英文）                             |
| Date            | DateTime | 发生时间                                     |
| Status          | String   | ✅ Verified / ✅ Delivered                   |
| Temperature (°C)| Decimal  | 冷链节点必填                                 |
| Details         | String   | 操作描述（英文）                             |
| Verified By     | String   | 验证机构/人员                                |
| Attachment URL  | String   | 检测报告/照片，OSS 地址                      |

#### 验收标准（AC）

- [ ] 溯源码支持手动输入和二维码扫描两种方式
- [ ] 无效溯源码给出 "Invalid trace code. Please check and try again." 提示
- [ ] 时间轴节点按时间升序排列，最新节点高亮
- [ ] 冷链节点展示温度曲线图
- [ ] 页面所有文字内容以英文显示
- [ ] 产地地图显示农场坐标标注

---

### 4.6 市场增长趋势（Market Growth Trend）

#### 功能描述

基于 `CP_Glide_Data_Master.xlsx` — Market_Data Sheet，可视化展示中国生鲜电商市场 2014–2028 年历史数据与增长预测。

#### 核心数据（来自 Master 数据表）

| Year | Market Size (Billion ¥) | Penetration Rate (%) | Type       | Key Event                                        |
|------|-------------------------|----------------------|------------|--------------------------------------------------|
| 2014 | 29                      | 0.3%                 | Historical | Early adopter market; mobile internet expansion  |
| 2015 | 54.2                    | 0.6%                 | Historical | Mobile payment adoption                          |
| 2016 | 91.4                    | 1.0%                 | Historical | Freshippo opens first store in Shanghai          |
| 2017 | 140.3                   | 1.5%                 | Historical | Dingdong founded; investor boom                  |
| 2018 | 204                     | 2.1%                 | Historical | Community group buying emerges                   |
| 2019 | 250                     | 2.6%                 | Historical | Market consolidation begins                      |
| 2020 | 255.4                   | 3.8%                 | Historical | COVID-19 accelerates online grocery adoption     |
| 2021 | 364.1                   | 5.0%                 | Historical | Community group buying peaks                     |
| 2022 | 465.8                   | 6.2%                 | Historical | Missfresh collapses; market shakeout             |
| 2023 | 642.4                   | 8.1%                 | Historical | Dingdong first monthly profit (Sep 2023)         |
| 2024 | 736.8                   | 9.8%                 | Historical | Dingdong full-year profit ¥295M                  |
| 2025 | 892                     | 11.5%                | Projected  | Freshippo FY2025 GMV ¥75B                        |
| 2026 | 1,081                   | 13.5%                | Projected  | CP Group projected market entry                  |
| 2027 | 1,310                   | 15.8%                | Projected  | Traceability becomes standard                    |
| 2028 | 1,587                   | 18.2%                | Projected  | Market maturation in Tier 1 cities               |

#### 页面布局

```
┌──────────────────────────────────────────────────┐
│  Metric Selector: Market Size / Penetration Rate  │
├──────────────────────────────────────────────────┤
│  Main Chart: Market Size Trend (2014–2028)        │
│  Solid line: Historical (2014–2024)               │
│  Dashed line + shaded: Projected (2025–2028)      │
│  Annotation: CP Group Entry (2026)                │
├─────────────────────┬────────────────────────────┤
│  Penetration Rate    │  Key Event Timeline        │
│  Area Chart          │  (Milestone annotations)   │
├──────────────────────────────────────────────────┤
│  Data Source Citation                             │
└──────────────────────────────────────────────────┘
```

#### 核心数据字段

| 字段名称             | 类型    | 说明                                           |
|----------------------|---------|------------------------------------------------|
| Year                 | Integer | 2014–2028                                      |
| Market Size (B ¥)    | Decimal | 市场规模                                       |
| YoY Growth Rate (%)  | Decimal | 同比增速（公式计算）                           |
| Penetration Rate (%) | Decimal | 市场渗透率                                     |
| Is Projected         | Boolean | True 时展示虚线/阴影区域                       |
| Key Event            | String  | 年度标志性事件                                 |
| Source               | String  | 100ec.cn / Statista / Freshippo Annual Report  |

#### 验收标准（AC）

- [ ] 历史数据与预测数据用不同样式区分（实线 vs 虚线）
- [ ] 2026 年 CP Group 入市节点有特殊标注
- [ ] 图表支持时间区间拖拽缩放
- [ ] 鼠标悬停显示该年度完整数据及数据来源
- [ ] 所有图表标签以英文显示

---

### 4.7 用户画像（Personas）

#### 功能描述

展示 CP Group 目标客群的典型用户画像，帮助产品与市场团队理解目标用户的特征、需求与行为模式。数据来源：`CP_Glide_Data_Master.xlsx` — Customer_Personas Sheet。

#### 目标用户画像列表（来自 Master 数据表）

| Persona ID | Name            | Age Range | City Tier      | Income (¥/yr) | Key Decision Driver              |
|------------|-----------------|-----------|----------------|---------------|----------------------------------|
| PA001      | Pragmatic Mei   | 28–38     | Tier 1         | 200,000       | Quality & safety; time efficiency|
| PA002      | Value Victor    | 35–50     | Tier 1–2       | 150,000       | Price-quality ratio; reliability |
| PA003      | Health Hero     | 25–35     | Tier 1–2       | 120,000       | Organic certification; clean label|
| PA004      | Premium Penny   | 40–55     | Tier 1         | 500,000+      | Exclusivity; white-glove service  |
| PA005      | Suburban Savvy  | 30–45     | Tier 2–3       | 80,000        | Convenience vs wet market        |

#### 各画像核心摘要

**PA001 – Pragmatic Mei**
- Occupation: Dual-income professional couple
- Monthly grocery budget: ¥3,500
- Shopping frequency: 2–3 times/week, evening after work
- JTBD: "I want to be certain my family's food is safe and high-quality, so I can cook confidently."
- Top pain points: Cannot verify food origin; inconsistent quality across orders
- Willingness to pay premium: 25–35%
- Preferred channel: Mobile app

**PA002 – Value Victor**
- Occupation: Small business owner / middle manager
- Monthly grocery budget: ¥2,800
- JTBD: "I want the best quality-per-yuan products so I can provide well for my family without overspending."
- Top pain points: Marketing vs actual quality gap; premium price without proof
- Willingness to pay premium: 15–25%
- Preferred channel: WeChat Mini-program; Desktop web

**PA003 – Health Hero**
- Occupation: Fitness professional / health-conscious millennial
- Monthly grocery budget: ¥4,200
- JTBD: "I want certified organic and functional foods delivered, so I can support my fitness goals."
- Top pain points: Greenwashing concerns; limited variety of health foods online
- Willingness to pay premium: 35–50%
- Preferred channel: Mobile app; Xiaohongshu research → app purchase

**PA004 – Premium Penny**
- Occupation: Senior executive / affluent family
- Monthly grocery budget: ¥8,000
- JTBD: "I want verifiable premium products with flawless delivery for special occasions."
- Top pain points: Counterfeiting risk for imported goods; delivery experience doesn't match premium expectations
- Willingness to pay premium: 50–80%
- Preferred channel: Dedicated app; WeChat concierge

**PA005 – Suburban Savvy**
- Occupation: Government worker / teacher
- Monthly grocery budget: ¥1,800
- JTBD: "I want fresh groceries close to home without extra delivery fees."
- Top pain points: High delivery fees for small orders; limited variety vs city-centre
- Willingness to pay premium: 10–15%
- Preferred channel: Community group buying; WeChat group order

#### 页面布局

```
┌──────────────────────────────────────────────────┐
│  Persona Selector Tabs / Cards (5 personas)       │
├─────────────────────┬────────────────────────────┤
│  Profile Card:       │  Priority Radar Chart      │
│  Avatar / Age /      │  Quality / Price /         │
│  Occupation /        │  Delivery / Safety /       │
│  Income / City Tier  │  Convenience / Transparency│
├──────────────────────────────────────────────────┤
│  Behaviour Tags:                                  │
│  Shopping Frequency / Basket Size / Preferred Time│
│  / Platform / Willingness to Pay Premium         │
├──────────────────────────────────────────────────┤
│  Pain Points & Goals Cards                        │
├──────────────────────────────────────────────────┤
│  JTBD Statement (Jobs to Be Done)                 │
└──────────────────────────────────────────────────┘
```

#### 验收标准（AC）

- [ ] Tab 切换画像时，内容区域平滑过渡
- [ ] 雷达图各维度可点击查看详细说明
- [ ] Pain Points 与 Goals 卡片可展开查看详细描述
- [ ] 管理员可在后台新增/编辑画像内容
- [ ] 所有文字内容以英文显示

---

## 五、接口规范（API Contract）

### 5.1 统一响应结构

```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": 1700000000000
}
```

### 5.2 统一错误码

| code | 含义                 |
|------|----------------------|
| 200  | 成功                 |
| 400  | 请求参数错误         |
| 401  | 未认证/Token 失效    |
| 403  | 无权限               |
| 404  | 资源不存在           |
| 500  | 服务端内部错误       |
| 4001 | 账号或密码错误       |
| 4002 | 账号已被锁定         |
| 4003 | Token 已过期         |

### 5.3 认证接口

```
POST /api/v1/auth/login
描述：用户登录，获取 JWT Token

请求体：
{
  "username": "admin",
  "password": "RSA加密后的密码字符串"
}

成功响应 data：
{
  "accessToken": "eyJ...",
  "refreshToken": "eyJ...",
  "expiresIn": 7200,
  "userInfo": {
    "userId": 1,
    "username": "admin",
    "role": "ADMIN"
  }
}

---

POST /api/v1/auth/refresh
描述：刷新 Access Token

请求体：
{
  "refreshToken": "eyJ..."
}

---

POST /api/v1/auth/logout
描述：退出登录，服务端加入黑名单
请求头：Authorization: Bearer {accessToken}
```

### 5.4 首页数据接口

```
GET /api/v1/dashboard/summary
描述：获取首页核心指标（Big Numbers）

响应 data：
{
  "coverCities": 28,
  "totalSkus": 15,
  "marketSizeBillion": 736.8,
  "marketCAGR": 0.22
}
```

### 5.5 竞争对手接口

```
GET /api/v1/competitors
描述：获取竞争对手列表及核心数据（仅叮咚、盒马）
Query 参数：
  - names: 逗号分隔，可选值 "dingdong,freshippo"（默认全部）
  - year: 数据年份（默认最新，2024）

响应 data：[
  {
    "id": 1,
    "name": "Dingdong Maicai",
    "businessModel": "Front Warehouse",
    "cityFocus": "Yangtze River Delta",
    "revenue2024": 23.07,
    "gmv2024": 26.5,
    "netProfit2024": 295,
    "warehousesOrStores": "1,000+ front warehouses",
    "mau": 8.22,
    "avgBasketSize": 70,
    "fulfillmentCostRate": "21.7%",
    "traceabilityLevel": "Partial",
    "privateLabelPct": "~5%",
    "profitStatus": "Profitable (FY2024)"
  },
  {
    "id": 2,
    "name": "Freshippo (Hema)",
    "businessModel": "Omnichannel Store-Warehouse",
    "cityFocus": "50 cities – Tier 1 & New Tier 1",
    "revenue2024": 75,
    "gmv2024": 75,
    "netProfit2024": null,
    "warehousesOrStores": "430 Hema Fresh stores",
    "mau": null,
    "avgBasketSize": 120,
    "fulfillmentCostRate": "~18-20%",
    "traceabilityLevel": "Partial",
    "privateLabelPct": "~35%",
    "profitStatus": "Profitable (FY2025)"
  }
]
```

### 5.6 产品目录接口

```
GET /api/v1/products
描述：分页获取产品列表（英文字段）
Query 参数：
  - category: Vegetables | Meat & Seafood | Fruit | Dairy & Eggs | Pantry | Beverages（可选）
  - keyword: 搜索关键词（可选）
  - sortBy: price_asc | price_desc | quality_desc（默认综合）
  - cpSelect: true（可选，筛选 CP Select 私标）
  - page: 页码（默认 1）
  - pageSize: 每页条数（默认 16）

响应 data：
{
  "total": 15,
  "list": [
    {
      "id": "P001",
      "nameEn": "Organic Baby Spinach",
      "category": "Vegetables",
      "origin": "Shandong Province, China",
      "price": 18.9,
      "originalPrice": 22.9,
      "qualityScore": 95,
      "stabilityScore": 92,
      "freshnessDays": 4,
      "certification": "Organic Certified (CNCA)",
      "cpSelect": false,
      "inStock": true,
      "traceable": true,
      "traceCode": "P001",
      "imageUrl": "https://oss.xxx.com/...",
      "tags": ["organic", "leafy", "healthy"]
    }
  ]
}
```

### 5.7 溯源接口

```
GET /api/v1/traceability/{traceCode}
描述：根据溯源码查询产品全链路溯源记录

响应 data：
{
  "productInfo": {
    "id": "P001",
    "nameEn": "Organic Baby Spinach",
    "origin": "Shandong Province, China",
    "certification": "Organic Certified (CNCA)"
  },
  "nodes": [
    {
      "stepNumber": 1,
      "stage": "Farm Origin",
      "location": "Shouguang Organic Farm, Shandong",
      "date": "2025-03-01",
      "status": "Verified",
      "temperatureC": 20,
      "details": "Certified organic fields, no synthetic pesticide use. CNCA inspection passed.",
      "verifiedBy": "CNCA Inspector #SH2024-112",
      "attachmentUrl": null
    },
    {
      "stepNumber": 4,
      "stage": "Cold Chain Transit",
      "location": "Shandong → Shanghai (G2 Highway)",
      "date": "2025-03-02",
      "status": "Verified",
      "temperatureC": 4,
      "details": "Refrigerated truck (4°C ± 1°C). 780km, 9 hours. No temperature breach.",
      "verifiedBy": "IoT Sensor #T-00234",
      "attachmentUrl": null
    }
  ]
}
```

### 5.8 市场趋势接口

```
GET /api/v1/market/trend
描述：获取市场增长趋势数据（2014–2028）
Query 参数：
  - metric: marketSize | penetrationRate（默认 marketSize）
  - startYear: 2014（默认）
  - endYear: 2028（默认）

响应 data：[
  {
    "year": 2014,
    "value": 29.0,
    "penetrationRate": 0.3,
    "isProjected": false,
    "keyEvent": "Early adopter market; mobile internet expansion begins",
    "source": "100ec.cn; Statista 2024"
  },
  {
    "year": 2024,
    "value": 736.8,
    "penetrationRate": 9.8,
    "isProjected": false,
    "keyEvent": "Dingdong full-year profit ¥295M; Freshippo 9 months profitable",
    "source": "Statista trend + company reports"
  },
  {
    "year": 2026,
    "value": 1081.0,
    "penetrationRate": 13.5,
    "isProjected": true,
    "keyEvent": "CP Group projected market entry",
    "source": "iResearch 2025 forecast; Statista CAGR ~27%"
  }
]
```

### 5.9 市场机会接口

```
GET /api/v1/opportunities
描述：获取市场机会列表（按 Score 降序）

响应 data：[
  {
    "rank": 1,
    "opportunity": "Full Farm-to-Table Supply Chain Traceability Platform",
    "score": 92,
    "whyItMatters": "Only 3% of China fresh e-commerce offers full traceability; 78% of middle-class consumers cite food safety as #1 concern",
    "howCPCanExecute": "Leverage CP Group's 200+ agri-subsidiaries to implement QR-code blockchain traceability across all SKUs",
    "targetSegment": "Pragmatic Middle-Class Buyers (25–40, household income ¥200K+)",
    "cpAdvantage": "CP Group controls entire supply chain from farm; no competitor has end-to-end traceability at scale",
    "timeHorizon": "12–18 months",
    "investmentLevel": "High (¥50–80M)"
  }
]
```

---

## 六、数据库设计

### 6.1 核心表清单

| 表名                  | 说明                               |
|-----------------------|------------------------------------|
| `sys_user`            | 系统用户                           |
| `sys_role`            | 角色                               |
| `cp_competitor`       | 竞争对手基础信息（仅叮咚、盒马）   |
| `cp_competitor_data`  | 竞争对手年度数据                   |
| `cp_opportunity`      | 市场机会（7条，来自 Master 表）     |
| `cp_product`          | 产品目录（15条，英文字段）         |
| `cp_traceability`     | 溯源主记录                         |
| `cp_trace_node`       | 溯源节点详情                       |
| `cp_market_data`      | 市场趋势数据（2014–2028）          |
| `cp_persona`          | 用户画像（5条，英文字段）          |

### 6.2 核心表结构

#### sys_user（用户表）
```sql
CREATE TABLE sys_user (
  id          BIGINT PRIMARY KEY AUTO_INCREMENT,
  username    VARCHAR(50) NOT NULL UNIQUE,
  password    VARCHAR(255) NOT NULL COMMENT 'BCrypt 加密',
  real_name   VARCHAR(50),
  role_id     BIGINT NOT NULL,
  status      TINYINT DEFAULT 1 COMMENT '1启用 0禁用',
  last_login  DATETIME,
  create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
  update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### cp_product（产品表，英文字段）
```sql
CREATE TABLE cp_product (
  id              VARCHAR(10) PRIMARY KEY COMMENT 'e.g. P001',
  name_en         VARCHAR(200) NOT NULL,
  category        VARCHAR(50) NOT NULL,
  sub_category    VARCHAR(50),
  origin          VARCHAR(200),
  price           DECIMAL(10,2) NOT NULL,
  original_price  DECIMAL(10,2),
  quality_score   INT,
  stability_score INT,
  freshness_days  INT,
  certification   VARCHAR(200),
  cp_select       TINYINT DEFAULT 0,
  in_stock        TINYINT DEFAULT 1,
  traceable       TINYINT DEFAULT 0,
  trace_code      VARCHAR(50),
  description     TEXT,
  tags            VARCHAR(500),
  image_url       VARCHAR(500),
  create_time     DATETIME DEFAULT CURRENT_TIMESTAMP,
  update_time     DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### cp_trace_node（溯源节点表，英文字段）
```sql
CREATE TABLE cp_trace_node (
  id              BIGINT PRIMARY KEY AUTO_INCREMENT,
  trace_id        BIGINT NOT NULL COMMENT '关联 cp_traceability.id',
  step_number     INT NOT NULL,
  stage           VARCHAR(100) COMMENT 'Farm Origin / Harvest & Grading / Pre-Cooling / Cold Chain Transit / Warehouse Inspection / Front Warehouse / Delivery to Consumer',
  location        VARCHAR(200),
  occurred_date   DATE,
  status          VARCHAR(50) COMMENT 'Verified / Delivered',
  temperature_c   DECIMAL(5,2) COMMENT '冷链温度，℃',
  details         TEXT,
  verified_by     VARCHAR(200),
  attachment_url  VARCHAR(500),
  create_time     DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### cp_market_data（市场趋势数据表）
```sql
CREATE TABLE cp_market_data (
  id                BIGINT PRIMARY KEY AUTO_INCREMENT,
  year              INT NOT NULL UNIQUE,
  market_size_b     DECIMAL(10,2) COMMENT '市场规模（十亿元）',
  penetration_rate  DECIMAL(5,2) COMMENT '渗透率 %',
  is_projected      TINYINT DEFAULT 0,
  key_event         VARCHAR(500),
  source            VARCHAR(200),
  create_time       DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 6.3 核心实体关系

```
sys_user N:1 sys_role

cp_product 1:1 cp_traceability（通过 trace_code 关联）
cp_traceability 1:N cp_trace_node

cp_competitor 1:N cp_competitor_data（一家企业多个年度数据）
```

---

## 七、权限与角色设计

### 7.1 角色定义

| 角色 Code    | 角色名称   | 描述                                          |
|--------------|------------|-----------------------------------------------|
| `ADMIN`      | 系统管理员 | 全部权限，含数据维护、用户管理                |
| `ANALYST`    | 战略分析师 | 可查看所有 Dashboard 模块，不可编辑           |
| `CONSUMER`   | 普通消费者 | 仅可访问 Consumer App 功能（产品目录、溯源）  |
| `GUEST`      | 访客       | 仅可浏览首页和产品目录，无法查看溯源详情      |

### 7.2 权限矩阵

| 功能模块               | ADMIN | ANALYST | CONSUMER | GUEST |
|------------------------|-------|---------|----------|-------|
| Home                   | ✅    | ✅      | ✅       | ✅    |
| Dashboard – Competitors| ✅    | ✅      | ❌       | ❌    |
| Dashboard – Opportunities| ✅  | ✅      | ❌       | ❌    |
| Dashboard – Market Trend| ✅   | ✅      | ❌       | ❌    |
| Dashboard – Personas   | ✅    | ✅      | ❌       | ❌    |
| Product Catalog        | ✅    | ✅      | ✅       | ✅    |
| Traceability           | ✅    | ✅      | ✅       | ❌    |
| Data Export            | ✅    | ✅      | ❌       | ❌    |
| Admin – Data Mgmt      | ✅    | ❌      | ❌       | ❌    |
| Admin – User Mgmt      | ✅    | ❌      | ❌       | ❌    |

### 7.3 前端权限控制方案

```javascript
// 路由守卫（Vue Router）
router.beforeEach((to, from, next) => {
  const requiredRole = to.meta.requiredRole
  const userRole = useUserStore().role
  if (requiredRole && !hasPermission(userRole, requiredRole)) {
    next('/403')
  } else {
    next()
  }
})

// 按钮级别权限指令（自定义 v-permission）
<el-button v-permission="'ADMIN'">Data Management</el-button>
```

---

## 八、非功能需求

### 8.1 性能需求

| 指标                  | 目标值                     |
|-----------------------|----------------------------|
| 首页 LCP（最大内容渲染）| < 2.5 秒                  |
| API 平均响应时间       | < 300ms                    |
| API P99 响应时间       | < 800ms                    |
| 图表渲染时间           | < 1 秒（数据量 < 1000 条） |
| 并发用户数支持         | ≥ 200                      |

### 8.2 安全需求

- 所有 Dashboard 接口必须携带有效 JWT Token（Spring Security 过滤器）
- 密码传输 RSA 加密，存储 BCrypt 哈希
- 接口限流：同一 IP 每分钟最多 100 次请求（Redis + Lua 脚本）
- XSS 防护：前端输入统一 escape，后端使用 XssFilter
- SQL 注入防护：MyBatis-Plus 参数化查询，禁止拼接 SQL
- 上传文件白名单校验（仅允许 jpg/png/pdf）

### 8.3 兼容性需求

| 类型     | 要求                                    |
|----------|-----------------------------------------|
| 浏览器   | Chrome 90+、Edge 90+、Firefox 88+       |
| 分辨率   | 1366×768 及以上，推荐 1920×1080         |
| 移动端   | 本期不要求，Product Catalog 做响应式适配 |

### 8.4 可用性

- 系统 SLA ≥ 99.5%（月均停机 < 3.6 小时）
- 数据库每日全量备份，保留 30 天
- 关键接口异常时前端展示友好降级提示，不白屏

### 8.5 语言与国际化

- **App（前端）全程仅以英文显示**，包括：导航、标签、提示信息、按钮、图表说明、产品信息、溯源记录、错误提示等所有面向用户的文字内容
- 代码层面使用 vue-i18n 框架，locale 固定为 `en`，预留多语言扩展接口（二期）

---

## 九、部署与环境要求

### 9.1 环境划分

| 环境   | 用途             | 域名示例                       |
|--------|------------------|--------------------------------|
| 开发   | 本地开发联调     | localhost:5173（前端）         |
| 测试   | QA 测试验收     | test.cpgroup-fresh.com         |
| 生产   | 正式上线         | www.cpgroup-fresh.com          |

### 9.2 服务器配置（最低要求）

| 角色           | 配置                      | 说明                |
|----------------|---------------------------|---------------------|
| Web/API 服务器 | 4 核 CPU / 8G 内存        | Spring Boot + Nginx |
| 数据库服务器   | 4 核 CPU / 16G 内存       | MySQL 8.0           |
| 缓存服务器     | 2 核 CPU / 4G 内存        | Redis 7.0           |

### 9.3 部署方式

```yaml
# docker-compose.yml 核心结构（示意）
services:
  frontend:
    image: nginx:alpine
    volumes:
      - ./dist:/usr/share/nginx/html
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    ports:
      - "80:80"

  backend:
    image: cp-group-api:latest
    environment:
      - SPRING_PROFILES_ACTIVE=prod
      - DB_HOST=mysql
      - REDIS_HOST=redis
    ports:
      - "8080:8080"

  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_DATABASE=cp_group
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:7.0-alpine
```

---

## 十、附录

### 附录 A：数据来源清单

| 数据模块         | 数据来源                                            | 获取方式                   |
|------------------|-----------------------------------------------------|----------------------------|
| 叮咚买菜数据     | Dingdong Q4 2024 Earnings Release; SEC EDGAR (Mar 2025) | 公开文件                |
| 盒马鲜生数据     | Alibaba Annual Report FY2025; SCMP Dec 2024         | 官网公告 / 媒体报道         |
| 市场规模数据     | Statista 2024; 100ec.cn; iResearch 2025 forecast    | 订阅数据库 / 行业报告       |
| 市场机会分析     | CP_Glide_Data_Master.xlsx — Opportunities Sheet     | 内部数据表                  |
| 产品数据         | CP_Glide_Data_Master.xlsx — Products Sheet          | 内部数据表                  |
| 溯源记录         | CP_Glide_Data_Master.xlsx — Traceability Sheet      | 内部数据表                  |
| 用户画像         | CP_Glide_Data_Master.xlsx — Customer_Personas Sheet | 内部数据表                  |

> **说明**：当前阶段所有可展示数据均来自 `CP_Glide_Data_Master.xlsx`，后续接入真实后端时以数据库为准。

### 附录 B：术语表

| 术语       | 说明                                                  |
|------------|-------------------------------------------------------|
| Dashboard  | 面向 CP Group 内部团队的战略智能看板（原 B2B 端）     |
| Consumer App | 面向终端用户的英文浏览/溯源界面（原 B2C 端）        |
| GMV        | Gross Merchandise Volume，商品交易总额                |
| MAU        | Monthly Active Users，月活跃用户数                    |
| CAGR       | Compound Annual Growth Rate，年复合增长率             |
| LCP        | Largest Contentful Paint，最大内容绘制时间            |
| SLA        | Service Level Agreement，服务级别协议                 |
| JWT        | JSON Web Token，无状态认证令牌                        |
| OSS        | Object Storage Service，对象存储服务                  |
| P99        | 99% 请求的响应时间上限                                |
| SKU        | Stock Keeping Unit，最小存货单位                      |
| CP Select  | CP Group 自有私标产品系列                             |
| JTBD       | Jobs to Be Done，用户核心任务框架                     |

### 附录 C：相关文档

- 接口文档：Apifox 在线文档（内部链接）
- 原型设计：`Prototype_Design-main/` 目录（Streamlit 原型）
- 数据来源：`CP_Glide_Data_Master.xlsx`（主数据表）
- 数据库 DDL：`/docs/database/init.sql`
- 部署手册：`/docs/deploy/README.md`

---

*文档维护：本文档随项目迭代更新，重大变更需通过评审后方可修改基线版本。*
