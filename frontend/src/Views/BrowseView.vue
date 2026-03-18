<template>
  <div class="page-wrapper">
    <section>
      <div class="browse">
        <h1>Browse Products</h1>
        
        <p v-if="route.query.style" class="filter-info">
          Showing: {{ route.query.style }}
        </p>
        
        <div v-if="loading" class="loading">
          Loading products...
        </div>
        
        <div v-else-if="error" class="error">
          {{ error }}
        </div>
        
        <div v-else-if="!filteredProducts || filteredProducts.length === 0" class="no-products">
          No products found{{ route.query.style ? ` for "${route.query.style}"` : '' }}.
        </div>
        
        <div v-else class="product-list">
          <button
            v-for="product in filteredProducts"
            :key="product.Product_Id"
            class="product-item"
            :style="{ backgroundColor: `#${product.Color}` }"
            @click="handleProductClick(product.Product_Id)">
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
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useInventory } from '../Composables/useInventory'
import { useProductFiltering } from '../Composables/useProductFiltering'
import { navigateToProductDetail } from '../Utils/navigationHelpers'

// Router setup
const router = useRouter()
const route = useRoute()

// Inventory management
const { products, loading, error, loadProducts } = useInventory()

// Product filtering
const { filteredProducts, watchRouteChanges } = useProductFiltering(products, route)

// Event handlers
const handleProductClick = (productId: number) => {
  navigateToProductDetail(router, productId)
}

// Initialize component
onMounted(() => {
  console.log('BrowseView mounted, fetching products...')
  console.log('Current route query:', route.query)
  loadProducts()
  watchRouteChanges()
})
</script>

<style scoped src="../styles/BrowseView.styles.css"></style>