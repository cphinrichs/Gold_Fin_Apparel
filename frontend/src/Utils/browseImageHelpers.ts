import { STYLE_TO_IMAGES, MATERIAL_TO_TEXTURE } from '../Constants/productMappings'

/**
 * Get the front-facing image URL for a product style
 * Returns the raw image path (for use in img src or CSS backgroundImage)
 */
export const getStyleImageUrl = (style: string): string => {
    console.log('getStyleImageUrl called with style:', style)
    console.log('Available styles in STYLE_TO_IMAGES:', Object.keys(STYLE_TO_IMAGES))
    
    const images = STYLE_TO_IMAGES[style]
    console.log('Images found for style:', images)
    
    if (!images || images.length === 0) {
        console.warn(`No images found for style: ${style}`)
        return ''
    }
    
    const imageUrl = images[0]
    console.log('Returning image URL:', imageUrl)
    console.log('Image URL type:', typeof imageUrl)
    
    // Return the imported image path directly
    return imageUrl || ''
}

/**
 * Get the material texture URL
 * Returns the raw texture path
 */
export const getMaterialTextureUrl = (material: string): string => {
    const texture = MATERIAL_TO_TEXTURE[material]
    if (!texture) {
        console.warn(`No texture found for material: ${material}`)
        return ''
    }
    return texture
}

/**
 * Get the design image URL by design ID
 * Returns the raw image path
 */
export const getDesignImageUrl = (designId: number): string => {
    try {
        return new URL(`../Assets/Designs/${designId}.png`, import.meta.url).href
    } catch (e) {
        console.error(`Failed to load design image for ID ${designId}:`, e)
        return ''
    }
}