<!-- 
Browse button will be in the Cart Page and be used to navigate back to browse products page. It will be a simple button with a link to the browse page.
-->

<template>
  <button class="browse-btn" @click="navigateToBrowse">
    <span class="btn-text">Browse</span>
  </button>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateToBrowse = () => {
  router.push({ name: 'Browse' })
}
</script>

<style scoped>
.browse-btn {
  background: transparent;
  border: 2px solid #333;
  padding: 0;
  min-height: 44px;
  width: 100%;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #333;
  text-transform: uppercase;
}

.browse-btn:hover {
  background-color: #333;
  color: #fff;
}

.browse-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.btn-icon {
  font-size: 1.2rem;
  font-weight: bold;
}

.btn-text {
  letter-spacing: 0.05em;
}
</style>

