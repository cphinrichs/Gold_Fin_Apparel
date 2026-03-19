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

export interface CartItem {
    cartItemId: string      // unique ID for this cart entry
    Product_Id: number
    Style: string
    Color: string           // hex with #
    Material: string
    Size: string
    Price: number
    Stock: number
    quantity: number
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