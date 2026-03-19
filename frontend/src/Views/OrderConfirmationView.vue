<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { getStyleImageUrl, getMaterialTextureUrl, getDesignImageUrl } from '../Utils/browseImageHelpers';

onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'instant' });
});

const state = window.history.state;

const maskedCard = computed(() => {
  const num = state?.cardNumber?.replace(/\s/g, '') ?? '';
  return num.length >= 4 ? 'XXXX XXXX XXXX ' + num.slice(-4) : 'XXXX XXXX XXXX XXXX';
});

// Deduplicate items: merge any entries with identical Style+Color+Material+Size
const rawItems: any[] = state?.orderedItems ?? [];
const orderedItems = rawItems.reduce((acc: any[], item: any) => {
  const existing = acc.find(
    (i) => i.Style === item.Style && i.Color === item.Color &&
           i.Material === item.Material && i.Size === item.Size
  );
  if (existing) {
    existing.quantity = (existing.quantity ?? 1) + (item.quantity ?? 1);
  } else {
    acc.push({ ...item, quantity: item.quantity ?? 1 });
  }
  return acc;
}, []);

// Parse shipping cost string ("Free" -> 0, "$9.99" -> 9.99)
const shippingCostNum = computed(() => {
  const raw: string = state?.shippingCost ?? 'Free';
  if (raw === 'Free' || state?.deliveryOption === 'pickup') return 0;
  const parsed = parseFloat(raw.replace(/[^\d.]/g, ''));
  return isNaN(parsed) ? 0 : parsed;
});

// Items subtotal
const itemsSubtotal = computed(() =>
  orderedItems.reduce((sum: number, item: any) => sum + item.Price * (item.quantity ?? 1), 0)
);

// Grand total = items + shipping
const grandTotal = computed(() =>
  (itemsSubtotal.value + shippingCostNum.value).toFixed(2)
);
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

    <!-- Ordered Items -->
    <div class="ordered-items-section" v-if="orderedItems.length > 0">
      <h2 class="ordered-items-title">Items Ordered</h2>
      <div class="ordered-items-grid">
        <div
          v-for="item in orderedItems"
          :key="item.cartItemId"
          class="ordered-item">
          <!-- Layered product image -->
          <div class="ordered-item-image" :style="{ backgroundColor: item.Color }">
            <div class="ord-layer material-layer" :style="{ backgroundImage: `url(${getMaterialTextureUrl(item.Material)})` }"></div>
            <div class="ord-layer design-layer" :style="{ backgroundImage: `url(${getDesignImageUrl(item.Design_Id)})` }"></div>
            <img
              v-if="getStyleImageUrl(item.Style)"
              :src="getStyleImageUrl(item.Style)"
              :alt="item.Style"
              class="ordered-style-image"
            />
            <!-- Quantity badge -->
            <span class="ord-qty-badge" v-if="item.quantity > 1">× {{ item.quantity }}</span>
          </div>
          <!-- Info below image -->
          <div class="ordered-item-info">
            <h3>{{ item.Style }}</h3>
            <p>{{ item.Material }} | {{ item.Size }}</p>
            <p class="ordered-item-price">${{ (item.Price * item.quantity).toFixed(2) }}</p>
          </div>
        </div>
      </div>
      <div class="ordered-total">
        <div class="ordered-total-rows">
          <div class="ordered-total-row" v-if="shippingCostNum > 0">
            <span class="ordered-total-label">Subtotal</span>
            <span class="ordered-total-value">${{ itemsSubtotal.toFixed(2) }}</span>
          </div>
          <div class="ordered-total-row" v-if="shippingCostNum > 0">
            <span class="ordered-total-label">Shipping</span>
            <span class="ordered-total-value">${{ shippingCostNum.toFixed(2) }}</span>
          </div>
          <div class="ordered-total-row grand">
            <span class="ordered-total-label">Order Total</span>
            <span class="ordered-total-value">${{ grandTotal }}</span>
          </div>
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

/* Ordered items */
.ordered-items-section {
  margin-top: 3rem;
}

.ordered-items-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #333;
  border-bottom: 3px solid #FFD700;
  padding-bottom: 0.6rem;
  margin-bottom: 1.5rem;
}

.ordered-items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.ordered-item {
  border: 1px solid #ddd;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Layered image area */
.ordered-item-image {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  flex-shrink: 0;
}

.ord-layer {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.ord-layer.material-layer {
  opacity: 0.35;
  mix-blend-mode: multiply;
}

.ord-layer.design-layer {
  opacity: 0.7;
  mix-blend-mode: overlay;
  background-size: 60%;
  background-position: center;
}

.ordered-style-image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.ord-qty-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background: #333;
  color: #FFD700;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 12px;
}

.ordered-item-info {
  padding: 8px 10px;
  background: #fff;
  text-align: center;
}

.ordered-item-info h3 {
  margin: 0 0 4px 0;
  font-size: 0.95rem;
  color: #333;
}

.ordered-item-info p {
  margin: 2px 0;
  font-size: 0.8rem;
  color: #555;
}

.ordered-item-price {
  font-weight: 700;
  font-size: 0.95rem !important;
  margin-top: 5px !important;
}

.ordered-total {
  margin-top: 20px;
  max-width: 400px;
  margin-left: auto;
  border: 2px solid #333;
  background: #f5f5f5;
}

.ordered-total-rows {
  display: flex;
  flex-direction: column;
}

.ordered-total-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 10px 20px;
  border-bottom: 1px solid #e0e0e0;
}

.ordered-total-row:last-child {
  border-bottom: none;
}

.ordered-total-row.grand {
  padding: 14px 20px;
  background: #efefef;
}

.ordered-total-label {
  font-size: 1rem;
  font-weight: 700;
  color: #333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.ordered-total-row.grand .ordered-total-label,
.ordered-total-row.grand .ordered-total-value {
  font-size: 1.1rem;
}

.ordered-total-value {
  font-size: 1rem;
  font-weight: 700;
  color: #333;
}
</style>
