<!--
Created by Nicolas Torquet at 27/03/2023
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->
<template>
  <v-sheet width="850">
    <h2>Reliability information</h2>
    <v-card class="mt-8">
      <v-card-title><v-icon icon="mdi-information"></v-icon> Global information</v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item><strong>File name:</strong> {{ filename }}</v-list-item>
          <v-list-item><strong>Start time:</strong> {{ data.startXp }}</v-list-item>
          <v-list-item><strong>End time:</strong> {{ data.endXp }}</v-list-item>
        </v-list>
      </v-card-text>
    </v-card>

    <v-card class="mt-8">
      <v-card-title><v-icon icon="mdi-rodent"></v-icon> Animals</v-card-title>
      <v-card-text>
        <v-table>
          <thead>
            <tr>
              <th>Animal ID</th>
              <th>Name</th>
              <th>Tag</th>
              <th>Genotype</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="mice in data.mouse">
              <td>{{ mice.animalId }}</td>
              <td>{{ mice.name_subject }}</td>
              <td>{{ mice.tag_subject }}</td>
              <td>{{ mice.genotype }}</td>
            </tr>
          </tbody>
        </v-table>
      </v-card-text>
    </v-card>

    <v-card class="mt-8">
      <v-card-title>Sensors information</v-card-title>
      <v-card-text v-if="data.sensors!='no sensors'">
        <v-row>
          <v-col><v-btn @click="showTemp">Temperature</v-btn></v-col>
          <v-col><v-btn @click="showHumidity">Humidity</v-btn></v-col>
          <v-col><v-btn @click="showSound">Sound</v-btn></v-col>
          <v-col><v-btn @click="showLight">Light</v-btn></v-col>
        </v-row>

        <br />
        <v-alert show :color="tempColor">
          <h4>Temperature</h4>
          <p>{{ data.highTempInformation }}</p>
          <p>{{ data.lowTempInformation }}</p>
        </v-alert>
      </v-card-text>
      <v-card-text v-else>
        No sensors
      </v-card-text>
    </v-card>

    <v-card class="mt-8">
      <v-card-title>Frames and duration information</v-card-title>
      <v-card-text>
        <v-table>
          <thead>
          <tr>
            <th></th>
            <th>Based on the start and end dates</th>
            <th>Based on the recorded frames</th>
            <th>Frames dropped</th>
          </tr>
          </thead>
          <tbody>
          <tr>
            <td>Number of frames</td>
            <td>{{ data.theoricalNumberOfFrame }}</td>
            <td>{{ data.nbFramesRecorded }}</td>
            <td>{{ data.nbOmittedFrames }} frames / {{ data.percentageOfOmittedFrames }} %</td>
          </tr>
          <tr>
            <td>Duration in seconds</td>
            <td>{{ data.realDurationInSeconds }}</td>
            <td>{{ data.nbFramesRecordedInSeconds }}</td>
            <td>{{ data.nbOmittedSeconds }}</td>
          </tr>
          <tr>
            <td>Duration in minutes</td>
            <td>{{ data.realDurationInMinutes }}</td>
            <td>{{ data.nbFramesRecordedInMinutes }}</td>
            <td>{{ data.nbOmittedMinutes }}</td>
          </tr>
          <tr>
            <td>Duration in hours</td>
            <td>{{ data.realDurationInHours }}</td>
            <td>{{ data.nbFramesRecordedInHours }}</td>
            <td>{{ data.nbOmittedHours }}</td>
          </tr>
          <tr>
            <td>Duration in days</td>
            <td>{{ data.realDurationInDays }}</td>
            <td>{{ data.nbFramesRecordedInDays }}</td>
            <td>{{ data.nbOmittedDays }}</td>
          </tr>
          </tbody>
        </v-table>
        <v-alert :color="frameColor">
          <h4 class="alert-heading">
            <v-icon icon="mdi-check-bold" v-if="frameColor=='success'"></v-icon>
            <v-icon icon="mdi-alert" v-if="frameColor=='warning'"></v-icon>
            <v-icon icon="mdi-alert-box" v-if="frameColor=='danger'"></v-icon>
            Experiment reliability based on dropped frames</h4>
          <p>{{ data.omissionInformation }}</p>
        </v-alert>
      </v-card-text>
    </v-card>

    <v-card class="mt-8">
      <v-card-title>About animal detections</v-card-title>
      <v-card-text>
        <v-table class="table">
          <thead>
          <tr>
            <th>Animal ID</th>
            <th>Number of detection</th>
            <th>% of detections based on recorded frames</th>
            <th>% of detections based on expected number of frames</th>
            <th><v-icon icon="mdi-alert-circle"></v-icon></th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="detection in data.aboutDetections">
            <td>{{ detection.animalId }}</td>
            <td>{{ detection.nbDetection }}</td>
            <td :class="'table-'+detection.detectionPercentRecordedFramesColor">{{ detection.detectionPercentRecordedFrames }} %</td>
            <td :class="'table-'+detection.detectionPercentTheoricalFramesColor">{{ detection.detectionPercentTheoricalFrames }} %</td>
            <td :class="'table-'+detection.messageDetectionFrameColor">
              <v-icon icon="mdi-check-bold" v-if="detection.messageDetectionFramesIcon=='check icon'"></v-icon>
              <v-icon icon="mdi-alert" v-if="detection.messageDetectionFramesIcon=='hotjar icon'"></v-icon>
            </td>
          </tr>
          </tbody>
        </v-table>
      </v-card-text>
    </v-card>

    <v-card class="mt-8">
      <v-card-title>About RFID detections</v-card-title>
      <v-card-text>
        <v-table class="table" v-if="data.rfidDetection">
          <thead>
          <tr>
            <th>Animal ID</th>
            <th>Number of RFID detections</th>
            <th>RFID match</th>
            <th>RFID mismatch</th>
            <th class="text-center">Proportion of mismatch</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(item, index) in data.about_rfid_detections">
            <td>{{ item.animalId }}</td>
            <td>{{ item.nbRFIDdetection }}</td>
            <td>{{ item.nbRFIDmatchdetection }}</td>
            <td>{{ item.nbRFIDmismatchdetection }}</td>
            <td><canvas :id="'mismatchProportion_'+index" style="width: 50%; height: 20vh"></canvas></td>
          </tr>
          </tbody>
        </v-table>
      </v-card-text>
    </v-card>


    <v-dialog v-model="modalOpen" width="800">
      <linePlot :selection="selection" :timeline="data.timeline" :temperature="data.temperature"
        :humidity="data.humidity" :sound="data.sound" :lightvisible="data.lightvisible" :lightvisibleandir="data.lightvisibleandir"></linePlot>
    </v-dialog>
  </v-sheet>

