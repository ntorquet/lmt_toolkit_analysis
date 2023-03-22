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
          <v-card
            variant="outlined"
          >
            <v-card-title>Welcome to LMT-toolkit</v-card-title>

            <v-card-text>
            <strong><nuxt-link to="https://livemousetracker.org/" target="_blank">Live Mouse Tracker (LMT)</nuxt-link></strong> is a powerful tool to investigate the behavior of mice and in particular their social behavior.<br />
              <strong>LMT</strong> provides tracking data in a database as a SQLite file. Exploiting them requires computer skills.<br />
              <strong>LMT-toolkit</strong> was created to help LMT users to explore their own data autonomously. <strong>LMT-toolkit</strong>
              allows to check the reliability of the LMT experiments and extract behavioral data.<br />
              The data extracted during the processing can be downloaded into a CSV file for each experiment.<br />
              In the future, <strong>LMT-toolkit</strong> will also offer the possibility to organise and manage LMT experiments for each project.
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row>
        <v-col>
          <v-timeline direction="horizontal"  class="mt-10 mb-10">
            <v-timeline-item v-for="(item, key) in timelineItems"
              :dot-color="item.color"
              :icon="item.icon"
            >
              <v-card>
                <v-card-title>{{ item.title }}</v-card-title>
                <v-card-text
                   class="text-center"
                >
                  <v-btn
                    :color="item.color"
                    variant="outlined"
                    @click="showDetails(key)"
                  >
                    See details
                  </v-btn>
                </v-card-text>
              </v-card>
            </v-timeline-item>
          </v-timeline>
        </v-col>
      </v-row>


    </v-container>
  </v-main>
  <show-details :data="dataforDetails" v-model="showDetailsInModal"></show-details>
</template>



<script>
import showDetails from "~/components/showDetails.vue";
export default {
  name: "index",
  components: {
    showDetails
  },
  data () {
    return {
      timelineItems: {
        selectSqlite: {
          title: 'Select a SQLite file',
          icon: 'mdi-download',
          color: 'pink',
          text: 'This file will be downloaded into the server to be process.'
        },
        reliability: {
          title: 'Check the reliability',
          icon: 'mdi-database-check',
          color: 'green',
          text: 'Check detection, identity corrections and whenever available through the sensor temperature, humidity, light and ambient noise.'
        },
        animalInfo: {
          title: 'Add animal information',
          icon: 'mdi-database-edit',
          color: 'purple',
          text: 'Add sex, treatment columns. Modify the name of each animal.'
        },
        rebuild: {
          title: 'Rebuild the database',
          icon: 'mdi-database-cog',
          color: 'red-lighten-1',
          text: 'This will create behavioral events into the event table of the SQLite file.'
        },
        configAnalysis: {
          title: 'Configure the analysis',
          icon: 'mdi-cogs',
          color: 'amber-lighten-1',
          text: 'Delimit a period to analyse, and more.'
        },
        analysis: {
          title: 'Analyse your data',
          icon: 'mdi-chart-line',
          color: 'cyan-lighten-1',
          text: 'LMT-toolkit processes LMT experiments automatically for you!'
        },
        save: {
          title: 'Save your results',
          icon: 'mdi-content-save',
          color: 'indigo-lighten-2',
          text: 'Download your result into a CSV file.'
        }
      },
      showDetailsInModal: false,
      dataforDetails: {}
    }
  },
  methods: {
    showDetails(toShow) {
      this.dataforDetails = this.timelineItems[toShow]
      this.showDetailsInModal = !this.showDetailsInModal
    }
  },
}
</script>

<style scoped>

</style>