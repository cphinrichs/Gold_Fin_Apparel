<!--
Visual and Interactive component on Browse vue. This component will serve as the filter widget for our application,
allowing users to filter products by various criteria such as size, color, style, and material.
-->
<script setup lang="ts">
import { ref, reactive, computed } from 'vue';

type Filters = {
  colors: string[];
  materials: string[];
  sizes: string[];
  styles: string[];
};

const isOpen = ref(false);

const filters = reactive<Filters>({
  colors: [],
  materials: [],
  sizes: [],
  styles: [],
});

const colorOptions = ['White', 'Black', 'Red', 'Blue', 'Green'];
const materialOptions = ['Cotton', 'Polyester', 'Wool', 'Silk', 'Kevlar'];
const sizeOptions = ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL'];
const styleOptions = ['Short Sleeve', 'Long Sleeve', 'Hoodie', 'Sweater', 'Vest', 'Kimono'];

const activeFilterCount = computed(() =>
  filters.colors.length + filters.materials.length + filters.sizes.length + filters.styles.length
);

const toggleFilter = (category: keyof typeof filters, value: string) => {
  const list = filters[category] as string[];
  const idx = list.indexOf(value);
  if (idx === -1) list.push(value);
  else list.splice(idx, 1);
};

const isSelected = (category: keyof typeof filters, value: string): boolean =>
  (filters[category] as string[]).includes(value);

const clearAll = () => {
  filters.colors = [];
  filters.materials = [];
  filters.sizes = [];
  filters.styles = [];
};

const emit = defineEmits<{ (e: 'filtersChanged', filters: Filters): void }>();
</script>

<template>
  <!-- Toggle hamburger button pinned to top-right below TaskBar -->
  <div class="filter-toggle-tab" @click="isOpen = !isOpen" :class="{ open: isOpen }">
    <span class="toggle-icon">{{ isOpen ? '✕' : '☰' }}</span>
    <span v-if="activeFilterCount > 0 && !isOpen" class="filter-badge">{{ activeFilterCount }}</span>
  </div>

  <!-- Slideout panel from right -->
  <div class="filter-panel" :class="{ open: isOpen }">
    <div class="panel-inner">
    <div class="panel-header">
      <h2>Sort &amp; Filter</h2>
      <button class="clear-btn" @click="clearAll" v-if="activeFilterCount > 0">
        Clear All ({{ activeFilterCount }})
      </button>
    </div>

    <!-- Color -->
    <div class="filter-group">
      <h3>Color</h3>
      <div class="filter-options">
        <label
          v-for="color in colorOptions"
          :key="color"
          class="filter-chip"
          :class="{ selected: isSelected('colors', color) }"
          @click="toggleFilter('colors', color)"
        >
          <span class="color-dot" :class="color.toLowerCase()"></span>
          {{ color }}
        </label>
      </div>
    </div>

    <!-- Material -->
    <div class="filter-group">
      <h3>Material</h3>
      <div class="filter-options">
        <label
          v-for="material in materialOptions"
          :key="material"
          class="filter-chip"
          :class="{ selected: isSelected('materials', material) }"
          @click="toggleFilter('materials', material)"
        >
          {{ material }}
        </label>
      </div>
    </div>

    <!-- Size -->
    <div class="filter-group">
      <h3>Size</h3>
      <div class="filter-options size-options">
        <label
          v-for="size in sizeOptions"
          :key="size"
          class="filter-chip size-chip"
          :class="{ selected: isSelected('sizes', size) }"
          @click="toggleFilter('sizes', size)"
        >
          {{ size }}
        </label>
      </div>
    </div>

    <!-- Style -->
    <div class="filter-group">
      <h3>Style</h3>
      <div class="filter-options">
        <label
          v-for="style in styleOptions"
          :key="style"
          class="filter-chip"
          :class="{ selected: isSelected('styles', style) }"
          @click="toggleFilter('styles', style)"
        >
          {{ style }}
        </label>
      </div>
    </div>

    <button class="apply-btn" @click="emit('filtersChanged', filters); isOpen = false">
      Apply Filters
    </button>
    </div>
  </div>

  <!-- Overlay backdrop -->
  <div class="filter-overlay" v-if="isOpen" @click="isOpen = false"></div>
</template>

<style scoped>
/* Toggle hamburger button in top-right corner below TaskBar */
.filter-toggle-tab {
  position: fixed;
  top: 85px;
  right: 0;
  z-index: 1100;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #333;
  color: #FFD700;
  padding: 10px 12px;
  border-radius: 8px 0 0 8px;
  cursor: pointer;
  box-shadow: -3px 2px 10px rgba(0, 0, 0, 0.25);
  transition: background 0.2s ease;
}

.filter-toggle-tab.open {
  background: #FFD700;
  color: #333;
}

.toggle-icon {
  font-size: 1.3rem;
  line-height: 1;
}

.filter-badge {
  background: #FFD700;
  color: #333;
  font-size: 0.7rem;
  font-weight: 700;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: -6px;
  left: -6px;
}

/* Panel slides in from right, starts below TaskBar */
.filter-panel {
  position: fixed;
  top: 84px;
  right: -340px;
  width: 300px;
  height: calc(100vh - 80px);
  background: #fff;
  z-index: 1050;
  overflow-y: scroll;
  padding: 0;
  box-shadow: none;
  transition: right 0.35s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.35s ease;
  display: block;
}

.filter-panel.open {
  right: 0;
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.18);
}

.panel-inner {
  padding: 1.5rem 1.5rem 5rem 1.5rem;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.panel-header h2 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #333;
  border-bottom: 3px solid #FFD700;
  padding-bottom: 0.4rem;
}

.clear-btn {
  background: none;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 0.3rem 0.6rem;
  font-size: 0.8rem;
  color: #666;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.clear-btn:hover {
  border-color: #FF4444;
  color: #FF4444;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.filter-group h3 {
  font-size: 0.95rem;
  font-weight: 700;
  color: #333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-left: 3px solid #FFD700;
  padding-left: 0.5rem;
  margin: 0;
}

.filter-options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

/* Chips */
.filter-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0.4rem 0.85rem;
  border: 2px solid #e0e0e0;
  border-radius: 20px;
  font-size: 0.875rem;
  color: #555;
  background: #fafafa;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
}

.filter-chip:hover {
  border-color: #FFD700;
  background: #fffde7;
}

.filter-chip.selected {
  border-color: #FFD700;
  background: #FFD700;
  color: #333;
  font-weight: 600;
}

/* Size chips slightly squared */
.size-chip {
  min-width: 48px;
  justify-content: center;
  border-radius: 6px;
  padding: 0.4rem 0.5rem;
}

/* Color dots */
.color-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 1px solid rgba(0,0,0,0.15);
  flex-shrink: 0;
}
.color-dot.white  { background: #ffffff; border-color: #ccc; }
.color-dot.black  { background: #1a1a1a; }
.color-dot.red    { background: #e53935; }
.color-dot.blue   { background: #1e88e5; }
.color-dot.green  { background: #43a047; }

/* Apply button */
.apply-btn {
  margin-top: 0.5rem;
  width: 100%;
  padding: 0.85rem;
  background: #333;
  color: #FFD700;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
  text-transform: uppercase;
}

.apply-btn:hover {
  background: #FFD700;
  color: #333;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Backdrop overlay */
.filter-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 1040;
}
</style>
