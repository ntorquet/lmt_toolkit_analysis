<!--
Created by Nicolas Torquet at 27/03/2023
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->
<template>
  <v-card color="white">
    <v-card-title>Sensors information - {{ selection }}</v-card-title>
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
  SubTitle
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
  SubTitle
)
export default {
  name: "linePlot",
  props: {
    selection: String,
    timeline: Array,
    temperature: Array,
    humidity: Array,
    sound: Array,
    lightvisible: Array,
    lightvisibleandir: Array,
    modalOpen: Boolean

  },
  data() {
    return {
      datasets: Object,
      myChart: Object,
      show: false
    }
  },
  methods: {
    renderChart(select) {
      const elem = document.getElementById('plot')
      if(typeof elem != 'undefined' && elem != null){
        const ctx = elem.getContext("2d")
        window.myChart = new Chart(ctx, {
          type: "line",
            data: {
              labels: this.timeline,
              datasets: this.datasets[select]
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
    this.datasets['temperature'] =
        [{
          label: 'temperature in °C',
          backgroundColor: ["rgba(246, 71, 71, 1)"],
          borderColor: ["rgba(246, 71, 71, 1)"],
          data: this.temperature,
          fill: false,
          tension: 0.1
        }]
    this.datasets['humidity'] =
        [{
          label: 'Humidity',
          backgroundColor: ["rgba(45, 85, 255, 1)"],
          borderColor: ["rgba(45, 85, 255, 1)"],
          data: this.humidity,
          fill: false,
          tension: 0.1
        }]
    this.datasets['sound'] =
        [{
          label: 'Sound',
          backgroundColor: ["rgba(165, 55, 253, 1)"],
          borderColor: ["rgba(165, 55, 253, 1)"],
          data: this.sound,
          fill: false,
          tension: 0.1
        }]
    this.datasets['light'] =
        [{
          label: 'Visible light',
          backgroundColor: ["rgba(63, 191, 63, 1)"],
          borderColor: ["rgba(63, 191, 63, 1)"],
          data: this.lightvisible,
          fill: false,
          tension: 0.1
        },
          {
          label: 'Visible and IR light',
          backgroundColor: ["rgba(255, 99, 132, 1)"],
          borderColor: ["rgba(255, 99, 132, 1)"],
          data: this.lightvisibleandir,
          fill: false,
          tension: 0.1
        },
        ]
    this.renderChart(this.selection)
  },
  watch: {
    selection: function(newSelection, oldSelection){
      // console.log('prop changed: '+newSelection)
      window.myChart.destroy()
      this.renderChart(newSelection)
    }
  }
}
</script>

<style scoped>

</style>