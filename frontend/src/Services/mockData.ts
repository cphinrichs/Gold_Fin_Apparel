/**
 * Mock data for frontend development
 * This file contains hardcoded test data that simulates API responses
 * 
 * TO REMOVE WHEN API IS CONNECTED:
 * 1. Set USE_MOCK_DATA = false in inventoryApi.ts and designApi.ts
 * 2. Delete this file
 */

import type { ProductApiResponse } from '../Types/product.types'
import type { DesignApiResponse } from '../Types/design.types'

/**
 * Mock inventory data
 * Includes various combinations of styles, colors, materials, and sizes
 */
export const mockInventory: ProductApiResponse[] = [
    // Tank Tops - White/Black in Cotton/Polyester
    { Product_Id: 1, Style: 'Tank Top', Color: 'FFFFFF', Material: 'Cotton', Size: 'S', Stock: 50, Price: 19.99 },
    { Product_Id: 2, Style: 'Tank Top', Color: 'FFFFFF', Material: 'Cotton', Size: 'M', Stock: 75, Price: 19.99 },
    { Product_Id: 3, Style: 'Tank Top', Color: 'FFFFFF', Material: 'Cotton', Size: 'L', Stock: 60, Price: 19.99 },
    { Product_Id: 4, Style: 'Tank Top', Color: 'FFFFFF', Material: 'Cotton', Size: 'XL', Stock: 45, Price: 19.99 },
    { Product_Id: 5, Style: 'Tank Top', Color: '000000', Material: 'Cotton', Size: 'S', Stock: 45, Price: 19.99 },
    { Product_Id: 6, Style: 'Tank Top', Color: '000000', Material: 'Cotton', Size: 'M', Stock: 70, Price: 19.99 },
    { Product_Id: 7, Style: 'Tank Top', Color: '000000', Material: 'Cotton', Size: 'L', Stock: 65, Price: 19.99 },
    
    // Short Sleeves - White/Black/Navy in Cotton/Polyester
    { Product_Id: 8, Style: 'Short Sleeve', Color: 'FFFFFF', Material: 'Cotton', Size: 'S', Stock: 55, Price: 24.99 },
    { Product_Id: 9, Style: 'Short Sleeve', Color: 'FFFFFF', Material: 'Cotton', Size: 'M', Stock: 80, Price: 24.99 },
    { Product_Id: 10, Style: 'Short Sleeve', Color: 'FFFFFF', Material: 'Cotton', Size: 'L', Stock: 70, Price: 24.99 },
    { Product_Id: 11, Style: 'Short Sleeve', Color: 'FFFFFF', Material: 'Cotton', Size: 'XL', Stock: 50, Price: 24.99 },
    { Product_Id: 12, Style: 'Short Sleeve', Color: '000000', Material: 'Polyester', Size: 'S', Stock: 40, Price: 22.99 },
    { Product_Id: 13, Style: 'Short Sleeve', Color: '000000', Material: 'Polyester', Size: 'M', Stock: 60, Price: 22.99 },
    { Product_Id: 14, Style: 'Short Sleeve', Color: '000000', Material: 'Polyester', Size: 'L', Stock: 55, Price: 22.99 },
    
    // Long Sleeves - Navy/Black in Cotton
    { Product_Id: 15, Style: 'Long Sleeve', Color: '1E3A5F', Material: 'Cotton', Size: 'S', Stock: 35, Price: 29.99 },
    { Product_Id: 16, Style: 'Long Sleeve', Color: '1E3A5F', Material: 'Cotton', Size: 'M', Stock: 50, Price: 29.99 },
    { Product_Id: 17, Style: 'Long Sleeve', Color: '1E3A5F', Material: 'Cotton', Size: 'L', Stock: 45, Price: 29.99 },
    { Product_Id: 18, Style: 'Long Sleeve', Color: '1E3A5F', Material: 'Cotton', Size: 'XL', Stock: 30, Price: 29.99 },
    { Product_Id: 19, Style: 'Long Sleeve', Color: '000000', Material: 'Cotton', Size: 'S', Stock: 40, Price: 29.99 },
    { Product_Id: 20, Style: 'Long Sleeve', Color: '000000', Material: 'Cotton', Size: 'M', Stock: 55, Price: 29.99 },
    
    // Kimonos - Various colors in Wool/Cotton
    { Product_Id: 21, Style: 'Kimono', Color: 'DC143C', Material: 'Wool', Size: 'S', Stock: 15, Price: 89.99 },
    { Product_Id: 22, Style: 'Kimono', Color: 'DC143C', Material: 'Wool', Size: 'M', Stock: 20, Price: 89.99 },
    { Product_Id: 23, Style: 'Kimono', Color: 'DC143C', Material: 'Wool', Size: 'L', Stock: 18, Price: 89.99 },
    { Product_Id: 24, Style: 'Kimono', Color: 'DC143C', Material: 'Wool', Size: 'XL', Stock: 12, Price: 89.99 },
    { Product_Id: 25, Style: 'Kimono', Color: 'DC143C', Material: 'Cotton', Size: 'S', Stock: 25, Price: 69.99 },
    { Product_Id: 26, Style: 'Kimono', Color: 'DC143C', Material: 'Cotton', Size: 'M', Stock: 30, Price: 69.99 },
    { Product_Id: 27, Style: 'Kimono', Color: 'DC143C', Material: 'Cotton', Size: 'L', Stock: 28, Price: 69.99 },
    { Product_Id: 28, Style: 'Kimono', Color: 'DC143C', Material: 'Cotton', Size: 'XL', Stock: 20, Price: 69.99 },
    
    { Product_Id: 29, Style: 'Kimono', Color: '000080', Material: 'Wool', Size: 'S', Stock: 18, Price: 89.99 },
    { Product_Id: 30, Style: 'Kimono', Color: '000080', Material: 'Wool', Size: 'M', Stock: 22, Price: 89.99 },
    { Product_Id: 31, Style: 'Kimono', Color: '000080', Material: 'Wool', Size: 'L', Stock: 20, Price: 89.99 },
    { Product_Id: 32, Style: 'Kimono', Color: '000080', Material: 'Wool', Size: 'XL', Stock: 15, Price: 89.99 },
    { Product_Id: 33, Style: 'Kimono', Color: '000080', Material: 'Cotton', Size: 'S', Stock: 28, Price: 69.99 },
    { Product_Id: 34, Style: 'Kimono', Color: '000080', Material: 'Cotton', Size: 'M', Stock: 35, Price: 69.99 },
    { Product_Id: 35, Style: 'Kimono', Color: '000080', Material: 'Cotton', Size: 'L', Stock: 32, Price: 69.99 },
    { Product_Id: 36, Style: 'Kimono', Color: '000080', Material: 'Cotton', Size: 'XL', Stock: 25, Price: 69.99 },
    
    { Product_Id: 37, Style: 'Kimono', Color: 'FFD700', Material: 'Wool', Size: 'S', Stock: 12, Price: 89.99 },
    { Product_Id: 38, Style: 'Kimono', Color: 'FFD700', Material: 'Wool', Size: 'M', Stock: 16, Price: 89.99 },
    { Product_Id: 39, Style: 'Kimono', Color: 'FFD700', Material: 'Wool', Size: 'L', Stock: 14, Price: 89.99 },
    { Product_Id: 40, Style: 'Kimono', Color: 'FFD700', Material: 'Wool', Size: 'XL', Stock: 10, Price: 89.99 },
    
    // Vests - Multiple colors in Leather/Blend/Cotton
    { Product_Id: 41, Style: 'Vest', Color: '8B4513', Material: 'Leather', Size: 'S', Stock: 20, Price: 79.99 },
    { Product_Id: 42, Style: 'Vest', Color: '8B4513', Material: 'Leather', Size: 'M', Stock: 25, Price: 79.99 },
    { Product_Id: 43, Style: 'Vest', Color: '8B4513', Material: 'Leather', Size: 'L', Stock: 22, Price: 79.99 },
    { Product_Id: 44, Style: 'Vest', Color: '8B4513', Material: 'Leather', Size: 'XL', Stock: 18, Price: 79.99 },
    { Product_Id: 45, Style: 'Vest', Color: '8B4513', Material: 'Leather', Size: 'XXL', Stock: 15, Price: 79.99 },
    
    { Product_Id: 46, Style: 'Vest', Color: '000000', Material: 'Leather', Size: 'S', Stock: 22, Price: 79.99 },
    { Product_Id: 47, Style: 'Vest', Color: '000000', Material: 'Leather', Size: 'M', Stock: 28, Price: 79.99 },
    { Product_Id: 48, Style: 'Vest', Color: '000000', Material: 'Leather', Size: 'L', Stock: 25, Price: 79.99 },
    { Product_Id: 49, Style: 'Vest', Color: '000000', Material: 'Leather', Size: 'XL', Stock: 20, Price: 79.99 },
    { Product_Id: 50, Style: 'Vest', Color: '000000', Material: 'Leather', Size: 'XXL', Stock: 16, Price: 79.99 },
    
    { Product_Id: 51, Style: 'Vest', Color: '4169E1', Material: 'Blend', Size: 'S', Stock: 30, Price: 49.99 },
    { Product_Id: 52, Style: 'Vest', Color: '4169E1', Material: 'Blend', Size: 'M', Stock: 40, Price: 49.99 },
    { Product_Id: 53, Style: 'Vest', Color: '4169E1', Material: 'Blend', Size: 'L', Stock: 35, Price: 49.99 },
    { Product_Id: 54, Style: 'Vest', Color: '4169E1', Material: 'Blend', Size: 'XL', Stock: 28, Price: 49.99 },
    { Product_Id: 55, Style: 'Vest', Color: '4169E1', Material: 'Blend', Size: 'XXL', Stock: 22, Price: 49.99 },
    
    { Product_Id: 56, Style: 'Vest', Color: '696969', Material: 'Cotton', Size: 'S', Stock: 35, Price: 39.99 },
    { Product_Id: 57, Style: 'Vest', Color: '696969', Material: 'Cotton', Size: 'M', Stock: 45, Price: 39.99 },
    { Product_Id: 58, Style: 'Vest', Color: '696969', Material: 'Cotton', Size: 'L', Stock: 40, Price: 39.99 },
    { Product_Id: 59, Style: 'Vest', Color: '696969', Material: 'Cotton', Size: 'XL', Stock: 32, Price: 39.99 },
    { Product_Id: 60, Style: 'Vest', Color: '696969', Material: 'Cotton', Size: 'XXL', Stock: 25, Price: 39.99 },
    
    // Hoodies - Popular colors in Cotton/Wool
    { Product_Id: 61, Style: 'Hoodie', Color: '808080', Material: 'Cotton', Size: 'S', Stock: 40, Price: 44.99 },
    { Product_Id: 62, Style: 'Hoodie', Color: '808080', Material: 'Cotton', Size: 'M', Stock: 55, Price: 44.99 },
    { Product_Id: 63, Style: 'Hoodie', Color: '808080', Material: 'Cotton', Size: 'L', Stock: 50, Price: 44.99 },
    { Product_Id: 64, Style: 'Hoodie', Color: '808080', Material: 'Cotton', Size: 'XL', Stock: 38, Price: 44.99 },
    { Product_Id: 65, Style: 'Hoodie', Color: '808080', Material: 'Cotton', Size: 'XXL', Stock: 30, Price: 44.99 },
    
    { Product_Id: 66, Style: 'Hoodie', Color: '000000', Material: 'Wool', Size: 'S', Stock: 45, Price: 49.99 },
    { Product_Id: 67, Style: 'Hoodie', Color: '000000', Material: 'Wool', Size: 'M', Stock: 60, Price: 49.99 },
    { Product_Id: 68, Style: 'Hoodie', Color: '000000', Material: 'Wool', Size: 'L', Stock: 55, Price: 49.99 },
    { Product_Id: 69, Style: 'Hoodie', Color: '000000', Material: 'Wool', Size: 'XL', Stock: 42, Price: 49.99 },
    { Product_Id: 70, Style: 'Hoodie', Color: '000000', Material: 'Wool', Size: 'XXL', Stock: 35, Price: 49.99 },
    
    { Product_Id: 71, Style: 'Hoodie', Color: '00008B', Material: 'Cotton', Size: 'S', Stock: 35, Price: 44.99 },
    { Product_Id: 72, Style: 'Hoodie', Color: '00008B', Material: 'Cotton', Size: 'M', Stock: 48, Price: 44.99 },
    { Product_Id: 73, Style: 'Hoodie', Color: '00008B', Material: 'Cotton', Size: 'L', Stock: 44, Price: 44.99 },
    { Product_Id: 74, Style: 'Hoodie', Color: '00008B', Material: 'Cotton', Size: 'XL', Stock: 33, Price: 44.99 },
    { Product_Id: 75, Style: 'Hoodie', Color: '00008B', Material: 'Cotton', Size: 'XXL', Stock: 28, Price: 44.99 },
    
    { Product_Id: 76, Style: 'Hoodie', Color: '8B0000', Material: 'Wool', Size: 'S', Stock: 25, Price: 49.99 },
    { Product_Id: 77, Style: 'Hoodie', Color: '8B0000', Material: 'Wool', Size: 'M', Stock: 38, Price: 49.99 },
    { Product_Id: 78, Style: 'Hoodie', Color: '8B0000', Material: 'Wool', Size: 'L', Stock: 35, Price: 49.99 },
    { Product_Id: 79, Style: 'Hoodie', Color: '8B0000', Material: 'Wool', Size: 'XL', Stock: 28, Price: 49.99 },
    { Product_Id: 80, Style: 'Hoodie', Color: '8B0000', Material: 'Wool', Size: 'XXL', Stock: 22, Price: 49.99 },
]

