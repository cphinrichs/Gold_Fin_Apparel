import { ref, computed } from 'vue'
import type { ProductData, ProductApiResponse } from '../Types/product.types'
import { 
    STYLE_TO_IMAGES, 
    MATERIAL_TO_TEXTURE, 
    STYLE_TO_OVERLAY,
    DEFAULT_PRODUCT_DATA 
} from '../Constants/productMappings'
import { 
    parseInventoryResponse,
    findProductById,
    findProductsByStyle,
    extractUniqueValues
} from '../Utils/productHelpers'

/**
 * Composable for managing product data and API interactions
 */
export const useProductData = () => {
    // State
    const productData = ref<ProductData>({ ...DEFAULT_PRODUCT_DATA })
    const currentColor = ref('')
    const currentMaterial = ref('')
    const currentSize = ref('')
    const inventory = ref<ProductApiResponse[]>([])
    const isLoading = ref(false)
    const error = ref<string | null>(null)

    // Computed properties
    const productImages = computed(() => {
        return STYLE_TO_IMAGES[productData.value.style] || []
    })

    const materialBackgroundImage = computed(() => {
        const texture = MATERIAL_TO_TEXTURE[currentMaterial.value]
        return texture ? `url(${texture})` : 'none'
    })

    const styleOverlayImage = computed(() => {
        const overlay = STYLE_TO_OVERLAY[productData.value.style]
        return overlay ? `url(${overlay})` : 'none'
    })

    const renderStars = computed(() => {
        const filledStars = '★'.repeat(productData.value.rating)
        const emptyStars = '☆'.repeat(5 - productData.value.rating)
        return filledStars + emptyStars
    })

    /**
     * Check if a material is available for the current color
     */
    const isMaterialAvailable = (material: string): boolean => {
        if (!currentColor.value) return true

        const colorCode = currentColor.value.replace('#', '')
        return inventory.value.some(product =>
            product.Style === productData.value.style &&
            product.Color === colorCode &&
            product.Material === material
        )
    }

    /**
     * Check if a color is available for the current material
     */
    const isColorAvailable = (color: string): boolean => {
        if (!currentMaterial.value) return true

        const colorCode = color.replace('#', '')
        return inventory.value.some(product =>
            product.Style === productData.value.style &&
            product.Color === colorCode &&
            product.Material === currentMaterial.value
        )
    }

    /**
     * Check if a size is available for the current color and material
     */
    const isSizeAvailable = (size: string): boolean => {
        if (!currentColor.value || !currentMaterial.value) return true

        const colorCode = currentColor.value.replace('#', '')
        return inventory.value.some(product =>
            product.Style === productData.value.style &&
            product.Color === colorCode &&
            product.Material === currentMaterial.value &&
            product.Size.trim() === size.trim()
        )
    }

    /**
     * Get first available color for current material and optionally size
     */
    const getFirstAvailableColor = (material?: string, size?: string): string => {
        const mat = material || currentMaterial.value
        if (!mat) return ''

        const availableProduct = inventory.value.find(product => {
            const matchesMaterial = product.Style === productData.value.style && product.Material === mat
            if (!size) return matchesMaterial
            return matchesMaterial && product.Size.trim() === size.trim()
        })

        return availableProduct ? `#${availableProduct.Color}` : ''
    }

    /**
     * Get first available material for current color and optionally size
     */
    const getFirstAvailableMaterial = (color?: string, size?: string): string => {
        const col = color || currentColor.value
        if (!col) return ''

        const colorCode = col.replace('#', '')
        const availableProduct = inventory.value.find(product => {
            const matchesColor = product.Style === productData.value.style && product.Color === colorCode
            if (!size) return matchesColor
            return matchesColor && product.Size.trim() === size.trim()
        })

        return availableProduct ? availableProduct.Material : ''
    }

    /**
     * Get first available size for current color and material
     */
    const getFirstAvailableSize = (color?: string, material?: string): string => {
        const col = color || currentColor.value
        const mat = material || currentMaterial.value
        
        if (!col || !mat) return ''

        const colorCode = col.replace('#', '')
        const availableProduct = inventory.value.find(product =>
            product.Style === productData.value.style &&
            product.Color === colorCode &&
            product.Material === mat
        )

        return availableProduct ? availableProduct.Size.trim() : ''
    }

    /**
     * Clear selections when color changes
     */
    const clearIncompatibleForColor = () => {
        // Check if current material is available for new color
        if (currentMaterial.value && !isMaterialAvailable(currentMaterial.value)) {
            const firstMaterial = getFirstAvailableMaterial(currentColor.value)
            currentMaterial.value = firstMaterial
        }

        // Check if current size is available for new color+material combination
        if (currentSize.value && !isSizeAvailable(currentSize.value)) {
            const firstSize = getFirstAvailableSize(currentColor.value, currentMaterial.value)
            currentSize.value = firstSize
        }
    }

    /**
     * Clear selections when material changes
     */
    const clearIncompatibleForMaterial = () => {
        // Check if current color is available for new material
        if (currentColor.value && !isColorAvailable(currentColor.value)) {
            const firstColor = getFirstAvailableColor(currentMaterial.value)
            currentColor.value = firstColor
        }

        // Check if current size is available for new material+color combination
        if (currentSize.value && !isSizeAvailable(currentSize.value)) {
            const firstSize = getFirstAvailableSize(currentColor.value, currentMaterial.value)
            currentSize.value = firstSize
        }
    }

    /**
     * Clear selections when size changes
     */
    const clearIncompatibleForSize = () => {
        const tempColor = currentColor.value
        const tempMaterial = currentMaterial.value

        // Check if current color is available for new size+material
        if (currentColor.value && currentMaterial.value) {
            const colorCode = currentColor.value.replace('#', '')
            const colorAvailable = inventory.value.some(product =>
                product.Style === productData.value.style &&
                product.Color === colorCode &&
                product.Material === currentMaterial.value &&
                product.Size.trim() === currentSize.value.trim()
            )

            if (!colorAvailable) {
                const firstColor = getFirstAvailableColor(currentMaterial.value, currentSize.value)
                currentColor.value = firstColor
            }
        }

        // Check if current material is available for new size+color
        if (currentMaterial.value && currentColor.value) {
            const colorCode = currentColor.value.replace('#', '')
            const materialAvailable = inventory.value.some(product =>
                product.Style === productData.value.style &&
                product.Color === colorCode &&
                product.Material === currentMaterial.value &&
                product.Size.trim() === currentSize.value.trim()
            )

            if (!materialAvailable) {
                const firstMaterial = getFirstAvailableMaterial(currentColor.value, currentSize.value)
                currentMaterial.value = firstMaterial
            }
        }
    }

    const formattedPrice = computed(() => {
        // Find the product that matches current selections
        if (currentColor.value && currentMaterial.value && currentSize.value) {
            const colorCode = currentColor.value.replace('#', '')
            const matchingProduct = inventory.value.find(product => 
                product.Style === productData.value.style &&
                product.Color === colorCode &&
                product.Material === currentMaterial.value &&
                product.Size.trim() === currentSize.value.trim()
            )
            
            if (matchingProduct) {
                return matchingProduct.Price.toFixed(2)
            }
        }
        return productData.value.price.toFixed(2)
    })

    // Methods
    const updateProductData = (
        currentProduct: ProductApiResponse, 
        relatedProducts: ProductApiResponse[]
    ) => {
        productData.value = {
            ...productData.value,
            name: `${currentProduct.Style}`,
            style: currentProduct.Style,
            price: currentProduct.Price,
            materials: extractUniqueValues(relatedProducts, 'Material'),
            colors: extractUniqueValues(relatedProducts, 'Color'),
            sizes: extractUniqueValues(relatedProducts, 'Size'),
            description: `${currentProduct.Style} made from ${currentProduct.Material}. Available in stock: ${currentProduct.Stock} units.`,
            features: [
                'High-quality construction',
                'Multiple color and material options',
                'Available in various sizes'
            ]
        }
    }

    const fetchProductData = async (productId: string) => {
        isLoading.value = true
        error.value = null

        try {
            console.log('Fetching product with ID:', productId)
            const response = await fetch('/api/inventory')
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`)
            }
            
            const responseData = await response.json()
            console.log('Full inventory response:', responseData)
            
            inventory.value = parseInventoryResponse(responseData)
            console.log('Parsed inventory length:', inventory.value.length)
            
            const currentProduct = findProductById(inventory.value, productId)
            
            if (!currentProduct) {
                throw new Error(`Product with ID ${productId} not found`)
            }
            
            console.log('Found product:', currentProduct)
            
            const relatedProducts = findProductsByStyle(inventory.value, currentProduct.Style)
            console.log('Related products found:', relatedProducts.length)
            
            updateProductData(currentProduct, relatedProducts)
            
            currentColor.value = `#${currentProduct.Color}`
            currentMaterial.value = currentProduct.Material
            currentSize.value = currentProduct.Size.trim()
            
        } catch (err) {
            console.error('Error fetching product:', err)
            error.value = err instanceof Error ? err.message : 'Failed to load product'
            productData.value.name = 'Error loading product'
            productData.value.description = 'Failed to load product details'
        } finally {
            isLoading.value = false
        }
    }

    return {
        // State
        productData,
        currentColor,
        currentMaterial,
        currentSize,
        isLoading,
        error,
        // Computed
        productImages,
        materialBackgroundImage,
        styleOverlayImage,
        renderStars,
        formattedPrice,
        // Methods
        fetchProductData,
        isMaterialAvailable,
        isColorAvailable,
        isSizeAvailable,
        clearIncompatibleForColor,
        clearIncompatibleForMaterial,
        clearIncompatibleForSize
    }
}