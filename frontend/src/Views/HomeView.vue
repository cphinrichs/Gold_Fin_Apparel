<template>
  <section class="home">
  </section>
  <section class="product-list">
    <div 
      class="carousel-container"
      @mouseenter="stopAutoPlay"
      @mouseleave="startAutoPlay"
    >
      <button class="carousel-btn prev" @click="prevSlide">
        &#10094;
      </button>
      
      <div class="carousel-wrapper">
        <div class="carousel-track" :style="{ transform: `translateX(-${currentIndex * (100 / itemsPerView)}%)` }">
          <div v-for="(product, index) in products" :key="index" class="product-item">
            <a href="/inspect">
              <img :src="product.image" :alt="product.alt">
            </a>
          </div>
        </div>
      </div>
      
      <button class="carousel-btn next" @click="nextSlide">
        &#10095;
      </button>
    </div>
    
    <div class="carousel-dots">
      <span 
        v-for="(dot, index) in Math.ceil(products.length / itemsPerView)" 
        :key="index"
        class="dot"
        :class="{ active: Math.floor(currentIndex / itemsPerView) === index }"
        @click="goToSlide(index * itemsPerView)"
      ></span>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from 'vue';

interface Product {
  image: string;
  alt: string;
  // Add more properties as needed when integrating with API
  // id?: number;
  // name?: string;
  // price?: number;
}

const currentIndex = ref(0);
const itemsPerView = ref(3); // Number of items visible at once
const autoPlayInterval = ref<number | null>(null);
const autoPlayDelay = 3000; // 3 seconds

const products = ref<Product[]>([
  { image: new URL('../Assets/Kimono/Designer(5).png', import.meta.url).href, alt: 'Product Image' },
  { image: new URL('../Assets/Kimono/Designer(5).png', import.meta.url).href, alt: 'Product Image' },
  { image: new URL('../Assets/Kimono/Designer(5).png', import.meta.url).href, alt: 'Product Image' },
  { image: new URL('../Assets/Kimono/Designer(5).png', import.meta.url).href, alt: 'Product Image' },
  { image: new URL('../Assets/Kimono/Designer(5).png', import.meta.url).href, alt: 'Product Image' },
  { image: new URL('../Assets/Kimono/Designer(5).png', import.meta.url).href, alt: 'Product Image' },
]);

const nextSlide = () => {
  if (currentIndex.value >= products.value.length - itemsPerView.value) {
    currentIndex.value = 0; // Loop back to start
  } else {
    currentIndex.value++;
  }
};

const prevSlide = () => {
  if (currentIndex.value <= 0) {
    currentIndex.value = products.value.length - itemsPerView.value; // Loop to end
  } else {
    currentIndex.value--;
  }
};

const goToSlide = (index: number) => {
  currentIndex.value = index;
  stopAutoPlay();
  startAutoPlay();
};

const startAutoPlay = () => {
  autoPlayInterval.value = window.setInterval(() => {
    nextSlide();
  }, autoPlayDelay);
};

const stopAutoPlay = () => {
  if (autoPlayInterval.value !== null) {
    clearInterval(autoPlayInterval.value);
    autoPlayInterval.value = null;
  }
};

// Function to fetch products from API (ready for integration)
const fetchProducts = async () => {
  try {
    // Replace with your actual API endpoint
    // const response = await fetch('YOUR_API_ENDPOINT');
    // const data = await response.json();
    // products.value = data.map((item: any) => ({
    //   image: item.imageUrl,
    //   alt: item.name,
    //   id: item.id,
    //   name: item.name,
    //   price: item.price
    // }));
  } catch (error) {
    console.error('Error fetching products:', error);
  }
};

onMounted(() => {
  // fetchProducts();
  startAutoPlay();
});

onUnmounted(() => {
  stopAutoPlay();
});
</script>

<style scoped>
.home {
  width: 100%;
  height: 100vh;
  background-color: #D8CEC5;
  font-family: Arial, sans-serif;
  background-image: url('../Assets/T-shirt/T-shirt(front).png');
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
}

.product-list {
  padding: 3rem 2rem;
  background-color: #f5f5f5;
}

.carousel-container {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.carousel-wrapper {
  overflow: hidden;
  flex: 1;
}

.carousel-track {
  display: flex;
  transition: transform 0.4s ease-in-out;
  gap: 2rem;
}

.product-item {
  flex: 0 0 calc(33.333% - 1.333rem);
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.product-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.product-item img {
  width: 100%;
  height: 300px;
  object-fit: contain;
}

.carousel-btn {
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
  flex-shrink: 0;
}

.carousel-btn:hover:not(:disabled) {
  background-color: rgba(0, 0, 0, 0.8);
}

.carousel-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.carousel-dots {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 2rem;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #ccc;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.dot.active {
  background-color: #333;
}

.dot:hover {
  background-color: #666;
}
</style>