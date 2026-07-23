<template>
  <div class="dashboard fade-in">
    <!-- Приветствие и профиль -->
    <div class="profile-section glass-card">
      <div class="profile-header">
        <div>
          <h1 class="profile-name">Привет, {{ profile?.name || 'Клиент' }}! 👋</h1>
          <p class="profile-subtitle">Добро пожаловать в личный кабинет</p>
        </div>
        <div class="profile-stats">
          <div class="stat-item">
            <div class="stat-value neon-text">{{ profile?.discount || 0 }}%</div>
            <div class="stat-label">Ваша скидка</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ profile?.visitCount || 0 }}</div>
            <div class="stat-label">Визитов</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Автомобили -->
    <section class="section">
      <div class="section-header">
        <h2 class="section-title"> Мои автомобили</h2>
        <button @click="showAddCarModal = true" class="btn btn-primary">
          + Добавить авто
        </button>
      </div>

      <div v-if="cars.length === 0" class="empty-state glass-card">
        <p>У вас пока нет добавленных автомобилей</p>
      </div>

      <div v-else class="grid-2">
        <div v-for="car in cars" :key="car.id" class="glass-card car-card">
          <div class="car-header">
            <h3 class="car-name">{{ car.brand_model }}</h3>
            <button @click="deleteCar(car.id)" class="btn-delete">✕</button>
          </div>
          <div class="car-details">
            <p><strong>Гос. номер:</strong> {{ car.license_plate }}</p>
            <p v-if="car.vin"><strong>VIN:</strong> {{ car.vin }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- История заказов -->
    <section class="section">
      <h2 class="section-title">📋 История заказов</h2>

      <div v-if="orders.length === 0" class="empty-state glass-card">
        <p>У вас пока нет заказов</p>
      </div>

      <div v-else class="orders-list">
        <div v-for="order in orders" :key="order.id" class="glass-card order-card">
          <div class="order-header">
            <span class="order-id">Заказ #{{ order.id }}</span>
            <span :class="['status-badge', getStatusClass(order.status)]">
              {{ order.status }}
            </span>
          </div>
          <div class="order-details">
            <div class="order-info">
              <p><strong>Автомобиль:</strong> {{ getCarName(order.car_id) }}</p>
              <p><strong>Дата:</strong> {{ formatDate(order.planned_start) }}</p>
              <p><strong>Сумма:</strong> {{ order.final_cost }} ₽</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Модальное окно добавления авто -->
    <div v-if="showAddCarModal" class="modal-overlay" @click.self="showAddCarModal = false">
      <div class="modal glass-card">
        <h3>Добавить автомобиль</h3>
        <form @submit.prevent="addCar">
          <div class="form-group">
            <label class="form-label">Марка и модель</label>
            <input v-model="newCar.brand_model" class="form-input" required />
          </div>
          <div class="form-group">
            <label class="form-label">Гос. номер</label>
            <input v-model="newCar.license_plate" class="form-input" required />
          </div>
          <div class="form-group">
            <label class="form-label">VIN (необязательно)</label>
            <input v-model="newCar.vin" class="form-input" />
          </div>
          <div class="modal-actions">
            <button type="button" @click="showAddCarModal = false" class="btn btn-outline">
              Отмена
            </button>
            <button type="submit" class="btn btn-primary">
              Добавить
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '../api/axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const profile = ref(null)
const cars = ref([])
const orders = ref([])
const showAddCarModal = ref(false)
const newCar = ref({
  brand_model: '',
  license_plate: '',
  vin: ''
})

// Загрузка данных при монтировании
onMounted(async () => {
  await loadProfile()
  if (profile.value) {
    await loadCars()
    await loadOrders()
  }
})

const loadProfile = async () => {
  try {
    const response = await apiClient.get('/me')
    profile.value = {
      id: response.data.data.id,
      name: response.data.data.name,
      discount: response.data.data.discount,
      visitCount: response.data.data.visitCount
    }
  } catch (error) {
    console.error('Ошибка загрузки профиля:', error)
    router.push('/login')
  }
}

const loadCars = async () => {
  try {
    const response = await apiClient.get(`/clients/${profile.value.id}/cars/`)
    cars.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки автомобилей:', error)
  }
}

const loadOrders = async () => {
  try {
    // Пока используем заглушку, позже добавим endpoint
    orders.value = []
  } catch (error) {
    console.error('Ошибка загрузки заказов:', error)
  }
}

const addCar = async () => {
  try {
    await apiClient.post(`/clients/${profile.value.id}/cars/`, newCar.value)
    showAddCarModal.value = false
    newCar.value = { brand_model: '', license_plate: '', vin: '' }
    await loadCars()
  } catch (error) {
    alert('Ошибка добавления автомобиля')
  }
}

const deleteCar = async (carId) => {
  if (!confirm('Удалить этот автомобиль?')) return
  
  try {
    await apiClient.delete(`/clients/cars/${carId}`, {
      params: { client_id: profile.value.id }
    })
    await loadCars()
  } catch (error) {
    alert('Ошибка удаления автомобиля')
  }
}

const getStatusClass = (status) => {
  const map = {
    'Ожидает': 'status-pending',
    'В работе': 'status-progress',
    'Выполнено': 'status-done',
    'Завершена': 'status-done'
  }
  return map[status] || 'status-pending'
}

const getCarName = (carId) => {
  const car = cars.value.find(c => c.id === carId)
  return car ? car.brand_model : 'Неизвестно'
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.profile-section {
  background: linear-gradient(135deg, rgba(220, 38, 38, 0.1), rgba(0, 0, 0, 0.3));
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}

.profile-name {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 5px;
}

.profile-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.1rem;
}

.profile-stats {
  display: flex;
  gap: 30px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 900;
  color: #dc2626;
  text-shadow: 0 0 20px rgba(220, 38, 38, 0.5);
}

.stat-label {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: rgba(255, 255, 255, 0.5);
  font-size: 1.1rem;
}

.car-card {
  position: relative;
}

.car-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.car-name {
  font-size: 1.3rem;
  font-weight: 700;
}

.btn-delete {
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.4);
  color: #f87171;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-delete:hover {
  background: rgba(239, 68, 68, 0.4);
  transform: scale(1.1);
}

.car-details p {
  margin: 8px 0;
  color: rgba(255, 255, 255, 0.8);
}

.car-details strong {
  color: white;
}

.order-card {
  margin-bottom: 15px;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.order-id {
  font-weight: 700;
  font-size: 1.1rem;
}

.order-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-info p {
  margin: 5px 0;
  color: rgba(255, 255, 255, 0.8);
}

.order-info strong {
  color: white;
}

/* Модальное окно */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  max-width: 500px;
  width: 90%;
  background: rgba(20, 20, 20, 0.95);
}

.modal h3 {
  margin-bottom: 20px;
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 20px;
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 30px;
}
</style>