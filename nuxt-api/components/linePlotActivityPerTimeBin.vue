<!--
Created by Nicolas Torquet at 03/07/2023
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
import {Chart,
  ArcElement,
  LineElement,
  BarElement,
  PointElement,
  BarController,
  BubbleController,
  DoughnutController,
  LineController,
  PieController,
  PolarAreaController,
  RadarController,
  ScatterController,
  CategoryScale,
  LinearScale,
  LogarithmicScale,
  RadialLinearScale,
  TimeScale,
  TimeSeriesScale,
  Decimation,
  Filler,
  Legend,
  Title,
  Tooltip,
  SubTitle,
  Colors
} from 'chart.js';

Chart.register(
  ArcElement,
  LineElement,
  BarElement,
  PointElement,
  BarController,
  BubbleController,
  DoughnutController,
  LineController,
  PieController,
  PolarAreaController,
  RadarController,
  ScatterController,
  CategoryScale,
  LinearScale,
  LogarithmicScale,
  RadialLinearScale,
  TimeScale,
  TimeSeriesScale,
  Decimation,
  Filler,
  Legend,
  Title,
  Tooltip,
  SubTitle,
  Colors
);

////////////////////////////////
// PROPS
////////////////////////////////
const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  timeline: {
    type: Array,
    required: true,
  },
  activity: {
    type: Object,
    required: true,
  }
});


////////////////////////////////
// DATA
////////////////////////////////
const datasets = ref(Object);
const myChart = ref(Object);
const colors = ref(["rgba(246, 71, 71, 1)"]);

////////////////////////////////
// METHODS
////////////////////////////////
const renderChart = () => {
  if (window.myChart) {
    window.myChart.destroy()
  }
  const elem = document.getElementById('plot')
  if(typeof elem != 'undefined' && elem != null){
    const ctx = elem.getContext("2d")
    window.myChart = new Chart(ctx, {
      type: "line",
        data: {
          labels: props.timeline,
          datasets: datasets['activity']
        },
        options: {
          responsive: false,
          elements: {
            point:{
              radius: 0
            }
          }
        }
    })
  }
  else{
    console.log("plot not define")
  }
};

////////////////////////////////
// ONMOUNTED
////////////////////////////////
onMounted(() => {
  datasets['activity'] = []
  for(let animal in props.activity){
    console.log(animal)
    datasets['activity'].push(
      {
        label: animal,
        data: props.activity[animal],
        fill: false,
        tension: 0.1
      }
    )
  }
})
onMounted(() => renderChart());

////////////////////////////////
// WATCHER
////////////////////////////////
watch(() => props.activity, (newValue, oldValue) => {
  console.log('timebin changed: ', newValue)
  datasets['activity'] = []
  for(let animal in props.activity){
    console.log(animal)
    datasets['activity'].push(
      {
        label: animal,
        data: props.activity[animal],
        fill: false,
        tension: 0.1
      }
    )
  }
  renderChart();
});

</script>

<template>
  <v-card color="white">
    <v-card-title>{{ title }}</v-card-title>
    <v-card-text>
      <canvas id="plot" height="500" width="1500"></canvas>
    </v-card-text>
  </v-card>
</template>


<style scoped>

</style>