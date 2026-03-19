import type { Router } from 'vue-router'

/**
 * Navigate to product detail page
 * @param router - Vue Router instance
 * @param productId - ID of the product to view
 */
export const navigateToProductDetail = (router: Router, productId: number): void => {
    console.log('Navigating to product:', productId)
    router.push({ 
        name: 'Inspect', 
        params: { id: productId.toString() } 
    })
}