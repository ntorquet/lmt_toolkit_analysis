<!--
Created by Nicolas Torquet at 20/03/2023
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->
<template>
  <div class="page-wrapper">
    <TheHeader />
    <div  class="content">
      <slot />
    </div>
    <TheFooter />
  </div>
</template>
<script setup lang="ts">
</script>

<style scoped>
.page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.content {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  height: 100%;
}
</style>