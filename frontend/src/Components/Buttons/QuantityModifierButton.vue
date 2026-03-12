<template>
  <div class="quantity-modifier">
    <button class="qty-btn decrease-btn" @click="decreaseQuantity">−</button>
    <span class="qty-display">{{ quantity }}</span>
    <button class="qty-btn increase-btn" @click="increaseQuantity">+</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const quantity = ref(1);

const increaseQuantity = () => {
  quantity.value++;
};

const decreaseQuantity = () => {
  if (quantity.value > 1) {
    quantity.value--;
  }
};
</script>

<style scoped>
.quantity-modifier {
  display: flex;
  align-items: center;
  gap: 0;
  border: 2px solid #333;
  width: fit-content;
  background: transparent;
}

.qty-btn {
  background: transparent;
  border: none;
  padding: 10px 16px;
  font-size: 1.1rem;
  font-weight: 500;
  cursor: pointer;
  color: #333;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qty-btn:hover {
  background-color: #f0f0f0;
  color: #333;
}

.qty-btn:active {
  background-color: #e0e0e0;
}

.decrease-btn {
  border-right: 1px solid #ddd;
}

.increase-btn {
  border-left: 1px solid #ddd;
}

.qty-display {
  padding: 10px 16px;
  font-weight: 600;
  font-size: 1rem;
  min-width: 50px;
  text-align: center;
  color: #333;
  user-select: none;
}

.quantity-modifier:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
