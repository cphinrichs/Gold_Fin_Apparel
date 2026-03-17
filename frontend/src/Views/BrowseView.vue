<template>
  <section>
    <div class="browse">
      <h1>Browse Products</h1>
      <div v-if="loading" class="loading">Loading products...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else class="product-list">
        <button
          v-for="product in products"
          :key="product.product_id"
          :class="['product-item']"
          :style="{ backgroundColor: `#${product.color}` }"
          @click="navigateToProduct(product.product_id)">
          <div class="product-info">
            <h3>{{ product.style }}</h3>
            <p>{{ product.material }}</p>
            <p>Size: {{ product.size.trim() }}</p>
            <p>Stock: {{ product.stock }}</p>
          </div>
        </button>
      </div>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

interface Product {
  product_id: number
  style: string
  color: string
  material: string
  size: string
  stock: number
}

const router = useRouter()
const products = ref<Product[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

const fetchProducts = async () => {
  try {
    loading.value = true
    error.value = null
  
    const response = await fetch('/api/inventory')
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    products.value = data.inventory
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load products'
    console.error('Error fetching products:', err)
  } finally {
    loading.value = false
  }
}

const navigateToProduct = (productId: number) => {
  router.push({ name: 'Inspect', params: { id: productId } })
}

onMounted(() => {
  fetchProducts()
})
</script>

<style scoped>
.browse {
  padding: 20px;
}

.loading,
.error {
  text-align: center;
  padding: 40px;
  font-size: 1.2rem;
}

.error {
  color: #d32f2f;
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
  object-fit: contain;
  border-radius: 4px;
}

.product-info {
  color: white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
  text-align: center;
}

.product-info h3 {
  margin: 0 0 8px 0;
  font-size: 1.2rem;
}

.product-info p {
  margin: 4px 0;
  font-size: 0.9rem;
}
</style>