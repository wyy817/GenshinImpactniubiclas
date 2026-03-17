import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: (import.meta.env.VITE_API_BASE_URL || '') + '/api/v1',
  timeout: 15000,
})

// Request interceptor — attach JWT if present
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('cp_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor — unwrap .data.data
api.interceptors.response.use(
  (response) => {
    const body = response.data
    if (body && body.code === 200) {
      return body.data
    }
    return body
  },
  (error) => {
    const msg =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      'Network error'
    ElMessage.error(msg)
    return Promise.reject(error)
  }
)

export default api
