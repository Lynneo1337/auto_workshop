<template>
  <div class="login-page fade-in">
    <div class="glass-card login-card">
      <h2 class="login-title">Вход в <span class="neon-text">Автомастерскую</span></h2>
      <p class="login-subtitle">Добро пожаловать! Войдите в свой аккаунт</p>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label class="form-label">Email, телефон или логин</label>
          <input 
            v-model="login" 
            type="text" 
            class="form-input"
            placeholder="mail@example.com или +79001234567" 
            @input="normalizeLogin"
          />
        </div>

        <div class="form-group">
          <label class="form-label">Пароль</label>
          <input 
            v-model="password" 
            type="password" 
            class="form-input"
            placeholder="Введите пароль" 
          />
        </div>

        <div class="form-group">
          <label class="form-label">Роль</label>
          <select v-model="role" class="form-input">
            <option value="client">Клиент</option>
            <option value="mechanic">Мастер</option>
            <option value="admin">Администратор</option>
          </select>
        </div>

        <button type="submit" class="btn btn-primary btn-full" :disabled="isLoading">
          {{ isLoading ? 'Вход...' : 'Войти' }}
        </button>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div class="register-link">
          <p>Нет аккаунта? <router-link to="/register" class="neon-text">Зарегистрироваться</router-link></p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../api/axios'

const router = useRouter()

const login = ref('')
const password = ref('')
const role = ref('client')
const error = ref('')
const isLoading = ref(false)

const normalizeLogin = () => {
  let val = login.value.replace(/\s/g, '').replace(/-/g, '').replace(/\(/g, '').replace(/\)/g, '')
  
  if (val.startsWith('8') && val.length === 11 && val.slice(1).match(/^\d+$/)) {
    login.value = '+7' + val.slice(1)
  }
  else if (val.startsWith('7') && val.length === 11 && val.slice(1).match(/^\d+$/)) {
    login.value = '+7' + val.slice(1)
  }
}

const handleLogin = async () => {
  error.value = ''
  isLoading.value = true
  
  try {
    const response = await apiClient.post('/login', {
      login: login.value,
      password: password.value,
      role: role.value
    })
    
    localStorage.setItem('token', response.data.access_token)
    localStorage.setItem('role', role.value)
    
    router.push('/dashboard')
    
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка сети. Попробуйте позже.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: calc(100vh - 100px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.login-card {
  max-width: 450px;
  width: 100%;
  padding: 40px;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(220, 38, 38, 0.3);
  box-shadow: 0 0 40px rgba(220, 38, 38, 0.1);
}

.login-title {
  font-size: 2rem;
  font-weight: 900;
  margin-bottom: 10px;
  text-align: center;
  color: white;
}

.login-subtitle {
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 30px;
  font-size: 1rem;
}

.form-group {
  margin-bottom: 20px;
}

.btn-full {
  width: 100%;
  margin-top: 10px;
}

.error-message {
  margin-top: 15px;
  padding: 12px;
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.4);
  border-radius: 10px;
  color: #f87171;
  font-size: 0.9rem;
  text-align: center;
}

.register-link {
  margin-top: 25px;
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
}

.register-link a {
  color: #dc2626;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s;
}

.register-link a:hover {
  text-shadow: 0 0 10px rgba(220, 38, 38, 0.5);
}
</style>