<template>
  <div class="page-wrapper">
    <SortFilterBrowseWidget @filtersChanged="handleFiltersChanged" />
    <section>
      <div class="browse">
        <h1>Browse Products</h1>
        
        <div v-if="loading" class="loading">
          Loading products...
        </div>
        
        <div v-else-if="error" class="error">
          {{ error }}
        </div>
        
        <div v-else-if="!productCombinations || productCombinations.length === 0" class="no-products">
          No products found{{ route.query.style ? ` for "${route.query.style}"` : '' }}.
        </div>
        
        <div v-else class="product-list">
          <button
            v-for="combination in productCombinations"
            :key="`${combination.inventory.Product_Id}-${combination.design.id}`"
            class="product-item"
            @click="handleProductClick(combination)">
            
            <!-- Product image container with layers -->
            <div class="product-image-container" :style="{ backgroundColor: `#${combination.inventory.Color}` }">
              <!-- Layer 1: Material texture -->
              <div 
                class="material-layer" 
                :style="{ backgroundImage: `url(${getMaterialTextureUrl(combination.inventory.Material)})` }">
              </div>
              
              <!-- Layer 2: Design -->
              <div 
                class="design-layer" 
                :style="{ backgroundImage: `url(${getDesignImageUrl(combination.design.id)})` }">
              </div>
              
              <!-- Layer 3: Style image (product silhouette) -->
              <img 
                v-if="getStyleImageUrl(combination.inventory.Style)" 
                :src="getStyleImageUrl(combination.inventory.Style)" 
                :alt="combination.inventory.Style"
                class="product-style-image"
                @error="handleImageError"
              />
            </div>
            
            <div class="product-info">
              <h3>{{ combination.design.name }}</h3>
              <p class="product-style-name">{{ combination.inventory.Style }}</p>
              <p class="product-details">
                {{ combination.inventory.Material }} | {{ combination.inventory.Size.trim() }}
              </p>
              <p class="product-price">${{ calculatePrice(combination) }}</p>
            </div>
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useInventory } from '../Composables/useInventory'
import { useDesigns } from '../Composables/useDesigns'
import { createProductCombinations } from '../Utils/productCombinations'
import { getStyleImageUrl, getMaterialTextureUrl, getDesignImageUrl } from '../Utils/browseImageHelpers'
import type { ProductCombination } from '../Types/product.types'
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
// Composables
const { products: inventory, loading: inventoryLoading, error: inventoryError, loadProducts } = useInventory()
const { designs, loading: designsLoading, error: designsError, loadDesigns } = useDesigns()

// State
const productCombinations = ref<ProductCombination[]>([])

// Computed
const loading = computed(() => inventoryLoading.value || designsLoading.value)
const error = computed(() => inventoryError.value || designsError.value)

// Load all combinations
const loadCombinations = () => {
  const styleFilter = route.query.style as string | undefined
  productCombinations.value = createProductCombinations(inventory.value, designs.value, styleFilter)
  console.log('Total product combinations:', productCombinations.value.length)
  
  // Log first combination for debugging
  if (productCombinations.value.length > 0) {
    console.log('First combination:', productCombinations.value[0])
  }
}

// Calculate total price (inventory price + design price)
const calculatePrice = (combination: ProductCombination): string => {
  const inventoryPrice = combination.inventory.Price || 0
  const designPrice = combination.design.price || 0
  return (inventoryPrice + designPrice).toFixed(2)
}

// Event handlers
const handleFiltersChanged = (filters: WidgetFilters) => {
  activeFilters.value = { ...filters }
}

const handleProductClick = (combination: ProductCombination) => {
  console.log('Combination clicked:', combination)
  
  // Navigate to Inspect view with product details
  router.push({ 
    name: 'Inspect', 
    params: { id: combination.inventory.Product_Id },
    query: { 
      designId: combination.design.id.toString(),
      color: combination.inventory.Color,
      material: combination.inventory.Material,
      size: combination.inventory.Size.trim(),
      style: combination.inventory.Style
    }
  })
}

const handleImageError = (event: Event) => {
  console.error('Image failed to load:', event)
  const img = event.target as HTMLImageElement
  console.error('Failed image src:', img.src)
}

// Initialize component
onMounted(async () => {
  console.log('BrowseView mounted')
  console.log('Current route query:', route.query)
  
  // Load inventory and designs
  await Promise.all([loadProducts(), loadDesigns()])
  
  // Create combinations after both are loaded
  loadCombinations()
})
</script>

<style scoped src="../styles/BrowseView.styles.css"></style>