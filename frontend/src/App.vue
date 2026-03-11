<script lang="ts" setup>
import { RouterView } from 'vue-router'
import TaskBar from "./Components/TaskBar.vue";
</script>

<template>
  <TaskBar />
  <RouterView />
  <footer class="container">
    <p>&copy; 2026 GoldFin Apparel. All rights reserved.</p>
  </footer>
</template>

<style>
.container {
  font-family: Arial, sans-serif;
}
</style>
