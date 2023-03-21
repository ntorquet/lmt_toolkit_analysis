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
    <v-app-bar-title><strong>LMT-toolkit</strong></v-app-bar-title>
    <v-row>
      <v-col><nuxt-link to="/reliability" class="nuxt-link">Reliability</nuxt-link></v-col>
      <v-col>Analysis</v-col>
      <v-col><nuxt-link to="/files" class="nuxt-link">Files list</nuxt-link></v-col>
      <v-col><nuxt-link to="/documentation" class="nuxt-link">Documentation</nuxt-link></v-col>
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