<script lang="ts" setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import CancelButton from '../Components/Buttons/CancelButton.vue';
import CompleteOrderButton from '../Components/Buttons/CompleteOrderButton.vue';
import { useCart } from '../Composables/useCart';

const router = useRouter();
const { cartItems, clearCart } = useCart();

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

// Track which fields the user has blurred (to show errors only after interaction)
const touched = reactive<Record<string, boolean>>({});
const touch = (field: string) => { touched[field] = true; };

// Validators
const validateName = (v: string) => /^[a-zA-Z\s\-']{2,}$/.test(v.trim());
const validateEmail = (v: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim());
const validateCity = (v: string) => /^[a-zA-Z\s\-']{2,}$/.test(v.trim());
const validateState = (v: string) => /^[a-zA-Z\s]{2,}$/.test(v.trim());
const validatePostalCode = (v: string) => /^\d{5}(-\d{4})?$/.test(v.trim());
const validatePhone = (v: string) => /^\(\d{3}\) \d{3}-\d{4}$/.test(v.trim());

const validateExpiration = (v: string): boolean => {
  if (!/^\d{2}\/\d{2}$/.test(v)) return false;
  const [mm, yy] = v.split('/').map(Number);
  if (mm < 1 || mm > 12) return false;
  const now = new Date();
  const expYear = 2000 + yy;
  const expMonth = mm; // 1-based
  const nowYear = now.getFullYear();
  const nowMonth = now.getMonth() + 1; // 1-based
  const isFuture = expYear > nowYear || (expYear === nowYear && expMonth > nowMonth);
  const isWithinMax = expYear <= nowYear + 5;
  return isFuture && isWithinMax;
};

const fieldErrors: Record<string, string> = {
  firstName: 'First name must contain only letters',
  lastName: 'Last name must contain only letters',
  email: 'Enter a valid email address (e.g. name@example.com)',
  city: 'City must contain only letters',
  state: 'Enter a valid state name or abbreviation',
  postalCode: 'Enter a valid 5-digit ZIP code (e.g. 72701)',
  phoneNumber: 'Enter a valid 10-digit phone number (e.g. (479) 555-0123)',
  expirationDate: 'Expiration date must be a valid (1 - 12) and future month within 5 years (MM/YY)',
};

const isFieldValid = (field: string): boolean => {
  const v = formData.value[field as keyof typeof formData.value];
  switch (field) {
    case 'firstName':  return validateName(v);
    case 'lastName':   return validateName(v);
    case 'email':      return validateEmail(v);
    case 'city':       return validateCity(v);
    case 'state':      return validateState(v);
    case 'postalCode': return validatePostalCode(v);
    case 'phoneNumber':return validatePhone(v);
    case 'expirationDate': return validateExpiration(v);
    default:           return !!v;
  }
};

const showError = (field: string): boolean => touched[field] && !isFieldValid(field);

// Auto-format phone to (XXX) XXX-XXXX
const formatPhone = (e: Event) => {
  const input = e.target as HTMLInputElement;
  const digits = input.value.replace(/\D/g, '').slice(0, 10);
  let formatted = digits;
  if (digits.length > 6) formatted = `(${digits.slice(0,3)}) ${digits.slice(3,6)}-${digits.slice(6)}`;
  else if (digits.length > 3) formatted = `(${digits.slice(0,3)}) ${digits.slice(3)}`;
  else if (digits.length > 0) formatted = `(${digits}`;
  formData.value.phoneNumber = formatted;
  input.value = formatted;
};

// Postal code: digits only, max 5
const formatPostalCode = (e: Event) => {
  const input = e.target as HTMLInputElement;
  const digits = input.value.replace(/\D/g, '').slice(0, 5);
  formData.value.postalCode = digits;
  input.value = digits;
};

const handleSaveAndContinue = (section: number) => {
  activeSection.value = section + 1;
};

const isPersonalInfoComplete = (): boolean => {
  return !!(
    validateName(formData.value.firstName) &&
    validateName(formData.value.lastName) &&
    formData.value.address &&
    validateEmail(formData.value.email) &&
    validateCity(formData.value.city) &&
    validateState(formData.value.state) &&
    validatePostalCode(formData.value.postalCode) &&
    validatePhone(formData.value.phoneNumber)
  );
};

const isPaymentComplete = (): boolean => {
  return (
    formData.value.cardNumber.replace(/\s/g, '').length === 16 &&
    validateExpiration(formData.value.expirationDate) &&
    formData.value.cvv.length === 3
  );
};

const formatCardNumber = (e: Event) => {
  const input = e.target as HTMLInputElement;
  const digits = input.value.replace(/\D/g, '').slice(0, 16);
  const formatted = digits.replace(/(\d{4})(?=\d)/g, '$1 ');
  formData.value.cardNumber = formatted;
  input.value = formatted;
};

const formatExpiration = (e: Event) => {
  const input = e.target as HTMLInputElement;
  const raw = input.value.replace(/\D/g, '').slice(0, 4);
  const formatted = raw.length > 2 ? raw.slice(0, 2) + '/' + raw.slice(2) : raw;
  formData.value.expirationDate = formatted;
  input.value = formatted;
};

const formatCvv = (e: Event) => {
  const input = e.target as HTMLInputElement;
  const digits = input.value.replace(/\D/g, '').slice(0, 3);
  formData.value.cvv = digits;
  input.value = digits;
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

  const orderedItems = JSON.parse(JSON.stringify(cartItems.value));
  const orderTotal = cartItems.value.reduce((sum, item) => sum + item.Price * item.quantity, 0).toFixed(2);

  clearCart();

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
      orderedItems,
      orderTotal,
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
              @blur="touch('email')"
              :class="{ 'input-error': showError('email') }"
              required
            />
            <span class="error-msg" v-if="showError('email')">{{ fieldErrors.email }}</span>
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
              @blur="touch('firstName')"
              :class="{ 'input-error': showError('firstName') }"
              required
            />
            <span class="error-msg" v-if="showError('firstName')">{{ fieldErrors.firstName }}</span>
          </div>
          <div class="form-group">
            <label for="lastName">Last Name</label>
            <input 
              type="text" 
              id="lastName" 
              v-model="formData.lastName" 
              placeholder="Last name"
              @blur="touch('lastName')"
              :class="{ 'input-error': showError('lastName') }"
              required
            />
            <span class="error-msg" v-if="showError('lastName')">{{ fieldErrors.lastName }}</span>
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
              @blur="touch('city')"
              :class="{ 'input-error': showError('city') }"
              required
            />
            <span class="error-msg" v-if="showError('city')">{{ fieldErrors.city }}</span>
          </div>
          <div class="form-group">
            <label for="state">State</label>
            <input 
              type="text" 
              id="state" 
              v-model="formData.state" 
              placeholder="State"
              @blur="touch('state')"
              :class="{ 'input-error': showError('state') }"
              required
            />
            <span class="error-msg" v-if="showError('state')">{{ fieldErrors.state }}</span>
          </div>
          <div class="form-group">
            <label for="postalCode">Postal Code</label>
            <input 
              type="text" 
              id="postalCode" 
              :value="formData.postalCode"
              @input="formatPostalCode"
              placeholder="72701"
              maxlength="5"
              inputmode="numeric"
              @blur="touch('postalCode')"
              :class="{ 'input-error': showError('postalCode') }"
              required
            />
            <span class="error-msg" v-if="showError('postalCode')">{{ fieldErrors.postalCode }}</span>
          </div>
        </div>
        <div class="form-group-row">
          <div class="form-group">
            <label for="phoneNumber">Phone Number</label>
            <input 
              type="tel" 
              id="phoneNumber" 
              :value="formData.phoneNumber"
              @input="formatPhone"
              placeholder="(479) 555-0123"
              maxlength="14"
              @blur="touch('phoneNumber')"
              :class="{ 'input-error': showError('phoneNumber') }"
              required
            />
            <span class="error-msg" v-if="showError('phoneNumber')">{{ fieldErrors.phoneNumber }}</span>
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
              :value="formData.cardNumber"
              @input="formatCardNumber"
              placeholder="1234 5678 9012 3456"
              maxlength="19"
              inputmode="numeric"
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
              :value="formData.expirationDate"
              @input="formatExpiration"
              placeholder="MM/YY"
              maxlength="5"
              inputmode="numeric"
              @blur="touch('expirationDate')"
              :class="{ 'input-error': showError('expirationDate') }"
              required
            />
            <span class="error-msg" v-if="showError('expirationDate')">{{ fieldErrors.expirationDate }}</span>
          </div>
          <div class="form-group">
            <label for="cvv">CVV</label>
            <input 
              type="text" 
              id="cvv" 
              :value="formData.cvv"
              @input="formatCvv"
              placeholder="123"
              maxlength="3"
              inputmode="numeric"
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

.form-group input.input-error {
  border-color: #e53935;
  box-shadow: 0 0 0 3px rgba(229, 57, 53, 0.1);
}

.error-msg {
  margin-top: 0.3rem;
  font-size: 0.8rem;
  color: #e53935;
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
