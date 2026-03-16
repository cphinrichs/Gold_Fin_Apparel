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
      <h1>Tops</h1>
      <p>Browse our collection of tops. Use the filter panel on the left to narrow your results.</p>
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