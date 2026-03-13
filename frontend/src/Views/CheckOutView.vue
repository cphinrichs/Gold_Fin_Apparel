<script lang="ts" setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import CancelButton from '../Components/Buttons/CancelButton.vue';
import CompleteOrderButton from '../Components/Buttons/CompleteOrderButton.vue';

const router = useRouter();

const activeSection = ref(0); // 0: Delivery, 1: Personal, 2: Shipping, 3: Payment
const deliveryOption = ref('');
const paymentMethod = ref('credit');
const shippingMethod = ref('standard'); // 'standard', 'express', 'overnight'

const formData = ref({
  email: '',
  firstName: '',
  lastName: '',
  address: '',
  city: '',
  state: '',
  postalCode: '',
  phoneNumber: '',
  cardNumber: '',
  expirationDate: '',
  cvv: ''
});

const sectionTitles = ['Delivery Options', 'Personal Information', 'Shipping Method', 'Payment'];

const handleSaveAndContinue = (section: number) => {
  activeSection.value = section + 1;
};

const isPersonalInfoComplete = (): boolean => {
  return !!(
    formData.value.email &&
    formData.value.firstName &&
    formData.value.lastName &&
    formData.value.address &&
    formData.value.city &&
    formData.value.state &&
    formData.value.postalCode &&
    formData.value.phoneNumber
  );
};

const isPaymentComplete = (): boolean => {
  return !!(
    formData.value.cardNumber &&
    formData.value.expirationDate &&
    formData.value.cvv
  );
};

const completeOrder = () => {
  let shippingLabel = 'Free Standard Shipping';
  let shippingCost = 'Free';
  let estimatedDelivery = '5–7 business days';
  if (deliveryOption.value === 'pickup') {
    shippingLabel = 'Store Pickup';
    shippingCost = 'Free';
    estimatedDelivery = 'Gold Fin Apparel';
  } else if (shippingMethod.value === 'express') {
    shippingLabel = 'Express Shipping';
    shippingCost = '$9.99';
    estimatedDelivery = '2–3 business days';
  } else if (shippingMethod.value === 'overnight') {
    shippingLabel = 'Overnight Shipping';
    shippingCost = '$14.99';
    estimatedDelivery = 'Next business day';
  }
  router.push({
    name: 'OrderConfirmation',
    state: {
      deliveryOption: deliveryOption.value,
      paymentMethod: paymentMethod.value,
      shippingMethod: shippingLabel,
      shippingCost,
      estimatedDelivery,
      email: formData.value.email,
      firstName: formData.value.firstName,
      lastName: formData.value.lastName,
      address: formData.value.address,
      city: formData.value.city,
      state: formData.value.state,
      postalCode: formData.value.postalCode,
      phoneNumber: formData.value.phoneNumber,
      cardNumber: formData.value.cardNumber,
      expirationDate: formData.value.expirationDate,
      cvv: formData.value.cvv,
    }
  });
};
</script>

