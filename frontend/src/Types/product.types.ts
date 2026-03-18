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