<!-- 
User will enter shipping and payment information, and complete their purchase on this page.
Summary of the order, including itemized costs and estimated delivery date. 

In future installments, will add a coupon field.
-->
<script lang="ts" setup>
import CompleteOrderButton from '../Components/Buttons/CompleteOrderButton.vue';
import CancelButton from './Buttons/CancelButton.vue';

</script>

<template>
    <section class="checkout-section">
        <div class="checkout-content">
            <!-- Cart content will go here -->
        </div>
        <div class="checkout-buttons">
            <CancelButton />
            <CompleteOrderButton />
        </div>
    </section>
</template>

<style scoped>
.checkout-section {
  padding: 80px 20px 20px 20px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.checkout-content {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.checkout-buttons {
  display: flex;
  gap: 20px;
  align-items: center;
  padding: 30px 20px;
  margin-top: auto;
  position: sticky;
  bottom: 0;
  z-index: 100;
}
</style>
