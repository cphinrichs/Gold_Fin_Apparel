import type { DesignApiResponse } from './design.types'

export interface ProductApiResponse {
    Product_Id: number
    Style: string
    Color: string
    Material: string
    Size: string
    Stock: number
    Price: number
}

export interface ProductData {
    name: string
    style: string
    rating: number
    reviewCount: number
    description: string
    materials: string[]
    features: string[]
    price: number
    colors: string[]
    sizes: string[]
}

/**
 * Represents a combination of an inventory item and a design
 */
export interface ProductCombination {
    inventory: ProductApiResponse
    design: DesignApiResponse
}