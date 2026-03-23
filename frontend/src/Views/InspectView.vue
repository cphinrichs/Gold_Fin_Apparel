<template>
    <div class="inspect-container">
        <section class="image-gallery">
            <div class="thumbnail-list">
                <button 
                    v-for="(image, index) in productImages" 
                    :key="index"
                    :class="['thumbnail-item', { active: currentImageIndex === index }]"
                    :style="{ backgroundColor: currentColor}"
                    @click="currentImageIndex = index">
                    <div class="thumbnail-overlay" :style="{ backgroundImage: materialBackgroundImage }"></div>
                    <div class="thumbnail-design" :style="{ backgroundImage: designBackgroundImage }"></div>
                    <img :src="image" :alt="`Product thumbnail ${index + 1}`">
                </button>
            </div>
            <div class="main-image">
                <div class="frame-layer"></div>
                <div class="frame-content">
                    <div class="color-background" :style="{ backgroundColor: currentColor }"></div>
                    <div class="material-layer" :style="{ backgroundImage: materialBackgroundImage }"></div>
                    <div class="design-layer" :style="{ backgroundImage: designBackgroundImage}"></div>
                    <img :src="productImages[currentImageIndex]" :alt="`${productData.name} - Main view`">
                </div>
            </div>
        </section>
        
        <aside class="product-details">
            <h2 class="product-style">{{ productData.style }}</h2>
            <h1 class="product-title">{{ productData.name }}</h1>
            <div class="product-rating">
                <span class="stars">{{ renderStars }}</span>
                <span class="review-count">{{ productData.reviewCount }} reviews</span>
            </div>
            
            <p class="product-description">{{ productData.description }}</p>
            
            <ul class="product-features">
                <li v-for="(feature, index) in productData.features" :key="index">
                    {{ feature }}
                </li>
            </ul>
            
            <div class="product-options">
                <div class="color-selector">
                    <label>Color</label>
                    <div class="color-options">
                        <button 
                            class="color-btn" 
                            v-for="(color, index) in productData.colors" 
                            :key="index" 
                            :class="{ 
                                active: currentColor === color,
                                unavailable: !isColorAvailable(color)
                            }"
                            :style="{ background: color }" 
                            @click="handleColorSelection($event, color, updateColor, clearIncompatibleForColor)">
                        </button>
                    </div>
                </div>

                <div class="material-selector">
                    <label>Material</label>
                    <div class="material-options">
                        <button 
                            class="material-btn" 
                            v-for="(material, index) in productData.materials" 
                            :key="index"
                            :class="{ 
                                active: currentMaterial === material,
                                unavailable: !isMaterialAvailable(material)
                            }"
                            @click="handleMaterialSelection($event, material, updateMaterial, clearIncompatibleForMaterial)">
                            {{ material }}
                        </button>
                    </div>
                </div>
                
                <div class="size-selector">
                    <label>Size</label>
                    <div class="size-options">
                        <button 
                            class="size-btn" 
                            v-for="(size, index) in sortedSizes" 
                            :key="index"
                            :class="{ 
                                active: currentSize === size,
                                unavailable: !isSizeAvailable(size)
                            }"
                            @click="handleSizeSelection($event, size, updateSize, clearIncompatibleForSize)">
                            {{ size }}
                        </button>
                    </div>
                    <router-link :to="{ name: 'SizeCharts' }" class="size-guide">
                        Size Guide
                    </router-link>
                </div>
            </div>
            
            <div class="price-section">
                <span class="price">${{ formattedPrice }}</span>
            </div>

            <!-- Quantity selector -->
            <div class="quantity-selector">
                <label class="quantity-label">Quantity</label>
                <div class="quantity-controls">
                    <button type="button" class="qty-btn" @click="quantity = Math.max(1, quantity - 1)">−</button>
                    <span class="qty-display">{{ quantity }}</span>
                    <button type="button" class="qty-btn" @click="quantity = Math.min(currentStock, quantity + 1)">+</button>
                </div>
            </div>
            
            <button type="button" class="add-to-cart" @click="handleAddToCart" :class="{ added: addedFeedback }">
                {{ addedFeedback ? 'ADDED TO CART ✓' : 'ADD TO CART' }}
            </button>
            
            <div class="shipping-returns">
                <details>
                    <summary>SHIPPING & RETURNS</summary>
                    <div class="details-content">
                        <p>All orders are dispatched from our warehouse in Vietnam.</p>
                        <p><strong>Standard Shipping:</strong> 3-10 business days</p>
                        <p><strong>Returns:</strong> 14 days from receiving your order</p>
                    </div>
                </details>
            </div>
        </aside>
    </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useProductData } from '../Composables/useProductData'
import { useProductSelection } from '../Composables/useProductSelection'
import { useCart } from '../Composables/useCart'
import type { CartItem } from '../Types/product.types'

const route = useRoute()

// Product data composable
const {
    productData,
    currentColor,
    currentMaterial,
    currentSize,
    currentProductId,
    currentStock,
    productImages,
    materialBackgroundImage,
    renderStars,
    formattedPrice,
    fetchProductData,
    isMaterialAvailable,
    isColorAvailable,
    isSizeAvailable,
    clearIncompatibleForColor,
    clearIncompatibleForMaterial,
    clearIncompatibleForSize
} = useProductData()

// Selection composable
const {
    currentImageIndex,
    selectedSize,
    handleColorSelection,
    handleSizeSelection,
    handleMaterialSelection
} = useProductSelection()

// Sort sizes from smallest to largest
const sortedSizes = computed(() => {
    const sizeOrder = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL']
    return [...productData.value.sizes].sort((a, b) => {
        const indexA = sizeOrder.indexOf(a)
        const indexB = sizeOrder.indexOf(b)
        
        // If both sizes are in the order array, sort by position
        if (indexA !== -1 && indexB !== -1) {
            return indexA - indexB
        }
        // If only one is in the array, prioritize it
        if (indexA !== -1) return -1
        if (indexB !== -1) return 1
        // If neither is in the array, sort alphabetically
        return a.localeCompare(b)
    })
})

// Get design image from query parameter
const designBackgroundImage = computed(() => {
    const designId = route.query.designId as string
    if (!designId) return ''
    
    try {
        const imageUrl = new URL(`../Assets/Designs/${designId}.png`, import.meta.url).href
        return `url(${imageUrl})`
    } catch (e) {
        console.error(`Failed to load design image for ID ${designId}:`, e)
        return ''
    }
})

// Cart composable
const { addToCart } = useCart()
const addedFeedback = ref(false)
const quantity = ref(1)

const handleAddToCart = () => {
    const cartItem: CartItem = {
        cartItemId: `${Date.now()}-${Math.random()}`,
        Product_Id: currentProductId.value,
        Design_Id: parseInt(route.query.designId as string) || 0,
        Style: productData.value.style,
        Color: currentColor.value,
        Material: currentMaterial.value,
        Size: selectedSize.value || productData.value.sizes[0] || '',
        Price: productData.value.price,
        Stock: currentStock.value,
        quantity: quantity.value
    }
    addToCart(cartItem)
    addedFeedback.value = true
    quantity.value = 1
    setTimeout(() => { addedFeedback.value = false }, 500)
}

// Helper functions to update refs from composables
const updateColor = (color: string) => {
    currentColor.value = color
}

const updateMaterial = (material: string) => {
    currentMaterial.value = material
}

const updateSize = (size: string) => {
    currentSize.value = size
}

// Initialize on mount
onMounted(() => {
    const productId = route.params.id as string
    if (productId) {
        fetchProductData(productId)
    }
})
</script>

<style scoped src="../styles/InspectView.styles.css"></style>