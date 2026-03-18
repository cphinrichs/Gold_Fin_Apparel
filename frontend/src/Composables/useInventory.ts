import { ref } from 'vue'
import type { Ref } from 'vue'
import { fetchInventory } from '../Services/inventoryApi'
import type { ProductApiResponse } from '../Types/product.types'

/**
 * Composable for managing inventory data and loading state
 */
export const useInventory = () => {
    // State
    const products: Ref<ProductApiResponse[]> = ref([])
    const loading = ref(false)
    const error: Ref<string | null> = ref(null)

    /**
     * Fetch all products from the API
     */
    const loadProducts = async () => {
        try {
            loading.value = true
            error.value = null

            const data = await fetchInventory()
            
            products.value = data
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

    return {
        products,
        loading,
        error,
        loadProducts
    }
}