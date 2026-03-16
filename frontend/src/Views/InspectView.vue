<template>
    <div class="inspect-container">
        <section class="image-gallery">
            <div class="thumbnail-list">
                <button 
                    v-for="(image, index) in productImages" 
                    :key="index"
                    :class="['thumbnail-item', { active: selectedImage === index }]"
                    :style="{ backgroundColor: selectedColor}"
                    @click="selectedImage = index">
                    <img :src="image" :alt="`Product thumbnail`">
                </button>
            </div>
            <div class="main-image" :style="{ backgroundColor: selectedColor, backgroundImage: materialBackgroundImage }">
                <img :src="productImages[selectedImage]" :alt="`Product Image`">
            </div>
        </section>
        
        <aside class="product-details">
            <h2 class ="product-style">{{ productData.style }}</h2>
            <h1 class="product-title">{{ productData.name }}</h1>
            <div class="product-rating">
                <span class="stars">{{ '★'.repeat(productData.rating) + '☆'.repeat(5 - productData.rating) }}</span>
                <span class="review-count">{{ productData.reviewCount }} reviews</span>
            </div>
            
            <p class="product-description">
                {{ productData.description }}
            </p>
            
            <ul class="product-features">
                <li v-for="(feature, index) in productData.features" 
                :key="index">{{ feature }}
                </li>
            </ul>
            
            <div class="product-options">
                <div class="color-selector">
                    <label>Color</label>
                    <div class="color-options">
                        <button class ="color-btn" v-for="(color, index) in productData.colors" 
                        :key="index" 
                        :style="{ background: color }" 
                        @click="activeColor($event, color)">
                        </button>
                    </div>
                </div>

                <div class="material-selector">
                    <label>Material</label>
                        <div class="material-options">
                            <button class ="material-btn" 
                                v-for="(material, index) in productData.materials" 
                                :key="index" 
                                @click="activeMaterial($event, material)">{{ material }}
                            </button>
                        </div>
                    </div>
                
                <div class="size-selector">
                    <label>Size</label>
                        <div class="size-options">
                            <button class ="size-btn" 
                                v-for="(size, index) in productData.sizes" 
                                :key="index" @click="activeSize">{{ size }}
                            </button>
                        </div>
                    <router-link :to="{ name: 'SizeCharts' }" class="size-guide">Size Guide</router-link>
                </div>
            </div>
            
            <div class="price-section">
                <span class="price">${{ productData.price.toFixed(2) }}</span>
            </div>
            
            <button class="add-to-cart">ADD TO CART</button>
            
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
import { ref, computed } from 'vue'
import productKimFront from '../Assets/Kimono/Designer(5).png'
import productKimLeft from '../Assets/Kimono/Designer(6).png'
import productKimBack from '../Assets/Kimono/Designer(7).png'
import productKimRight from '../Assets/Kimono/Designer(8).png'
import productKimDetail from '../Assets/Kimono/Designer(9).png'
import materialCotton from '../Assets/Textures/material-cotton.png'
import materialPolyester from '../Assets/Textures/material-polyester.png'
import materialLeather from '../Assets/Textures/material-leather.png'
import materialWool from '../Assets/Textures/material-wool.png'
import materialBlend from '../Assets/Textures/material-blend.png'
import materialKevlar from '../Assets/Textures/material-kevlar.png'

const selectedImage = ref(0)
const selectedColor = ref('#f5f5f5')
const selectedMaterial = ref('')

const materialTextures: Record<string, string> = {
    'Wool': materialWool,
    'Leather': materialLeather,
    'Blend': materialBlend,
    'Cotton': materialCotton,
    'Polyester': materialPolyester,
    'Kevlar': materialKevlar
}

const materialBackgroundImage = computed(() => {
    if (selectedMaterial.value && materialTextures[selectedMaterial.value]) {
        return `url(${materialTextures[selectedMaterial.value]})`
    }
    return 'none'
})

const activeColor = (event: Event, color: string) => {
    const buttons = document.querySelectorAll('.color-btn')
    buttons.forEach(btn => btn.classList.remove('active'))
    const target = event.currentTarget as HTMLElement
    target?.classList.add('active')
    selectedColor.value = color
}

