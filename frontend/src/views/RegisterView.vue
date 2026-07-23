<template>
  <div class="register-page fade-in">
    <div class="glass-card register-card">
      <h2 class="register-title">Регистрация в <span class="neon-text">Автомастерской</span></h2>
      <p class="register-subtitle">Создайте аккаунт клиента</p>

      <form @submit.prevent="handleRegister">
        <!-- ФИО -->
        <div class="form-group">
          <label class="form-label">ФИО</label>
          <input 
            v-model="form.full_name" 
            type="text" 
            class="form-input"
            placeholder="Иванов Иван Иванович" 
            required
          />
        </div>

        <!-- Телефон -->
        <div class="form-group">
          <label class="form-label">Телефон</label>
          <input 
            v-model="form.phone" 
            type="tel" 
            class="form-input"
            placeholder="+79001234567" 
            @input="normalizePhone"
            required
          />
        </div>

        <!-- Email -->
        <div class="form-group">
          <label class="form-label">Email</label>
          <input 
            v-model="form.email" 
            type="email" 
            class="form-input"
            placeholder="ivan@example.com" 
            required
          />
        </div>

        <!-- Пароль -->
        <div class="form-group">
          <label class="form-label">Пароль</label>
          <input 
            v-model="form.password" 
            type="password" 
            class="form-input"
            placeholder="Минимум 6 символов" 
            required
          />
        </div>

        <!-- Кнопка регистрации -->
        <button type="submit" class="btn btn-primary btn-full" :disabled="isLoading">
          {{ isLoading ? 'Регистрация...' : 'Зарегистрироваться' }}
        </button>

        <!-- Сообщение об ошибке -->
        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <!-- Сообщение об успехе -->
        <div v-if="success" class="success-message">
          Регистрация успешна! Перенаправление...
        </div>

        <!-- Ссылка на вход -->
        <div class="login-link">
          <p>Уже есть аккаунт? <router-link to="/login" class="neon-text">Войти</router-link></p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../api/axios'

const router = useRouter()

const form = reactive({
  full_name: '',
  phone: '',
  email: '',
  password: ''
})

const error = ref('')
const success = ref(false)
const isLoading = ref(false)

// Автоматическая конвертация телефона
const normalizePhone = () => {
  let val = form.phone.replace(/\s/g, '').replace(/-/g, '').replace(/\(/g, '').replace(/\)/g, '')
  
  // Если начинается с 8 и длина 11 цифр - меняем на +7
  if (val.startsWith('8') && val.length === 11 && val.slice(1).match(/^\d+$/)) {
    form.phone = '+7' + val.slice(1)
  }
  // Если начинается с 7 и длина 11 цифр - добавляем +
  else if (val.startsWith('7') && val.length === 11 && val.slice(1).match(/^\d+$/)) {
    form.phone = '+7' + val.slice(1)
  }
}

const handleRegister = async () => {
  error.value = ''
  success.value = false
  isLoading.value = true
  
  try {
    await apiClient.post('/clients/', {
      full_name: form.full_name,
      phone: form.phone,
      email: form.email,
      password: form.password
    })
    
    success.value = true
    
    // Автоматически входим после регистрации
    setTimeout(async () => {
      try {
        const loginResponse = await apiClient.post('/login', {
          login: form.phone,
          password: form.password,
          role: 'client'
        })
        
        localStorage.setItem('token', loginResponse.data.access_token)
        localStorage.setItem('role', 'client')
        router.push('/dashboard')
      } catch (loginErr) {
        // Если авто-вход не удался, просто перенаправляем на вход
        router.push('/login')
      }
    }, 1500)
    
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка регистрации. Попробуйте позже.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: calc(100vh - 100px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.register-card {
  max-width: 500px;
  width: 100%;
  padding: 40px;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(220, 38, 38, 0.3);
  box-shadow: 0 0 40px rgba(220, 38, 38, 0.1);
}

.register-title {
  font-size: 2rem;
  font-weight: 900;
  margin-bottom: 10px;
  text-align: center;
  color: white;
}

.register-subtitle {
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 30px;
  font-size: 1rem;
}

.form-group {
  margin-bottom: 20px;
}

.input-hint {
  margin-top: 5px;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.5);
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

.success-message {
  margin-top: 15px;
  padding: 12px;
  background: rgba(34, 197, 94, 0.15);
  border: 1px solid rgba(34, 197, 94, 0.4);
  border-radius: 10px;
  color: #4ade80;
  font-size: 0.9rem;
  text-align: center;
}

.login-link {
  margin-top: 25px;
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
}

.login-link a {
  color: #dc2626;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s;
}

.login-link a:hover {
  text-shadow: 0 0 10px rgba(220, 38, 38, 0.5);
}
</style>