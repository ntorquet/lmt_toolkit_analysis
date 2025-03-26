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
      <h1>Version history</h1>
      <v-card class="mt-10">
        <v-card-title><v-icon icon="mdi-alert-box"></v-icon> Why this page is important</v-card-title>
        <v-card-text>
          LMT-toolkit uses the LMT-analysis code provided on GitHub <nuxt-link to="https://github.com/fdechaumont/lmt-analysis" target="_blank">here</nuxt-link>.<br />
          This code can changed to improve analysis or to correct bugs. As a <strong>LMT-toolkit</strong> user, you should know if you can compare data from different version of the code.<br />
          Some important changes will impact the results. This page gives you an history of all changes so that you know if a new analysis is needed.
        </v-card-text>
      </v-card>
      <v-table class="mt-10 mb-10">
        <thead>
          <tr>
            <th>Version</th>
            <th>Date</th>
            <th>LMT-toolkit Changes / Notes</th>
            <th>LMT-analysis Changes / Notes</th>
            <th>LMT-analysis release</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="version in versions.reverse()">
            <td>
              <a :href="version.lmt_toolkit_version_link" target="_blank">
                <v-chip color="black"><v-icon icon="mdi-github" class="mr-1"></v-icon> <strong>{{ version.lmt_toolkit_version }}</strong></v-chip></a>
            </td>
            <td>{{ version.lmt_toolkit_version_date }}</td>
            <td>
              {{ version.lmt_toolkit_version_changes }}
            </td>
            <td>
              {{ version.lmt_analysis_version_changes }}
            </td>
            <td><a :href="version.lmt_analysis_version_link" target="_blank"><v-chip color="primary"><v-icon icon="mdi-github" class="mr-1"></v-icon> <strong>{{ version.lmt_analysis_version }}</strong></v-chip></a></td>
          </tr>
        </tbody>
      </v-table>
    </v-container>
  </v-main>
</template>

<script>
import axios from "axios";
export default {
  name: "versions",
  data:function (){
		return{
      versions: [],
    }
  },
  methods: {
    getVersions() {
      this.files = []
      this.filesItems = []
      axios.get(`http://127.0.0.1:8000/api/versions`)
          .then(response => {
            this.versions = response.data
            this.organizeFiles()
          })
          .catch(error => {
            console.log(JSON.stringify(error))
          })
    },
  },
  mounted() {
    this.getVersions()
  }
}
</script>

<style scoped>

</style>