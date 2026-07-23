<template>
  <Navbar />
  <main class="main-content">
    <router-view />
  </main>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
</script>

<style>
.main-content {
  flex: 1;
  width: 100%;
  min-height: calc(100vh - 180px);
  padding: 40px 20px;
  max-width: 1400px;
  margin: 0 auto;
}
</style>