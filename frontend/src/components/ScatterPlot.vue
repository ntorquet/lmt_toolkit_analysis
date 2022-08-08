<template>
  <b-modal size="lg" :title="'Plot - '+selection" ok-only>
    <canvas id="plot" style="width: 50%; height: 20vh"></canvas>
  </b-modal>
</template>

<script>
import {
  Chart,
  Scatter,
  ArcElement,
  PieController,
  TimeScale,
  TimeSeriesScale,
  Filler,
  Legend,
  Title,
  Tooltip,
  SubTitle,
  LineElement,
  BarElement,
  PointElement,
  BarController,
  BubbleController,
  DoughnutController,
  LineController,
  PolarAreaController,
  RadarController,
  ScatterController,
  CategoryScale,
  LinearScale,
  LogarithmicScale,
  RadialLinearScale, Decimation
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
  name: "ScatterPlot",
  props: {
    selection: String,
    x_data: Array,
    y_data: Array,
  },
  data() {
    return {
      datasets: Object,
      myChart: Object,
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
    this.renderChart(this.selection)
  },
}
</script>

<style scoped>

</style>