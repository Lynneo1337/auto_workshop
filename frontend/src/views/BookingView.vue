<template>
  <div class="booking-page fade-in">
    <div class="page-header">
      <h1 class="page-title">Онлайн <span class="neon-text">запись</span></h1>
      <p class="page-subtitle">Выберите автомобиль, услугу и удобное время</p>
    </div>

    <div v-if="cars.length === 0" class="glass-card empty-state">
      <p>У вас нет привязанных автомобилей. Добавьте авто в личном кабинете.</p>
      <router-link to="/dashboard" class="btn btn-primary" style="margin-top: 20px;">В личный кабинет</router-link>
    </div>

    <div v-else class="glass-card booking-form">
      <form @submit.prevent="submitBooking">
        <div class="form-group">
          <label class="form-label">Ваш автомобиль</label>
          <select v-model="form.car_id" class="form-input" required>
            <option value="" disabled>Выберите авто...</option>
            <option v-for="car in cars" :key="car.id" :value="car.id">
              {{ car.brand_model }} ({{ car.license_plate }})
            </option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label">Услуга</label>
          <select v-model="form.service_id" class="form-input" required>
            <option value="" disabled>Выберите услугу...</option>
            <option v-for="service in services" :key="service.id" :value="service.id">
              {{ service.name }} - {{ service.price }} ₽
            </option>
          </select>
        </div>

        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">Дата и время начала</label>
            <input v-model="form.planned_start" type="datetime-local" class="form-input" required />
          </div>
          <div class="form-group">
            <label class="form-label">Длительность (часов)</label>
            <input v-model.number="form.duration" type="number" min="1" max="8" class="form-input" required />
          </div>
        </div>

        <button type="submit" class="btn btn-primary btn-full" :disabled="isLoading">
          {{ isLoading ? 'Оформление...' : 'Подтвердить запись' }}
        </button>

        <div v-if="error" class="error-message">{{ error }}</div>
        <div v-if="success" class="success-message">Заявка успешно создана! Ожидайте подтверждения от администратора.</div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../api/axios'

const router = useRouter()
const cars = ref([])
const services = ref([])
const isLoading = ref(false)
const error = ref('')
const success = ref(false)

const form = reactive({
  car_id: '',
  service_id: '',
  planned_start: '',
  duration: 2
})

onMounted(async () => {
  if (!localStorage.getItem('token')) {
    router.push('/login')
    return
  }
  
  try {
    const profileRes = await apiClient.get('/me')
    const clientId = profileRes.data.data.id
    
    const [carsRes, servicesRes] = await Promise.all([
      apiClient.get(`/clients/${clientId}/cars/`),
      apiClient.get('/services/')
    ])
    
    cars.value = carsRes.data
    services.value = servicesRes.data
  } catch (err) {
    error.value = 'Ошибка загрузки данных'
  }
})

const submitBooking = async () => {
  isLoading.value = true
  error.value = ''
  success.value = false
  
  const startDate = new Date(form.planned_start)
  const endDate = new Date(startDate.getTime() + form.duration * 60 * 60 * 1000)
  
  const payload = {
    client_id: 0, 
    car_id: parseInt(form.car_id),
    planned_start: startDate.toISOString(),
    planned_end: endDate.toISOString(),
    items: [{ service_id: parseInt(form.service_id), quantity: 1 }]
  }
  
  try {
    const profileRes = await apiClient.get('/me')
    payload.client_id = profileRes.data.data.id
    
    await apiClient.post('/orders/', payload)
    success.value = true
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка при создании заявки. Возможно, слот занят.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.booking-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 900;
}

.page-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.1rem;
}

.booking-form {
  padding: 40px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: rgba(255, 255, 255, 0.7);
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
  text-align: center;
}

.success-message {
  margin-top: 15px;
  padding: 12px;
  background: rgba(34, 197, 94, 0.15);
  border: 1px solid rgba(34, 197, 94, 0.4);
  border-radius: 10px;
  color: #4ade80;
  text-align: center;
}
</style>