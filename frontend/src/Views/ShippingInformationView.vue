<script setup lang="ts">

</script>

<template>
<section class="shipping-information"> 
  <h1>Shipping Information</h1>
  <div class="intro-section">
    <p>We're committed to getting your order to you quickly and safely. Learn more about our shipping options, timelines, and policies below.</p>
  </div>

  <div class="shipping-section">
    <h2>Shipping Methods</h2>
    <div class="shipping-box">
      <div class="shipping-option">
        <h3>Standard Shipping</h3>
        <p class="shipping-detail">FREE on all orders</p>
        <p>Delivery: 5-7 business days</p>
      </div>
      <div class="shipping-option">
        <h3>Express Shipping</h3>
        <p class="shipping-detail">$9.99</p>
        <p>Delivery: 2-3 business days</p>
      </div>
      <div class="shipping-option">
        <h3>Overnight Shipping</h3>
        <p class="shipping-detail">$14.99</p>
        <p>Delivery: Next business day</p>
      </div>
    </div>
  </div>

  <div class="shipping-section">
    <h2>Processing & Handling</h2>
    <div class="shipping-box">
      <p><strong>Order Processing:</strong> Most orders are processed and shipped within 1-2 business days. Orders placed on weekends or holidays will be processed the next business day.</p>
      <p><strong>Order Tracking:</strong> You'll receive a shipping confirmation email with tracking information once your order ships.</p>
      <p><strong>Holidays:</strong> We're closed on major holidays. Orders placed during these periods will be processed the next business day.</p>
    </div>
  </div>

  <div class="shipping-section">
    <h2>Shipping Destinations</h2>
    <div class="shipping-box">
      <p>We currently ship to all 50 US states. For international orders or questions about shipping to your location, please contact our support team.</p>
    </div>
  </div>

  <div class="shipping-section">
    <h2>Shipping Costs</h2>
    <div class="shipping-box">
      <p><strong>Free shipping</strong> on all standard shipping orders over $50. Standard shipping is also available for a flat rate of $5.99 on orders under $50.</p>
      <p>Express and overnight shipping rates are calculated based on weight and destination at checkout.</p>
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
}

h2 {
  font-size: 1.3rem;
  color: #000000;
  border-bottom: #000000 solid 2px;
  border-top: #000000 solid 2px;
  padding: 1.5rem 0;
  margin-bottom: 1rem;
}

h3 {
  font-size: 1.1rem;
  color: #000000;
  margin: 0 0 0.5rem 0;
}

.intro-section {
  font-size: 1.1rem;
  line-height: 1.2;
  color: #000000;
}

.shipping-section {
  margin: 2.5rem 0;
}

.shipping-box {
  padding: 2rem;
  border-radius: 4px;
}

.shipping-option {
  display: inline-block;
  width: calc(33.333% - 1.5rem);
  margin-right: 2rem;
  vertical-align: top;
}

.shipping-option:nth-child(3n) {
  margin-right: 0;
}

.shipping-option h3 {
  margin-top: 0;
}

.shipping-detail {
  font-weight: 600;
  color: #000000;
  margin: 0.5rem 0 0.5rem 0;
}

.shipping-box p {
  font-size: 1rem;
  line-height: 1.2;
  color: #000000;
  margin: 1rem 0;
}

section {
  padding: 0px 20px;
  max-width: 1200px;
  margin: 0 auto;
}
</style>
