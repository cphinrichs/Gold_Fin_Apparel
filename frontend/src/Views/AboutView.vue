<script setup lang="ts">
import About from '../Components/About.vue';
//import logo from '../Assets/goldfin_logo.jpg';
</script>

<template>
  <section class="about"> 
    <div class="aboutus"> 
         <h1>About Us</h1>
    <!-- simple, easy to edit inline logo placed top right -->
    <img src="../Assets/goldfin_logo.jpg" alt="GoldFin Logo" class="logo"/>
    <p class = "p">
    Welcome to Gold Fin Apparel! We are a company dedicated to providing high-quality, stylish clothing for our customers. Our mission is to create unique and fashionable apparel that allows individuals to express their personality and stand out from the crowd.
    At Gold Fin Apparel, we believe in the power of self-expression through fashion. We strive to design clothing that not only looks great but also makes our customers feel confident and empowered. Our team of talented designers works tirelessly to create innovative and trendy pieces that cater to a wide range of styles and preferences.
    Our values are rooted in creativity, quality, and customer satisfaction. We are committed to using sustainable materials and ethical manufacturing practices to minimize our environmental impact. We also prioritize customer feedback and continuously seek ways to improve our products and services.
    Thank you for choosing Gold Fin Apparel. We look forward to being a part of your fashion journey and helping you express your unique style!
     </p>
    </div>

  <h1>Meet The Team</h1>
    <p class = "p2">
      Our team is composed of passionate individuals who are dedicated to bringing you the best in fashion. Each member brings their unique skills and creativity to the table, ensuring that Gold Fin Apparel remains at the forefront of style and innovation.
    </p>
    <h2>Dillon Hines - Team Lead & Jira Guru</h2>
    <p class = "info">
        Dillon is responsible for overseeing the development of our applications and ensuring that our team is working efficiently. With a strong background in software engineering, he leads the charge in creating innovative solutions for our customers.
    </p>
    <h2>Kara Lynch - Backend Developer, DBA, & Code Maxxer</h2>
    <p class = "info">
        Kara is responsible for developing and maintaining our backend systems and databases. With a strong background in software engineering, she ensures that our applications run smoothly and efficiently. As a DBA, Kara also manages our data integrity and performance, ensuring that our systems are reliable and secure.
    </p>
    <h2>Jacob Martin - Backend Developer & Car Enthusiast</h2>
    <p class = "info">
        Jacob is responsible for developing and maintaining our backend systems. With a strong background in software engineering, he ensures that our applications run smoothly and efficiently. In his free time, Jacob enjoys working on cars and attending automotive events.
    </p>
    <h2>Parker Hinrichs - Frontend Developer & GitHub Moderator</h2>
    <p class = "info">
        Parker is responsible for developing and maintaining our frontend systems. With a strong background in software engineering, he ensures that our applications run smoothly and efficiently. As a GitHub moderator, Parker also helps manage our open-source contributions and community interactions.
    </p>
    <h2>Tyson Lucas - Frontend Developer & Chill Dude</h2>
    <p class = "info">
        Tyson is responsible for developing and maintaining our frontend systems. With a strong background in software engineering, he ensures that our applications run smoothly and efficiently. Also known for his chill demeanor and love of all things gold, Tyson brings a unique perspective to our team and helps keep things lighthearted.
    </p>
    <h2> Janniebeth Melendez Torres - Information Developer & Powerpoint Savant</h2>
    <p class = "info">
        Janniebeth is responsible for creating and maintaining our documentation and information resources. With a strong background in technical writing, she ensures that our customers have access to clear and concise information about our products and services. As a PowerPoint savant, Janniebeth also creates engaging presentations to help communicate our brand and mission to a wider audience.
    </p>
  </section>
</template>

<style scoped>
h1{
  margin-left: 10px;
}

h2{
  margin-left: 10px;
}

.aboutus {
  padding: 10px;
}

.logo {
  position: absolute;
  bottom: -380px;
  right: -15px;
  width: 250px;
  height: auto;
}

.p{
  font-size: 1.2rem;
  line-height: 1.6;
  margin-right: 200px;
  padding: 10px;

}

.p2{
    font-size: 1.2rem;
    line-height: 1.6;
    margin-right: 200px;
    padding: 10px;

}

.info{
    font-size: 1.2rem;
    line-height: 1.5;
    margin-right: 200px;
    padding: 10px;
}
</style>