import type { ProductApiResponse, ProductCombination } from '../Types/product.types'
import type { DesignApiResponse } from '../Types/design.types'

/**
 * Create all possible combinations of inventory items and designs
 * @param inventory - Array of inventory items
 * @param designs - Array of designs
 * @param styleFilter - Optional style filter to limit combinations
 * @returns Array of product combinations
 */
export const createProductCombinations = (
    inventory: ProductApiResponse[],
    designs: DesignApiResponse[],
    styleFilter?: string
): ProductCombination[] => {
    const combinations: ProductCombination[] = []
    
    // Filter inventory by style if specified
    const filteredInventory = styleFilter 
        ? inventory.filter(item => item.Style.toLowerCase() === styleFilter.toLowerCase())
        : inventory
    
    console.log('Creating combinations for:', {
        inventoryCount: filteredInventory.length,
        designsCount: designs.length,
        styleFilter
    })
    
    // Create cartesian product of inventory x designs
    for (const inventoryItem of filteredInventory) {
        for (const design of designs) {
            combinations.push({
                inventory: inventoryItem,
                design: design
            })
        }
    }
    
    console.log(`Created ${combinations.length} combinations`)
    return combinations
}

/**
 * Group combinations by style
 * @param combinations - Array of product combinations
 * @returns Map of style names to their combinations
 */
export const groupCombinationsByStyle = (
    combinations: ProductCombination[]
): Map<string, ProductCombination[]> => {
    const grouped = new Map<string, ProductCombination[]>()
    
    for (const combo of combinations) {
        const style = combo.inventory.Style
        if (!grouped.has(style)) {
            grouped.set(style, [])
        }
        grouped.get(style)!.push(combo)
    }
    
    return grouped
}

/**
 * Get unique styles from combinations
 * @param combinations - Array of product combinations
 * @returns Array of unique style names
 */
export const getUniqueStyles = (combinations: ProductCombination[]): string[] => {
    const styles = new Set<string>()
    for (const combo of combinations) {
        styles.add(combo.inventory.Style)
    }
    return Array.from(styles)
}