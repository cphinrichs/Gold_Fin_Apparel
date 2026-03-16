<script setup lang="ts">
import About from '../Components/About.vue';
import { ref } from 'vue';
//import logo from '../Assets/goldfin_logo.jpg';

const showMembers = ref(false);
</script>

<template>
  <section class="about"> 
    <div class="aboutus"> 
         <h1>About Us</h1>
    <!-- simple, easy to edit inline logo placed top right -->
    <img src="../Assets/goldenfinger.png" alt="GoldFinger Logo" class="logo"/>
    <p class = "p">
    Welcome to Gold Fin Apparel! We are a company dedicated to providing high-quality, stylish clothing for our customers. Our mission is to create unique and fashionable apparel that allows individuals to express their personality and stand out from the crowd.
    At Gold Fin Apparel, we believe in the power of self-expression through fashion. We strive to design clothing that not only looks great but also makes our customers feel confident and empowered. Our team of talented designers works tirelessly to create innovative and trendy pieces that cater to a wide range of styles and preferences.
    Our values are rooted in creativity, quality, and customer satisfaction. We are committed to using sustainable materials and ethical manufacturing practices to minimize our environmental impact. We also prioritize customer feedback and continuously seek ways to improve our products and services.
    Thank you for choosing Gold Fin Apparel. We look forward to being a part of your fashion journey and helping you express your unique style!
     </p>
    </div>

  <button class="members-toggle" @click="showMembers = !showMembers">
    <span class="toggle-arrow" :class="{ open: showMembers }">▶</span>
    Meet The Team
  </button>

  <div v-if="showMembers" class="members-section">
  <h1>Golden Finger </h1>
    <p class = "p2">
      Our team is composed of passionate individuals who are dedicated to bringing you the best in fashion. Each member brings their unique skills and creativity to the table, ensuring that Gold Fin Apparel remains at the forefront of style and innovation.
    </p>
    <h2>Dillon Hines - Team Lead & Full Stack Developer</h2>
    <p class = "info">
        Dillon is responsible for overseeing the development of our applications and ensuring that our team is working efficiently. With a strong background in software engineering, he leads the charge in creating innovative solutions for our customers.
    </p>
    <h2>Kara Lynch - Backend Developer, & DBA</h2>
    <p class = "info">
        Kara is responsible for developing and maintaining our backend systems and databases. With a strong background in software engineering, she ensures that our applications run smoothly and efficiently. As a DBA, Kara also manages our data integrity and performance, ensuring that our systems are reliable and secure.
    </p>
    <h2>Jacob Martin - Backend Developer & Architect</h2>
    <p class = "info">
        Jacob is responsible for developing and maintaining our backend systems. With a strong background in software engineering, he ensures that our applications run smoothly and efficiently.
    </p>
    <h2>Parker Hinrichs - Frontend Developer</h2>
    <p class = "info">
        Parker is responsible for developing and maintaining our frontend systems. With a strong background in software engineering, he ensures that our applications run smoothly and efficiently.
    </p>
    <h2>Tyson Lucas - Frontend Developer</h2>
    <p class = "info">
        Tyson is responsible for developing and maintaining our frontend systems. With a strong background in software engineering, he ensures that our applications run smoothly and efficiently.
    </p>
    <h2> Janniebeth Melendez Torres - Information Developer </h2>
    <p class = "info">
        Janniebeth is responsible for creating and maintaining our documentation and information resources. With a strong background in technical writing, she ensures that our customers have access to clear and concise information about our products and services.
    </p>
  </div>
  </section>
</template>

<style scoped>
h1 {
  margin-left: 10px;
  font-size: 2.5rem;
  color: #000000;
  border-bottom: 3px solid #000000;
  padding-bottom: 1rem;
  margin-top: 0rem;
}

h2 {
  margin-left: 10px;
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 0.25rem;
}

.aboutus {
  padding: 0px;
  max-width: 800px;
  margin: 0;
  text-align: left;
  position: relative;
}

.logo {
  position: absolute;
  top: 0px;
  right: -510px;
  width: 500px;
  height: auto;
  z-index: 10;
}

.p {
  font-size: 1.3rem;
  margin-right: 0;
  margin-left: 10px;
  padding: 5px;
  color: #555;
  border-bottom: 3px solid #0000;
}

.p2 {
  font-size: 1.3rem;
  margin-right: 0;
  margin-left: 10px;
  border-radius: 4px;
  color: #555;
}

.info {
  font-size: 1.1rem;
  margin-right: 0;
  padding: 1.5rem;
  margin-left: 10px;
  margin-top: -0.95rem;
  color: #555;
  transition: all 0.3s ease;
}

section {
  padding: 20px 5px;
}

.members-toggle {
  background: #333;
  color: white;
  border: none;
  padding: 1rem 2rem;
  font-size: 1.2rem;
  font-weight: 600;
  cursor: pointer;
  border-radius: 6px;
  margin: 2rem 0;
  text-transform: uppercase;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  transition: all 0.3s ease;
}

.members-toggle:hover {
  background: #555;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.toggle-arrow {
  display: inline-block;
  transition: transform 0.3s ease;
}

.toggle-arrow.open {
  transform: rotate(90deg);
}

.members-section {
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>