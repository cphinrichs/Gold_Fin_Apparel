<!--
Users will press this button to complete their order and be taken to the order confirmation page.
-->

<template>
  <button type="button" class="complete-order-btn" @click="showConfirm = true">
    <span class="btn-icon">✓</span>
    <span class="btn-text">Complete Order</span>
  </button>

  <!-- Confirmation Modal -->
  <teleport to="body">
    <div v-if="showConfirm" class="confirm-overlay" @click.self="showConfirm = false">
      <div class="confirm-dialog">
        <h3 class="confirm-title">Confirm Order</h3>
        <p class="confirm-message">
          Are you ready to place your order? Please confirm that all your information is correct before completing your purchase.
        </p>
        <div class="confirm-actions">
          <button type="button" class="confirm-no-btn" @click="showConfirm = false">No, Go Back</button>
          <button type="button" class="confirm-yes-btn" @click="handleCompleteOrder">Yes, Place Order</button>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const emit = defineEmits(['complete']);
const showConfirm = ref(false);

const handleCompleteOrder = () => {
  showConfirm.value = false;
  emit('complete');
};
</script>

<style scoped>
.complete-order-btn {
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

.complete-order-btn:hover {
  background-color: #333;
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.complete-order-btn:active {
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

/* Confirmation Modal */
.confirm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.confirm-dialog {
  background: #fff;
  border-radius: 8px;
  padding: 2.5rem 2rem;
  max-width: 460px;
  width: 90%;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.confirm-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.confirm-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 1rem;
}

.confirm-message {
  font-size: 0.95rem;
  color: #555;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.confirm-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.confirm-no-btn {
  padding: 0.7rem 1.8rem;
  background: #f0f0f0;
  color: #333;
  border: 2px solid #ccc;
  border-radius: 4px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.confirm-no-btn:hover {
  background: #e0e0e0;
  border-color: #aaa;
}

.confirm-yes-btn {
  padding: 0.7rem 1.8rem;
  background: #333;
  color: #fff;
  border: 2px solid #333;
  border-radius: 4px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.confirm-yes-btn:hover {
  background: #FFD700;
  border-color: #FFD700;
  color: #333;
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
}
</style>
