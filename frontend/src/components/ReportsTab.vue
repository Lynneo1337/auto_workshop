<template>
  <div class="reports-section fade-in">
    <div class="reports-header">
      <h2 class="section-title">📊 Отчёты и аналитика</h2>
      <div class="date-filters">
        <div class="form-group">
          <label class="form-label">С</label>
          <input v-model="startDate" type="date" class="form-input" />
        </div>
        <div class="form-group">
          <label class="form-label">По</label>
          <input v-model="endDate" type="date" class="form-input" />
        </div>
        <button @click="loadReports" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Загрузка...' : 'Обновить' }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
    </div>

    <div v-else class="reports-grid">
      <div class="glass-card report-card">
        <div class="report-icon">💰</div>
        <h3 class="report-title">Выручка за период</h3>
        <div class="report-value neon-text">{{ formatMoney(revenue.total_revenue) }} ₽</div>
        <div class="report-subtitle">Закрытых заказов: {{ revenue.total_orders }}</div>
      </div>

      <div class="glass-card report-card full-width">
        <h3 class="report-title"> Загрузка мастеров</h3>
        <div v-if="mechanicsLoad.length === 0" class="empty-report">
          Нет данных за выбранный период
        </div>
        <table v-else class="data-table">
          <thead>
            <tr>
              <th>Мастер</th>
              <th>Специализация</th>
              <th>Выполнено заказов</th>
              <th>Выручка</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="mechanic in mechanicsLoad" :key="mechanic.mechanic_id">
              <td>{{ mechanic.full_name }}</td>
              <td>{{ mechanic.specialization }}</td>
              <td>{{ mechanic.orders_count }}</td>
              <td class="price-cell">{{ formatMoney(mechanic.total_revenue) }} ₽</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Популярные услуги -->
      <div class="glass-card report-card full-width">
        <h3 class="report-title"> Популярные услуги</h3>
        <div v-if="popularServices.length === 0" class="empty-report">
          Нет данных за выбранный период
        </div>
        <table v-else class="data-table">
          <thead>
            <tr>
              <th>Услуга</th>
              <th>Количество заказов</th>
              <th>Выручка</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in popularServices" :key="service.service_name">
              <td>{{ service.service_name }}</td>
              <td>{{ service.total_quantity }}</td>
              <td class="price-cell">{{ formatMoney(service.total_revenue) }} ₽</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Список клиентов со скидкой -->
      <div v-if="discountedClients.clients.length > 0" class="glass-card report-card full-width">
        <h3 class="report-title"> Клиенты со скидкой</h3>
        <table class="data-table">
          <thead>
            <tr>
              <th>ФИО</th>
              <th>Телефон</th>
              <th>Визитов</th>
              <th>Скидка</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="client in discountedClients.clients" :key="client.id">
              <td>{{ client.full_name }}</td>
              <td>{{ client.phone }}</td>
              <td>{{ client.visit_count }}</td>
              <td class="discount-cell">{{ client.current_discount }}%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '../api/axios'

const loading = ref(false)
const startDate = ref('')
const endDate = ref('')
const revenue = ref({ total_revenue: 0, total_orders: 0 })
const mechanicsLoad = ref([])
const popularServices = ref([])
const discountedClients = ref({ total_discounted_clients: 0, clients: [] })

onMounted(() => {
  const today = new Date()
  const firstDay = new Date(today.getFullYear(), today.getMonth(), 1)
  
  startDate.value = firstDay.toISOString().split('T')[0]
  endDate.value = today.toISOString().split('T')[0]
  
  loadReports()
})

const loadReports = async () => {
  loading.value = true
  
  try {
    const start = new Date(startDate.value).toISOString()
    const end = new Date(endDate.value).toISOString()
    
    const [revenueRes, mechanicsRes, popularRes, discountedRes] = await Promise.all([
      apiClient.get('/reports/revenue', { params: { start_date: start, end_date: end } }),
      apiClient.get('/reports/mechanics-load', { params: { start_date: start, end_date: end } }),
      apiClient.get('/reports/popular-services', { params: { start_date: start, end_date: end, limit: 10 } }),
      apiClient.get('/reports/discounted-clients')
    ])
    
    revenue.value = revenueRes.data
    mechanicsLoad.value = mechanicsRes.data
    popularServices.value = popularRes.data
    discountedClients.value = discountedRes.data
  } catch (error) {
    console.error('Ошибка загрузки отчётов:', error)
  } finally {
    loading.value = false
  }
}

const formatMoney = (amount) => {
  return parseFloat(amount || 0).toLocaleString('ru-RU', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}
</script>

<style scoped>
.reports-section {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.reports-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-wrap: wrap;
  gap: 20px;
}

.date-filters {
  display: flex;
  gap: 15px;
  align-items: flex-end;
  flex-wrap: wrap;
}

.date-filters .form-group {
  margin-bottom: 0;
}

.date-filters .form-input {
  width: 150px;
}

.reports-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
}

.report-card {
  padding: 30px;
  text-align: center;
}

.report-card.full-width {
  grid-column: 1 / -1;
  text-align: left;
}

.report-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.report-title {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 15px;
  font-weight: 500;
}

.report-value {
  font-size: 2.5rem;
  font-weight: 900;
  margin-bottom: 10px;
}

.report-subtitle {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.9rem;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  color: white;
  margin-top: 20px;
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
}

.data-table tr:hover td {
  background: rgba(255, 255, 255, 0.02);
}

.price-cell {
  font-weight: 700;
  color: #dc2626;
}

.discount-cell {
  font-weight: 700;
  color: #4ade80;
}

.empty-report {
  text-align: center;
  padding: 40px;
  color: rgba(255, 255, 255, 0.5);
}

.loading-state {
  padding: 60px;
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

@media (max-width: 768px) {
  .reports-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .date-filters {
    flex-direction: column;
  }
  
  .date-filters .form-input {
    width: 100%;
  }
}
</style>