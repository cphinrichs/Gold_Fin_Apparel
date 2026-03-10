<!--
This component will serve as the taskbar for our application,
providing navigation links and quick access to key features.
-->
<template>
  <nav class="taskbar">
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/products">Products</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</template>

<script lang="ts" setup>
</script>

<style scoped>
.taskbar {
  background-color: #333;
  color: white;
  padding: 1rem;
}

.taskbar ul {
  list-style: none;
  display: flex;
  gap: 1rem;
}

.taskbar a {
  color: white;
  text-decoration: none;
}

.taskbar a:hover {
  text-decoration: underline;
}
</style>