<!-- 
This page will allow users to review their selected items, 
enter shipping and payment information, delete and complete their purchase.
-->
<script setup lang="ts">
import CheckOutButton from './Buttons/CheckOutButton.vue';
import BrowseButton from './Buttons/BrowseButton.vue';
import { ref, computed } from 'vue';
import { useCart } from '../Composables/useCart';
import { getStyleImageUrl, getMaterialTextureUrl, getDesignImageUrl } from '../Utils/browseImageHelpers';

const { cartItems, removeFromCart, removeQuantityFromCart, clearCart } = useCart();

const cartTotal = computed(() =>
  cartItems.value.reduce((sum, item) => sum + item.Price * (item.quantity ?? 1), 0).toFixed(2)
);

// Single-item remove dialog
const pendingRemoveId = ref<string | null>(null);
const pendingRemoveQty = ref(1);
const pendingItemMaxQty = ref(1);

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
  const item = cartItems.value.find(i => i.cartItemId === cartItemId);
  pendingItemMaxQty.value = item?.quantity ?? 1;
  pendingRemoveQty.value = 1;
  pendingRemoveId.value = cartItemId;
};

const confirmRemove = () => {
  if (pendingRemoveId.value) {
    removeQuantityFromCart(pendingRemoveId.value, pendingRemoveQty.value);
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
                        class="cart-item">
                        <!-- Layered product image -->
                        <div class="cart-item-image" :style="{ backgroundColor: item.Color }">
                            <div class="cart-layer material-layer" :style="{ backgroundImage: `url(${getMaterialTextureUrl(item.Material)})` }"></div>
                            <div class="cart-layer design-layer" :style="{ backgroundImage: `url(${getDesignImageUrl(item.Design_Id)})` }"></div>
                            <img
                                v-if="getStyleImageUrl(item.Style)"
                                :src="getStyleImageUrl(item.Style)"
                                :alt="item.Style"
                                class="cart-style-image"
                            />
                        </div>
                        <!-- Info below image -->
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
                <p v-if="pendingItemMaxQty === 1">Are you sure you want to remove this item from your cart?</p>
                <template v-else>
                  <p>How many would you like to remove?</p>
                  <div class="qty-selector">
                    <button class="qty-btn" @click="pendingRemoveQty = Math.max(1, pendingRemoveQty - 1)">−</button>
                    <span class="qty-display">{{ pendingRemoveQty }}</span>
                    <button class="qty-btn" @click="pendingRemoveQty = Math.min(pendingItemMaxQty, pendingRemoveQty + 1)">+</button>
                  </div>
                  <p class="qty-hint">{{ pendingRemoveQty === pendingItemMaxQty ? 'This will remove the item entirely.' : `${pendingItemMaxQty - pendingRemoveQty} will remain in your cart.` }}</p>
                </template>
                <div class="confirm-actions">
                    <button class="confirm-no" @click="cancelRemove">Cancel</button>
                    <button class="confirm-yes" @click="confirmRemove">Remove</button>
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
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.2s;
  position: relative;
  overflow: hidden;
}

.cart-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Layered image area */
.cart-item-image {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  flex-shrink: 0;
}

.cart-layer {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.material-layer {
  opacity: 0.35;
  mix-blend-mode: multiply;
}

.design-layer {
  opacity: 0.7;
  mix-blend-mode: overlay;
  background-size: 60%;
  background-position: center;
}

.cart-style-image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.cart-item-info {
  padding: 10px 12px;
  background: #fff;
  text-align: center;
}

.cart-item-info h3 {
  margin: 0 0 4px 0;
  font-size: 1rem;
}

.cart-item-info p {
  margin: 3px 0;
  font-size: 0.85rem;
  color: #555;
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

/* Quantity selector in remove dialog */
.qty-selector {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin: 0.75rem 0;
}

.qty-btn {
  width: 36px;
  height: 36px;
  border: 2px solid #333;
  border-radius: 4px;
  background: #fff;
  color: #333;
  font-size: 1.2rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s, color 0.2s;
}

.qty-btn:hover {
  background: #333;
  color: #FFD700;
}

.qty-display {
  font-size: 1.4rem;
  font-weight: 700;
  color: #333;
  min-width: 2rem;
  text-align: center;
}

.qty-hint {
  font-size: 0.85rem !important;
  color: #888 !important;
  margin: 0 0 0.5rem 0 !important;
}

</style>