<template>
  <section class="checkout-page">
    <div class="checkout-header">
      <h1>Checkout</h1>
      <p>Complete your purchase by providing your delivery, personal, shipping, and payment information.</p>
    </div>

    <form class="checkout-form">
      <!-- Delivery Options Section -->
      <div class="form-section" :class="{ active: activeSection === 0 }">
        <h2>Delivery Options</h2>
        <div class="delivery-options">
          <label class="radio-option">
            <input type="radio" v-model="deliveryOption" value="deliver" />
            <span>Deliver to Address</span>
          </label>
          <label class="radio-option">
            <input type="radio" v-model="deliveryOption" value="pickup" />
            <span>Pick Up in Store</span>
          </label>
          <div class="store-address">
            <span> Gold Fin Apparel — 67 Dickson Street, Fayetteville, AR 72702</span>
            <span class="store-hours">Mon–Sat: 9am–7pm &nbsp;|&nbsp; Sun: 11am–5pm</span>
          </div>
        </div>
        <div class="section-actions" v-if="deliveryOption">
          <button type="button" class="save-continue-btn" @click="handleSaveAndContinue(0)">
            Save & Continue
          </button>
        </div>
      </div>

      <!-- Personal Information Section -->
      <transition name="fadeSlide">
      <div class="form-section" :class="{ active: activeSection === 1, completed: activeSection > 1 }" v-show="activeSection >= 1">
        <h2>Personal Information</h2>
        <div class="section-content">
        <div class="form-group-row">
          <div class="form-group">
            <label for="email">Email Address</label>
            <input 
              type="email" 
              id="email" 
              v-model="formData.email" 
              placeholder="Enter your email"
              required
            />
          </div>
        </div>
        <div class="form-group-row">
          <div class="form-group">
            <label for="firstName">First Name</label>
            <input 
              type="text" 
              id="firstName" 
              v-model="formData.firstName" 
              placeholder="First name"
              required
            />
          </div>
          <div class="form-group">
            <label for="lastName">Last Name</label>
            <input 
              type="text" 
              id="lastName" 
              v-model="formData.lastName" 
              placeholder="Last name"
              required
            />
          </div>
        </div>
        <div class="form-group-row">
          <div class="form-group">
            <label for="address">Physical Address</label>
            <input 
              type="text" 
              id="address" 
              v-model="formData.address"
              placeholder="Street address"
              required
            />
          </div>
        </div>
        <div class="form-group-row">
          <div class="form-group">
            <label for="city">City</label>
            <input 
              type="text" 
              id="city" 
              v-model="formData.city" 
              placeholder="City"
              required
            />
          </div>
          <div class="form-group">
            <label for="state">State</label>
            <input 
              type="text" 
              id="state" 
              v-model="formData.state" 
              placeholder="State"
              required
            />
          </div>
          <div class="form-group">
            <label for="postalCode">Postal Code</label>
            <input 
              type="text" 
              id="postalCode" 
              v-model="formData.postalCode" 
              placeholder="Postal code"
              required
            />
          </div>
        </div>
        <div class="form-group-row">
          <div class="form-group">
            <label for="phoneNumber">Phone Number</label>
            <input 
              type="tel" 
              id="phoneNumber" 
              v-model="formData.phoneNumber" 
              placeholder="(123) 456-7890"
              required
            />
          </div>
        </div>
        <div class="section-actions" v-if="activeSection === 1">
          <button type="button" class="save-continue-btn" @click="handleSaveAndContinue(1)" :disabled="!isPersonalInfoComplete()">
            Save & Continue
          </button>
        </div>
        </div>
      </div>
      </transition>

      <!-- Shipping Section -->
      <transition name="fadeSlide">
      <div class="form-section" :class="{ active: activeSection === 2, completed: activeSection > 2 }" v-show="activeSection >= 2">
        <h2>Shipping Method</h2>
        <div class="section-content">
        <!-- Store Pickup -->
        <div v-if="deliveryOption === 'pickup'" class="shipping-option selected">
          <div class="option-header">
            <input type="radio" checked disabled />
            <span class="option-title">Store Pickup</span>
          </div>
          <p class="option-details">Location: 67 Dickson Street, Fayetteville, AR 72702</p>
        </div>
        <!-- Delivery shipping options -->
        <div v-else class="shipping-options-list">
          <label class="shipping-option" :class="{ selected: shippingMethod === 'standard' }">
            <div class="option-header">
              <input type="radio" v-model="shippingMethod" value="standard" />
              <span class="option-title">Free Standard Shipping</span>
            </div>
            <p class="option-details">Estimated delivery: 5–7 business days &nbsp;|&nbsp; Free</p>
          </label>
          <label class="shipping-option" :class="{ selected: shippingMethod === 'express' }">
            <div class="option-header">
              <input type="radio" v-model="shippingMethod" value="express" />
              <span class="option-title">Express Shipping</span>
            </div>
            <p class="option-details">Estimated delivery: 2–3 business days &nbsp;|&nbsp; $9.99</p>
          </label>
          <label class="shipping-option" :class="{ selected: shippingMethod === 'overnight' }">
            <div class="option-header">
              <input type="radio" v-model="shippingMethod" value="overnight" />
              <span class="option-title">Overnight Shipping</span>
            </div>
            <p class="option-details">Estimated delivery: Next business day &nbsp;|&nbsp; $14.99</p>
          </label>
        </div>
        <div class="section-actions" v-if="activeSection === 2">
          <button type="button" class="save-continue-btn" @click="handleSaveAndContinue(2)">
            Save & Continue
          </button>
        </div>
        </div>
      </div>
      </transition>

      <!-- Payment Section -->
      <transition name="fadeSlide">
      <div class="form-section" :class="{ active: activeSection === 3 }" v-show="activeSection >= 3">
        <h2>Payment</h2>
        <div class="section-content">
        <div class="form-group-row">
          <label class="label-title">Payment Method</label>
        </div>
        <div class="payment-methods">
          <label class="radio-option">
            <input type="radio" v-model="paymentMethod" value="credit" />
            <span>Credit Card</span>
          </label>
          <label class="radio-option">
            <input type="radio" v-model="paymentMethod" value="debit" />
            <span>Debit Card</span>
          </label>
        </div>

        <div class="form-group-row" style="margin-top: 2rem;">
          <label class="label-title">Add Card</label>
        </div>
        <div class="form-group-row">
          <div class="form-group">
            <label for="cardNumber">Card Number</label>
            <input 
              type="text" 
              id="cardNumber" 
              v-model="formData.cardNumber" 
              placeholder="1234 5678 9012 3456"
              maxlength="19"
              required
            />
          </div>
        </div>
        <div class="form-group-row">
          <div class="form-group">
            <label for="expirationDate">Expiration Date</label>
            <input 
              type="text" 
              id="expirationDate" 
              v-model="formData.expirationDate" 
              placeholder="MM/YY"
              maxlength="5"
              required
            />
          </div>
          <div class="form-group">
            <label for="cvv">CVV</label>
            <input 
              type="text" 
              id="cvv" 
              v-model="formData.cvv" 
              placeholder="123"
              maxlength="4"
              required
            />
          </div>
        </div>
        </div>
      </div>
      </transition>

      <!-- Checkout Component (Buttons) -->
      <div class="checkout-component" v-if="activeSection === 3">
        <CancelButton />
        <CompleteOrderButton v-if="isPaymentComplete()" @complete="completeOrder" />
      </div>
    </form>
  </section>
