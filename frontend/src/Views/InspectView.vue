<template>
    <div class="inspect-container">
        <section class="inspect">
            <ul>
                <li class="inspect-item">
                    <img src="../Assets/Designer(5).png" alt="Product Image">
                </li>
                <li class="inspect-item">
                    <img src="../Assets/Designer(5).png" alt="Product Image">
                </li>
                <li class="inspect-item">
                    <img src="../Assets/Designer(5).png" alt="Product Image">
                </li>
                <li class="inspect-item">
                    <img src="../Assets/Designer(5).png" alt="Product Image">
                </li>
                <li class="inspect-item">
                    <img src="../Assets/Designer(5).png" alt="Product Image">
                </li>
            </ul>
        </section>
        <aside class ="inspect-aside">

            <img src ="../Assets/Designer(5).png" alt="Product Image">
        </aside>
        <aside class ="details-aside">
            <h1>Product Name</h1>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
        </aside>
    </div>
</template>

<script lang="ts" setup>
</script>

<style scoped>
.inspect-container {
    display: flex;
    gap: 2rem;
    padding: 2rem;
}

.inspect {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.inspect ul {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 0;
    margin: 0;
}

.inspect-item {
    list-style: none;
    border: 1px solid black;
}

.inspect-item img {
    width: 150px;
    height: auto;
    display: block;
}

.inspect-aside {
    flex: 1;
    border: 1px solid black;
    display: flex;
    align-items: flex-end;
}

.inspect-aside img {
    width: 100%;
    height: auto;
    max-height: 100%;
    object-fit: contain;
}

.details-aside {
    flex: 1;
}
</style>