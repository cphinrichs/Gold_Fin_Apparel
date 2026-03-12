<!-- 
This page will allow users to review their selected items, 
enter shipping and payment information, delete and complete their purchase.
-->
<script setup lang="ts">
import CheckOutButton from './Buttons/CheckOutButton.vue';
import DeleteFromCartButton from './Buttons/DeleteFromCartButton.vue';
import QuantityModifierButton from './Buttons/QuantityModifierButton.vue';
import BrowseButton from './Buttons/BrowseButton.vue';
</script>

<template>
    <section class="cart-section">
        <div class="cart-container">
            <!-- <div class="cart-items">
                <DeleteFromCartButton />
                <QuantityModifierButton />
            </div>  -->
        </div>
        <div class="browse-footer">
            <BrowseButton />
        </div>
        <div class="checkout-browse-footer">
            <CheckOutButton />
        </div>
    </section>
</template>

<style scoped>
.cart-section {
  padding: 80px 20px 100px 20px;
  min-height: 100vh;
  position: relative;
}

.cart-container {
  max-width: 1200px;
  margin: 0 auto;
}

.cart-items {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  align-items: center;
  margin: 30px 0;
}

.checkout-browse-footer {
  position: fixed;
  bottom: 20px;
  left: 20px;
  z-index: 999;
}
</style>