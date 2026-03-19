<!-- 
This page will allow users to review their selected items, 
enter shipping and payment information, delete and complete their purchase.
-->
<script setup lang="ts">
import CheckOutButton from './Buttons/CheckOutButton.vue';
import BrowseButton from './Buttons/BrowseButton.vue';
import { ref, computed } from 'vue';
import { useCart } from '../Composables/useCart';

const { cartItems, removeFromCart, clearCart } = useCart();

const cartTotal = computed(() =>
  cartItems.value.reduce((sum, item) => sum + item.Price * (item.quantity ?? 1), 0).toFixed(2)
);

// Single-item remove dialog
const pendingRemoveId = ref<string | null>(null);

// Clear all dialog
const showClearConfirm = ref(false);

const promptClearAll = () => {
  showClearConfirm.value = true;
};

const confirmClearAll = () => {
  clearCart();
  showClearConfirm.value = false;
};

const cancelClearAll = () => {
  showClearConfirm.value = false;
};

const promptRemove = (cartItemId: string) => {
  pendingRemoveId.value = cartItemId;
};

const confirmRemove = () => {
  if (pendingRemoveId.value) {
    removeFromCart(pendingRemoveId.value);
    pendingRemoveId.value = null;
  }
};

const cancelRemove = () => {
  pendingRemoveId.value = null;
};
</script>

<template>
    <section class="cart-section">
        <div class="cart-container">

            <!-- Empty cart state -->
            <div v-if="cartItems.length === 0" class="empty-cart">
                <p>Your cart is empty.</p>
            </div>

            <!-- Cart items grid -->
            <div v-else>
                <div class="cart-items-grid">
                    <div
                        v-for="item in cartItems"
                        :key="item.cartItemId"
                        class="cart-item"
                        :style="{ backgroundColor: item.Color }">
                        <div class="cart-item-info">
                            <h3>{{ item.Style }}</h3>
                            <p>{{ item.Material }}</p>
                            <p>Size: {{ item.Size }}</p>
                            <p class="cart-item-price">${{ item.Price.toFixed(2) }}</p>
                        </div>
                        <!-- Quantity badge top-right -->
                        <span class="quantity-badge" v-if="item.quantity > 1">× {{ item.quantity }}</span>
                        <!-- X remove button bottom-left -->
                        <button class="remove-btn" @click="promptRemove(item.cartItemId)" title="Remove from cart">
                            ✕
                        </button>
                    </div>
                </div>

                <!-- Cart total + Clear All row -->
                <div class="cart-total-row">
                    <button class="clear-all-btn" @click="promptClearAll">Clear All</button>
                    <div class="cart-total">
                        <span class="cart-total-label">Order Total</span>
                        <span class="cart-total-value">${{ cartTotal }}</span>
                    </div>
                </div>
            </div>

        </div>

        <div class="browse-footer">
            <BrowseButton />
        </div>
        <div class="checkout-browse-footer" v-if="cartItems.length > 0">
            <CheckOutButton />
        </div>
    </section>

    <!-- Clear All confirmation dialog -->
    <Teleport to="body">
        <div class="confirm-overlay" v-if="showClearConfirm" @click.self="cancelClearAll">
            <div class="confirm-dialog">
                <p>Are you sure you want to remove <strong>all items</strong> from your cart? This cannot be undone.</p>
                <div class="confirm-actions">
                    <button class="confirm-no" @click="cancelClearAll">No</button>
                    <button class="confirm-yes" @click="confirmClearAll">Yes, Clear All</button>
                </div>
            </div>
        </div>
    </Teleport>

    <!-- Remove single item confirmation dialog -->
    <Teleport to="body">
        <div class="confirm-overlay" v-if="pendingRemoveId !== null" @click.self="cancelRemove">
            <div class="confirm-dialog">
                <p>Are you sure you want to remove this item from your cart?</p>
                <div class="confirm-actions">
                    <button class="confirm-no" @click="cancelRemove">No</button>
                    <button class="confirm-yes" @click="confirmRemove">Yes</button>
                </div>
            </div>
        </div>
    </Teleport>
</template>

<style scoped>
.cart-section {
  padding: 20px 20px 100px 20px;
  min-height: 100vh;
  position: relative;
}

.cart-container {
  max-width: 1200px;
  margin: 0 auto;
}

.empty-cart {
  text-align: center;
  padding: 60px 20px;
  font-size: 1.2rem;
  color: #555;
}

/* Same grid layout as BrowseView */
.cart-items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.cart-item {
  border: 1px solid #ddd;
  cursor: default;
  padding: 15px;
  aspect-ratio: 1 / 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  transition: box-shadow 0.2s;
  position: relative;
}

.cart-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.cart-item-info {
  color: white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
  text-align: center;
}

.cart-item-info h3 {
  margin: 0 0 8px 0;
  font-size: 1.2rem;
}

.cart-item-info p {
  margin: 4px 0;
  font-size: 0.9rem;
}

.cart-item-price {
  font-weight: 700;
  font-size: 1rem !important;
  margin-top: 6px !important;
}

/* X button — bottom-left corner of card */
.remove-btn {
  position: absolute;
  bottom: 10px;
  left: 10px;
  width: 32px;
  height: 32px;
  background: rgba(0, 0, 0, 0.55);
  color: #fff;
  border: 2px solid #fff;
  border-radius: 50%;
  font-size: 0.95rem;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
  padding: 0;
}

/* Quantity badge top-right */
.quantity-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #333;
  color: #FFD700;
  font-size: 0.85rem;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: 12px;
  letter-spacing: 0.3px;
}

/* Cart total row */
.cart-total-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 24px;
}

.clear-all-btn {
  padding: 0.55rem 1.4rem;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border: 2px solid #c0392b;
  border-radius: 4px;
  background: transparent;
  color: #c0392b;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.clear-all-btn:hover {
  background: #c0392b;
  color: #fff;
}

.cart-total {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 1rem;
  padding: 16px 20px;
  border: 2px solid #333;
  max-width: 400px;
  margin-left: auto;
}

.cart-total-label {
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.cart-total-value {
  font-size: 1.3rem;
  font-weight: 700;
  color: #333;
}

.checkout-browse-footer {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 999;
}

/* Confirmation dialog */
.confirm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.confirm-dialog {
  background: #fff;
  border: 2px solid #333;
  border-radius: 6px;
  padding: 2rem 2.5rem;
  max-width: 360px;
  width: 90%;
  text-align: center;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.confirm-dialog p {
  font-size: 1rem;
  color: #333;
  margin: 0 0 1.5rem 0;
  line-height: 1.5;
}

.confirm-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.confirm-yes,
.confirm-no {
  padding: 0.6rem 1.8rem;
  font-size: 0.95rem;
  font-weight: 700;
  border: 2px solid #333;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.confirm-yes {
  background: #333;
  color: #FFD700;
}

.confirm-no {
  background: #fff;
  color: #333;
}

</style>