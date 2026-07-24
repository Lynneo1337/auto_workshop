<template>
  <div class="services-page fade-in">
    <div class="page-header">
      <h1 class="page-title">Наши <span class="neon-text">услуги</span></h1>
      <p class="page-subtitle">
        Полный спектр услуг по ремонту и обслуживанию автомобилей
      </p>
    </div>

    <!-- Фильтр по специализации -->
    <div class="filter-section">
      <label class="form-label">Фильтр по специализации:</label>
      <select v-model="selectedSpecialization" class="form-input filter-select">
        <option value="">Все услуги</option>
        <option v-for="spec in specializations" :key="spec" :value="spec">
          {{ spec }}
        </option>
      </select>
    </div>

    <!-- Список услуг -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Загрузка услуг...</p>
    </div>

    <div v-else-if="filteredServices.length === 0" class="empty-state glass-card">
      <p>Услуги пока не добавлены</p>
    </div>

    <div v-else class="services-grid">
      <div 
        v-for="service in filteredServices" 
        :key="service.id" 
        class="glass-card service-card"
      >
        <div class="service-header">
          <h3 class="service-name">{{ service.name }}</h3>
          <div class="service-price">{{ formatPrice(service.price) }} ₽</div>
        </div>
        
        <div v-if="service.req_specialization" class="service-spec">
          <span class="spec-label">Специализация:</span>
          <span class="spec-value">{{ service.req_specialization }}</span>
        </div>
        
        <div class="service-footer">
  <router-link :to="isLoggedIn ? '/booking' : '/login'" class="btn btn-primary btn-sm">
    Записаться
  </router-link>
</div>
      </div>
    </div>

    <!-- CTA секция -->
    <section class="cta-section glass-card">
      <h2>Не нашли нужную услугу?</h2>
      <p>Свяжитесь с нами, и мы поможем решить вашу задачу</p>
      <div class="cta-buttons">
        <button @click="$router.push('/')" class="btn btn-primary">
           Заказать звонок
        </button>
        <router-link to="/register" class="btn btn-outline">
          Создать аккаунт
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import apiClient from '../api/axios'

const services = ref([])
const loading = ref(true)
const selectedSpecialization = ref('')
const isLoggedIn = ref(false)

// Загрузка услуг
onMounted(async () => {
  try {
    const response = await apiClient.get('/services/')
    services.value = response.data
    isLoggedIn.value = !!localStorage.getItem('token')
  } catch (error) {
    console.error('Ошибка загрузки услуг:', error)
  } finally {
    loading.value = false
  }
})

// Получаем уникальные специализации
const specializations = computed(() => {
  const specs = services.value
    .map(s => s.req_specialization)
    .filter(Boolean)
  return [...new Set(specs)]
})

// Фильтруем услуги
const filteredServices = computed(() => {
  if (!selectedSpecialization.value) {
    return services.value
  }
  return services.value.filter(s => s.req_specialization === selectedSpecialization.value)
})

const formatPrice = (price) => {
  return parseFloat(price).toLocaleString('ru-RU')
}
</script>

<style scoped>
.services-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 50px;
  padding: 40px 20px;
  background: linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(10, 10, 10, 0.5) 100%);
  border-radius: 30px;
  border: 1px solid rgba(220, 38, 38, 0.2);
}

.page-title {
  font-size: 3rem;
  font-weight: 900;
  margin-bottom: 15px;
}

.page-subtitle {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.7);
  max-width: 600px;
  margin: 0 auto;
}

/* Фильтр */
.filter-section {
  margin-bottom: 40px;
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.filter-select {
  max-width: 300px;
  flex: 1;
}

/* Сетка услуг */
.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
  margin-bottom: 60px;
}

.service-card {
  padding: 30px;
  transition: all 0.3s ease;
}

.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 50px rgba(220, 38, 38, 0.2);
}

.service-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
  gap: 20px;
}

.service-name {
  font-size: 1.4rem;
  font-weight: 700;
  flex: 1;
}

.service-price {
  font-size: 1.8rem;
  font-weight: 900;
  color: #dc2626;
  text-shadow: 0 0 15px rgba(220, 38, 38, 0.4);
  white-space: nowrap;
}

.service-spec {
  margin-bottom: 20px;
  padding: 10px 15px;
  background: rgba(220, 38, 38, 0.1);
  border-radius: 8px;
  border-left: 3px solid #dc2626;
}

.spec-label {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
  margin-right: 8px;
}

.spec-value {
  color: white;
  font-weight: 600;
}

.service-footer {
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

/* CTA секция */
.cta-section {
  text-align: center;
  padding: 50px;
  background: linear-gradient(135deg, rgba(220, 38, 38, 0.15) 0%, rgba(10, 10, 10, 0.6) 100%);
}

.cta-section h2 {
  font-size: 2rem;
  margin-bottom: 15px;
}

.cta-section p {
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 30px;
  font-size: 1.1rem;
}

.cta-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

/* Loading state */
.loading-state {
  text-align: center;
  padding: 80px 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(220, 38, 38, 0.2);
  border-top-color: #dc2626;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: rgba(255, 255, 255, 0.5);
  font-size: 1.1rem;
}

/* Адаптивность */
@media (max-width: 768px) {
  .page-title {
    font-size: 2.2rem;
  }
  
  .services-grid {
    grid-template-columns: 1fr;
  }
  
  .service-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .service-price {
    font-size: 1.5rem;
  }
}
</style>