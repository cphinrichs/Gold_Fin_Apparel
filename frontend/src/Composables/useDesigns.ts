import {ref} from 'vue'
import type {Ref} from 'vue'
import {fetchDesigns} from '../Services/designApi'
import type {DesignApiResponse} from '../Types/design.types'

/**
 * Composable for managing design data and loading state
 */
export const useDesigns = () => {
    // State
    const designs: Ref<DesignApiResponse[]> = ref([])
    const loading = ref(false)
    const error: Ref<string | null> = ref(null)

    /**
     * Fetch all designs from the API
     */
    const loadDesigns = async () => {
        try {
            loading.value = true
            error.value = null

            const data = await fetchDesigns()

            designs.value = data
            console.log('designs.value set to:', designs.value)
            console.log('Number of designs:', designs.value.length)
        } catch (err) {
            error.value = (err as Error).message
            console.error('Error loading designs:', error.value)
        } finally {
            loading.value = false
        }
    }

    return {
        designs,
        loading,
        error,
        loadDesigns
    }
}