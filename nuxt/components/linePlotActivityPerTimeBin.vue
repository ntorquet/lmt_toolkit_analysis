<!--
Created by Nicolas Torquet at 03/07/2023
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->
<template>
  <v-card color="white">
    <v-card-title>{{ title }}</v-card-title>
    <v-card-text>
      <canvas id="plot" style="width: 50%; height: 20vh"></canvas>
    </v-card-text>
  </v-card>
</template>

<script>
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
} from 'chart.js'

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
)
export default {
  name: "linePlot",
  props: {
    title: String,
    timeline: Array,
    activity: Object,

  },
  data() {
    return {
      datasets: Object,
      myChart: Object,
      colors: ["rgba(246, 71, 71, 1)" ]
    }
  },
  methods: {
    renderChart() {
      const elem = document.getElementById('plot')
      if(typeof elem != 'undefined' && elem != null){
        const ctx = elem.getContext("2d")
        window.myChart = new Chart(ctx, {
          type: "line",
            data: {
              labels: this.timeline,
              datasets: this.datasets['activity']
            },
            options: {
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
    }
  },
  mounted() {
    this.datasets['activity'] = []
    for(let animal in this.activity){
      console.log(animal)
      this.datasets['activity'].push(
        {
          label: animal,
          data: this.activity[animal],
          fill: false,
          tension: 0.1
        }
      )
    }
    this.renderChart()
  },
}
</script>

<style scoped>

</style>