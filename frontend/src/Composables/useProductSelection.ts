import { ref } from 'vue'
import { toggleActiveButton } from '../Utils/productHelpers'

/**
 * Composable for managing user selections (color, material, size)
 */
export const useProductSelection = () => {
    const currentImageIndex = ref(0)
    const selectedSize = ref('')

    const handleColorSelection = (
        event: Event, 
        color: string, 
        updateColor: (color: string) => void,
        clearIncompatible: () => void
    ) => {
        const target = event.currentTarget as HTMLElement
        toggleActiveButton('.color-btn', target)
        updateColor(color)
        clearIncompatible()
    }

    const handleSizeSelection = (
        event: Event,
        size: string,
        updateSize: (size: string) => void,
        clearIncompatibleForSize: (size: string) => void
    ) => {
        const button = event.target as HTMLButtonElement
        if (button.classList.contains('unavailable')) {
            return
        }
        updateSize(size)
        clearIncompatibleForSize(size)
        selectedSize.value = size
    }

    const handleMaterialSelection = (
        event: Event, 
        material: string, 
        updateMaterial: (material: string) => void,
        clearIncompatible: () => void
    ) => {
        const target = event.currentTarget as HTMLElement
        toggleActiveButton('.material-btn', target)
        updateMaterial(material)
        clearIncompatible()
    }

    return {
        currentImageIndex,
        selectedSize,
        handleColorSelection,
        handleSizeSelection,
        handleMaterialSelection
    }
}