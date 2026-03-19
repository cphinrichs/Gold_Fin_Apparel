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
    const currentProductId = ref(0)
    const currentStock = ref(0)
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

    const formattedPrice = computed(() => {
        return productData.value.price.toFixed(2)
    })

    // Methods
    const updateProductData = (
        currentProduct: ProductApiResponse, 
        relatedProducts: ProductApiResponse[]
    ) => {
        productData.value = {
            ...productData.value,
            name: `${currentProduct.Style} - ${currentProduct.Material}`,
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
            
            const inventory = parseInventoryResponse(responseData)
            console.log('Parsed inventory length:', inventory.length)
            
            const currentProduct = findProductById(inventory, productId)
            
            if (!currentProduct) {
                throw new Error(`Product with ID ${productId} not found`)
            }
            
            console.log('Found product:', currentProduct)
            
            const relatedProducts = findProductsByStyle(inventory, currentProduct.Style)
            console.log('Related products found:', relatedProducts.length)
            
            updateProductData(currentProduct, relatedProducts)
            
            currentColor.value = `#${currentProduct.Color}`
            currentMaterial.value = currentProduct.Material
            currentProductId.value = currentProduct.Product_Id
            currentStock.value = currentProduct.Stock
            
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
        currentProductId,
        currentStock,
        isLoading,
        error,
        // Computed
        productImages,
        materialBackgroundImage,
        styleOverlayImage,
        renderStars,
        formattedPrice,
        // Methods
        fetchProductData
    }
}