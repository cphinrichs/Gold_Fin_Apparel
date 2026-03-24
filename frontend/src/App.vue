<script lang="ts" setup>
import { RouterView } from 'vue-router'
import TaskBar from "./Components/TaskBar.vue";
</script>

<template>
  <div class="app-wrapper">
    <TaskBar />
    <div class="main-content">
      <RouterView />
    </div>
    <footer class="footer">
      <p>&copy; 2026 GoldFin Apparel. All rights reserved.</p>
    </footer>
  </div>
</template>

<style>
.app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  margin-top: 80px;
}

.footer {
  font-family: Arial, sans-serif;
  padding: 2rem;
  text-align: center;
  background: linear-gradient(to top, #000000 0%, #0a0a0a 100%);
  color: #d4af37;
  border-top: 2px solid rgba(212, 175, 55, 0.3);
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.5);
}

.footer p {
  margin: 0;
  font-size: 0.95rem;
  letter-spacing: 1px;
  text-transform: uppercase;
}

body {
  background-color: #0a0a0a;
  background-image: 
    radial-gradient(circle at 15% 30%, rgba(212, 175, 55, 0.08) 0%, transparent 15%),
    radial-gradient(circle at 85% 70%, rgba(212, 175, 55, 0.08) 0%, transparent 15%),
    radial-gradient(circle at 50% 50%, rgba(212, 175, 55, 0.05) 0%, transparent 25%),
    repeating-linear-gradient(0deg, transparent 0px, transparent 40px, rgba(212, 175, 55, 0.03) 40px, rgba(212, 175, 55, 0.03) 80px),
    repeating-linear-gradient(90deg, transparent 0px, transparent 40px, rgba(212, 175, 55, 0.03) 40px, rgba(212, 175, 55, 0.03) 80px),
    repeating-linear-gradient(45deg, transparent 0px, transparent 60px, rgba(212, 175, 55, 0.02) 60px, rgba(212, 175, 55, 0.02) 120px),
    repeating-linear-gradient(-45deg, transparent 0px, transparent 60px, rgba(212, 175, 55, 0.02) 60px, rgba(212, 175, 55, 0.02) 120px),
    radial-gradient(circle at 25% 75%, rgba(212, 175, 55, 0.06) 0%, transparent 20%),
    radial-gradient(circle at 75% 25%, rgba(212, 175, 55, 0.06) 0%, transparent 20%);
  background-size: 
    100% 100%,
    100% 100%,
    100% 100%,
    80px 80px,
    80px 80px,
    120px 120px,
    120px 120px,
    100% 100%,
    100% 100%;
}
</style>
