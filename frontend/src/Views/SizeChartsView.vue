<script setup lang="ts">

</script>

<template>
<section class="size-charts"> 
<img src="../Assets/goldfin_logo.jpg" alt="GoldFin Logo" class="logo"/>
  <h1>Size Charts</h1>
  <h2>Tops Size Chart</h2>
    <div class="size-chart">
      <p>To help you find the perfect fit, please refer to our size chart below</p>
      <table class="size-table">
        <thead>
          <tr>
            <th>Size</th>
            <th>Chest (inches)</th>
            <th>Waist (inches)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Small (S)</strong></td>
            <td>34-36</td>
            <td>28-30</td>
          </tr>
          <tr>
            <td><strong>Medium (M)</strong></td>
            <td>38-40</td>
            <td>32-34</td>
          </tr>
          <tr>
            <td><strong>Large (L)</strong></td>
            <td>42-44</td>
            <td>36-38</td>
          </tr>
          <tr>
            <td><strong>Extra Large (XL)</strong></td>
            <td>46-48</td>
            <td>40-42</td>
          </tr>
        </tbody>
      </table>
    </div>
    <h2>Socks Size Chart</h2>
    <div class="size-chart">
      <p>Find your perfect sock fit using our size chart</p>
      <table class="size-table">
        <thead>
          <tr>
            <th>Size</th>
            <th>Shoe Size</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Small (S)</strong></td>
            <td>5-7</td>
          </tr>
          <tr>
            <td><strong>Medium (M)</strong></td>
            <td>8-10</td>
          </tr>
          <tr>
            <td><strong>Large (L)</strong></td>
            <td>11-13</td>
          </tr>
          <tr>
            <td><strong>Extra Large (XL)</strong></td>
            <td>14+</td>
          </tr>
        </tbody>
      </table>
    </div>
    <h2>Hats Size Chart</h2>
    <div class="size-chart">
      <p>Choose the right hat size based on head circumference</p>
      <table class="size-table">
        <thead>
          <tr>
            <th>Size</th>
            <th>Head Circumference (inches)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Small (S)</strong></td>
            <td>20-21</td>
          </tr>
          <tr>
            <td><strong>Medium (M)</strong></td>
            <td>21.5-22.5</td>
          </tr>
          <tr>
            <td><strong>Large (L)</strong></td>
            <td>23-24</td>
          </tr>
          <tr>
            <td><strong>Extra Large (XL)</strong></td>
            <td>24.5+</td>
          </tr>
        </tbody>
      </table>
    </div>
</section>
</template>

<style scoped>
.logo {
  position: fixed;
  bottom: 0px;
  right: 0px;
  width: 250px;
  height: auto;
  z-index: 10;
}

h1{
  font-size: 2.5rem;
  color: #000000;
  border-bottom: 3px solid #000000;
  padding-bottom: 1rem;
  margin: 2rem 0;
  text-align: center;

}

h2{
  max-width: 600px;
  margin-left: 0.5rem;
  text-align: center;
  font-size: 1.5rem;
  color: #000000;
}

p{
  max-width: 600px;
  text-align: center;
  line-height: 1.0;
  margin: 1rem 0;
  font-size: 1.2rem;
  color: #000000;
}
.size-chart {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 600px;
}

.size-table {
  width: 100%;
  max-width: 600px;
  border-collapse: collapse;
  margin: 1.5rem 0;
  background: #fff;
  border: 2px solid #333;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.size-table thead {
  background: #333;
  color: white;
}

.size-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  font-size: 1rem;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #333;
}

.size-table td {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.size-table tbody tr:last-child td {
  border-bottom: none;
}

.size-table tbody tr:nth-child(odd) {
  background: #f9f9f9;
}

.size-table tbody tr:hover {
  background: #f0f0f0;
  transition: background 0.2s ease;
}

.size-table tbody tr:nth-child(even):hover {
  background: #e8e8e8;
}

section {
  padding: 20px clamp(16px, 5vw, 60px);
  max-width: 1200px;
  margin: 0 auto;
  box-sizing: border-box;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

h1 {
  font-size: clamp(1.8rem, 4vw, 2.5rem);
  width: 100%;
  max-width: 600px;
  text-align: center;
}

.size-table {
  width: 100%;
  max-width: 600px;
}
</style>
