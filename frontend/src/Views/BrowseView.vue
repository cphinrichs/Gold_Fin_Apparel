<script lang="ts" setup>
import SortFilterWidget from '../Components/Widgets/SortFilterWidget.vue';

const handleFiltersChanged = (filters: any) => {
  console.log('Filters applied:', filters);
};
</script>

<template>
  <div class="page-wrapper">
    <SortFilterWidget @filtersChanged="handleFiltersChanged" />
    <section class="page-section">
      <h1>Products</h1>
      <p>Browse our full collection of products and explore different categories. Use the filter panel on the right to narrow your results.</p>
    </section>
  </div>
</template>

<style scoped>
.page-wrapper {
  position: relative;
}
.page-section {
  padding: 60px 20px;
  max-width: 1200px;
  margin: 0 auto;
}
</style>