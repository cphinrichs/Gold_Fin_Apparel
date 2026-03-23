import type { ProductApiResponse } from '../Types/product.types'
import { mockInventory, simulateApiDelay } from './mockData'

/**
 * ⚠️ MOCK DATA TOGGLE ⚠️
 * Set to 'true' to use mock data for development
 * Set to 'false' to connect to the real API
 * 
 * TO CONNECT TO REAL API:
 * 1. Change USE_MOCK_DATA to false
 * 2. Ensure your backend API is running
 * 3. Delete mockData.ts if no longer needed
 */
const USE_MOCK_DATA = false

/**
 * Fetch all inventory products from the API (or mock data)
 * @returns Promise with array of products
 * @throws Error if the request fails
 */
export const fetchInventory = async (): Promise<ProductApiResponse[]> => {
    // Return mock data if flag is enabled
    if (USE_MOCK_DATA) {
        console.log('🔧 Using MOCK inventory data (USE_MOCK_DATA = true)')
        await simulateApiDelay(300) // Simulate network delay
        return mockInventory
    }

    // Real API call
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