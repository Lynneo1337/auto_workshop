<template>
  <div class="admin-dashboard fade-in" v-if="isAdmin">
    <div class="page-header">
      <h1 class="page-title">Панель <span class="neon-text">Администратора</span></h1>
      <p class="page-subtitle">Управление заявками, мастерами и боксами</p>
    </div>

    <!-- Статистика сверху -->
    <div class="stats-grid">
      <div class="glass-card stat-card">
        <div class="stat-value neon-text">{{ orders.filter(o => o.status === 'Ожидает').length }}</div>
        <div class="stat-label">Ожидают назначения</div>
      </div>
      <div class="glass-card stat-card">
        <div class="stat-value" style="color: #60a5fa">{{ orders.filter(o => o.status === 'В работе').length }}</div>
        <div class="stat-label">В работе</div>
      </div>
      <div class="glass-card stat-card">
        <div class="stat-value" style="color: #4ade80">{{ orders.filter(o => o.status === 'Выполнено').length }}</div>
        <div class="stat-label">Готовы к закрытию</div>
      </div>
    </div>

    <!-- Таблица заявок -->
    <div class="glass-card table-container">
      <h2 class="section-title">Все заявки</h2>
      
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
      </div>

      <table v-else class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Клиент / Авто</th>
            <th>Статус</th>
            <th>Мастер / Бокс</th>
            <th>Дата</th>
            <th>Сумма</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orders" :key="order.id">
            <td>#{{ order.id }}</td>
            <td>
              <div class="client-info">{{ order.client_name }}</div>
              <div class="car-info">{{ order.car_info }}</div>
            </td>
            <td>
              <span :class="['status-badge', getStatusClass(order.status)]">
                {{ order.status }}
              </span>
            </td>
            <td>
              <div>{{ order.mechanic_name }}</div>
              <div class="sub-text">Бокс {{ order.bay_number }}</div>
            </td>
            <td>{{ formatDate(order.planned_start) }}</td>
            <td class="price-cell">{{ order.final_cost }} ₽</td>
            <td class="actions-cell">
              <button 
                v-if="order.status === 'Ожидает'" 
                @click="openAssignModal(order)" 
                class="btn btn-primary btn-sm"
              >
                Назначить
              </button>
              <button 
                v-if="order.status === 'Выполнено'" 
                @click="openCloseModal(order)" 
                class="btn btn-outline btn-sm"
                style="border-color: #4ade80; color: #4ade80;"
              >
                Закрыть
              </button>
              <span v-if="['В работе', 'Завершена'].includes(order.status)" class="sub-text">
                {{ order.status === 'Завершена' ? 'Архив' : 'В процессе' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Модальное окно: Назначение (ФТ2, ФТ4) -->
    <div v-if="showAssignModal" class="modal-overlay" @click.self="showAssignModal = false">
      <div class="modal glass-card">
        <h3>Назначение заявки #{{ selectedOrder?.id }}</h3>
        <form @submit.prevent="assignOrder">
          <div class="form-group">
            <label class="form-label">Выберите мастера</label>
            <select v-model="assignForm.mechanic_id" class="form-input" required>
              <option value="" disabled>Выберите мастера...</option>
              <option v-for="m in mechanics" :key="m.id" :value="m.id">
                {{ m.full_name }} ({{ m.specialization }})
              </option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Выберите бокс</label>
            <select v-model="assignForm.bay_id" class="form-input" required>
              <option value="" disabled>Выберите бокс...</option>
              <option v-for="b in bays" :key="b.id" :value="b.id">
                Бокс {{ b.number }} (Вместимость: {{ b.capacity }})
              </option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showAssignModal = false" class="btn btn-outline">Отмена</button>
            <button type="submit" class="btn btn-primary" :disabled="isLoading">Назначить</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Модальное окно: Закрытие (ФТ3) -->
    <div v-if="showCloseModal" class="modal-overlay" @click.self="showCloseModal = false">
      <div class="modal glass-card">
        <h3>Закрытие заявки #{{ selectedOrder?.id }}</h3>
        <div class="order-summary">
          <p>Клиент: <strong>{{ selectedOrder?.client_name }}</strong></p>
          <p>Итоговая сумма (со скидкой): <strong class="neon-text">{{ selectedOrder?.final_cost }} ₽</strong></p>
        </div>
        <form @submit.prevent="closeOrder">
          <div class="form-group">
            <label class="form-label">Способ оплаты</label>
            <select v-model="closeForm.payment_method" class="form-input" required>
              <option value="Наличные">Наличные</option>
              <option value="Карта">Карта</option>
              <option value="Безналичный расчет">Безналичный расчет</option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showCloseModal = false" class="btn btn-outline">Отмена</button>
            <button type="submit" class="btn btn-primary" :disabled="isLoading">Принять оплату и закрыть</button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <div v-else class="access-denied fade-in">
    <h2>Доступ запрещен</h2>
    <p>У вас нет прав администратора.</p>
    <router-link to="/" class="btn btn-primary">На главную</router-link>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../api/axios'

const router = useRouter()
const isAdmin = computed(() => localStorage.getItem('role') === 'admin')

const orders = ref([])
const mechanics = ref([])
const bays = ref([])
const loading = ref(true)
const isLoading = ref(false)

const showAssignModal = ref(false)
const showCloseModal = ref(false)
const selectedOrder = ref(null)

const assignForm = ref({ mechanic_id: '', bay_id: '' })
const closeForm = ref({ payment_method: 'Наличные' })

onMounted(async () => {
  if (!isAdmin.value) return
  await loadData()
})

const loadData = async () => {
  try {
    const [ordersRes, mechRes, baysRes] = await Promise.all([
      apiClient.get('/admin/orders'),
      apiClient.get('/mechanics/'), // Предполагаем, что такой endpoint есть или создадим простой
      apiClient.get('/bays/')
    ])
    orders.value = ordersRes.data
    mechanics.value = mechRes.data
    bays.value = baysRes.data
  } catch (error) {
    console.error('Ошибка загрузки данных админа:', error)
  } finally {
    loading.value = false
  }
}

const openAssignModal = (order) => {
  selectedOrder.value = order
  assignForm.value = { mechanic_id: '', bay_id: '' }
  showAssignModal.value = true
}

const openCloseModal = (order) => {
  selectedOrder.value = order
  closeForm.value = { payment_method: 'Наличные' }
  showCloseModal.value = true
}

const assignOrder = async () => {
  isLoading.value = true
  try {
    await apiClient.put(`/admin/orders/${selectedOrder.value.id}/assign`, assignForm.value)
    showAssignModal.value = false
    await loadData() // Обновляем таблицу
  } catch (error) {
    alert('Ошибка назначения: ' + (error.response?.data?.detail || error.message))
  } finally {
    isLoading.value = false
  }
}

const closeOrder = async () => {
  isLoading.value = true
  try {
    await apiClient.post(`/orders/${selectedOrder.value.id}/close`, closeForm.value)
    showCloseModal.value = false
    await loadData() // Обновляем таблицу (скидка клиента уже пересчитана на бэкенде!)
  } catch (error) {
    alert('Ошибка закрытия: ' + (error.response?.data?.detail || error.message))
  } finally {
    isLoading.value = false
  }
}

const getStatusClass = (status) => {
  const map = {
    'Ожидает': 'status-pending',
    'В работе': 'status-progress',
    'Выполнено': 'status-done',
    'Завершена': 'status-cancelled' // Используем красный/серый для архива
  }
  return map[status] || 'status-pending'
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('ru-RU', { day: '2-digit', month: '2-digit', hour: '2-digit', minute:'2-digit' })
}
</script>

<style scoped>
.admin-dashboard {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.page-header {
  text-align: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 900;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  text-align: center;
  padding: 25px;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 900;
}

.stat-label {
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 1px;
  margin-top: 5px;
}

.table-container {
  padding: 30px;
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  color: white;
}

.data-table th {
  text-align: left;
  padding: 15px;
  border-bottom: 2px solid rgba(220, 38, 38, 0.3);
  color: rgba(255, 255, 255, 0.7);
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.85rem;
}

.data-table td {
  padding: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  vertical-align: middle;
}

.data-table tr:hover td {
  background: rgba(255, 255, 255, 0.02);
}

.client-info {
  font-weight: 600;
  color: white;
}

.car-info {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.6);
  margin-top: 4px;
}

.sub-text {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 4px;
}

.price-cell {
  font-weight: 700;
  color: #dc2626;
}

.actions-cell {
  display: flex;
  gap: 8px;
  flex-direction: column;
}

.modal {
  max-width: 500px;
  width: 90%;
  background: rgba(20, 20, 20, 0.95);
  padding: 40px;
}

.order-summary {
  background: rgba(220, 38, 38, 0.1);
  border: 1px solid rgba(220, 38, 38, 0.3);
  border-radius: 10px;
  padding: 15px;
  margin-bottom: 25px;
}

.order-summary p {
  margin: 8px 0;
  color: rgba(255, 255, 255, 0.8);
}

.access-denied {
  text-align: center;
  padding: 100px 20px;
}

.loading-state {
  padding: 40px;
  text-align: center;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(220, 38, 38, 0.2);
  border-top-color: #dc2626;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>