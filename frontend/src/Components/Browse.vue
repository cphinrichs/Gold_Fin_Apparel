<!-- 
This page will allow users to browse through our products, 
filter by categories, sort by various criteria, and view product details.
-->
<script setup lang="ts">
import SortFilterWidget from './Widgets/SortFilterWidget.vue';

const handleFiltersChanged = (filters: any) => {
  console.log('Filters applied:', filters);
};
</script>

<template>
  <div class="browse-wrapper">
    <SortFilterWidget @filtersChanged="handleFiltersChanged" />
    <section class="browse-section">
      <h1>Browse</h1>
      <p>Browse our full collection of apparel. Use the filter panel on the left to narrow your results.</p>
    </section>
  </div>
</template>

<style scoped>
.browse-wrapper {
  position: relative;
}
.browse-section {
  padding: 60px 20px;
  max-width: 1200px;
  margin: 0 auto;
}
</style>