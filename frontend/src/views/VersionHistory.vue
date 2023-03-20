<!--
Created by Nicolas Torquet at 12/07/2022
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->
<template>
  <h1 class="title">Version history</h1>
  <b-card title="Why this page is important" class="card_info">
    LMT-toolkit uses the LMT-analysis code provided on GitHub <a href="https://github.com/fdechaumont/lmt-analysis" target="_blank">here</a>.<br />
    This code can changed to improve analysis or to correct bugs. As a <strong>LMT-toolkit</strong> user, you should know if you can compare data from different version of the code.<br />
    Some important changes will impact the results. This page gives you an history of all changes so that you know if a new analysis is needed.
  </b-card>
  <br />
  <b-container>
    <b-table-simple hover small caption-top responsive>
      <b-thead>
        <b-tr>
          <b-th style="width: 5%">Version</b-th>
          <b-th style="width: 10%">Date</b-th>
          <b-th>LMT-toolkit Changes / Notes</b-th>
          <b-th>LMT-analysis Changes / Notes</b-th>
          <b-th>LMT-analysis release</b-th>
        </b-tr>
      </b-thead>
      <b-tbody>
        <b-tr v-for="version in versions.reverse()">
          <b-td valign="middle">
            <a href="version.lmt_toolkit_version_link" target="_blank">
            <b-badge variant="dark" pill><b-icon-github></b-icon-github> {{ version.lmt_toolkit_version }}</b-badge></a>
          </b-td>
          <b-td valign="middle">{{ version.lmt_toolkit_version_date }}</b-td>
          <b-td>
            {{ version.lmt_toolkit_version_changes }}
          </b-td>
          <b-td>
            {{ version.lmt_analysis_version_changes }}
          </b-td>
          <b-td valign="middle"><a :href="version.lmt_analysis_version_link" target="_blank"><b-badge variant="secondary" pill><b-icon-github></b-icon-github> {{ version.lmt_analysis_version }}</b-badge></a></b-td>
        </b-tr>
      </b-tbody>
    </b-table-simple>

  </b-container>
</template>

<script>
import {BIconGithub} from "bootstrap-icons-vue"
import axios from "axios";
export default {
  name: "VersionHistory",
  components: {
    'BIconGithub': BIconGithub,
  },
  data:function (){
		return{
      versions: [],
    }
  },
  methods: {
    getVersions() {
      this.files = []
      this.filesItems = []
      axios.get(`api/v1/versions`)
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
.card_info {
  margin: auto;
  width: 100em;
}

b-table-simple {
  margin: 2.5%;
  width: 95%;
}


</style>