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
import {ref, onMounted} from "vue";
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement} from 'chart.js';
ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement);


////////////////////////////////
// PROPS
////////////////////////////////
const props = defineProps({
  data: {
    type: Array,
    required: true,
  },
  labels: {
    type: Array,
    required: true,
  },
  chartId: {
    type: String,
    default: 'line-chart'
  },
  datasetIdKey: {
    type: String,
    default: 'label'
  },
  width: {
    type: Number,
    default: 400
  },
  height: {
    type: Number,
    default: 400
  },
  cssClasses: {
    default: '',
    type: String
  },
  styles: {
    type: Object,
    default: () => {}
  },
});

////////////////////////////////
// DATA
////////////////////////////////
const chartData = ref({
  labels: [],
  datasets: []
});
const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false
});


////////////////////////////////
// ONMOUNTED
////////////////////////////////
onMounted( () => {
  chartData.datasets = props.data
  chartData.labels = props.labels
});

</script>

<template>
  <Line
    :chart-options="chartOptions"
    :chart-data="chartData"
    :chart-id="chartId"
    :dataset-id-key="datasetIdKey"
    :css-classes="cssClasses"
    :styles="styles"
    :width="width"
    :height="height"
  />
</template>


<style scoped>

</style>