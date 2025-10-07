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
const props = defineProps({
  presetInfo: {
    type: Object,
    required: true
  }
});
</script>


<template>
  <v-dialog v-model="props.presetInfo.show" width="800">
    <v-card width="auto" prepend-icon="mdi-information" :title="props.presetInfo.presetName">
      <v-card-text>{{ props.presetInfo.presetDescription }}</v-card-text>
      <v-card-actions>
        <v-btn class="ms-auto" text="Ok" @click="props.presetInfo.show=false"></v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>





<style scoped>

</style>