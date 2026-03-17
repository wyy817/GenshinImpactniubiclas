import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('cp_token') || '')
  const role = ref(localStorage.getItem('cp_role') || '')
  const username = ref(localStorage.getItem('cp_username') || '')

  function login(newToken, newRole, newUsername) {
    token.value = newToken
    role.value = newRole
    username.value = newUsername
    localStorage.setItem('cp_token', newToken)
    localStorage.setItem('cp_role', newRole)
    localStorage.setItem('cp_username', newUsername)
  }

  function logout() {
    token.value = ''
    role.value = ''
    username.value = ''
    localStorage.removeItem('cp_token')
    localStorage.removeItem('cp_role')
    localStorage.removeItem('cp_username')
  }

  const isLoggedIn = computed(() => !!token.value)
  const isAnalyst = computed(() => ['ADMIN', 'ANALYST'].includes(role.value))

  return { token, role, username, login, logout, isLoggedIn, isAnalyst }
})
