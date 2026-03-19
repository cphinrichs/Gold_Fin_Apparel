<template>
  <button class="checkout-btn" @click="handleCheckout">
    <span class="btn-icon">✓</span>
    <span class="btn-text">Checkout</span>
  </button>
</template>

<script setup lang="ts">
const handleCheckout = () => {
  window.location.href = '/checkout';
};
</script>

<style scoped>
.checkout-btn {
  background: transparent;
  border: 2px solid #333;
  padding: 12px 28px;
  font-size: 1rem;
  font-weight: 500;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #333;
  text-transform: uppercase;
}

.checkout-btn:hover {
  background-color: #333;
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.checkout-btn:active {
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
