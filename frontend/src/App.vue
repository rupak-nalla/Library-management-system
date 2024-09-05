<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header>
    
    <div class="wrapper">

      <nav>
        <RouterLink to="/" style="color: white; text-decoration: none;padding-right: 20px;font-size: 20px;">Library System</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
nav{
  padding: 10px;
  background-color: rgb(18, 18, 18);
  
  font-family: 'CustomFont';
}
@font-face {
    font-family: 'CustomFont';
    src: url('../assets/font/ClashDisplay_Complete/Fonts/TTF/ClashDisplay-Variable.ttf') format('truetype'); /* Adjust the path as necessary */
}

</style>
