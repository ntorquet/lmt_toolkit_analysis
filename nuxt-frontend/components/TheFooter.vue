<!--
Created by Nicolas Torquet at 20/03/2023
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->
<template>
  <v-footer color="black" height="100em">
    <div class="px-4 py-2 bg-black text-center w-100">
      <v-row>
        <v-col>LMT-toolkit v0.2 - Copyright © CNRS - INSERM - UNISTRA - ICS - IGBMC 2022</v-col>
      </v-row>
      <v-row>
        <v-col>
          <nuxt-link to="https://github.com/ntorquet/lmt_toolkit_analysis" target="_blank" class="nuxt-link"><v-icon icon="mdi-github"></v-icon> GitHub</nuxt-link>
        </v-col>
      </v-row>
    </div>
  </v-footer>
</template>

<script>
import axios from "axios";
export default {
  name: "TheFooter",
  data:function (){
		return{
      versions: [],
    }
  },
  methods: {
    getVersions() {
      this.files = []
      this.filesItems = []
      axios.get(`http://127.0.0.1:8000/api/v1/versions`)
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
.nuxt-link{
  color: white;
  text-decoration: None;
}

.nuxt-link:hover{
  text-decoration: underline;
}
</style>