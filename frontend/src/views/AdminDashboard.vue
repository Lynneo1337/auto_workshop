<template>
  <div class="admin-dashboard fade-in" v-if="isAdmin">
    <div class="page-header">
      <h1 class="page-title">Панель <span class="neon-text">Администратора</span></h1>
      <p class="page-subtitle">Управление заявками, мастерами и боксами</p>
    </div>

    <div class="tabs">
      <button 
        :class="['tab-btn', { active: activeTab === 'orders' }]" 
        @click="activeTab = 'orders'"
      >
         Заявки
      </button>
      <button 
        :class="['tab-btn', { active: activeTab === 'callbacks' }]" 
        @click="activeTab = 'callbacks'"
      >
        📞 Обратные звонки
        <span v-if="unreadCallbacksCount > 0" class="badge">{{ unreadCallbacksCount }}</span>
      </button>
      <button 
        :class="['tab-btn', { active: activeTab === 'reports' }]" 
        @click="activeTab = 'reports'"
      >
        📊 Отчёты
      </button>
    </div>

    <div v-if="activeTab === 'orders'">
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

      <div v-if="showAssignModal" class="modal-overlay" @click.self="showAssignModal = false">
        <div class="modal glass-card">
          <h3>Назначение заявки #{{ selectedOrder?.id }}</h3>
          <div class="order-summary">
            <p>Клиент: <strong>{{ selectedOrder?.client_name }}</strong></p>
            <p>Авто: <strong>{{ selectedOrder?.car_info }}</strong></p>
            <p>Дата: <strong>{{ formatDate(selectedOrder?.planned_start) }}</strong></p>
          </div>
          <form @submit.prevent="assignOrder">
            <div class="form-group">
  <label class="form-label">Мастер</label>
  <select v-model="assignForm.mechanic_id" class="form-input" required>
    <option :value="null" disabled>Выберите мастера...</option>
    <option 
      v-for="m in filteredMechanics" 
      :key="m.id" 
      :value="m.id"
      :disabled="!m.isSuitable"
    >
      {{ m.full_name }} ({{ m.specialization }})
      <template v-if="!m.isSuitable"> ⚠️ Не подходит</template>
    </option>
  </select>
  <p v-if="requiredSpecialization" class="input-hint">
    Требуемая специализация: <strong>{{ requiredSpecialization }}</strong>
  </p>
