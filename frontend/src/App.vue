<script lang="ts" setup>
import { RouterView } from 'vue-router'
import TaskBar from "./Components/TaskBar.vue";
</script>

<template>
  <TaskBar />
  <div class="main-content">
    <RouterView />
  </div>
  <footer class="container">
    <p>&copy; 2026 GoldFin Apparel. All rights reserved.</p>
  </footer>
</template>

<style>
.main-content {
  margin-top: 80px; 
  min-height: calc(100vh - 80px - 60px);
}
.container {
  font-family: Arial, sans-serif;
}
</style>
