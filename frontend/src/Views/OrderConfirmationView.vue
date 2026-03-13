<script setup lang="ts">
import { computed } from 'vue';

const state = window.history.state;

const maskedCard = computed(() => {
  const num = state?.cardNumber?.replace(/\s/g, '') ?? '';
  return num.length >= 4 ? 'XXXX XXXX XXXX ' + num.slice(-4) : 'XXXX XXXX XXXX XXXX';
});
</script>

<template>
  <section class="confirmation-page">
    <div class="confirmation-header">
      <div class="checkmark">✓</div>
      <h1>Order Confirmed!</h1>
      <p>Thank you for your purchase, {{ state?.firstName }}! Your order has been successfully placed. A confirmation will be sent to <strong>{{ state?.email }}</strong>.</p>
    </div>

    <div class="confirmation-grid">

      <!-- Delivery Option -->
      <div class="confirm-section">
        <h2>Delivery Option</h2>
        <div class="confirm-detail">
          <span class="label">Method</span>
          <span class="value">{{ state?.deliveryOption === 'deliver' ? 'Deliver to Address' : 'Pick Up in Store' }}</span>
        </div>
        <div class="confirm-detail">
          <span class="label">Address</span>
          <span class="value" v-if="state?.deliveryOption === 'pickup'">67 Dickson Street, Fayetteville, AR 72702</span>
          <span class="value" v-else>{{ state?.address }}, {{ state?.city }}, {{ state?.state }} {{ state?.postalCode }}</span>
        </div>
      </div>

      <!-- Personal Information -->
      <div class="confirm-section">
        <h2>Personal Information</h2>
        <div class="confirm-detail">
          <span class="label">Name</span>
          <span class="value">{{ state?.firstName }} {{ state?.lastName }}</span>
        </div>
        <div class="confirm-detail">
          <span class="label">Email</span>
          <span class="value">{{ state?.email }}</span>
        </div>
        <div class="confirm-detail">
          <span class="label">Phone</span>
          <span class="value">{{ state?.phoneNumber }}</span>
        </div>
        <div class="confirm-detail">
          <span class="label">Address</span>
          <span class="value">{{ state?.address }}, {{ state?.city }}, {{ state?.state }} {{ state?.postalCode }}</span>
        </div>
      </div>

      <!-- Shipping Method -->
      <div class="confirm-section">
        <h2>Shipping Method</h2>
        <div class="confirm-detail">
          <span class="label">Method</span>
          <span class="value">{{ state?.shippingMethod }}</span>
        </div>
        <div class="confirm-detail">
          <span class="label">{{ state?.deliveryOption === 'pickup' ? 'Location' : 'Estimated Delivery' }}</span>
          <span class="value">{{ state?.estimatedDelivery }}</span>
        </div>
        <div class="confirm-detail" v-if="state?.deliveryOption !== 'pickup'">
          <span class="label">Cost</span>
          <span class="value">{{ state?.shippingCost }}</span>
        </div>
      </div>

      <!-- Payment Information -->
      <div class="confirm-section">
        <h2>Payment Information</h2>
        <div class="confirm-detail">
          <span class="label">Payment Type</span>
          <span class="value">{{ state?.paymentMethod === 'credit' ? 'Credit Card' : 'Debit Card' }}</span>
        </div>
        <div class="confirm-detail">
          <span class="label">Card Number</span>
          <span class="value secure">{{ maskedCard }}</span>
        </div>
        <div class="confirm-detail">
          <span class="label">Expiration</span>
          <span class="value secure">XX/XX</span>
        </div>
        <div class="confirm-detail">
          <span class="label">CVV</span>
          <span class="value secure">XXX</span>
        </div>
      </div>

    </div>

    <div class="confirmation-footer">
      <router-link to="/" class="home-btn">Return to Home</router-link>
    </div>
  </section>
</template>

<style scoped>
.confirmation-page {
  padding: 60px 20px;
  max-width: 900px;
  margin: 0 auto;
}

.confirmation-header {
  text-align: center;
  margin-bottom: 3rem;
}

.checkmark {
  width: 70px;
  height: 70px;
  background: #FFD700;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin: 0 auto 1.5rem auto;
}

.confirmation-header h1 {
  font-size: 2.5rem;
  color: #333;
  border-bottom: 3px solid #000;
  padding-bottom: 1rem;
  margin-bottom: 1rem;
}

.confirmation-header p {
  font-size: 1rem;
  color: #555;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.7;
}

.confirmation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
  gap: 2rem;
}

.confirm-section {
  padding: 2rem;
  background: #f9f9f9;
  border-left: 4px solid #FFD700;
  border-top: 2px solid #e0e0e0;
  border-right: 2px solid #e0e0e0;
  border-bottom: 2px solid #e0e0e0;
  border-radius: 4px;
}

.confirm-section h2 {
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e0e0e0;
}

.confirm-detail {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f0f0f0;
  gap: 1rem;
}

.confirm-detail:last-child {
  border-bottom: none;
}

.label {
  font-weight: 600;
  color: #555;
  font-size: 0.9rem;
  white-space: nowrap;
}

.value {
  color: #333;
  font-size: 0.95rem;
  text-align: right;
}

.value.secure {
  letter-spacing: 1px;
  color: #888;
  font-family: monospace;
}

.confirmation-footer {
  margin-top: 3rem;
  text-align: center;
}

.home-btn {
  display: inline-block;
  padding: 0.85rem 2.5rem;
  background: #333;
  color: #FFD700;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  letter-spacing: 1px;
  border-radius: 4px;
  transition: all 0.3s ease;
  text-transform: uppercase;
}

.home-btn:hover {
  background: #FFD700;
  color: #333;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}
</style>
