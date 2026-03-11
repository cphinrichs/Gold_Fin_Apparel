<template>
  <section class="home">
  </section>
  <section class="product-list">
    <ul>
      <li class="product-item">
        <a href="/inspect"><img src="../Assets/Designer(5).png" alt="Product Image"></a>
      </li>
      <li class="product-item">
        <a href="/inspect"><img src="../Assets/Designer(5).png" alt="Product Image"></a>
      </li>
      <li class="product-item">
        <a href="/inspect"><img src="../Assets/Designer(5).png" alt="Product Image"></a>
      </li>
    </ul>
  </section>
</template>

<script lang="ts" setup>
</script>

<style scoped>
.home {
  width: 100%;
  height: 100vh;
  font-family: Arial, sans-serif;
  background-image: url('../Assets/Designer(5).png');
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
}

.products {
  padding: 3rem 2rem;
  background-color: #f5f5f5;
}

.products h2 {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 2rem;
  color: #333;
}

.product-list {
  padding: 3rem 2rem;
  background-color: #f5f5f5;
}

.product-list ul {
  list-style: none;
  display: flex;
  gap: 2rem;
  padding: 0;
  margin: 0;
  max-width: 1200px;
  margin: 0 auto;
  justify-content: center;
}

.product-item {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  flex: 1;
  max-width: 350px;
}

.product-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.product-item img {
  width: 100%;
  height: 300px;
  object-fit: contain;
}

</style>