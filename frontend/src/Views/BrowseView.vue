<template>
  <section>
    <div class="browse">
      <h1>Browse Products</h1>
      <div class="product-list">
        <button
          v-for="(product, index) in products"
          :key="index"
          :class="['product-item']">
          <img :src="product.image" :alt="`Product thumbnail`">
        </button>
      </div>
    </div>
  </section>
</template>

<script lang="ts" setup>
import productImage from '../Assets/Designer(5).png'

const products = [
  {
    id: 1,
    name: 'Kyoto Signature',
    price: '$499',
    image: productImage
  },
  {
    id: 2,
    name: 'Kyoto Signature',
    price: '$499',
    image: productImage
  }
] 
</script>

<style scoped>
.browse {
  padding: 20px;
}

.product-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.product-item {
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
  padding: 15px;
  transition: transform 0.2s, box-shadow 0.2s;
  aspect-ratio: 1 / 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.product-item img {
  width: 100%;
  height: 100%;
  
  border-radius: 4px;
}
</style>