# Frontend Mock Data Setup

This document explains how to use the mock data system for frontend development without API connection.

## 🔧 Mock Data Status

**Mock data is currently ENABLED** for both inventory and designs.

## What's Included

The mock data system provides:

### **Inventory Data** (80 products)
- **Tank Tops**: White, Black in Cotton (Sizes: S-XL)
- **Short Sleeves**: White, Black, Navy in Cotton/Polyester (Sizes: S-XL)
- **Kimonos**: Red, Navy Blue, Gold in Wool/Cotton (Sizes: S-XL)
- **Vests**: Brown, Black, Royal Blue, Gray in Leather/Blend/Cotton (Sizes: S-XXL)

**Available Materials** (match texture files in `Assets/Textures/`):
- Blend
- Cotton
- Kevlar
- Leather
- Polyester
- Wool

**Available Styles**:
- Tank Top
- Short Sleeve
- Vest
- Kimono

### **Designs** (20 designs)
- Dragon Pattern, Cherry Blossom, Phoenix Rising, Geometric Waves, etc.
- Prices range from $6.00 to $15.00

## How to Use

### Development Mode (Mock Data)
Mock data is **already enabled** by default. Just start your development server:

```bash
npm run dev
```

The console will show:
```
🔧 Using MOCK inventory data (USE_MOCK_DATA = true)
🔧 Using MOCK designs data (USE_MOCK_DATA = true)
```

### Switching to Real API

When you're ready to connect to the real backend API:

1. **Open these files:**
   - `frontend/src/Services/inventoryApi.ts`
   - `frontend/src/Services/designApi.ts`

2. **Change the flag in each file:**
   ```typescript
   const USE_MOCK_DATA = false  // Change from true to false
   ```

3. **Ensure your backend is running:**
   - Start your Flask backend API
   - Verify it's accessible at the correct endpoint

4. **(Optional) Clean up:**
   - Delete `frontend/src/Services/mockData.ts` if no longer needed

## Mock Data Structure

### ProductApiResponse
```typescript
{
  Product_Id: number      // Unique product ID
  Style: string          // 'T-Shirt', 'Kimono', 'Vest', 'Hoodie'
  Color: string          // Hex color without '#' (e.g., 'FFFFFF')
  Material: string       // 'Cotton', 'Polyester', 'Silk', etc.
  Size: string           // 'S', 'M', 'L', 'XL', 'XXL'
  Stock: number          // Available quantity
  Price: number          // Product price
}
```

### DesignApiResponse
```typescript
{
  id: number            // Unique design ID
  name: string          // Design name
  price: number         // Additional cost for design
}
```

## Features Working with Mock Data

✅ **Home Page Carousel** - Displays unique product styles  
✅ **Browse Page** - Full product combinations with filters  
✅ **Product Detail (Inspect)** - Individual product with selectors  
✅ **Cart Functionality** - Add/remove items  
✅ **Color/Material/Size Selection** - Validation based on available combinations  
✅ **Stock Management** - Respects stock limits  

## Network Simulation

The mock data includes a simulated API delay (300ms) to mimic real network conditions. This helps identify loading state issues during development.

## Troubleshooting

### Products not showing?
1. Check browser console for the mock data confirmation message
2. Verify `USE_MOCK_DATA = true` in both API service files
3. Check that `mockData.ts` exists and is imported correctly

### Want to add more products?
Edit `frontend/src/Services/mockData.ts`:
- Add entries to `mockInventory` array
- Add entries to `mockDesigns` array
- Follow the existing data structure

### Images not displaying?
- The mock data uses product-style-based images from `Assets/` folder
- Ensure image files exist in the appropriate folders
- Check `Constants/productMappings.ts` for style-to-image mappings

## Files Modified for Mock Data

- ✨ **NEW:** `frontend/src/Services/mockData.ts` - Mock data source
- 📝 **UPDATED:** `frontend/src/Services/inventoryApi.ts` - Added mock toggle
- 📝 **UPDATED:** `frontend/src/Services/designApi.ts` - Added mock toggle
- 📝 **UPDATED:** `frontend/src/Views/HomeView.vue` - Uses real product data
- 📝 **UPDATED:** `frontend/src/Composables/useProductData.ts` - Uses mock-enabled API service

## Next Steps

1. Continue developing your frontend features
2. Test with the mock data to ensure everything works
3. When backend is ready, flip the switch to `USE_MOCK_DATA = false`
4. Test with real API to ensure compatibility
5. Remove mock data files when no longer needed

## Quick Testing Guide

To verify the mock data is working:

1. **Home Page** - Navigate to `/` to see the product carousel with real mock products
2. **Browse Page** - Navigate to `/browse` to see all product combinations
3. **Product Detail (Inspect)** - Try these examples:
   - `/inspect/1` - White Cotton Tank Top (Small) - $19.99
   - `/inspect/8` - White Cotton Short Sleeve (Small) - $24.99
   - `/inspect/15` - Navy Cotton Long Sleeve (Small) - $29.99
   - `/inspect/21` - Red Wool Kimono (Small) - $89.99
   - `/inspect/41` - Brown Leather Vest (Small) - $79.99
   - `/inspect/61` - Gray Cotton Hoodie (Small) - $44.99
4. **Check Console** - You should see messages like:
   ```
   🔧 Using MOCK inventory data (USE_MOCK_DATA = true)
   🔧 Using MOCK designs data (USE_MOCK_DATA = true)
   ```

---

**Note:** All mock data is TypeScript-typed and matches the expected API response format, ensuring a smooth transition to the real API.
