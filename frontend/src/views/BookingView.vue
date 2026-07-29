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
  <label class="form-label">Услуги</label>
  <div v-for="(service, index) in selectedServices" :key="index" class="service-row">
    <select v-model="service.service_id" class="form-input service-select" required>
      <option value="" disabled>Выберите услугу...</option>
      <option v-for="s in services" :key="s.id" :value="s.id">
        {{ s.name }} - {{ s.price }} ₽
      </option>
    </select>
    <button 
      v-if="selectedServices.length > 1" 
      type="button" 
      @click="removeService(index)" 
      class="btn-remove"
    >
      ✕
    </button>
  </div>
  <button type="button" @click="addService" class="btn btn-outline btn-sm" style="margin-top: 10px;">
    + Добавить услугу
  </button>
</div>

<div class="grid-2">
  <div class="form-group">
    <label class="form-label">Дата и время начала</label>
    <input 
      v-model="form.planned_start" 
      type="datetime-local" 
      class="form-input" 
      :min="minDateTime"
      required 
    />
  </div>
  <div class="form-group">
    <label class="form-label">Общая длительность (часов)</label>
    <input 
      :value="totalDuration" 
      type="text" 
      class="form-input" 
      readonly
      style="background: rgba(255, 255, 255, 0.05); cursor: not-allowed;"
    />
    <p class="input-hint">Рассчитано автоматически на основе выбранных услуг</p>
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
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../api/axios'

const minDateTime = computed(() => {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day}T${hours}:${minutes}`
})

const totalDuration = computed(() => {
  let total = 0
  selectedServices.value.forEach(s => {
    if (s.service_id) {
      const service = services.value.find(srv => srv.id === parseInt(s.service_id))
      if (service) {
        total += service.duration_hours || 1
      }
    }
  })
  return total || 1 // Минимум 1 час
})

const router = useRouter()
const cars = ref([])
const services = ref([])
const isLoading = ref(false)
const error = ref('')
const success = ref(false)

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
    
    console.log('ID клиента:', clientId)
    console.log('Автомобили:', cars.value)
    console.log('Услуги:', services.value)
  } catch (err) {
    console.error('Ошибка загрузки данных:', err)
    error.value = 'Ошибка загрузки данных'
  }
})

const form = reactive({
  car_id: '',
  planned_start: '',
  duration: 2
})

const selectedServices = ref([{ service_id: '', quantity: 1 }])

const addService = () => {
  selectedServices.value.push({ service_id: '', quantity: 1 })
}

const removeService = (index) => {
  selectedServices.value.splice(index, 1)
}

const submitBooking = async () => {
  isLoading.value = true
  error.value = ''
  success.value = false
  
  const startDate = new Date(form.planned_start)
  const now = new Date()
  
  if (startDate < now) {
    error.value = 'Нельзя выбрать прошедшую дату и время'
    isLoading.value = false
    return
  }
  
const endDate = new Date(startDate.getTime() + totalDuration.value * 60 * 60 * 1000)
  
  const items = selectedServices.value
    .filter(s => s.service_id)
    .map(s => ({
      service_id: parseInt(s.service_id),
      quantity: s.quantity
    }))
  
  if (items.length === 0) {
    error.value = 'Выберите хотя бы одну услугу'
    isLoading.value = false
    return
  }
  
  const payload = {
    client_id: 0, 
    car_id: parseInt(form.car_id),
    planned_start: startDate.toISOString(),
    planned_end: endDate.toISOString(),
    items: items
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

.service-row {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.service-select {
  flex: 1;
}

.btn-remove {
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.4);
  color: #f87171;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-remove:hover {
  background: rgba(239, 68, 68, 0.4);
  transform: scale(1.05);
}

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