</div>
            <div class="form-group">
              <label class="form-label">Бокс</label>
              <select v-model="assignForm.bay_id" class="form-input" required>
                <option :value="null" disabled>Выберите бокс...</option>
                <option v-for="b in bays" :key="b.id" :value="b.id">
                  Бокс {{ b.number }} (вместимость: {{ b.capacity }})
                </option>
              </select>
            </div>
            <div class="modal-actions">
              <button type="button" @click="showAssignModal = false" class="btn btn-outline">Отмена</button>
              <button type="submit" class="btn btn-primary" :disabled="isLoading">
                {{ isLoading ? 'Назначение...' : 'Назначить' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <div v-if="showCloseModal" class="modal-overlay" @click.self="showCloseModal = false">
        <div class="modal glass-card">
          <h3>Закрытие заявки #{{ selectedOrder?.id }}</h3>
          <div class="order-summary">
            <p>Клиент: <strong>{{ selectedOrder?.client_name }}</strong></p>
            <p>Авто: <strong>{{ selectedOrder?.car_info }}</strong></p>
            <p>Итоговая сумма: <strong class="neon-text">{{ selectedOrder?.final_cost }} ₽</strong></p>
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
              <button type="submit" class="btn btn-primary" :disabled="isLoading">
                {{ isLoading ? 'Закрытие...' : 'Принять оплату и закрыть' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="activeTab === 'callbacks'">
      <CallbacksTab />
    </div>

    <ReportsTab v-if="activeTab === 'reports'" />
  </div>

  <div v-else class="access-denied fade-in">
    <h2>Доступ запрещен</h2>
    <p>У вас нет прав администратора.</p>
    <router-link to="/" class="btn btn-primary">На главную</router-link>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../api/axios'
import ReportsTab from '../components/ReportsTab.vue'
import CallbacksTab from '../components/CallbacksTab.vue'

const router = useRouter()
const isAdmin = computed(() => localStorage.getItem('role') === 'admin')
const activeTab = ref('orders')

const orders = ref([])
const mechanics = ref([])
const bays = ref([])
const loading = ref(true)
const isLoading = ref(false)

const showAssignModal = ref(false)
const showCloseModal = ref(false)
const selectedOrder = ref(null)

const assignForm = ref({ mechanic_id: null, bay_id: null })
const closeForm = ref({ payment_method: 'Наличные' })

const unreadCallbacksCount = ref(0)

const loadUnreadCallbacksCount = async () => {
  try {
    const response = await apiClient.get('/admin/callbacks/unread-count')
    unreadCallbacksCount.value = response.data.count
  } catch (error) {
    console.error('Ошибка загрузки количества обратных звонков:', error)
  }
}

onMounted(async () => {
  if (!isAdmin.value) return
  await loadData()
  await loadUnreadCallbacksCount()
})

const services = ref([])

const loadData = async () => {
  try {
    const [ordersRes, mechRes, baysRes, servicesRes] = await Promise.all([
      apiClient.get('/admin/orders'),
      apiClient.get('/mechanics/'),
      apiClient.get('/bays/'),
      apiClient.get('/services/')
    ])
    orders.value = ordersRes.data
    mechanics.value = mechRes.data
    bays.value = baysRes.data
    services.value = servicesRes.data
  } catch (error) {
    console.error('Ошибка загрузки данных админа:', error)
  } finally {
    loading.value = false
  }
}

const openAssignModal = (order) => {
  selectedOrder.value = order
  assignForm.value = { mechanic_id: null, bay_id: null }
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
    const payload = {
      mechanic_id: assignForm.value.mechanic_id ? parseInt(assignForm.value.mechanic_id) : null,
      bay_id: assignForm.value.bay_id ? parseInt(assignForm.value.bay_id) : null,
      auto_assign: false
    }
    
    await apiClient.put(`/admin/orders/${selectedOrder.value.id}/assign`, payload)
    showAssignModal.value = false
    await loadData()
  } catch (error) {
    const errorMsg = error.response?.data?.detail || JSON.stringify(error.response?.data) || error.message
    alert('Ошибка назначения: ' + errorMsg)
  } finally {
    isLoading.value = false
  }
}

const closeOrder = async () => {
  isLoading.value = true
  try {
    await apiClient.post(`/orders/${selectedOrder.value.id}/close`, {
      payment_method: closeForm.value.payment_method
    })
    showCloseModal.value = false
    await loadData()
  } catch (error) {
    const errorMsg = error.response?.data?.detail || error.message
    alert('Ошибка закрытия: ' + errorMsg)
  } finally {
    isLoading.value = false
  }
}

const getStatusClass = (status) => {
  const map = {
    'Ожидает': 'status-pending',
    'В работе': 'status-progress',
    'Выполнено': 'status-done',
    'Завершена': 'status-cancelled'
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

const requiredSpecialization = computed(() => {
  if (!selectedOrder.value || !selectedOrder.value.services) return null
  const firstService = selectedOrder.value.services[0]
  const service = services.value.find(s => s.name === firstService.name)
  return service?.req_specialization || null
})

const filteredMechanics = computed(() => {
  return mechanics.value.map(m => ({
    ...m,
    isSuitable: !requiredSpecialization.value || m.specialization === requiredSpecialization.value
  }))
})
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

.page-subtitle {
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.1rem;
}

.tabs {
  display: flex;
  gap: 10px;
}

.tab-btn {
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.tab-btn:hover {
  background: rgba(220, 38, 38, 0.1);
  border-color: rgba(220, 38, 38, 0.3);
  color: white;
}

.tab-btn.active {
  background: linear-gradient(135deg, #dc2626, #991b1b);
  border-color: #dc2626;
  color: white;
  box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
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

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: white;
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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
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
  padding: 40px;
}

.modal h3 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: white;
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

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 14px 18px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: white;
  font-size: 1rem;
  transition: all 0.3s;
  outline: none;
}

.form-input:focus {
  border-color: #dc2626;
  background: rgba(0, 0, 0, 0.5);
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.2);
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 30px;
}

.btn {
  padding: 12px 24px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  text-decoration: none;
}

.btn-primary {
  background: linear-gradient(135deg, #dc2626, #991b1b);
  color: white;
  box-shadow: 0 4px 15px rgba(220, 38, 38, 0.3);
}

.btn-primary:hover {
  background: linear-gradient(135deg, #ef4444, #b91c1c);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(220, 38, 38, 0.5);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-outline {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
}

.btn-outline:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: #dc2626;
  color: #ef4444;
}

.btn-sm {
  padding: 8px 16px;
  font-size: 0.85rem;
}

.neon-text {
  color: #dc2626;
  text-shadow: 0 0 10px rgba(220, 38, 38, 0.5);
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: inline-block;
}

.status-pending {
  background: rgba(234, 179, 8, 0.15);
  color: #facc15;
  border: 1px solid rgba(234, 179, 8, 0.3);
}

.status-progress {
  background: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.status-done {
  background: rgba(34, 197, 94, 0.15);
  color: #4ade80;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.status-cancelled {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.access-denied {
  text-align: center;
  padding: 100px 20px;
}

.access-denied h2 {
  font-size: 2rem;
  margin-bottom: 20px;
  color: #dc2626;
}

.access-denied p {
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 30px;
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

.fade-in {
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.badge {
  display: inline-block;
  margin-left: 8px;
  padding: 2px 8px;
  background: #dc2626;
  color: white;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 700;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .data-table {
    font-size: 0.85rem;
  }
  
  .data-table th,
  .data-table td {
    padding: 10px;
  }
}
</style>