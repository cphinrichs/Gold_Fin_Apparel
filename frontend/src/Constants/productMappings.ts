// Kimono product images
import productKimFront from '../Assets/Kimono/Designer(5).png'
import productKimLeft from '../Assets/Kimono/Designer(6).png'
import productKimBack from '../Assets/Kimono/Designer(7).png'
import productKimRight from '../Assets/Kimono/Designer(8).png'
import productKimDetail from '../Assets/Kimono/Designer(9).png'

// Vest product images
import productVestFront from '../Assets/Vest/vest(1).png'
import productVestLeft from '../Assets/Vest/vest(2).png'
import productVestBack from '../Assets/Vest/vest(3).png'
import productVestRight from '../Assets/Vest/vest(4).png'
import productVestDetail from '../Assets/Vest/vest(5).png'

// Tank Top product images
import productTankFront from '../Assets/Tank/tank(1).png'
import productTankLeft from '../Assets/Tank/tank(2).png'
import productTankBack from '../Assets/Tank/tank(3).png'
import productTankRight from '../Assets/Tank/tank(4).png'
import productTankDetail from '../Assets/Tank/tank(5).png'

// T-Shirt product images
import productShirtFront from '../Assets/T-shirt/shirt(1).png'
import productShirtLeft from '../Assets/T-shirt/shirt(2).png'
import productShirtBack from '../Assets/T-shirt/shirt(3).png'
import productShirtRight from '../Assets/T-shirt/shirt(4).png'
import productShirtDetail from '../Assets/T-shirt/shirt(5).png'

// Material texture images
import materialCotton from '../Assets/Textures/material-cotton.png'
import materialPolyester from '../Assets/Textures/material-polyester.png'
import materialLeather from '../Assets/Textures/material-leather.png'
import materialWool from '../Assets/Textures/material-wool.png'
import materialBlend from '../Assets/Textures/material-blend.png'
import materialKevlar from '../Assets/Textures/material-kevlar.png'


import type { ProductData } from '../Types/product.types'

// Map product styles to their respective image sets
export const STYLE_TO_IMAGES: Record<string, string[]> = {
    'Kimono': [productKimFront, productKimLeft, productKimBack, productKimRight, productKimDetail],
    'Vest': [productVestFront, productVestLeft, productVestBack, productVestRight, productVestDetail],
    'Tank Top': [productTankFront, productTankLeft, productTankBack, productTankRight, productTankDetail],
    'Short Sleeve': [productShirtFront, productShirtLeft, productShirtBack, productShirtRight, productShirtDetail],
    'Hoodie': [productKimFront, productKimLeft, productKimBack, productKimRight, productKimDetail]
}

// Export function to get the first (front-facing) image for a style
export const getStyleFrontImage = (style: string): string => {
    const images = STYLE_TO_IMAGES[style]
    return images && images.length > 0 ? images[0] : ''
}

// Map material names to their texture images
export const MATERIAL_TO_TEXTURE: Record<string, string> = {
    'Wool': materialWool,
    'Leather': materialLeather,
    'Blend': materialBlend,
    'Cotton': materialCotton,
    'Polyester': materialPolyester,
    'Kevlar': materialKevlar
}

// Default product data structure
export const DEFAULT_PRODUCT_DATA: ProductData = {
    name: 'Loading...',
    style: 'Loading...', 
    rating: 5,
    reviewCount: 200,
    description: 'Loading product details...',
    materials: ['Cotton', 'Polyester', 'Wool', 'Blend', 'Leather', 'Kevlar'],
    features: [
        'Screen Print with Sleeve Graphics',
        '100% Cotton, Pre-Shrunk Jersey',
        'Ribbed Collar with Double Needle Stitching',
    ],
    price: 0,
    colors: ['#FFFFFF', '#000000', '#FF0000', '#0000FF', '#008000'],
    sizes: ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL']
}