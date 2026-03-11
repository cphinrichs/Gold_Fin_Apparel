<!--
This component will serve as the taskbar for our application,
providing navigation links and quick access to key features.
-->
<template>
  <nav class="taskbar">
    <a href="/"><h1 class="logo">GOLDFIN</h1></a>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/products">Products</a></li>
      <li><a href="/about">About</a></li>
      <li><a href="/help">Help</a></li>
    </ul>
  </nav>
</template>

<script lang="ts" setup>

</script>

<style scoped>
.taskbar {
  background-color: #333;
  padding: 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
}

.logo {
  font-family: Georgia, 'Times New Roman', Times, serif;
  font-size: 2.8rem;
  letter-spacing: 0.15em;
  font-weight: 700;
  color: #fff;
  margin: 0;
}

.taskbar ul {
  list-style: none;
  display: flex;
  gap: 1rem;
  margin: 0;
  padding: 0;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.taskbar a {
  color: white;
  text-decoration: none;
  text-transform: uppercase;
}

.taskbar a:hover {
  text-decoration: underline;
}
</style>