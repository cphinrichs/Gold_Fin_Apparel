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

const COLOR_NAMES: Record<string, string> = {
  'FFFFFF': 'White',
  '000000': 'Black',
  '808080': 'Gray',
  'FF0000': 'Red',
  'FF1493': 'Deep Pink',
  'FFC0CB': 'Pink',
  'FFA500': 'Orange',
  'FFFF00': 'Yellow',
  'FFD700': 'Gold',
  '00FF00': 'Lime',
  '008080': 'Teal',
  '0000FF': 'Blue',
  '000080': 'Navy',
  '4B0082': 'Indigo',
  '800080': 'Purple',
  '800000': 'Maroon',
  'A52A2A': 'Brown',
};

const getColorName = (color: string): string => {
  const hex = color.replace(/^#/, '').toUpperCase();
  return COLOR_NAMES[hex] ?? hex;
};

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
                        <!-- Layered product image with info overlay inside -->
                        <div class="cart-item-image" :style="{ backgroundColor: item.Color }">
                            <!-- Layer 1: Material texture -->
                            <div class="material-layer" :style="{ backgroundImage: `url(${getMaterialTextureUrl(item.Material)})` }"></div>
                            <!-- Layer 2: Design -->
                            <div class="design-layer" :style="{ backgroundImage: `url(${getDesignImageUrl(item.Design_Id)})` }"></div>
                            <!-- Layer 3: Style silhouette -->
                            <img
                                v-if="getStyleImageUrl(item.Style)"
                                :src="getStyleImageUrl(item.Style)"
                                :alt="item.Style"
                                class="cart-style-image"
                            />
                            <!-- Info overlay -->
                            <div class="cart-item-info">
                                <h3>{{ item.Style }}</h3>
                                <p class="cart-item-details">{{ item.Material }} | {{ item.Size }}</p>
                                <p class="cart-item-color">
                                    <span class="color-swatch" :style="{ backgroundColor: item.Color }"></span>
                                    {{ getColorName(item.Color) }}
                                </p>
                                <p class="cart-item-price">${{ (item.Price * (item.quantity ?? 1)).toFixed(2) }}</p>
                            </div>
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
                    <div class="qty-remove-controls">
                        <button class="qty-btn" @click="pendingRemoveQty = Math.max(1, pendingRemoveQty - 1)">−</button>
                        <span class="qty-display">{{ pendingRemoveQty }} / {{ pendingItemMaxQty }}</span>
                        <button class="qty-btn" @click="pendingRemoveQty = Math.min(pendingItemMaxQty, pendingRemoveQty + 1)">+</button>
                    </div>
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
  gap: 1.5rem;
  margin-top: 2rem;
}

.cart-item {
  position: relative;
  display: flex;
  flex-direction: column;
  border: 2px solid transparent;
  border-radius: 8px;
  overflow: hidden;
  cursor: default;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background: transparent;
}

.cart-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Image container — matches product-image-container */
.cart-item-image {
  position: relative;
  width: 100%;
  aspect-ratio: 3/4;
  overflow: hidden;
}

/* Layer 1: Material texture */
.material-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  pointer-events: none;
  z-index: 1;
  mix-blend-mode: multiply;
  opacity: 0.4;
}

/* Layer 2: Design graphic */
.design-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
  pointer-events: none;
  z-index: 2;
}

/* Layer 3: Style silhouette */
.cart-style-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  pointer-events: none;
  z-index: 3;
  display: block;
}

/* Info overlay — matches product-info */
.cart-item-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.9) 0%, rgba(0, 0, 0, 0.75) 40%, transparent 70%);
  color: white;
  padding: 1.5rem 1rem;
  z-index: 4;
  text-align: center;
}

.cart-item-info h3 {
  font-size: 1rem;
  margin: 0 0 0.25rem 0;
  font-weight: 600;
  line-height: 1.3;
}

.cart-item-details {
  font-size: 0.75rem;
  margin: 0 0 0.25rem 0;
  opacity: 0.8;
}

.cart-item-price {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 0.25rem 0 0 0;
  color: #ffd700;
}

.cart-item-color {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin: 3px 0;
  font-size: 0.8rem;
  opacity: 0.9;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.color-swatch {
  display: inline-block;
  width: 13px;
  height: 13px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.5);
  flex-shrink: 0;
}

/* X button — bottom-left, above overlay */
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
  z-index: 5;
}

/* Quantity badge top-right, above overlay */
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
  z-index: 5;
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

.qty-remove-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin: 0 0 1.5rem 0;
}

.qty-btn {
  width: 34px;
  height: 34px;
  border: 2px solid #333;
  border-radius: 4px;
  background: #fff;
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
  color: #fff;
}

.qty-display {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  min-width: 60px;
  text-align: center;
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