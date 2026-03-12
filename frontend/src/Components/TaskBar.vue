<!--
This component will serve as the taskbar for our application,
providing navigation links and quick access to key features.
-->
<template>
  <nav class="taskbar">
    <a href="/"><h1 class="logo">GOLDFIN</h1></a>
    <ul>
      <li><a href="/">Home</a></li>
      <li>
        <a href="/browse">Browse</a>
        <ul class="dropdown">
          <li><a href="/tops">Tops</a></li>
          <li><a href="/hats">Hats</a></li>
          <li><a href="/socks">Socks</a></li>
          <li><a href="/accessories">Accessories</a></li>
        </ul>
      </li>
      <li><a href="/about">About</a></li>
      <li><a href="/help">Help</a></li>
    </ul>
    <a href="/checkout" class="cart-button">
      <svg class="cart-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="9" cy="21" r="1"></circle>
        <circle cx="20" cy="21" r="1"></circle>
        <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
      </svg>
    </a>
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

.taskbar > ul {
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
  text-decoration: none;
  background: 
    radial-gradient(circle at 20% 50%, #FFD700 0%, #FFD700 20%, transparent 50%),
    radial-gradient(circle at 60% 30%, #FFD700 0%, #FFD700 20%, transparent 50%),
    radial-gradient(circle at 80% 70%, #FFD700 0%, #FFD700 20%, transparent 50%),
    radial-gradient(circle at 40% 80%, #FFD700 0%, #FFD700 20%, transparent 50%);
  background-size: 100% 100%;
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 
    1px 1px 0px rgba(0, 0, 0, 0.5);
}

.taskbar li {
  position: relative;
}

.dropdown {
  list-style: none;
  position: absolute;
  top: 100%;
  left: 0;
  background-color: #222;
  border: 1px solid #444;
  border-radius: 4px;
  padding: 0.5rem 0;
  min-width: 150px;
  display: none;
  z-index: 1001;
}

.taskbar li:hover > .dropdown {
  display: block;
}

.dropdown li {
  padding: 0;
  margin: 0;
}

.dropdown a {
  display: block;
  padding: 0.75rem 1rem;
  color: white;
  text-decoration: none;
  text-transform: none;
  transition: background-color 0.2s;
}

.cart-button {
  margin-left: auto;
  color: #333;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: 600;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cart-icon {
  width: 24px;
  height: 24px;
  color: white;
  margin-right: 1.0rem;
}

.cart-button:hover {
  text-decoration: none;
}
</style>