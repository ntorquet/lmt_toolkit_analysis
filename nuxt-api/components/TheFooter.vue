<!--
Created by Nicolas Torquet at 20/03/2023
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->

<script setup>
////////////////////////////////
// IMPORT
////////////////////////////////
import axios from "axios";
import {ref, onMounted} from "vue";


////////////////////////////////
// DATA
////////////////////////////////
const versions = ref([]);
const lastVersion = ref("");

////////////////////////////////
// METHODS
////////////////////////////////
const getVersions = () => {
  console.log("getVersion")
  axios.get(`http://127.0.0.1:8000/api/versions/`)
      .then(response => {
        versions.value = response.data;
        lastVersion.value = versions.value[versions.value.length-1]["lmt_toolkit_version"];
      })
      .catch(error => {
        console.log(JSON.stringify(error));
      })
}

////////////////////////////////
// ONMOUNTED
////////////////////////////////
onMounted(() => getVersions());

</script>

<template>
  <v-footer color="black">
    <div class="px-4 py-2 bg-black text-center w-100">
      <v-row>
        <v-col>LMT-toolkit {{ lastVersion }} - Copyright © CNRS - INSERM - UNISTRA - ICS - IGBMC 2022</v-col>
      </v-row>
      <v-row>
        <v-col>
          <nuxt-link to="https://github.com/ntorquet/lmt_toolkit_analysis" target="_blank" class="nuxt-link"><v-icon icon="mdi-github"></v-icon> GitHub</nuxt-link>
        </v-col>
      </v-row>
    </div>
  </v-footer>
</template>


<style scoped>
.nuxt-link{
  color: white;
  text-decoration: None;
}

.nuxt-link:hover{
  text-decoration: underline;
}
</style>