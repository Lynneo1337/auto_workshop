<template>
  <nav class="navbar">
    <div class="nav-container">
      <router-link to="/" class="logo">
        <span class="logo-icon">🔧</span>
        <span class="logo-text">АВТО<span class="red">СЕРВИС</span></span>
      </router-link>

      <ul class="nav-links">
        <template v-if="isLoggedIn">
          <li>
            <router-link to="/dashboard" class="nav-link">
              Личный кабинет
            </router-link>
          </li>
          <li>
            <button @click="logout" class="nav-link btn-logout">
              Выйти
            </button>
          </li>
        </template>
        <template v-else>
          <li>
            <router-link to="/login" class="nav-link btn-login">
              Войти
            </router-link>
          </li>
          <li>
            <router-link to="/register" class="nav-link btn-register">
              Регистрация
            </router-link>
          </li>
        </template>
      </ul>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoggedIn = ref(false)

onMounted(() => {
  isLoggedIn.value = !!localStorage.getItem('token')
})

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('role')
  isLoggedIn.value = false
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(10, 10, 10, 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(220, 38, 38, 0.3);
  box-shadow: 0 4px 30px rgba(220, 38, 38, 0.1);
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: white;
  transition: transform 0.3s;
}

.logo:hover {
  transform: scale(1.05);
}

.logo-icon {
  font-size: 2rem;
  filter: drop-shadow(0 0 10px rgba(220, 38, 38, 0.5));
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 900;
  letter-spacing: 2px;
  color: white;
}

.logo-text .red {
  color: #dc2626;
  text-shadow: 0 0 20px rgba(220, 38, 38, 0.5);
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 10px;
  align-items: center;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 10px 20px;
  border-radius: 10px;
  font-weight: 500;
  transition: all 0.3s;
  position: relative;
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

.nav-link:hover {
  background: rgba(220, 38, 38, 0.2);
  color: #ef4444;
}

.nav-link.router-link-active {
  background: rgba(220, 38, 38, 0.3);
  color: #ef4444;
}

.btn-login {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-login:hover {
  background: rgba(255, 255, 255, 0.2);
}

.btn-register {
  background: linear-gradient(135deg, #dc2626, #991b1b);
  box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
}

.btn-register:hover {
  background: linear-gradient(135deg, #ef4444, #b91c1c);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(220, 38, 38, 0.6);
  color: white;
}

.btn-logout {
  background: rgba(220, 38, 38, 0.2);
  border: 1px solid rgba(220, 38, 38, 0.4);
}

.btn-logout:hover {
  background: rgba(220, 38, 38, 0.4);
  color: white;
}
</style>