</template>

<style scoped>
.checkout-page {
  padding: 60px 20px;
  max-width: 900px;
  margin: 0 auto;
}

.checkout-header {
  margin-bottom: 3rem;
  text-align: center;
}

.checkout-header h1 {
  font-size: 2.5rem;
  color: #333;
  border-bottom: 3px solid #000;
  padding-bottom: 1rem;
  margin-bottom: 1rem;
}

.checkout-header p {
  font-size: 1rem;
  color: #000000;
  max-width: 700px;
  margin: 0 auto;
}

.checkout-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-section {
  padding: 2rem;
  border-left: 4px solid #000000;
  border-top: 2px solid #e0e0e0;
  border-right: 2px solid #e0e0e0;
  border-bottom: 2px solid #e0e0e0;
  border-radius: 4px;
  background: #f9f9f9;
}

.form-section:not(.active):not(.completed) {
  opacity: 0.5;
  pointer-events: none;
}

.form-section.active {
  opacity: 1;
  pointer-events: auto;
  background: #ffffff;
  border-left-color: #FFD700;
}

.form-section.completed {
  opacity: 0.7;
  pointer-events: none;
  background: #f0f0f0;
}

.form-section h2 {
  font-size: 1.3rem;
  color: #000000;
  margin-bottom: 1.5rem;
  font-weight: 600;
}

.section-content {
  display: block;
}

/* Smooth appearance transitions */
.fadeSlide-enter-active {
  animation: slideInDown 1.2s ease-out;
}

.fadeSlide-leave-active {
  animation: slideOutUp 0.5s ease-in;
}

@keyframes slideInDown {
  from {
    opacity: 0;
    transform: translateY(-50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideOutUp {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(50px);
  }
}

.form-group-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group-row:last-child {
  margin-bottom: 0;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.label-title {
  font-weight: 600;
  color: #333;
  font-size: 0.95rem;
  grid-column: 1 / -1;
}

.form-group input[type="text"],
.form-group input[type="email"],
.form-group input[type="tel"] {
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input[type="text"]:focus,
.form-group input[type="email"]:focus,
.form-group input[type="tel"]:focus {
  outline: none;
  border-color: #FFD700;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.1);
}

.delivery-options,
.payment-methods {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.store-address {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-left: 2.5rem;
  font-size: 0.9rem;
  color: #444;
}

.store-hours {
  font-size: 0.85rem;
  color: #666;
}

.radio-option {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0.5rem 0;
}

.radio-option input[type="radio"] {
  margin-right: 1rem;
  cursor: pointer;
  width: 18px;
  height: 18px;
  accent-color: #FFD700;
}

.radio-option span {
  font-size: 1rem;
  color: #333;
  font-weight: 500;
}

.shipping-options-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.shipping-option {
  display: block;
  padding: 1.5rem;
  border: 2px solid #e0e0e0;
  border-radius: 4px;
  background: white;
  transition: all 0.3s ease;
  cursor: pointer;
}

.shipping-option.selected {
  border-color: #FFD700;
  background: #fffef0;
}

.option-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.option-header input[type="radio"] {
  margin-right: 1rem;
  width: 18px;
  height: 18px;
  accent-color: #FFD700;
}

.option-title {
  font-weight: 600;
  color: #333;
  font-size: 1rem;
}

.option-details {
  margin-left: 2.25rem;
  font-size: 0.9rem;
  color: #666;
}

.section-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e0e0e0;
}

.save-continue-btn {
  padding: 0.75rem 2rem;
  background: #FFD700;
  color: #333;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-continue-btn:hover:not(:disabled) {
  background: #e0c200;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
}

.save-continue-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.checkout-component {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 2rem;
  gap: 1rem;
}
</style>