</template>

<script>
import linePlot from "@/components/linePlot"
import {
  Chart,
  ArcElement,
  PieController,
  TimeScale,
  TimeSeriesScale,
  Filler,
  Legend,
  Title,
  Tooltip,
  SubTitle
} from 'chart.js'
Chart.register(
  ArcElement,
  PieController,
  TimeScale,
  TimeSeriesScale,
  Filler,
  Legend,
  Title,
  Tooltip,
  SubTitle
)
export default {
  name: "showReliability",
  components: {
    linePlot,
  },
  props: {
    filename: String,
    data: Object,
  },
  data: function() {
    return{
      modalOpen: false,
      selection: 'temperature',
      tempColor: '',
      frameColor: '',
      detections: [],
    }
  },
  mounted () {
    if(this.data.rfidDetection) {
      for (let i=1; i<=Object.keys(this.data.about_rfid_detections).length; i++) {
        const ctx = document.getElementById('mismatchProportion_' + i).getContext("2d")
        const myChart = new Chart(ctx, {
          type: "pie",
          data: {
            labels: ['Match', 'Mismatch'],
            datasets: [
              {
                backgroundColor: ["rgba(75, 192, 192, 1)", "rgba(255, 99, 132, 1)"],
                data: this.data.about_rfid_detections[i].match_mismatch_proportion
              }
            ]
          },
          options: {
            maintainAspectRatio: false,
            responsive: true,
            legend: {
              position: 'right'
            },
          }
        })
      }
    }


    // temperature message
    if(this.data.highTemp == 'veryHigh' || this.data.highTemp == 'veryLow'){
     this.tempColor = 'danger'
    }
    else if(this.data.highTemp == 'high' || this.data.highTemp == 'low'){
      this.tempColor = 'warning'
    }
    else {
      this.tempColor = 'success'
    }

    // frame message
    if(this.data.percentageOfOmittedFrames < 0) {
      this.frameColor = 'warning'
    }
    else if(this.data.percentageOfOmittedFrames < 0.08){
      this.frameColor = 'success'
    }
    else if(this.data.percentageOfOmittedFrames < 1){
      this.frameColor = 'warning'
    }
    else {
      this.frameColor = 'danger'
    }

    // animal detections
    let loopNumber = 0
    if(this.data.aboutDetections['null']){
      loopNumber = Object.keys(this.data.aboutDetections).length -1
      this.data.aboutDetections['null'].animalId = 'None'
      if(this.data.aboutDetections['null'].detectionPercentTheoricalFramesColor == "red") {
        this.data.aboutDetections['null'].detectionPercentTheoricalFramesColor = 'danger'
      }
      else {
        this.data.aboutDetections['null'].detectionPercentTheoricalFramesColor = 'success'
      }
      if(this.data.aboutDetections['null'].detectionPercentRecordedFramesColor == 'red') {
        this.data.aboutDetections['null'].detectionPercentRecordedFramesColor = 'danger'
      }
      else {
        this.data.aboutDetections['null'].detectionPercentRecordedFramesColor = 'success'
      }
      if (this.data.aboutDetections['null'].messageDetectionFrameColor == 'red') {
        this.data.aboutDetections['null'].messageDetectionFrameColor = 'danger'
      }
      else {
        this.data.aboutDetections['null'].messageDetectionFrameColor = 'success'
      }
    }
    else {
      loopNumber = Object.keys(this.data.aboutDetections).length
    }
    for(let i = 1; i <= loopNumber; i++){

      if(this.data.aboutDetections[i].detectionPercentTheoricalFramesColor == "red") {
        this.data.aboutDetections[i].detectionPercentTheoricalFramesColor = 'danger'
      }
      else {
        this.data.aboutDetections[i].detectionPercentTheoricalFramesColor = 'success'
      }
      if(this.data.aboutDetections[i].detectionPercentRecordedFramesColor == 'red') {
        this.data.aboutDetections[i].detectionPercentRecordedFramesColor = 'danger'
      }
      else {
        this.data.aboutDetections[i].detectionPercentRecordedFramesColor = 'success'
      }
      if (this.data.aboutDetections[i].messageDetectionFrameColor == 'red') {
        this.data.aboutDetections[i].messageDetectionFrameColor = 'danger'
      }
      else {
        this.data.aboutDetections[i].messageDetectionFrameColor = 'success'
      }
    }



  },
  methods: {
    showTemp() {
      this.selection = 'temperature'
      this.modalOpen = !this.modalOpen
    },
    showHumidity() {
      this.selection = 'humidity'
      this.modalOpen = !this.modalOpen
    },
    showSound() {
      this.selection = 'sound'
      this.modalOpen = !this.modalOpen
    },
    showLight() {
      this.selection = 'light'
      this.modalOpen = !this.modalOpen
    }
  }
}
</script>

<style scoped>

</style>