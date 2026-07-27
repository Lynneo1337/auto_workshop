<template>
  <div class="callbacks-section fade-in">
    
    <div class="section-header">
      <h2 class="section-title"> Обратные звонки</h2>
      <div class="stats">
        <span class="stat-item">
          Всего: <strong>{{ callbacks.length }}</strong>
        </span>
        <span class="stat-item pending">
          Ожидают: <strong>{{ pendingCount }}</strong>
        </span>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
    </div>

    <div v-else-if="callbacks.length === 0" class="glass-card empty-state">
      <p>Нет заявок на обратный звонок</p>
    </div>

    <div v-else class="callbacks-list">
      <div v-for="callback in callbacks" :key="callback.id" class="glass-card callback-card">
        <div class="callback-header">
          <div class="callback-info">
            <h3 class="callback-name">{{ callback.client_name }}</h3>
            <p class="callback-phone">📱 {{ callback.phone }}</p>
          </div>
          <span :class="['status-badge', callback.status === 'Ожидает обработки' ? 'status-pending' : 'status-done']">
            {{ callback.status }}
          </span>
        </div>
        
        <div class="callback-date">
          Создана: {{ formatDate(callback.created_at) }}
        </div>

        <div class="callback-actions">
          <button 
            v-if="callback.status === 'Ожидает обработки'"
            @click="markAsProcessed(callback.id)"
            class="btn btn-primary btn-sm"
            :disabled="processingId === callback.id"
          >
            {{ processingId === callback.id ? 'Обработка...' : '✓ Обработано' }}
          </button>
          <button 
            v-else
            @click="markAsPending(callback.id)"
            class="btn btn-outline btn-sm"
          >
            Вернуть в ожидание
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import apiClient from '../api/axios'

const callbacks = ref([])
const loading = ref(true)
const processingId = ref(null)

onMounted(async () => {
  console.log('🔔 CallbacksTab: компонент смонтирован, начинаем загрузку...')
  await loadCallbacks()
})

const loadCallbacks = async () => {
  try {
    console.log('🔔 CallbacksTab: отправляем запрос на /admin/callbacks')
    const response = await apiClient.get('/admin/callbacks')
    console.log('🔔 CallbacksTab: получен ответ от сервера:', response.data)
    
    callbacks.value = response.data
    console.log('🔔 CallbacksTab: значение callbacks.value установлено, длина:', callbacks.value.length)
  } catch (error) {
    console.error('❌ CallbacksTab: ошибка загрузки обратных звонков:', error)
  } finally {
    loading.value = false
    console.log('🔔 CallbacksTab: загрузка завершена, loading = false')
  }
}

const pendingCount = computed(() => {
  const count = callbacks.value.filter(c => c.status === 'Ожидает обработки').length
  console.log('🔔 CallbacksTab: подсчитано ожидающих:', count)
  return count
})

const markAsProcessed = async (id) => {
  processingId.value = id
  try {
    await apiClient.put(`/admin/callbacks/${id}/status?status=Обработана`)
    await loadCallbacks()
  } catch (error) {
    alert('Ошибка обновления статуса')
  } finally {
    processingId.value = null
  }
}

const markAsPending = async (id) => {
  try {
    await apiClient.put(`/admin/callbacks/${id}/status?status=Ожидает обработки`)
    await loadCallbacks()
  } catch (error) {
    alert('Ошибка обновления статуса')
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.callbacks-section {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}

.stats {
  display: flex;
  gap: 20px;
}

.stat-item {
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.95rem;
}

.stat-item strong {
  color: white;
  font-size: 1.2rem;
}

.stat-item.pending {
  background: rgba(234, 179, 8, 0.15);
  border: 1px solid rgba(234, 179, 8, 0.3);
}

.stat-item.pending strong {
  color: #facc15;
}

.callbacks-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.callback-card {
  padding: 25px;
}

.callback-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
  gap: 15px;
}

.callback-name {
  font-size: 1.3rem;
  font-weight: 700;
  color: white;
  margin-bottom: 8px;
}

.callback-phone {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1rem;
}

.callback-date {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.85rem;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.callback-actions {
  display: flex;
  gap: 10px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: rgba(255, 255, 255, 0.5);
  font-size: 1.1rem;
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
  .callbacks-list {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>