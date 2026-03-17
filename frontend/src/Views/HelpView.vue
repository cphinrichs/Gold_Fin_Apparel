<script setup lang="ts">

</script>

<template>
<section class="help"> 
  <h1>Help Center</h1>
   <div class="help-intro">
     <p class = "p2">Welcome to our Help Center. We're here to help you with any questions or concerns you may have. Please select one of the options below to learn more.</p>
   </div>
   <div class="help-links">
     <a href="/contactus" class="help-link">
       <h3>Contact Us</h3>
       <p>Get in touch with our support team</p>
     </a>
     <a href="/returnpolicy" class="help-link">
       <h3>Return Policy</h3>
       <p>Learn about our return process</p>
     </a>
     <a href="/shippinginformation" class="help-link">
       <h3>Shipping Information</h3>
       <p>Find out how we ship your orders</p>
     </a>
     <a href="/sizecharts" class="help-link">
       <h3>Size Charts</h3>
       <p>Find your perfect fitting size</p>
     </a>
   </div>
   <img src="../Assets/goldfin3.png" alt="GoldFin 3 Logo" class="logo"/>
</section>
</template>

<style scoped>
.logo {
  display: block;
  margin: 3rem auto 0;
  width: 700px;
  height: auto;
  z-index: 10;
}

h1 {
  margin-left: 10px;
  font-size: 2.5rem;
  color: #000000;
  border-bottom: 3px solid #000000;
  padding-bottom: 0.5rem;
  max-width: 800px;
}

.p2 {
  font-size: 1.1rem;
  line-height: 1.8;
  margin-right: 0;
  padding: 20px;
  max-width: 800px;
  padding: 1.5rem 0;
  border-radius: 4px;
  color: #555;
}

.help-intro {
  max-width: 800px;
  margin: 2rem 0;
  font-size: 1.1rem;
  line-height: 1.6;
}

.help-links {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin: 3rem 0;
}

.help-link {
  text-decoration: none;
  padding: 2rem;
  border: 2px solid #333;
  border-radius: 8px;
  transition: all 0.3s ease;
  color: #333;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.help-link:hover {
  border-color: #333;
  background-color: #f9f9f9;
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.help-link h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
}

.help-link p {
  margin: 0;
  color: #666;
  font-size: 0.95rem;
}

section {
  padding: 0px 20px;
  max-width: 1200px;
  margin: 0 auto;
}
</style>