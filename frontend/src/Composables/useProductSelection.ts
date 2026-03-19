import { ref } from 'vue'
import { toggleActiveButton } from '../Utils/productHelpers'

/**
 * Composable for managing user selections (color, material, size)
 */
export const useProductSelection = () => {
    const currentImageIndex = ref(0)
    const selectedSize = ref('')

    const handleColorSelection = (event: Event, color: string, updateColor: (color: string) => void) => {
        const target = event.currentTarget as HTMLElement
        toggleActiveButton('.color-btn', target)
        updateColor(color)
    }

    const handleSizeSelection = (event: Event, size: string) => {
        const target = event.currentTarget as HTMLElement
        toggleActiveButton('.size-btn', target)
        selectedSize.value = size
    }

    const handleMaterialSelection = (event: Event, material: string, updateMaterial: (material: string) => void) => {
        const target = event.currentTarget as HTMLElement
        toggleActiveButton('.material-btn', target)
        updateMaterial(material)
    }

    return {
        currentImageIndex,
        selectedSize,
        handleColorSelection,
        handleSizeSelection,
        handleMaterialSelection
    }
}