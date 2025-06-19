<!--
Created by Nicolas Torquet at 19/06/2025
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->

<script setup>
////////////////////////////////
// PROPS
////////////////////////////////
import {text} from "node:stream/consumers";

const props = defineProps({
  presetName: {
    type: String,
    required: true
  },
  presetDescription: {
    type: text,
    required: true
  }
});
</script>


<template>
  <v-card>
    <v-card-title>{{ props.presetName }}</v-card-title>
    <v-card-text>{{ props.presetDescription }}</v-card-text>
  </v-card>
</template>





<style scoped>

</style>