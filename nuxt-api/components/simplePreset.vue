<!--
Created by Nicolas Torquet at 15/06/2023
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->

<script setup>

</script>

<template>
  <v-card>
      <v-card-title> Simple preset</v-card-title>
      <v-card-text>
        <v-alert class="mb-2">
            By default, the analysis will be done on the total duration of the experiment.<br />
            You can limit the analysis by filling in the fields below.
          </v-alert>
          <v-text-field label="Start time (computed from the launching of the recording)" v-model="minT"></v-text-field>
          <v-select
                  label="Unit"
                  v-model="unitMinT"
                  :items="unitStartEnd"
                  item-title="text"
                  item-value="value"
          ></v-select>
          <v-text-field label="End time (computed from the launching of the recording)" v-model="maxT"></v-text-field>
          <v-select
                  label="Unit"
                  v-model="unitMaxT"
                  :items="unitStartEnd"
                  item-title="text"
                  item-value="value"
          ></v-select>

          <v-alert type="warning" v-if="durationChecker!=''" >
            {{ durationChecker }}
          </v-alert>
          <v-btn v-else @click="doAnalysis('simplePreset')">
              <v-icon icon="mdi-arrow-right-bold"></v-icon>  Analyse
          </v-btn>
      </v-card-text>
  </v-card>
</template>


<style scoped>

</style>