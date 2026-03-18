<!--
This component will serve as the taskbar for our application,
providing navigation links and quick access to key features.
-->
<template>
  <nav class="taskbar">
    <router-link to="/"><h1 class="logo">GOLDFIN</h1></router-link>
    <ul>
      <li><router-link to="/">Home</router-link></li>
      <li>
        <router-link to="/browse">Browse</router-link>
        <ul class="dropdown">
          <li><router-link to="/browse?style=Tank Top">Tank Tops</router-link></li>
          <li><router-link to="/browse?style=Short Sleeve">T-Shirts</router-link></li>
          <li><router-link to="/browse?style=Long Sleeve">Long Sleeves</router-link></li>
          <li><router-link to="/browse?style=Hoodie">Hoodies</router-link></li>
          <li><router-link to="/browse?style=Vest">Vests</router-link></li>
          <li><router-link to="/browse?style=Kimono">Kimonos</router-link></li>
        </ul>
      </li>
      <li><router-link to="/about">About</router-link></li>
      <li>
        <router-link to="/help">Help</router-link>
        <ul class="dropdown">
          <li><router-link to="/contactus">Contact Us</router-link></li>
          <li><router-link to="/returnpolicy">Return Policy</router-link></li>
          <li><router-link to="/shippinginformation">Shipping Information</router-link></li>
          <li><router-link to="/sizecharts">Size Charts</router-link></li>
        </ul>
      </li>
    </ul>
    <router-link to="/cart" class="cart-button">
      <svg class="cart-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="9" cy="21" r="1"></circle>
        <circle cx="20" cy="21" r="1"></circle>
        <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
      </svg>
    </router-link>
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
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: opacity 0.3s ease, visibility 0.3s ease, transform 0.3s ease;
  z-index: 1001;
}

.taskbar li:hover > .dropdown {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
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