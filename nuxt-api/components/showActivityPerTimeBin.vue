<!--
Created by Nicolas Torquet at 12/04/2023
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->



<template>
  <div>
    <v-alert type="warning" class="mb-5">
      Keep in mind that LMT-toolkit uses analysis scripts that are constantly updated and improved.<br />
      We do our best to verify the accuracy of the results. It is your responsibility to check data accuracy.<br />
    </v-alert>

    <v-card class="mb-5">
      <v-card-title>Activity per time bin</v-card-title>
      <v-card-text>
        <h3>Total distance travelled during the experiment:</h3>
        <v-list>
          <v-list-item v-for="animal in Object.keys(dataActivity.totalDistance)">
            <strong>{{ animal }}</strong>: {{ Math.ceil(dataActivity.totalDistance[animal]) }} cm
          </v-list-item>
        </v-list>
        <linePlotActivityPerTimeBin :title='"Activity per time bin (distance travelled every "+timeBin.toString()+" minutes) in centimeters"' :timeline="dataActivity.timeLine" :activity="dataActivity.activity"></linePlotActivityPerTimeBin>
      </v-card-text>
    </v-card>

    <v-btn>
      <v-icon icon="mdi-table-arrow-down"></v-icon>
      <download-csv
         :data = "dataToCSVActivity"
         :name = "name_csv+filename.split('.sqlite')[0]+'.csv'">
        Download Data as CSV file
        </download-csv>
    </v-btn>
  </div>
</template>

<script>
import JsonCSV from 'vue-json-csv'
import linePlotActivityPerTimeBin from "~/components/linePlotActivityPerTimeBin.vue";

export default {
  name: "showActivityPerTimeBin",
  props: {
    filename: String,
    dataActivity: Object,
    timeBin: Number,
  },
  components: {
    'downloadCsv': JsonCSV,
    linePlotActivityPerTimeBin,
  },
  data() {
     return {
       dataToCSVActivity: [],
       name_csv: 'LMT_v1_0_5-toolkit_v1-1_activitypertimebin_',
     }
  },
  methods: {
    convertJsonToCSVFormat() {
    //   let dataToConvert = this.data
    //   // console.log(this.data)
      for(let animal in this.dataActivity.results){
        this.dataToCSVActivity.push(this.dataActivity.results[animal])
      }
    },
  },
  mounted() {
    this.convertJsonToCSVFormat()
  },
  updated() {
    this.convertJsonToCSVFormat()
  }
}
</script>

<style scoped>

</style>