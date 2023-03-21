<!--
Created by Nicolas Torquet at 21/03/2023
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->
<template>
  <v-main>
    <v-container>
      <h1>Analysis</h1>
      <v-timeline direction="horizontal"  class="mt-10 mb-10">
        <v-timeline-item
          dot-color="pink"
          icon="mdi-download"
        >
          <v-card>
            <v-card-title>Select a SQLite file</v-card-title>
            <v-card-text>
              This file will be downloaded into the server to be process.
            </v-card-text>
          </v-card>
        </v-timeline-item>
        <v-timeline-item
          dot-color="green"
          icon="mdi-database-check"
        >
          <v-card>
            <v-card-title>Check the reliability</v-card-title>
            <v-card-text>
              Check detection, identity corrections and whenever available through the sensor temperature, humidity, light and ambient noise.
            </v-card-text>
          </v-card>
        </v-timeline-item>
        <v-timeline-item
          dot-color="purple"
          icon="mdi-database-edit"
        >
          <v-card>
            <v-card-title>Add animal information</v-card-title>
            <v-card-text>
              Add sex, treatment columns. Modify the name of each animal.
            </v-card-text>
          </v-card>
        </v-timeline-item>
        <v-timeline-item
          dot-color="red-lighten-1"
          icon="mdi-database-cog"
        >
          <v-card>
            <v-card-title>Rebuild the database</v-card-title>
            <v-card-text>This will create behavioral events into the event table of the SQLite file.</v-card-text>
          </v-card>
        </v-timeline-item>
        <v-timeline-item
          dot-color="amber-lighten-1"
          icon="mdi-cogs"
        >
          <v-card>
            <v-card-title>Configure the analysis</v-card-title>
            <v-card-text>
              Delimit a period to analyse, and more.
            </v-card-text>
          </v-card>
        </v-timeline-item>
        <v-timeline-item
          dot-color="cyan-lighten-1"
          icon="mdi-chart-line"
        >
          <v-card>
            <v-card-title>Analyse your data</v-card-title>
            <v-card-text>
              LMT-toolkit will process the analysis for you.
            </v-card-text>
          </v-card>
        </v-timeline-item>
        <v-timeline-item
          dot-color="indigo-lighten-2"
          icon="mdi-content-save"
        >
          <v-card>
            <v-card-title>Save your results</v-card-title>
            <v-card-text>
              Download your result into a CSV file.
            </v-card-text>
          </v-card>
        </v-timeline-item>
      </v-timeline>
    </v-container>
  </v-main>
</template>

<script>
export default {
  name: "analysis"
}
</script>

<style scoped>

</style>