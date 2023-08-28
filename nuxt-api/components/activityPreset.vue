<!--
Created by Nicolas Torquet at 15/06/2023
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->

<template>
  <v-card>
      <v-card-title> Activity preset</v-card-title>
      <v-card-text>
        <v-alert class="mb-2">
            The activity preset will give you the activity (distance travelled in meters) by each animal. <br />
            By default, the analysis will be done on the total duration of the experiment.<br />
            You have to select a time bin to proceed.
          </v-alert>
          <v-text-field label="Time bin in minutes" v-model="timeBinComponent"></v-text-field>

          <v-btn v-if="timeBinComponent!=''" @click="doAnalysis('activityPreset')">
              <v-icon icon="mdi-arrow-right-bold"></v-icon>  Analyse
          </v-btn>
      </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "ActivityPreset",
  props: {
    timeBin: Number
  },
  data() {
    return {
      timeBinComponent: Number,
    }
  },
  mounted() {
    this.timeBinComponent = this.timeBin
  }
}
</script>

<style scoped>

</style>