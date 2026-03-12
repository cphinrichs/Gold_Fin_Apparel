<!--
Cancel button component for the Checkout page. When clicked, it will return the user to the cart page to review their items or make changes before proceeding to checkout.
-->

<template>
  <button class="cancel-btn" @click="handleCancel">
    <span class="btn-icon">✕</span>
    <span class="btn-text">Cancel</span>
  </button>
</template>

<script setup lang="ts">
const handleCancel = () => {
  window.history.back();
};
</script>

<style scoped>
.cancel-btn {
  background: transparent;
  border: 2px solid #dc3545;
  padding: 12px 28px;
  font-size: 1rem;
  font-weight: 500;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #dc3545;
  text-transform: uppercase;
}

.cancel-btn:hover {
  background-color: #dc3545;
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
}

.cancel-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(220, 53, 69, 0.2);
}

.btn-icon {
  font-size: 1.2rem;
  font-weight: bold;
}

.btn-text {
  letter-spacing: 0.05em;
}
</style>
