<template>
  <section class="home">
    <div class="hero-overlay"></div>
    <div class="hero-content">
      <img 
        src="../Assets/goldenfinger.png" 
        alt="Gold Fin Apparel" 
        class="hero-logo" 
        @click="scrollToProducts"
      />
    </div>
  </section>
  <section class="product-list" ref="productSection">
    <h2 class="section-title">Featured Products</h2>
    <div class="product-grid">
      <div 
        v-for="(product, index) in products" 
        :key="index" 
        class="product-item"
        :style="{ animationDelay: `${index * 0.05}s` }"
        @click="navigateToProduct(product.id)"
      >
        <div class="product-image-wrapper">
          <img :src="product.image" :alt="product.alt">
          <div class="product-overlay">
            <span class="view-details">View Details</span>
          </div>
        </div>
        <div class="product-info">
          <h3>{{ product.style }}</h3>
          <p class="product-price">${{ product.price.toFixed(2) }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
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
const productSection = ref<HTMLElement | null>(null)

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

const navigateToProduct = (productId: number) => {
  router.push({ name: 'Inspect', params: { id: productId } })
}

const scrollToProducts = () => {
  productSection.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

onMounted(async () => {
  await loadProducts()
})
</script>

<style scoped>
/* Hero Section */
.home {
  position: relative;
  width: 100%;
  height: 100vh;
  font-family: Arial, sans-serif;
  background-image: url('../Assets/landing.png');
  background-size: cover;
  background-position: center top;
  background-repeat: no-repeat;
  background-attachment: fixed;
  margin-top: -80px;
  padding-top: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.7) 0%, rgba(0, 0, 0, 0.5) 100%);
  animation: fadeIn 1s ease-in;
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  color: white;
  max-width: 800px;
  padding: 2rem;
}

.hero-logo {
  max-width: 800px;
  width: 90%;
  cursor: pointer;
  height: auto;
  animation: fadeInUp 1s ease-out;
  filter: drop-shadow(0 10px 30px rgba(0, 0, 0, 0.5));
  transition: transform 0.3s ease;
}

.hero-logo:hover {
  transform: scale(1.05);
}

/* Product List Section */
.product-list {
  padding: 4rem 2rem;
  background: linear-gradient(to bottom, #0a0a0a 0%, #1a1a1a 100%);
  animation: fadeIn 1s ease-in;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  margin: 0 0 3rem 0;
  color: #d4af37;
  font-weight: 700;
  position: relative;
  animation: fadeInDown 0.8s ease-out;
  text-transform: uppercase;
  letter-spacing: 3px;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 3px;
  background: linear-gradient(90deg, transparent 0%, #d4af37 50%, transparent 100%);
  border-radius: 2px;
}

/* Product Grid */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem;
}

.product-item {
  background: #1a1a1a;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  animation: slideInUp 0.6s ease-out backwards;
  border: 1px solid rgba(212, 175, 55, 0.2);
}

.product-item:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 12px 35px rgba(212, 175, 55, 0.3), 0 8px 20px rgba(0, 0, 0, 0.6);
  border-color: rgba(212, 175, 55, 0.5);
}

.product-image-wrapper {
  position: relative;
  overflow: hidden;
  width: 100%;
  height: 300px;
  background: #0f0f0f;
}

.product-item img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 0.5s ease;
}

.product-item:hover img {
  transform: scale(1.1);
}

.product-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to top, rgba(212, 175, 55, 0.9) 0%, rgba(0, 0, 0, 0.7) 100%);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.product-item:hover .product-overlay {
  opacity: 1;
}

.view-details {
  color: #0a0a0a;
  font-weight: 700;
  font-size: 1rem;
  padding: 1rem;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.product-info {
  padding: 1.5rem;
  text-align: center;
  background: #1a1a1a;
}

.product-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.3rem;
  color: #e8e8e8;
  font-weight: 600;
  transition: color 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.product-item:hover .product-info h3 {
  color: #d4af37;
}

.product-price {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 700;
  background: linear-gradient(135deg, #d4af37 0%, #f4d03f 50%, #d4af37 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 1px;
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-logo {
    max-width: 400px;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .product-grid {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 1.5rem;
  }
}

@media (max-width: 480px) {
  .hero-logo {
    max-width: 280px;
  }
  
  .product-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
</style>