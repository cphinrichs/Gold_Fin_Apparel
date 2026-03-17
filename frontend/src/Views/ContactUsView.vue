<script setup lang="ts">

</script>

<template>
<section class="contact-us"> 
  <h1>Contact Us</h1>
  <div class="intro-section">
    <p>We're here to help! If you have any questions or need assistance, please don't hesitate to reach out. Our dedicated support team is committed to providing you with the best service possible.</p>
  </div>

  <div class="contact-methods">
    <div class="contact-box">
      <h2>Email</h2>
      <p class="contact-detail">support@goldfinapparel.com</p>
      <p>We typically respond to emails within 24 hours during business days.</p>
    </div>

    <div class="contact-box">
      <h2>Phone</h2>
      <p class="contact-detail">(123) 456-7890</p>
      <p>Monday - Friday: 9:00 AM - 6:00 PM EST</p>
    </div>

    <div class="contact-box">
      <h2>Customer Support Hours</h2>
      <p>We're available to assist you during standard business hours. Feel free to contact us with any inquiries about our products, services, or your orders.</p>
    </div>
  </div>
</section>
</template>

<style scoped>
h1 {
  font-size: 2.5rem;
  color: #000000;
  border-bottom: 3px solid #000000;
  padding-bottom: 1rem;
  margin: 2rem 0;
  text-align: center;

}

h2 {
  font-size: 1.3rem;
  color: #000000;
  border-bottom: #000000 solid 2px;
  border-top: #000000 solid 2px;
  padding: 1rem 0;
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.intro-section {
  max-width: 800px;
  font-size: 1.3rem;
  color: #000000;
  margin-right: auto;
}

.contact-methods {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin: 3rem 0;
}

.contact-box {
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.contact-box:hover {
  border-color: #000000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background: #f9f9f9;
}

.contact-detail {
  font-size: 1.2rem;
  font-weight: 600;
  color: #000000;
  margin: 0.5rem 0 1rem 0;
}

.contact-box p {
  font-size: 1.2rem;
  line-height: 1.2;
  color: #000000;
  margin: 0.5rem 0;
}

section {
  padding: 20px clamp(16px, 5vw, 60px);
  max-width: 1200px;
  margin: 0 auto;
  box-sizing: border-box;
  width: 100%;
}

h1 {
  font-size: clamp(1.8rem, 4vw, 2.5rem);
}

h2 {
  font-size: clamp(1rem, 2vw, 1.3rem);
}

.contact-methods {
  grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr));
}
</style>
