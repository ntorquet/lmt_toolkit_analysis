<!--
Created by Nicolas Torquet at 17/05/2024
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->

<template>
  <v-card class="mt-4 mr-4" width="400">
      <v-card-title> Openfield preset</v-card-title>
      <v-card-text>
        <v-alert class="mb-2">
            This preset can be used to analyze openfield experiments with a single animal in the arena.<br />
            By default, the analysis will be done on the 15 first minutes of the experiment.<br />
            You can select a different duration but it will not exceed the experiment duration. The analysis starts at the beginning of the experiment.
          </v-alert>
          <v-text-field label="Duration in minutes"  type="number" v-model="durationComponent"></v-text-field>


      </v-card-text>
    <v-card-actions>
      <v-btn style="position: absolute; bottom: 0;" v-if="durationComponent!=''" @click="doAnalysis('openfieldPreset')" text="Analyze">
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn class="right-0" style="position: absolute; bottom: 0;" icon="mdi-information" @click="dialog=true"></v-btn>
    </v-card-actions>
  </v-card>


  <v-dialog v-model="dialog">
    <v-card class="mr-3 ml-3" prepend-icon="mdi-information" title="Openfield preset information">
      <v-card-text>
        <h2>Protocol</h2>
        Transparent cage of 50 x 50 cm with a new sawdust bottom.<br />
        The test mouse is placed in the cage and allowed to explore the environment for x minutes.<br />
        The LMT acquisition is started once the animal is placed in the cage.
      </v-card-text>

      <v-card-text>
        <h2>Analysis</h2>
      </v-card-text>

      <v-card-actions>
        <v-btn variant="outlined" @click="dialog=false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

</template>



<script>
export default {
  name: "OpenfieldPreset",
  props: {
    duration: Number
  },
  data() {
    return {
      durationComponent: Number,
      dialog: false,
    }
  },
  mounted() {
    this.durationComponent = this.duration
  }
}
</script>


<style scoped>

</style>