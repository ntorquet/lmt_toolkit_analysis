<template>
  <h4>Reliability information</h4>
  <div id="globale_information">
    <b-card title="Global information">
      <b-card-body>
        <b-list-group>
          <b-list-group-item><strong>File name:</strong> {{ filename }}</b-list-group-item>
          <b-list-group-item><strong>Start time:</strong> {{ data.startXp }}</b-list-group-item>
          <b-list-group-item><strong>End time:</strong> {{ data.endXp }}</b-list-group-item>
        </b-list-group>
      </b-card-body>
    </b-card>
  </div>

  <br />
  <hr/>
  <br />

  <div id="animals">
    <h5>Animals</h5>
    <table id="animalTable" class="table">
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
    </table>
  </div>

  <br />
  <hr />
  <br />

  <!--      SENSORS    -->
  <div id="sensors">
    <h5><b-icon-thermometer-half></b-icon-thermometer-half> Sensors information</h5>
    <div v-if="data.sensors!='no sensors'">
      <b-row>
        <b-col><b-button @click="showTemp">Temperature</b-button></b-col>
        <b-col><b-button @click="showHumidity">Humidity</b-button></b-col>
        <b-col><b-button @click="showSound">Sound</b-button></b-col>
        <b-col><b-button @click="showLight">Light</b-button></b-col>
      </b-row>
      <br />
      <b-alert show v-model:variant="tempColor">
        <h4 class="alert-heading">Temperature</h4>
        <p>{{ data.highTempInformation }}</p>
        <p>{{ data.lowTempInformation }}</p>
      </b-alert>
    </div>
    <div v-else>
      <div>No sensors</div>
    </div>
  </div>

  <br />
  <hr/>
  <br />

  <div id="frames_and_duration_information">
    <h5>Frames and duration information</h5>
    <table class="table">
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
        <td :class="'table-'+frameColor">{{ data.nbOmittedFrames }} frames / {{ data.percentageOfOmittedFrames }} %</td>
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
    </table>
    <b-alert show v-model:variant="frameColor">
      <h4 class="alert-heading">
        <b-icon-check v-if="frameColor=='success'"></b-icon-check>
        <b-icon-exclamation-triangle v-if="frameColor=='warning'"></b-icon-exclamation-triangle>
        <b-icon-x-circle v-if="frameColor=='danger'"></b-icon-x-circle>
        Experiment reliability based on dropped frames</h4>
      <p>{{ data.omissionInformation }}</p>
    </b-alert>
  </div>

  <br />
  <hr/>
  <br />

  <div id="about_video_detections" v-if="data.aboutDetections">
    <h5>About animal detections</h5>
    <table class="table">
      <thead>
      <tr>
        <th>Animal ID</th>
        <th>Number of detection</th>
        <th>% of detections based on recorded frames</th>
        <th>% of detections based on expected number of frames</th>
        <th><b-icon-exclamation-circle></b-icon-exclamation-circle></th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="detection in data.aboutDetections">
        <td>{{ detection.animalId }}</td>
        <td>{{ detection.nbDetection }}</td>
        <td :class="'table-'+detection.detectionPercentRecordedFramesColor">{{ detection.detectionPercentRecordedFrames }} %</td>
        <td :class="'table-'+detection.detectionPercentTheoricalFramesColor">{{ detection.detectionPercentTheoricalFrames }} %</td>
        <td :class="'table-'+detection.messageDetectionFrameColor">
          <b-icon-check v-if="detection.messageDetectionFramesIcon=='check icon'"></b-icon-check>
          <b-icon-exclamation-triangle v-if="detection.messageDetectionFramesIcon=='hotjar icon'"></b-icon-exclamation-triangle>
        </td>
      </tr>
      </tbody>
    </table>
  </div>

  <br />
  <hr/>
  <br />

  <div id="about_rfid_detections">
    <h5>About RFID detections</h5>
    <table class="table" v-if="data.rfidDetection">
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
    </table>
    <b-card header="There is no RFID detections on the database" v-else>
      <p>This is could be for several reasons:</p>
      <ul>
        <li>The mouse or the mice had no RFID chips</li>
        <li>The RFID floor had was not plugged in</li>
        <li>The RFID floor had a problem (RFID antenna COM port not assigned)</li>
      </ul>
    </b-card>
  </div>

  <LinePlot v-model="modalOpen" v-model:selection="selection" :timeline="data.timeline" :temperature="data.temperature"
            :humidity="data.humidity" :sound="data.sound" :lightvisible="data.lightvisible" :lightvisibleandir="data.lightvisibleandir"></LinePlot>


</template>

<script>
import LinePlot from "@/components/LinePlot"
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
import {
  BIconCheck,
  BIconExclamationCircle,
  BIconThermometerHalf,
  BIconExclamationTriangle,
  BIconGlobe,
  BIconXCircle,
  BIconInfoCircle,
} from "bootstrap-icons-vue";
import Popper from "vue3-popper"
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
  name: "ShowReliability",
  components: {
    LinePlot,
    Popper,
    BIconCheck,
    BIconExclamationCircle,
    BIconThermometerHalf,
    BIconExclamationTriangle,
    BIconGlobe,
    BIconXCircle,
    BIconInfoCircle,
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
div{
  padding-left: 4em;
  padding-right: 4em;
}
</style>