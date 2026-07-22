<template>
  <div class="login-container">
    <h2>Вход в Автомастерскую</h2>
    
    <input v-model="login" type="text" placeholder="Email или телефон / Логин" />
    
    <input v-model="password" type="password" placeholder="Пароль" />
    
    <select v-model="role">
      <option value="client">Клиент</option>
      <option value="mechanic">Мастер</option>
      <option value="admin">Администратор</option>
    </select>

    <button @click="handleLogin" :disabled="isLoading">
      {{ isLoading ? 'Вход...' : 'Войти' }}
    </button>
    
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../api/axios'

const router = useRouter()

// Реактивные переменные (как state в React, но проще)
const login = ref('')
const password = ref('')
const role = ref('client')
const error = ref('')
const isLoading = ref(false)

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
    
    alert('Успешный вход! Токен сохранен.')
    // router.push('/dashboard')
    
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка сети'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  max-width: 300px;
  margin: 50px auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
  font-family: sans-serif;
}
input, select, button {
  padding: 10px;
  font-size: 16px;
}
button {
  background-color: #42b883;
  color: white;
  border: none;
  cursor: pointer;
}
button:disabled {
  background-color: #ccc;
}
.error {
  color: red;
  font-size: 14px;
}
</style>