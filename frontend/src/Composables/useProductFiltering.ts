import { computed, watch } from 'vue'
import type { Ref } from 'vue'
import type { RouteLocationNormalizedLoaded } from 'vue-router'
import type { ProductApiResponse } from '../Types/product.types'

/**
 * Composable for filtering products based on route query parameters
 * @param products - Ref containing all products
 * @param route - Vue Router route object
 */
export const useProductFiltering = (
    products: Ref<ProductApiResponse[]>,
    route: RouteLocationNormalizedLoaded
) => {
    /**
     * Filter products by style from route query
     */
    const filteredProducts = computed(() => {
        const styleFilter = route.query.style as string
        
        if (!styleFilter) {
            return products.value
        }
        
        console.log('Filtering by style:', styleFilter)
        const filtered = products.value.filter(product => product.Style === styleFilter)
        console.log('Filtered products:', filtered)
        
        return filtered
    })

    /**
     * Watch for route query changes
     */
    const watchRouteChanges = () => {
        watch(() => route.query.style, (newStyle) => {
            console.log('Route query changed to:', newStyle)
        })
    }

    return {
        filteredProducts,
        watchRouteChanges
    }
}