/**
 * Mock designs data
 * Includes various design patterns that can be applied to products
 */
export const mockDesigns: DesignApiResponse[] = [
    { id: 1, name: 'Dragon Pattern', price: 12.00 },
    { id: 2, name: 'Cherry Blossom', price: 10.00 },
    { id: 3, name: 'Phoenix Rising', price: 15.00 },
    { id: 4, name: 'Geometric Waves', price: 8.00 },
    { id: 5, name: 'Mountain Landscape', price: 11.00 },
    { id: 6, name: 'Koi Fish', price: 13.00 },
    { id: 7, name: 'Abstract Art', price: 9.00 },
    { id: 8, name: 'Tribal Pattern', price: 10.00 },
    { id: 9, name: 'Floral Garden', price: 11.00 },
    { id: 10, name: 'Urban Skyline', price: 12.00 },
    { id: 11, name: 'Ocean Waves', price: 10.00 },
    { id: 12, name: 'Forest Trail', price: 11.00 },
    { id: 13, name: 'Midnight Stars', price: 9.00 },
    { id: 14, name: 'Sunset Gradient', price: 8.00 },
    { id: 15, name: 'Lightning Strike', price: 14.00 },
    { id: 16, name: 'Bamboo Forest', price: 10.00 },
    { id: 17, name: 'Tiger Stripes', price: 13.00 },
    { id: 18, name: 'Peacock Feathers', price: 15.00 },
    { id: 19, name: 'Vintage Logo', price: 7.00 },
    { id: 20, name: 'Minimalist Lines', price: 6.00 },
]

/**
 * Helper function to simulate API delay
 * Makes the mock data feel more like a real API call
 */
export const simulateApiDelay = (ms: number = 500): Promise<void> => {
    return new Promise(resolve => setTimeout(resolve, ms))
}