const activeSize = (event: Event) => {
    const buttons = document.querySelectorAll('.size-btn')
    buttons.forEach(btn => btn.classList.remove('active'))
    const target = event.currentTarget as HTMLElement
    target?.classList.add('active')
}

const activeMaterial = (event: Event, material: string) => {
    const buttons = document.querySelectorAll('.material-btn')
    buttons.forEach(btn => btn.classList.remove('active'))
    const target = event.currentTarget as HTMLElement
    target?.classList.add('active')
    selectedMaterial.value = material
}

const productImages = [
    productKimFront,
    productKimLeft,
    productKimBack,
    productKimRight,
    productKimDetail
]

// Mock product data - replace with API call later
const productData = ref({
    name: 'Kyoto Signature',
    style: 'Kimono',
    rating: 5,
    reviewCount: 200,
    description: 'Test',
    materials: ['Cotton', 'Polyester', 'Wool', 'Blend', 'Leather', 'Kevlar'],
    features: [
        'Screen Print with Sleeve Graphics',
        '100% Cotton, Pre-Shrunk Jersey',
        'Ribbed Collar with Double Needle Stitching',
    ],
    price: 37.00,
    colors: ['#FFFFFF', '#000000', '#FF0000', '#0000FF', '#008000'],
    sizes: ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL']
})

// TODO: Replace with actual API call
// const fetchProductData = async (productId: string) => {
//     const response = await fetch(`/api/products/${productId}`)
//     productData.value = await response.json()
// }
</script>

<style scoped>
.inspect-container {
    display: flex;
    gap: 3rem;
    padding: 2rem;
    max-width: 1400px;
}

.image-gallery {
    display: flex;
    gap: 1rem;
    align-items: stretch;
}

.thumbnail-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    flex: 0 0 80px;
}

.thumbnail-item {
    width: 80px;
    flex: 1;
    border: 2px solid transparent;
    cursor: pointer;
    padding: 0;
}

.thumbnail-item:hover,
.thumbnail-item.active {
    border-color: #333;
}

.thumbnail-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.main-image {
    flex: 1;
    background: #f5f5f5;
    display: flex;
    align-items: center;
    justify-content: center;
}

.main-image img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}

.product-details {
    flex: 0 0 450px;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}
.product-style {
    font-size: 1.2rem;
    color: #666;
    text-transform: uppercase;
    margin: 0;
}

.product-title {
    font-size: 2rem;
    font-weight: 700;
    margin: 0;
}

.product-rating {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.stars {
    color: #FFD700;
}

.review-count {
    color: #666;
    font-size: 0.9rem;
}

.product-description {
    font-size: 1.1rem;
    line-height: 1.6;
    margin: 0;
}

.product-features {
    list-style: none;
    padding: 0;
    margin: 0;
}

.product-features li {
    padding: 0.5rem 0;
    border-bottom: 1px solid #eee;
}

.product-options label {
    display: block;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.material-options,
.color-options,
.size-options {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.material-btn,
.color-btn,
.size-btn {
    padding: 0.75rem 1.25rem;
    border: 2px solid #ddd;
    background: white;
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 500;
}

.material-btn.active,
.color-btn.active,
.size-btn.active {
    border-color: #333;
    background: #f0f0f0;
}

.size-guide {
    display: inline-block;
    margin-top: 0.5rem;
    color: #666;
    text-decoration: underline;
}

.price-section {
    font-size: 1.5rem;
    font-weight: 700;
}

.add-to-cart {
    width: 100%;
    padding: 1rem;
    background: #333;
    color: white;
    border: none;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
}

.add-to-cart:hover {
    background: #000;
}

.shipping-returns summary {
    cursor: pointer;
    font-weight: 600;
    padding: 1rem;
    background: #f5f5f5;
    border: 1px solid #ddd;
    user-select: none;
}

.details-content {
    padding: 1rem;
    border: 1px solid #ddd;
    border-top: none;
}

@media (max-width: 768px) {
    .inspect-container {
        flex-direction: column;
    }
    
    .image-gallery {
        flex-direction: column-reverse;
    }
    
    .thumbnail-list {
        flex-direction: row;
        overflow-x: auto;
    }
    
    .product-details {
        flex: 1;
    }
}
</style>