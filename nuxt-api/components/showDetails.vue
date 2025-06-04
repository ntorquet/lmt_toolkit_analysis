<!--
Created by Nicolas Torquet at 22/03/2023
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
const props = defineProps({
  data: {
    type: Object,
    required: true,
  }
});

</script>

<template>
  <v-dialog
    width="800"
  >
    <v-card>
      <v-card-title><v-icon :icon="props.data.icon" :color="props.data.color"></v-icon> {{ props.data.title }}</v-card-title>
      <v-divider :color="props.data.color" thickness="2" class="border-opacity-100"></v-divider>
      <v-card-text>
        {{ props.data.text }}
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<style scoped>

</style>