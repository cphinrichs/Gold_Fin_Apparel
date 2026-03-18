import type { ProductApiResponse } from '../Types/product.types'

/**
 * Extract unique values from array of products
 * @param products - Array of product objects
 * @param key - Property key to extract
 * @returns Array of unique values
 */
export const extractUniqueValues = (
    products: ProductApiResponse[], 
    key: keyof ProductApiResponse
): string[] => {
    return Array.from(new Set(products.map(p => {
        const value = p[key]
        // Handle color hex formatting
        if (key === 'Color') {
            return `#${value}`
        }
        // Trim size values
        if (key === 'Size') {
            return String(value).trim()
        }
        return String(value)
    })))
}

/**
 * Parse inventory data from API response
 * Handles both array and object with inventory property formats
 * @param responseData - Raw API response
 * @returns Array of products
 */
export const parseInventoryResponse = (responseData: any): ProductApiResponse[] => {
    if (Array.isArray(responseData)) {
        return responseData
    } else if (responseData.inventory && Array.isArray(responseData.inventory)) {
        return responseData.inventory
    } else {
        throw new Error('Unexpected API response format')
    }
}

/**
 * Find a product by ID in inventory
 * @param inventory - Array of all products
 * @param productId - Product ID to find
 * @returns Product object or undefined
 */
export const findProductById = (
    inventory: ProductApiResponse[], 
    productId: string
): ProductApiResponse | undefined => {
    return inventory.find(product => product.Product_Id === parseInt(productId))
}

/**
 * Find all products matching a specific style
 * @param inventory - Array of all products
 * @param style - Style to match
 * @returns Array of matching products
 */
export const findProductsByStyle = (
    inventory: ProductApiResponse[], 
    style: string
): ProductApiResponse[] => {
    return inventory.filter(product => product.Style === style)
}

/**
 * Toggle active class on button elements
 * @param selector - CSS selector for buttons to toggle
 * @param targetElement - Element to set as active
 */
export const toggleActiveButton = (selector: string, targetElement: HTMLElement): void => {
    const buttons = document.querySelectorAll(selector)
    buttons.forEach(btn => btn.classList.remove('active'))
    targetElement.classList.add('active')
}