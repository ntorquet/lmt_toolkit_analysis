<!--
Created by Nicolas Torquet at 20/03/2023
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->
<template>
  <v-main>
    <v-container>
      <v-row>
        <v-col>
          <v-card>
            <v-card-title>Welcome to LMT-toolkit</v-card-title>

            <v-card-text>
            <p><strong><nuxt-link to="https://livemousetracker.org/" target="_blank">Live Mouse Tracker (LMT)</nuxt-link></strong> is a powerful tool to investigate the behavior of mice and in particular their social behavior.<br />
              <strong>LMT</strong> provides tracking data in a database as a SQLite file. Exploiting them requires computer skills.<br />
              <strong>LMT-toolkit</strong> was created to help LMT users to explore their own data autonomously. <strong>LMT-toolkit</strong>
              allows to check the reliability of the LMT experiments and extract behavioral data.<br />
              The data extracted during the processing can be downloaded into a CSV file for each experiment.<br />
              In the future, <strong>LMT-toolkit</strong> will also offer the possibility to organise and manage LMT experiments for each project.
            </p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>


      <v-row>
        <v-col>
          <v-card>
            <v-card-title><v-icon icon="mdi-check-decagram"></v-icon> Reliability</v-card-title>
            <v-card-text>
              LMT-toolkit checks the reliability of your experiments:
              rate of detection, identity corrections and whenever available through the sensor temperature, humidity, light and ambient noise.
            </v-card-text>
          </v-card>
        </v-col>
        <v-col>
          <v-card>
            <v-card-title><v-icon icon="mdi-chart-line"></v-icon> Analysis</v-card-title>
            <v-card-text>
              LMT-toolkit processes LMT experiments automatically, using the Python code
              available on Github (<nuxt-link to="https://github.com/fdechaumont/lmt-analysis" target="_blank"><v-icon icon="mdi-github"></v-icon> https://github.com/fdechaumont/lmt-analysis</nuxt-link>).<br />
              LMT-toolkit extracts the total duration, the number of occurrences and the mean duration of each occurrence
              for the behaviors described <nuxt-link to="https://livemousetracker.org/" target="_blank">here</nuxt-link>.<br />
              Please visit the version history page for information about the code used.
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row align="center">
        <v-col>
          <v-card>
            <v-card-title class="text-center">
              <strong>Try now !</strong>
            </v-card-title>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
export default {
  name: "index"
}
</script>

<style scoped>

</style>