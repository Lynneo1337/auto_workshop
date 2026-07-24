<template>
  <div class="mechanic-dashboard fade-in" v-if="isMechanic">
    <div class="page-header">
      <h1 class="page-title">Мои <span class="neon-text">заявки</span></h1>
      <p class="page-subtitle">Список назначенных работ</p>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
    </div>

    <div v-else-if="orders.length === 0" class="glass-card empty-state">
      <p>На данный момент нет назначенных заявок</p>
    </div>

    <div v-else class="orders-list">
      <div v-for="order in orders" :key="order.id" class="glass-card order-card">
        <div class="order-header">
          <div>
            <span class="order-id">Заявка #{{ order.id }}</span>
            <span :class="['status-badge', getStatusClass(order.status)]">
              {{ order.status }}
            </span>
          </div>
          <div class="order-date">{{ formatDate(order.planned_start) }}</div>
        </div>

        <div class="order-body">
          <div class="client-info">
            <div class="info-label">Клиент:</div>
            <div class="info-value">{{ order.client_name }}</div>
          </div>
          <div class="car-info">
            <div class="info-label">Автомобиль:</div>
            <div class="info-value">{{ order.car_info }}</div>
          </div>
          <div class="services-info">
            <div class="info-label">Работы:</div>
            <ul class="services-list">
              <li v-for="(service, idx) in order.services" :key="idx">
                {{ service.name }} (x{{ service.quantity }})
              </li>
            </ul>
          </div>
        </div>

        <div class="order-footer">
          <button 
            v-if="order.status === 'В работе'" 
            @click="openCompleteModal(order)" 
            class="btn btn-primary"
          >
            ✓ Отметить выполненным
          </button>
          <span v-else class="sub-text">Ожидает начала работ</span>
        </div>
      </div>
    </div>

    <div v-if="showCompleteModal" class="modal-overlay" @click.self="showCompleteModal = false">
      <div class="modal glass-card">
        <h3>Завершение работ #{{ selectedOrder?.id }}</h3>
        <form @submit.prevent="completeOrder">
          <div class="form-group">
            <label class="form-label">Комментарий (необязательно)</label>
            <textarea 
              v-model="completeForm.comment" 
              class="form-input" 
              rows="3"
              placeholder="Например: заменены все детали, проведена диагностика..."
            ></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showCompleteModal = false" class="btn btn-outline">Отмена</button>
            <button type="submit" class="btn btn-primary" :disabled="isLoading">
              {{ isLoading ? 'Сохранение...' : 'Подтвердить' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <div v-else class="access-denied fade-in">
    <h2>Доступ запрещен</h2>
    <p>Эта страница доступна только мастерам</p>
    <router-link to="/" class="btn btn-primary">На главную</router-link>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../api/axios'

const router = useRouter()
const isMechanic = computed(() => localStorage.getItem('role') === 'mechanic')

const orders = ref([])
const loading = ref(true)
const isLoading = ref(false)
const showCompleteModal = ref(false)
const selectedOrder = ref(null)
const completeForm = ref({ comment: '' })

const mechanicId = ref(null)

onMounted(async () => {
  if (!isMechanic.value) return
  
  try {
    const response = await apiClient.get('/me')
    mechanicId.value = response.data.data.id
    await loadOrders()
  } catch (error) {
    console.error('Ошибка получения данных мастера:', error)
  } finally {
    loading.value = false
  }
})

const loadOrders = async () => {
  try {
    const response = await apiClient.get('/mechanic/orders', {
      params: { mechanic_id: mechanicId.value }
    })
    orders.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки заявок:', error)
  }
}

const openCompleteModal = (order) => {
  selectedOrder.value = order
  completeForm.value = { comment: '' }
  showCompleteModal.value = true
}

const completeOrder = async () => {
  isLoading.value = true
  try {
    await apiClient.post(
      `/mechanic/orders/${selectedOrder.value.id}/complete`,
      { ...completeForm.value },
      {
        params: { mechanic_id: mechanicId.value }
      }
    )
    showCompleteModal.value = false
    await loadOrders()
  } catch (error) {
    const errorMsg = error.response?.data?.detail || 
                     error.message || 
                     JSON.stringify(error)
    alert('Ошибка: ' + errorMsg)
  } finally {
    isLoading.value = false
  }
}

const getStatusClass = (status) => {
  const map = {
    'Ожидает': 'status-pending',
    'В работе': 'status-progress',
    'Выполнено': 'status-done'
  }
  return map[status] || 'status-pending'
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.mechanic-dashboard {
  max-width: 1000px;
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

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.order-card {
  padding: 30px;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.order-id {
  font-size: 1.3rem;
  font-weight: 700;
  margin-right: 15px;
}

.order-date {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.95rem;
}

.order-body {
  margin-bottom: 25px;
}

.info-label {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.85rem;
  margin-bottom: 5px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  color: white;
  font-size: 1.1rem;
  margin-bottom: 20px;
}

.services-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.services-list li {
  padding: 8px 0;
  color: rgba(255, 255, 255, 0.8);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.services-list li:last-child {
  border-bottom: none;
}

.order-footer {
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal {
  max-width: 500px;
  width: 90%;
  background: rgba(20, 20, 20, 0.95);
  padding: 40px;
}

.modal h3 {
  margin-bottom: 25px;
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 20px;
}

textarea.form-input {
  resize: vertical;
  min-height: 100px;
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 30px;
}

.access-denied {
  text-align: center;
  padding: 100px 20px;
}

.loading-state {
  padding: 80px 20px;
  text-align: center;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(220, 38, 38, 0.2);
  border-top-color: #dc2626;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.1rem;
}
</style>