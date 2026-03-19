<template>
  <button class="add-to-cart-btn" @click="handleAddToCart">
    <span class="btn-icon">+</span>
    <span class="btn-text">Add to Cart</span>
  </button>
</template>

<script setup lang="ts">
const handleAddToCart = () => {
  // Add to cart logic here
  console.log('Item added to cart');
};
</script>

<style scoped>
.add-to-cart-btn {
  background: transparent;
  border: 2px solid #FFD700;
  padding: 12px 28px;
  font-size: 1rem;
  font-weight: 500;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #FFD700;
  text-transform: uppercase;
}

.add-to-cart-btn:hover {
  background-color: #FFD700;
  color: #333;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
}

.add-to-cart-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(255, 215, 0, 0.2);
}

.btn-icon {
  font-size: 1.2rem;
  font-weight: bold;
}

.btn-text {
  letter-spacing: 0.05em;
}
</style>
