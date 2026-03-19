<template>
  <div class="page-wrapper">
    <SortFilterBrowseWidget @filtersChanged="handleFiltersChanged" />
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
        
        <div v-else-if="!displayedProducts || displayedProducts.length === 0" class="no-products">
          No products found{{ route.query.style ? ` for "${route.query.style}"` : '' }}.
        </div>
        
        <div v-else class="product-list">
          <button
            v-for="product in displayedProducts"
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
import { onMounted, ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useInventory } from '../Composables/useInventory'
import { useProductFiltering } from '../Composables/useProductFiltering'
import { navigateToProductDetail } from '../Utils/navigationHelpers'
import SortFilterBrowseWidget from '../Components/Widgets/SortFilterBrowseWidget.vue'

// Router setup
const router = useRouter()
const route = useRoute()

// Inventory management
const { products, loading, error, loadProducts } = useInventory()

// Product filtering (route-query based)
const { filteredProducts, watchRouteChanges } = useProductFiltering(products, route)

// Widget filter state
type WidgetFilters = {
  colors: string[]
  materials: string[]
  sizes: string[]
  styles: string[]
  sort: string
}
const activeFilters = ref<WidgetFilters>({
  colors: [],
  materials: [],
  sizes: [],
  styles: [],
  sort: '',
})

// Final displayed products — apply widget filters + sort on top of route-filtered list
const displayedProducts = computed(() => {
  let list = filteredProducts.value

  const { colors, materials, sizes, styles, sort } = activeFilters.value

  if (colors.length > 0) {
    list = list.filter(p => colors.some(c => c.toLowerCase() === p.Color.toLowerCase()))
  }
  if (materials.length > 0) {
    list = list.filter(p => materials.includes(p.Material))
  }
  if (sizes.length > 0) {
    list = list.filter(p => sizes.includes(p.Size.trim()))
  }
  if (styles.length > 0) {
    list = list.filter(p => styles.includes(p.Style))
  }

  if (sort === 'price_asc') {
    list = [...list].sort((a, b) => a.Price - b.Price)
  } else if (sort === 'price_desc') {
    list = [...list].sort((a, b) => b.Price - a.Price)
  }

  return list
})

// Event handlers
const handleFiltersChanged = (filters: WidgetFilters) => {
  activeFilters.value = { ...filters }
}

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