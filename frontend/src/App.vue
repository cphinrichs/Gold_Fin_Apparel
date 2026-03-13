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
  padding: 1rem 2rem;
  text-align: left;
}

body {
  background-color: #f5f5f5;
  background-image: 
    radial-gradient(circle at 15% 30%, rgba(140, 140, 140, 0.18) 0%, transparent 15%),
    radial-gradient(circle at 85% 70%, rgba(140, 140, 140, 0.18) 0%, transparent 15%),
    radial-gradient(circle at 50% 50%, rgba(160, 160, 160, 0.12) 0%, transparent 25%),
    repeating-linear-gradient(0deg, transparent 0px, transparent 40px, rgba(180, 180, 180, 0.07) 40px, rgba(180, 180, 180, 0.07) 80px),
    repeating-linear-gradient(90deg, transparent 0px, transparent 40px, rgba(180, 180, 180, 0.07) 40px, rgba(180, 180, 180, 0.07) 80px),
    repeating-linear-gradient(45deg, transparent 0px, transparent 60px, rgba(170, 170, 170, 0.05) 60px, rgba(170, 170, 170, 0.05) 120px),
    repeating-linear-gradient(-45deg, transparent 0px, transparent 60px, rgba(170, 170, 170, 0.05) 60px, rgba(170, 170, 170, 0.05) 120px),
    radial-gradient(circle at 25% 75%, rgba(150, 150, 150, 0.10) 0%, transparent 20%),
    radial-gradient(circle at 75% 25%, rgba(150, 150, 150, 0.10) 0%, transparent 20%);
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
