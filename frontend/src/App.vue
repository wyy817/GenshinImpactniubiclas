<template>
  <el-config-provider>
    <div class="app-wrapper">
      <AppHeader />
      <main class="app-main">
        <router-view />
      </main>
    </div>
    <!-- Floating Report Editor — analyst / admin only -->
    <ReportEditorPanel v-if="authStore.isLoggedIn && (authStore.role === 'ANALYST' || authStore.role === 'ADMIN')" />
  </el-config-provider>
</template>

<script setup>
import AppHeader from './components/AppHeader.vue'
import ReportEditorPanel from './components/ReportEditorPanel.vue'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f5f7fa;
  color: #303133;
}

.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-main {
  flex: 1;
  padding: 24px;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
}

/* Global utility classes */
.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 8px;
}

.page-subtitle {
  font-size: 15px;
  color: #606266;
  margin-bottom: 24px;
}

.section-gap {
  margin-top: 32px;
}
</style>
