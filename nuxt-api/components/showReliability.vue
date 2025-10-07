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
import {ref, onMounted} from "vue";
// import {Chart} from "chart.js";
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
} from 'chart.js';
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
);


////////////////////////////////
// PROPS
////////////////////////////////
const props = defineProps({
  filename: {
    type: String,
    required: true,
  },
  data: {
    type: Object,
    required: true,
  },
});

////////////////////////////////
// DATA
////////////////////////////////
const modalOpen = ref(false);
const selection = ref('temperature');
const tempColor = ref('');
const frameColor = ref('');
const detections = ref([]);


////////////////////////////////
// METHODS
////////////////////////////////
const prepareData = () => {
  if(props.data.rfidDetection) {
    for (let i=1; i<=Object.keys(props.data.about_rfid_detections).length; i++) {
      const ctx = document.getElementById('mismatchProportion_' + i).getContext("2d")
      const myChart = new Chart(ctx, {
        type: "pie",
        data: {
          labels: ['Match', 'Mismatch'],
          datasets: [
            {
              backgroundColor: ["rgba(75, 192, 192, 1)", "rgba(255, 99, 132, 1)"],
              data: props.data.about_rfid_detections[i].match_mismatch_proportion
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
  if(props.data.highTemp == 'veryHigh' || props.data.highTemp == 'veryLow'){
   tempColor.value = 'error'
  }
  else if(props.data.highTemp == 'high' || props.data.highTemp == 'low'){
    tempColor.value = 'warning'
  }
  else {
    tempColor.value = 'success'
  }

  // frame message
  if(props.data.percentageOfOmittedFrames < 0) {
    frameColor.value = 'warning'
  }
  else if(props.data.percentageOfOmittedFrames < 0.08){
    frameColor.value = 'success'
  }
  else if(props.data.percentageOfOmittedFrames < 1){
    frameColor.value = 'warning'
  }
  else {
    frameColor.value = 'error'
  }

  // animal detections
  let loopNumber = 0
  if(props.data.aboutDetections['null']){
    loopNumber = Object.keys(props.data.aboutDetections).length - 1
    props.data.aboutDetections['null'].animalId = 'None'
    if(props.data.aboutDetections['null'].detectionPercentTheoricalFramesColor == "red") {
      props.data.aboutDetections['null'].detectionPercentTheoricalFramesColor = 'error'
    }
    else {
      props.data.aboutDetections['null'].detectionPercentTheoricalFramesColor = 'success'
    }
    if(props.data.aboutDetections['null'].detectionPercentRecordedFramesColor == 'red') {
      props.data.aboutDetections['null'].detectionPercentRecordedFramesColor = 'error'
    }
    else {
      props.data.aboutDetections['null'].detectionPercentRecordedFramesColor = 'success'
    }
    if (props.data.aboutDetections['null'].messageDetectionFrameColor == 'red') {
      props.data.aboutDetections['null'].messageDetectionFrameColor = 'error'
    }
    else {
      props.data.aboutDetections['null'].messageDetectionFrameColor = 'success'
    }
  }
  else {
    loopNumber = Object.keys(props.data.aboutDetections).length
  }
  for(let i = 1; i <= loopNumber; i++){

    if(props.data.aboutDetections[i].detectionPercentTheoricalFramesColor == "red") {
      props.data.aboutDetections[i].detectionPercentTheoricalFramesColor = 'error'
    }
    else {
      props.data.aboutDetections[i].detectionPercentTheoricalFramesColor = 'success'
    }
    if(props.data.aboutDetections[i].detectionPercentRecordedFramesColor == 'red') {
      props.data.aboutDetections[i].detectionPercentRecordedFramesColor = 'danger'
    }
    else {
      props.data.aboutDetections[i].detectionPercentRecordedFramesColor = 'success'
    }
    if (props.data.aboutDetections[i].messageDetectionFrameColor == 'red') {
      props.data.aboutDetections[i].messageDetectionFrameColor = 'danger'
    }
    else {
      props.data.aboutDetections[i].messageDetectionFrameColor = 'success'
    }
  }
}
const showTemp = () => {
  selection.value = 'temperature'
  modalOpen.value = !modalOpen.value
}
const showHumidity = () => {
  selection.value = 'humidity'
  modalOpen.value = !modalOpen.value
}
const showSound = () => {
  selection.value = 'sound'
  modalOpen.value = !modalOpen.value
}
const showLight = () => {
  selection.value = 'light'
  modalOpen.value = !modalOpen.value
}


////////////////////////////////
// ONMOUNTED
////////////////////////////////
onMounted(async () => {
  await nextTick();
  prepareData();
});

</script>

<template>
  <v-sheet width="850">
    <h2 class="pt-2 pl-2">Quality control</h2>
    <v-card class="mt-8">
      <v-card-title><v-icon icon="mdi-information"></v-icon> Global information</v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item><strong>File name:</strong> {{ props.filename }}</v-list-item>
          <v-list-item><strong>Start time:</strong> {{ props.data.startXp }}</v-list-item>
          <v-list-item><strong>End time:</strong> {{ props.data.endXp }}</v-list-item>
        </v-list>
      </v-card-text>
    </v-card>

    <v-card class="mt-8">
      <v-card-title><v-icon icon="mdi-rodent"></v-icon> Animals</v-card-title>
      <v-card-text>
        <v-table>
          <thead>
            <tr>
              <th v-for="(value, name) in props.data.mouse[0]" or>{{ name }}</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="mice in props.data.mouse">
              <td v-for="animalInfo in mice">{{ animalInfo }}</td>
            </tr>
          </tbody>
        </v-table>
      </v-card-text>
    </v-card>

    <v-card class="mt-8">
      <v-card-title>Sensors information</v-card-title>
      <v-card-text v-if="props.data.sensors!='no sensors'">
        <v-row>
          <v-col><v-btn @click="showTemp">Temperature</v-btn></v-col>
          <v-col><v-btn @click="showHumidity">Humidity</v-btn></v-col>
          <v-col><v-btn @click="showSound">Sound</v-btn></v-col>
          <v-col><v-btn @click="showLight">Light</v-btn></v-col>
        </v-row>

        <br />
        <v-alert :color="tempColor">
          <h4>Temperature</h4>
          <p>{{ props.data.highTempInformation }}</p>
          <p>{{ props.data.lowTempInformation }}</p>
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
            <td>{{ props.data.theoricalNumberOfFrame }}</td>
            <td>{{ props.data.nbFramesRecorded }}</td>
            <td>{{ props.data.nbOmittedFrames }} frames / {{ props.data.percentageOfOmittedFrames }} %</td>
          </tr>
          <tr>
            <td>Duration in seconds</td>
            <td>{{ props.data.realDurationInSeconds }}</td>
            <td>{{ props.data.nbFramesRecordedInSeconds }}</td>
            <td>{{ props.data.nbOmittedSeconds }}</td>
          </tr>
          <tr>
            <td>Duration in minutes</td>
            <td>{{ props.data.realDurationInMinutes }}</td>
            <td>{{ props.data.nbFramesRecordedInMinutes }}</td>
            <td>{{ props.data.nbOmittedMinutes }}</td>
          </tr>
          <tr>
            <td>Duration in hours</td>
            <td>{{ props.data.realDurationInHours }}</td>
            <td>{{ props.data.nbFramesRecordedInHours }}</td>
            <td>{{ props.data.nbOmittedHours }}</td>
          </tr>
          <tr>
            <td>Duration in days</td>
            <td>{{ props.data.realDurationInDays }}</td>
            <td>{{ props.data.nbFramesRecordedInDays }}</td>
            <td>{{ props.data.nbOmittedDays }}</td>
          </tr>
          </tbody>
        </v-table>
        <v-alert :color="frameColor">
          <h4 class="alert-heading">
            <v-icon icon="mdi-check-bold" v-if="frameColor=='success'"></v-icon>
            <v-icon icon="mdi-alert" v-if="frameColor=='warning'"></v-icon>
            <v-icon icon="mdi-alert-box" v-if="frameColor=='danger'"></v-icon>
            Experiment reliability based on dropped frames</h4>
          <p>{{ props.data.omissionInformation }}</p>
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
          <tr v-for="detection in props.data.aboutDetections">
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
        <v-table class="table" v-if="props.data.rfidDetection">
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
          <tr v-for="(item, index) in props.data.about_rfid_detections">
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
      <linePlot :selection="selection" :timeline="props.data.timeline" :temperature="props.data.temperature"
        :humidity="props.data.humidity" :sound="props.data.sound" :lightvisible="props.data.lightvisible" :lightvisibleandir="props.data.lightvisibleandir"></linePlot>
    </v-dialog>
  </v-sheet>

</template>


<style scoped>

</style>