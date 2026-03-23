<template>
  <section class="home">
  </section>
  <section class="product-list">
    <div 
      class="carousel-container"
      @mouseenter="stopAutoPlay"
      @mouseleave="startAutoPlay"
    >
      <button class="carousel-btn prev" @click="prevSlide">
        &#10094;
      </button>
      
      <div class="carousel-wrapper">
        <div class="carousel-track" :style="{ transform: `translateX(-${currentIndex * (100 / itemsPerView)}%)` }">
          <div v-for="(product, index) in products" :key="index" class="product-item" @click="navigateToProduct(product.id)">
            <img :src="product.image" :alt="product.alt">
            <div class="product-info">
              <h3>{{ product.style }}</h3>
              <p class="product-price">${{ product.price.toFixed(2) }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <button class="carousel-btn next" @click="nextSlide">
        &#10095;
      </button>
    </div>
    
    <div class="carousel-dots">
      <span 
        v-for="(dot, index) in Math.ceil(products.length / itemsPerView)" 
        :key="index"
        class="dot"
        :class="{ active: Math.floor(currentIndex / itemsPerView) === index }"
        @click="goToSlide(index * itemsPerView)"
      ></span>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useInventory } from '../Composables/useInventory'
import { getStyleFrontImage } from '../Constants/productMappings'
import type { ProductApiResponse } from '../Types/product.types'

interface DisplayProduct {
  id: number
  image: string
  alt: string
  style: string
  price: number
  color: string
}

const router = useRouter()
const { products: inventoryData, loadProducts } = useInventory()

const currentIndex = ref(0)
const itemsPerView = ref(3) // Number of items visible at once
const autoPlayInterval = ref<number | null>(null)
const autoPlayDelay = 3000 // 3 seconds

// Get unique products by style for display
const products = computed<DisplayProduct[]>(() => {
  const uniqueStyles = new Map<string, ProductApiResponse>()
  
  // Get one representative product per style
  inventoryData.value.forEach(product => {
    if (!uniqueStyles.has(product.Style)) {
      uniqueStyles.set(product.Style, product)
    }
  })
  
  // Convert to display format
  return Array.from(uniqueStyles.values()).map(product => ({
    id: product.Product_Id,
    image: getStyleFrontImage(product.Style),
    alt: `${product.Style} - ${product.Material}`,
    style: product.Style,
    price: product.Price,
    color: product.Color
  }))
})

const nextSlide = () => {
  if (currentIndex.value >= products.value.length - itemsPerView.value) {
    currentIndex.value = 0 // Loop back to start
  } else {
    currentIndex.value++
  }
}

const prevSlide = () => {
  if (currentIndex.value <= 0) {
    currentIndex.value = products.value.length - itemsPerView.value // Loop to end
  } else {
    currentIndex.value--
  }
}

const goToSlide = (index: number) => {
  currentIndex.value = index
  stopAutoPlay()
  startAutoPlay()
}

const startAutoPlay = () => {
  autoPlayInterval.value = window.setInterval(() => {
    nextSlide()
  }, autoPlayDelay)
}

const stopAutoPlay = () => {
  if (autoPlayInterval.value !== null) {
    clearInterval(autoPlayInterval.value)
    autoPlayInterval.value = null
  }
}

const navigateToProduct = (productId: number) => {
  router.push({ name: 'Inspect', params: { id: productId } })
}

onMounted(async () => {
  await loadProducts()
  startAutoPlay()
})

onUnmounted(() => {
  stopAutoPlay()
})
</script>

<style scoped>
.home {
  width: 100%;
  height: 100vh;
  font-family: Arial, sans-serif;
  background-image: url('../Assets/landing.png');
  background-size: cover;
  background-position: center top;
  background-repeat: no-repeat;
  margin-top: -80px;
  padding-top: 80px;
}

.product-list {
  padding: 3rem 2rem;
  background-color: #f5f5f5;
}

.carousel-container {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.carousel-wrapper {
  overflow: hidden;
  flex: 1;
}

.carousel-track {
  display: flex;
  transition: transform 0.4s ease-in-out;
  gap: 2rem;
}

.product-item {
  flex: 0 0 calc(33.333% - 1.333rem);
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  cursor: pointer;
}

.product-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.product-item img {
  width: 100%;
  height: 300px;
  object-fit: contain;
}

.product-info {
  padding: 1rem;
  text-align: center;
}

.product-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
  color: #333;
}

.product-price {
  margin: 0;
  font-size: 1.1rem;
  font-weight: bold;
  color: #2c3e50;
}

.carousel-btn {
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
  flex-shrink: 0;
}

.carousel-btn:hover:not(:disabled) {
  background-color: rgba(0, 0, 0, 0.8);
}

.carousel-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.carousel-dots {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 2rem;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #ccc;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.dot.active {
  background-color: #333;
}

.dot:hover {
  background-color: #666;
}
</style>