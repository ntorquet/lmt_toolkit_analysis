<!--
Created by Nicolas Torquet at 22/03/2023
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->
<template>
  <v-dialog
    width="800"
  >
    <v-card>
      <v-card-title><v-icon :icon="data.icon" :color="data.color"></v-icon> {{ data.title }}</v-card-title>
      <v-divider :color="data.color" thickness="2" class="border-opacity-100"></v-divider>
      <v-card-text>
        {{ data.text }}
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "showDetails",
  props: {
    data: Object,
    // showDetailsInModal: Boolean
  },
  data () {
    return {
      dialog: false,
    }
  },
}
</script>

<style scoped>

</style>