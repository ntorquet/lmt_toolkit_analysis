<!--
Created by Nicolas Torquet at 27/03/2023
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
  SubTitle
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
  SubTitle
);


////////////////////////////////
// PROPS
////////////////////////////////
const props = defineProps({
  selection: {
    type: String,
    required: true
  },
  timeline: {
    type: Array,
    required: true
  },
  temperature: {
    type: Array,
    required: true
  },
  humidity: {
    type: Array,
    required: true
  },
  sound: {
    type: Array,
    required: true
  },
  lightvisible: {
    type: Array,
    required: true
  },
  lightvisibleandir: {
    type: Array,
    required: true
  }
});


////////////////////////////////
// DATA
////////////////////////////////
const datasets = ref(Object);


////////////////////////////////
// METHODS
////////////////////////////////
const renderChart = (select) => {
  if (window.myChart) {
    window.myChart.destroy()
  }
  const elem = document.getElementById('plot');
  if(typeof elem != 'undefined' && elem != null){
    const ctx = elem.getContext("2d");
    window.myChart = new Chart(ctx, {
      type: "line",
        data: {
          labels: props.timeline,
          datasets: datasets[select]
        },
        options: {
          elements: {
            point:{
              radius: 0
            }
          }
        }
    });
  }
  else{
    console.log("plot not define");
  }
}


////////////////////////////////
// ONMOUNTED
////////////////////////////////
onMounted(() => {
  datasets['temperature'] =
    [{
      label: 'temperature in °C',
      backgroundColor: ["rgba(246, 71, 71, 1)"],
      borderColor: ["rgba(246, 71, 71, 1)"],
      data: props.temperature,
      fill: false,
      tension: 0.1
    }]
  datasets['humidity'] =
    [{
      label: 'Humidity',
      backgroundColor: ["rgba(45, 85, 255, 1)"],
      borderColor: ["rgba(45, 85, 255, 1)"],
      data: props.humidity,
      fill: false,
      tension: 0.1
    }]
  datasets['sound'] =
    [{
      label: 'Sound',
      backgroundColor: ["rgba(165, 55, 253, 1)"],
      borderColor: ["rgba(165, 55, 253, 1)"],
      data: props.sound,
      fill: false,
      tension: 0.1
    }]
  datasets['light'] =
    [{
      label: 'Visible light',
      backgroundColor: ["rgba(63, 191, 63, 1)"],
      borderColor: ["rgba(63, 191, 63, 1)"],
      data: props.lightvisible,
      fill: false,
      tension: 0.1
    },
      {
      label: 'Visible and IR light',
      backgroundColor: ["rgba(255, 99, 132, 1)"],
      borderColor: ["rgba(255, 99, 132, 1)"],
      data: props.lightvisibleandir,
      fill: false,
      tension: 0.1
    },
    ]
})
onMounted(() => renderChart(props.selection));


</script>


<template>
  <v-card color="white">
    <v-card-title>Sensors information - {{ props.selection }}</v-card-title>
    <v-card-text>
      <canvas id="plot" style="width: 50%; height: 20vh"></canvas>
    </v-card-text>
  </v-card>
</template>


<style scoped>

</style>