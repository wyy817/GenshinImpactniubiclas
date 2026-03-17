<template>
  <el-header class="app-header">
    <div class="header-content">
      <div class="logo" @click="router.push('/')">
        <span class="logo-icon">🌿</span>
        <span class="logo-text">CP Fresh</span>
      </div>

      <el-menu mode="horizontal" :router="true" :default-active="route.path" class="nav-menu" :ellipsis="false">
        <el-menu-item index="/">Home</el-menu-item>
        <el-menu-item index="/products">Products</el-menu-item>
        <el-menu-item index="/traceability">Traceability</el-menu-item>
        <el-sub-menu index="dashboard" v-if="authStore.isLoggedIn">
          <template #title>Dashboard</template>
          <el-menu-item index="/competitors">Competitors</el-menu-item>
          <el-menu-item index="/opportunities">Opportunities</el-menu-item>
          <el-menu-item index="/market-growth">Market Growth</el-menu-item>
          <el-menu-item index="/personas">Personas</el-menu-item>
          <el-menu-item
            v-if="authStore.role === 'ADMIN' || authStore.role === 'ANALYST'"
            index="/inventory"
          >Inventory</el-menu-item>
        </el-sub-menu>
      </el-menu>

      <div class="header-right">
        <template v-if="authStore.isLoggedIn">
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-icon><User /></el-icon>
              {{ authStore.username }}
              <el-tag size="small" type="info" style="margin-left:6px;">{{ authStore.role }}</el-tag>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">Logout</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <el-button type="primary" @click="router.push('/login')">Login</el-button>
        </template>
      </div>
    </div>
  </el-header>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { User } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

function handleCommand(cmd) {
  if (cmd === 'logout') {
    authStore.logout()
    ElMessage.success('Logged out')
    router.push('/')
  }
}
</script>

<style scoped>
.app-header {
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
.header-content {
  display: flex;
  align-items: center;
  height: 60px;
  max-width: 1200px;
  margin: 0 auto;
}
.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  margin-right: 32px;
  flex-shrink: 0;
}
.logo-icon { font-size: 22px; }
.logo-text { font-size: 18px; font-weight: 700; color: #303133; }
.nav-menu {
  flex: 1;
  border-bottom: none !important;
}
.header-right {
  margin-left: 24px;
  flex-shrink: 0;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  color: #303133;
}
</style>
