import type { ProductApiResponse } from '../Types/product.types'

/**
 * Fetch all inventory products from the API
 * @returns Promise with array of products
 * @throws Error if the request fails
 */
export const fetchInventory = async (): Promise<ProductApiResponse[]> => {
    console.log('Fetching products from /api/inventory...')
    
    const response = await fetch('/api/inventory')
    
    console.log('Response status:', response.status)
    console.log('Response ok:', response.ok)
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('Full API response:', data)
    
    // Handle both response formats
    if (Array.isArray(data)) {
        console.log('Data is array, returning directly')
        return data
    } else if (data.inventory && Array.isArray(data.inventory)) {
        console.log('Data has inventory property')
        return data.inventory
    } else {
        console.error('Unexpected data format:', data)
        throw new Error('Unexpected API response format')
    }
}