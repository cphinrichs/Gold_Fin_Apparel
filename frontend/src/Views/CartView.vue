<script lang="ts" setup>
import { onMounted } from 'vue';
import Cart from '../Components/Cart.vue';

onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'instant' });
});
</script>

<template>
 <section>
  <div>
    <h1>Cart Page</h1>
    <p>Here, users will be able to review their selected items, once reviewed and edited can advance to checkout page.</p>
  </div>
  <Cart />
  </section>
</template>

<style scoped>
section {
  padding: 80px 20px 20px 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}
</style>