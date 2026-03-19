<template>
  <button class="delete-btn">
    <span class="btn-icon">✕</span>
    <span class="btn-text">Remove</span>
  </button>
</template>

<script setup lang="ts">
const handleDelete = () => {
  // Delete logic here
};
</script>

<style scoped>
.delete-btn {
  background: transparent;
  border: 2px solid #d9534f;
  padding: 12px 28px;
  font-size: 1rem;
  font-weight: 500;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #d9534f;
  text-transform: uppercase;
}

.delete-btn:hover {
  background-color: #d9534f;
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(217, 83, 79, 0.25);
}

.delete-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(217, 83, 79, 0.15);
}

.btn-icon {
  font-size: 1.2rem;
  font-weight: bold;
}

.btn-text {
  letter-spacing: 0.05em;
}
</style>
