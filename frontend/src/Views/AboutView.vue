<script setup lang="ts">
import TaskBar from '../Components/TaskBar.vue';
import About from '../Components/About.vue';
//import logo from '../Assets/goldfin_logo.jpg';
</script>

<template>
    <TaskBar />
    <div class="about"> 
        <About />
    </div>
    <!-- simple, easy to edit inline logo placed top right below header-->
    <img src="../Assets/goldfin_logo.jpg" alt="GoldFin Logo"
    style="
        position: absolute;
        top: 220px;
        right: 20px;
        width: 200px;
        height: auto; 
        border: 2px solid #333;
        border-radius: 10px;
        "/>
</template>

<style>
</style>