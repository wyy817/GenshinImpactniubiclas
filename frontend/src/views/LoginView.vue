<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-header">
        <div class="login-logo">🌿</div>
        <h2>CP Group Dashboard</h2>
        <p>Sign in to access market intelligence and analytics</p>
      </div>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="Username" prop="username">
          <el-input
            v-model="form.username"
            placeholder="Enter username"
            size="large"
            prefix-icon="User"
            clearable
          />
        </el-form-item>
        <el-form-item label="Password" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="Enter password"
            size="large"
            prefix-icon="Lock"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-button
          type="primary"
          size="large"
          style="width:100%;margin-top:8px"
          :loading="loading"
          @click="handleLogin"
          round
        >
          Sign In
        </el-button>
      </el-form>

      <!-- Demo credentials (hidden for production)
      <div class="demo-credentials">
        <div class="demo-title">
          <el-icon><InfoFilled /></el-icon>
          Demo Credentials
        </div>
        <div class="cred-grid">
          <div
            v-for="cred in credentials"
            :key="cred.user"
            class="cred-item"
            @click="fillCred(cred)"
          >
            <el-tag :type="cred.tagType" size="small">{{ cred.role }}</el-tag>
            <div class="cred-detail">
              <span class="cred-user">{{ cred.user }}</span>
              <span class="cred-pass">{{ cred.pass }}</span>
            </div>
          </div>
        </div>
        <p class="demo-hint">Click any row to auto-fill credentials</p>
      </div>
      -->
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { InfoFilled } from '@element-plus/icons-vue'
import api from '../api/index.js'
import { useAuthStore } from '../stores/auth.js'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const formRef = ref(null)
const loading = ref(false)
const form = reactive({ username: '', password: '' })

const rules = {
  username: [{ required: true, message: 'Please enter your username', trigger: 'blur' }],
  password: [{ required: true, message: 'Please enter your password', trigger: 'blur' }],
}

const credentials = [
  { user: 'admin', pass: 'admin123', role: 'ADMIN', tagType: 'danger' },
  { user: 'analyst', pass: 'analyst123', role: 'ANALYST', tagType: 'warning' },
  { user: 'consumer', pass: 'consumer123', role: 'CONSUMER', tagType: 'success' },
]

function fillCred(cred) {
  form.username = cred.user
  form.password = cred.pass
}

async function handleLogin() {
  if (!formRef.value) return
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    const data = await api.post('/auth/login', {
      username: form.username,
      password: form.password,
    })
    auth.login(data.token, data.role, data.username)
    ElMessage.success(`Welcome, ${data.username}!`)

    const redirect = route.query.redirect
    if (redirect) {
      router.push(redirect)
    } else if (['ADMIN', 'ANALYST'].includes(data.role)) {
      router.push('/competitors')
    } else {
      router.push('/products')
    }
  } catch {
    // error handled by api interceptor
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: calc(100vh - 64px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.login-card {
  background: #fff;
  border-radius: 20px;
  padding: 48px 40px;
  width: 100%;
  max-width: 440px;
  box-shadow: 0 8px 40px rgba(0,0,0,0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-logo {
  font-size: 48px;
  margin-bottom: 12px;
}

.login-header h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 6px;
}

.login-header p {
  font-size: 14px;
  color: #909399;
}

.demo-credentials {
  margin-top: 28px;
  background: #f5f7fa;
  border-radius: 12px;
  padding: 16px;
}

.demo-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #606266;
  margin-bottom: 12px;
}

.cred-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.cred-item {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #fff;
  border-radius: 8px;
  padding: 10px 12px;
  cursor: pointer;
  border: 1px solid #ebeef5;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.cred-item:hover {
  border-color: #409eff;
  box-shadow: 0 2px 8px rgba(64,158,255,0.15);
}

.cred-detail {
  display: flex;
  gap: 8px;
  align-items: center;
}

.cred-user {
  font-weight: 600;
  font-size: 13px;
  color: #303133;
}

.cred-pass {
  font-size: 12px;
  color: #909399;
}

.demo-hint {
  font-size: 11px;
  color: #c0c4cc;
  margin-top: 8px;
  text-align: center;
}
</style>
