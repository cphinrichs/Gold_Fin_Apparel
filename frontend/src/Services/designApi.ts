import type {DesignApiResponse} from '../Types/design.types'
import { mockDesigns, simulateApiDelay } from './mockData'

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
 * Fetch all designs from the API (or mock data)
 * @returns Promise with array of designs
 * @throws Error if the request fails
 */
export const fetchDesigns = async (): Promise<DesignApiResponse[]> => {
    // Return mock data if flag is enabled
    if (USE_MOCK_DATA) {
        console.log('🔧 Using MOCK designs data (USE_MOCK_DATA = true)')
        await simulateApiDelay(300) // Simulate network delay
        return mockDesigns
    }

    // Real API call
    console.log('Fetching designs from /api/designs...')
    
    const response = await fetch('/api/designs')

    console.log('Response status:', response.status)
    console.log('Response ok:', response.ok)

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    console.log('Full API response:', data)

    // Handle both response formats
    let designs: DesignApiResponse[] = []
    
    if (Array.isArray(data)) {
        console.log('Data is array, returning directly')
        designs = data
    } else if (data.designs && Array.isArray(data.designs)) {
        console.log('Data has designs property')
        designs = data.designs
    } else {
        console.error('Unexpected data format:', data)
        throw new Error('Unexpected API response format')
    }

    // Debug: Log the first design to see its structure
    if (designs.length > 0) {
        console.log('First design:', designs[0])
        console.log('Design keys:', Object.keys(designs[0]))
    }

    return designs
}