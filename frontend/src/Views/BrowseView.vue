<template>
  <div class="page-wrapper">
    <section>
      <div class="browse">
      <h1>Browse Products</h1>
      <div v-if="loading" class="loading">Loading products...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="!products || products.length === 0" class="no-products">
        No products found. Products array: {{ products }}
      </div>
      <div v-else class="product-list">
        <button
          v-for="product in products"
          :key="product.Product_Id"
          :class="['product-item']"
          :style="{ backgroundColor: `#${product.Color}` }"
          @click="navigateToProduct(product.Product_Id)">
          <div class="product-info">
            <h3>{{ product.Style }}</h3>
            <p>{{ product.Material }}</p>
            <p>Size: {{ product.Size.trim() }}</p>
            <p>Stock: {{ product.Stock }}</p>
          </div>
        </button>
      </div>
    </div>
  </section>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

interface Product {
  Product_Id: number
  Style: string
  Color: string
  Material: string
  Size: string
  Stock: number
  Price: number
}

const router = useRouter()
const products = ref<Product[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

const fetchProducts = async () => {
  try {
    loading.value = true
    error.value = null
  
    console.log('Fetching products from /api/inventory...')
    const response = await fetch('/api/inventory')
    console.log('Response status:', response.status)
    console.log('Response ok:', response.ok)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('Full API response:', data)
    console.log('Type of data:', typeof data)
    console.log('Is array?', Array.isArray(data))
    
    // Handle both response formats
    if (Array.isArray(data)) {
      products.value = data
      console.log('Data is array, set directly')
    } else if (data.inventory && Array.isArray(data.inventory)) {
      products.value = data.inventory
      console.log('Data has inventory property')
    } else {
      console.error('Unexpected data format:', data)
      products.value = []
    }
    
    console.log('products.value set to:', products.value)
    console.log('Number of products:', products.value.length)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load products'
    console.error('Error fetching products:', err)
    products.value = []
  } finally {
    loading.value = false
    console.log('Loading complete. Products count:', products.value.length)
  }
}

const navigateToProduct = (productId: number) => {
  console.log('Navigating to product:', productId)
  router.push({ name: 'Inspect', params: { id: productId.toString() } })
}

onMounted(() => {
  console.log('BrowseView mounted, fetching products...')
  fetchProducts()
})
</script>

<style scoped>
.page-wrapper {
  position: relative;
}

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