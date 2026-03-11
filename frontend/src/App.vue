<template>
  <TaskBar />
  <RouterView />
</template>

<script lang="ts" setup>
import { RouterView } from 'vue-router';
import TaskBar from "./Components/TaskBar.vue";
import router from "./Router";
import Home from "./Views/HomeView.vue";
</script>

<style>
.container {
  font-family: Arial, sans-serif;
  padding: 2rem;
}
</style>
