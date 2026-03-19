import { ref, computed } from 'vue'
import type { CartItem } from '../Types/product.types'

const CART_STORAGE_KEY = 'goldfin_cart'

// Shared reactive cart state (module-level so it persists across component instances)
const cartItems = ref<CartItem[]>(loadFromStorage())

function loadFromStorage(): CartItem[] {
    try {
        const raw = localStorage.getItem(CART_STORAGE_KEY)
        const items: CartItem[] = raw ? JSON.parse(raw) : []
        // Normalize items that predate the quantity field
        return items.map(item => ({ ...item, quantity: item.quantity ?? 1 }))
    } catch {
        return []
    }
}

function saveToStorage(items: CartItem[]) {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(items))
}

export const useCart = () => {
    const cartCount = computed(() =>
        cartItems.value.reduce((sum, item) => sum + (item.quantity ?? 1), 0)
    )

    const addToCart = (item: CartItem) => {
        const existing = cartItems.value.find(
            (c) =>
                c.Style === item.Style &&
                c.Color === item.Color &&
                c.Material === item.Material &&
                c.Size === item.Size
        )
        if (existing) {
            existing.quantity += item.quantity ?? 1
            cartItems.value = [...cartItems.value]
        } else {
            cartItems.value = [...cartItems.value, { ...item, quantity: item.quantity ?? 1 }]
        }
        saveToStorage(cartItems.value)
    }

    const removeFromCart = (cartItemId: string) => {
        cartItems.value = cartItems.value.filter((c) => c.cartItemId !== cartItemId)
        saveToStorage(cartItems.value)
    }

    const removeQuantityFromCart = (cartItemId: string, amount: number) => {
        const item = cartItems.value.find((c) => c.cartItemId === cartItemId)
        if (!item) return
        if (amount >= item.quantity) {
            cartItems.value = cartItems.value.filter((c) => c.cartItemId !== cartItemId)
        } else {
            item.quantity -= amount
            cartItems.value = [...cartItems.value]
        }
        saveToStorage(cartItems.value)
    }

    const clearCart = () => {
        cartItems.value = []
        saveToStorage(cartItems.value)
    }

    return {
        cartItems,
        cartCount,
        addToCart,
        removeFromCart,
        removeQuantityFromCart,
        clearCart,
    }
}
