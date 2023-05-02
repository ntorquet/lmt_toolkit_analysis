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
      <h1>Documentation</h1>
      <v-alert
          color="#2A3B4D"
          theme="dark"
          icon="mdi-alert-box"
          prominent
           class="mt-10"
      >
          You can find these descriptions <nuxt-link to="https://livemousetracker.org/" class="nuxt-link" target="_blank">here</nuxt-link> and in the <nuxt-link to="https://www.nature.com/articles/s41551-019-0396-1.epdf?shared_access_token=8wpLBUUytAaGAtXL96vwIdRgN0jAjWel9jnR3ZoTv0MWp3GqbF86Gf14i30j-gtSG2ayVLmU-s57ZbhM2WJjw18inKlRYt31Cg_hLJbPCqlKdjWBImyT1OrH5tewfPqUthmWceoct6RVAL_Vt8H-Og%3D%3D" class="nuxt-link" target="_blank">LMT publication</nuxt-link>.<br />
          LMT-toolkit uses the LMT-analysis code provided on GitHub <a href="https://github.com/fdechaumont/lmt-analysis" class="nuxt-link" target="_blank">here</a>.
      </v-alert>

      <v-table class="mt-10 mb-10">
        <thead>
          <tr>
            <th>Name</th>
            <th>Representation</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="doc in documentation">
            <td>{{ doc.name }}</td>
            <td><span v-if="doc.representation"><img :src="doc.representation" :alt="doc.name" /></span></td>
            <td>{{ doc.description }}</td>
          </tr>
        </tbody>
      </v-table>

      <v-alert
          color="#2A3B4D"
          theme="dark"
          icon="mdi-rodent"
          prominent
           class="mt-10"
      >
        For social events, we computed the variables either in general or separately according to the identity of the interacting individual. These behaviours are not exclusive: one animal can be involved in several of them simultaneously.
      </v-alert>

    </v-container>
  </v-main>
</template>

<script>
import axios from "axios";
export default {
  name: "documentation",
  data:function (){
		return{
      documentation: [],
    }
  },
  methods: {
    getEventDocumentation() {
      axios.get(`http://127.0.0.1:8000/api/v1/eventDocumentation`)
          .then(response => {
            this.documentation = response.data
          })
          .catch(error => {
            console.log(JSON.stringify(error))
          })
    },
  },
  mounted() {
    this.getEventDocumentation()
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