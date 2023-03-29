<!--
Created by Nicolas Torquet at 20/03/2023
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->
<template>
  <v-app-bar color="black">
    <v-app-bar-title><nuxt-link to="/" class="nuxt-link"><strong>LMT-toolkit</strong></nuxt-link></v-app-bar-title>
    <v-row>
      <v-col><a href="/reliability" class="nuxt-link">Reliability</a></v-col>
      <v-col><a href="/analysis" class="nuxt-link">Analysis</a></v-col>
      <v-col><nuxt-link to="/files" class="nuxt-link">Files list</nuxt-link></v-col>
      <v-col><nuxt-link to="/documentation" target="_blank" class="nuxt-link">Documentation</nuxt-link></v-col>
      <v-col><nuxt-link to="/versions" class="nuxt-link">Versions</nuxt-link></v-col>
    </v-row>

  </v-app-bar>
</template>

<script>
export default {
  name: "TheHeader",
}
</script>

<style scoped>
.nuxt-link{
  color: white;
  text-decoration: None;
}

.nuxt-link:hover{
  text-decoration: underline;
}

</style>