import type {DesignApiResponse} from '../Types/design.types'

/**
 * Fetch all designs from the API
 * @returns Promise with array of designs
 * @throws Error if the request fails
 */
export const fetchDesigns = async (): Promise<DesignApiResponse[]> => {
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