<!--
Created by Nicolas Torquet at 12/04/2023
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->

<script setup>
////////////////////////////////
// IMPORT
////////////////////////////////
import { ref, onMounted, watch } from 'vue';
import linePlotActivityPerTimeBin from "~/components/linePlotActivityPerTimeBin.vue";


////////////////////////////////
// PROPS
////////////////////////////////
const props = defineProps({
  filename: {
    type: String,
    required: true,
  },
  dataActivity: {
    type: Object,
    required: true,
  },
  timeBin: {
    type: Number,
    required: true,
  }
});

////////////////////////////////
// DATA
////////////////////////////////
const dataToCSVActivity = ref([]);
const name_csv = ref('LMT_v1_0_7-toolkit_v2_activitypertimebin_');


////////////////////////////////
// METHODS
////////////////////////////////
const convertJsonToCSVFormat = () => {
  console.log("***** show activity *****");
  console.log("***** timebin *****");
  console.log(props.timeBin);
  console.log("***** results *****");
  console.log(props.dataActivity);
  //   let dataToConvert = this.data
  //   // console.log(this.data)
  dataToCSVActivity.value = [];
  for(let animal in props.dataActivity.results){
    dataToCSVActivity.value.push(props.dataActivity.results[animal]);
  }
};
const downloadCSV = (data, filename) => {
  const keys = [...new Set(data.flatMap(row => Object.keys(row)))];

  const csvContent = [
    keys.map(key => key.includes(',') ? `"${key}"` : key).join(','),
    ...data.map(row =>
      keys.map(key => {
        const value = row[key] !== undefined ? row[key] : '';

        return value;
      }).join(',')
    )
  ].join('\n');

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

////////////////////////////////
// ONMOUNTED
////////////////////////////////
onMounted(() => convertJsonToCSVFormat());

////////////////////////////////
// WATCHER
////////////////////////////////

watch(() => props.timeBin, (newValue, oldValue) => {
  console.log('timebin changed: ', newValue)
  convertJsonToCSVFormat();
});

watch(() => props.dataActivity, (newValue, oldValue) => {
  console.log('dataActivity changed: ', newValue)
  convertJsonToCSVFormat();
});

</script>

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

    <v-btn @click="downloadCSV(dataToCSVActivity, name_csv + filename.split('.sqlite')[0] + '.csv')">
      <v-icon icon="mdi-table-arrow-down"></v-icon>
        Download Data as CSV file
    </v-btn>
  </div>
</template>

<style scoped>

</style>