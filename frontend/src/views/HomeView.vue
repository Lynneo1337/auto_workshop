<template>
  <div class="home-page fade-in">
    <!-- Hero секция -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          Профессиональный <span class="neon-text">автосервис</span>
        </h1>
        <p class="hero-subtitle">
          Качественный ремонт и диагностика автомобилей любой сложности
        </p>
        <div class="hero-buttons">
          <router-link to="/services" class="btn btn-primary">
            Наши услуги
          </router-link>
          <router-link :to="isLoggedIn ? '/booking' : '/login'" class="btn btn-outline">
            Записаться онлайн
        </router-link>
        </div>
      </div>
      <div class="hero-features">
        <div class="feature-card glass-card">
          <div class="feature-icon">👨‍🔧</div>
          <h3>5 мастеров</h3>
          <p>Различные профили специализации</p>
        </div>
        <div class="feature-card glass-card">
          <div class="feature-icon">🏢</div>
          <h3>2 бокса</h3>
          <p>Вместимость до 4 автомобилей</p>
        </div>
        <div class="feature-card glass-card">
          <div class="feature-icon">💰</div>
          <h3>Скидки</h3>
          <p>Система лояльности для постоянных клиентов</p>
        </div>
      </div>
    </section>

    <!-- Преимущества -->
    <section class="section">
      <h2 class="section-title">Почему выбирают нас</h2>
      <div class="grid-3">
        <div class="glass-card advantage-card">
          <h3 class="advantage-title"> Быстро</h3>
          <p>Оптимальные сроки ремонта без потери качества</p>
        </div>
        <div class="glass-card advantage-card">
          <h3 class="advantage-title"> Качественно</h3>
          <p>Опытные мастера и современное оборудование</p>
        </div>
        <div class="glass-card advantage-card">
          <h3 class="advantage-title">Честные цены</h3>
          <p>Фиксированный прайс, никаких скрытых платежей</p>
        </div>
      </div>
    </section>

    <!-- Контакты -->
    <section class="section">
      <div class="glass-card contacts-section">
        <h2 class="section-title">Контакты</h2>
        <div class="contacts-grid">
          <div class="contact-item">
            <div class="contact-icon">📞</div>
            <div>
              <h4>Телефон</h4>
              <p class="contact-value">+7 (999) 123-45-67</p>
            </div>
          </div>
          <div class="contact-item">
            <div class="contact-icon">📍</div>
            <div>
              <h4>Адрес</h4>
              <p class="contact-value">г. Москва, ул. Примерная, 123</p>
            </div>
          </div>
          <div class="contact-item">
            <div class="contact-icon">🕐</div>
            <div>
              <h4>Режим работы</h4>
              <p class="contact-value">Пн-Пт: 9:00 - 20:00<br/>Сб-Вс: 10:00 - 18:00</p>
            </div>
          </div>
        </div>
        
        <!-- Кнопка обратного звонка -->
        <div class="callback-section">
          <p>Нужна консультация?</p>
          <button @click="showCallbackModal = true" class="btn btn-primary">
            📞 Заказать обратный звонок
          </button>
        </div>
      </div>
    </section>

    <!-- Модальное окно обратного звонка -->
    <div v-if="showCallbackModal" class="modal-overlay" @click.self="showCallbackModal = false">
      <div class="modal glass-card">
        <h3>Заказать обратный звонок</h3>
        <p class="modal-subtitle">Оставьте свои данные, и мы перезвоним вам в ближайшее время</p>
        
        <form @submit.prevent="submitCallback">
          <div class="form-group">
            <label class="form-label">Ваше имя</label>
            <input v-model="callbackForm.name" type="text" class="form-input" required />
          </div>
          <div class="form-group">
            <label class="form-label">Телефон</label>
            <input 
              v-model="callbackForm.phone" 
              type="tel" 
              class="form-input" 
              placeholder="+79001234567"
              @input="normalizePhone"
              required 
            />
          </div>
          <div class="modal-actions">
            <button type="button" @click="showCallbackModal = false" class="btn btn-outline">
              Отмена
            </button>
            <button type="submit" class="btn btn-primary" :disabled="isLoading">
              {{ isLoading ? 'Отправка...' : 'Отправить' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import apiClient from '../api/axios'

const isLoggedIn = ref(false)
onMounted(() => { isLoggedIn.value = !!localStorage.getItem('token') })

const showCallbackModal = ref(false)
const isLoading = ref(false)

const callbackForm = reactive({
  name: '',
  phone: ''
})

const normalizePhone = () => {
  let val = callbackForm.phone.replace(/\s/g, '').replace(/-/g, '').replace(/\(/g, '').replace(/\)/g, '')
  
  if (val.startsWith('8') && val.length === 11 && val.slice(1).match(/^\d+$/)) {
    callbackForm.phone = '+7' + val.slice(1)
  } else if (val.startsWith('7') && val.length === 11 && val.slice(1).match(/^\d+$/)) {
    callbackForm.phone = '+7' + val.slice(1)
  }
}

const submitCallback = async () => {
  isLoading.value = true
  
  try {
    await apiClient.post('/callback/', {
      client_name: callbackForm.name,
      phone: callbackForm.phone
    })
    
    alert('Заявка отправлена! Мы перезвоним вам в ближайшее время.')
    showCallbackModal.value = false
    callbackForm.name = ''
    callbackForm.phone = ''
  } catch (error) {
    alert('Ошибка отправки заявки. Попробуйте позже.')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  gap: 60px;
}

/* Hero секция */
.hero-section {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(10, 10, 10, 0.5) 100%);
  border-radius: 30px;
  border: 1px solid rgba(220, 38, 38, 0.2);
}

.hero-content {
  margin-bottom: 60px;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 900;
  margin-bottom: 20px;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.3rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 40px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.hero-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.hero-features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  max-width: 1000px;
  margin: 0 auto;
}

.feature-card {
  text-align: center;
  padding: 30px;
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: #dc2626;
}

.feature-card p {
  color: rgba(255, 255, 255, 0.7);
}

/* Секции */
.section {
  padding: 40px 20px;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 40px;
  font-weight: 700;
}

/* Преимущества */
.advantage-card {
  text-align: center;
  padding: 40px 30px;
}

.advantage-title {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #dc2626;
}

.advantage-card p {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
}

/* Контакты */
.contacts-section {
  max-width: 900px;
  margin: 0 auto;
  padding: 50px;
}

.contacts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
  margin-bottom: 40px;
}

.contact-item {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.contact-icon {
  font-size: 2.5rem;
}

.contact-item h4 {
  font-size: 1.1rem;
  margin-bottom: 8px;
  color: white;
}

.contact-value {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.5;
}

.callback-section {
  text-align: center;
  padding-top: 30px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.callback-section p {
  font-size: 1.2rem;
  margin-bottom: 20px;
  color: rgba(255, 255, 255, 0.8);
}

/* Модальное окно */
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
  font-size: 1.8rem;
  margin-bottom: 10px;
  text-align: center;
}

.modal-subtitle {
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 30px;
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

/* Адаптивность */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.2rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .contacts-grid {
    grid-template-columns: 1fr;
  }
}
</style>