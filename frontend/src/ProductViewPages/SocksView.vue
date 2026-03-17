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
      <h1>Socks</h1>
      <p>Browse our collection of socks. Use the filter panel on the left to narrow your results.</p>
    </section>
  </div>
</template>

<style scoped>
.page-wrapper {
  position: relative;
  width: 100%;
  box-sizing: border-box;
}
.page-section {
  padding: clamp(30px, 5vw, 60px) clamp(16px, 5vw, 60px);
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}
.page-section h1 {
  font-size: clamp(1.8rem, 4vw, 2.5rem);
}
.page-section p {
  font-size: clamp(0.95rem, 1.5vw, 1.1rem);
  max-width: 700px;
}
</style>