<!--
Created by Nicolas Torquet at 21/03/2023
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
import {ref, watch} from "vue";
import axios from "axios";


////////////////////////////////
// DATA
////////////////////////////////
const timelineItems = ref({
  selectSqlite: {
    title: 'Select a SQLite file',
    icon: 'mdi-download',
    color: 'pink',
    text: 'This file will be downloaded into the server to be process.'
  },
  reliability: {
    title: 'Check the reliability',
    icon: 'mdi-database-check',
    color: 'grey',
    text: 'Check detection, identity corrections and whenever available through the sensor temperature, humidity, light and ambient noise.'
  },
  animalInfo: {
    title: 'Add animal information',
    icon: 'mdi-database-edit',
    color: 'grey',
    text: 'Add sex, treatment columns. Modify the name of each animal.'
  },
  rebuild: {
    title: 'Rebuild the database',
    icon: 'mdi-database-cog',
    color: 'grey',
    text: 'This will create behavioral events into the event table of the SQLite file.'
  },
  configAnalysis: {
    title: 'Configure the analysis',
    icon: 'mdi-cogs',
    color: 'grey',
    text: 'Delimit a period to analyse, and more.'
  },
  analysis: {
    title: 'Analyse your data',
    icon: 'mdi-chart-line',
    color: 'grey',
    text: 'LMT-toolkit processes LMT experiments automatically for you!'
  },
  save: {
    title: 'Save your results',
    icon: 'mdi-content-save',
    color: 'grey',
    text: 'Download your result into a CSV file.'
  }
});
const step = ref(1);
const file = ref('');
const uploading = ref(false);
const checked = ref(false);
const dataReliability = ref({});
const task = ref({});
const filename = ref('');
const error = ref(false);
const uploadPercentage = ref(0);
const errorMessage = ref('');
const tasksProgression = ref(0);
const unitStartEnd = ref([
  {value: '', text: 'By default ...'},
  {value: 'frame(s)', text: 'frame(s)'},
  {value: 'second(s)', text: 'second(s)'},
  {value: 'minute(s)', text: 'minute(s)'},
  {value: 'hour(s)', text: 'hour(s)'},
  {value: 'day(s)', text: 'day(s)'},
]);
const minT = ref(0);
const unitMinT = ref('');
const maxT = ref(-1);
const unitMaxT = ref('');
const durationAnalysisStart = ref('From the beginning');
const durationAnalysisEnd = ref('to the end of the experiment');
const timeUnit = ref({
  'frame(s)': 1,
  'second(s)': 30,
  'minute(s)': 30*60,
  'hour(s)': 30*60*60,
  'day(s)': 30*60*60*24,
  'week(s)': 30*60*60*24*7,
});
const durationChecker = ref('');
const task_id = ref('');
const file_id = ref('');
const reliabilityModalOpen = ref(false);
const animalsInfo = ref({});
const messageStep6 = ref('');
const resultsSimplePreset = ref({});
const resultsActivityPerTimeBin = ref({});
const preset = ref(null);
const showSimplePreset = ref(false);
const showActivityPerTimeBinPreset = ref(false);
const timeBin = ref(10);
const logInfo = ref({});
const logChecked = ref(false);
const logOnChecking = ref(false);
const rebuildVersion = ref({});
const presetInfoToSend = ref({
  simplePreset: {
    presetName: "Simple preset",
    presetDescription: "Number of occurrences, total time and mean time per occurrence of every behaviors that are listed in the document section for each individual and for the whole experiment.",
    show: false
  },
  activityPerTimeBinPreset: {
    presetName: "Activity per timebin preset",
    presetDescription: "Total distance and distance travelled per time bin selected for each individual.",
    show: false
  }
});
const currentPresetInfo = ref("simplePreset");

////////////////////////////////
// METHODS
////////////////////////////////
const onFilePicked = (event) => {
  const files = event.target.files;
  let tempFilename = files[0].name;

  if(tempFilename.includes(".sqlite"))
  {
    file.value = files[0];
    filename.value = files[0].name;
    error.value = false;
    errorMessage.value = '';
  }
  else
  {
    file.value = '';
    filename.value = '';
    error.value = true;
    errorMessage.value = 'Wrong file: we must select a SQLite file';
  }
}
const upload = async () => {
  step.value = 2;
  uploading.value = true;
  console.log(file.value);
  let formData = new FormData();
  formData.append('file_name', filename.value)
  formData.append('sqlite', file.value)

  try {
    const response = await axios.post(
      `http://127.0.0.1:8000/api/files/`,
      formData,
      {
        onUploadProgress: function (progressEvent) {
          uploading.value = true;
          uploadPercentage.value = parseInt(
            Math.round((progressEvent.loaded / progressEvent.total) * 100)
          );
        }
      }
    );
    console.log('success!!');
    uploading.value = false;
    file_id.value = response.data.file_id;
    checkReliability(file_id.value);
    step.value = 3;
    console.log(response.data);
    task_id.value = response.data.task_id;
    getProgression();
    filename.value = response.data.filename;
  }
  catch (errorResp) {
    console.log('FAILURE!!');
    console.log(JSON.stringify(errorResp));
    error.value = true;
    uploading.value = false;
    processing.value = false;
  }
}


const getProgression = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/celery-progress/${task_id.value}/`);
    task.value = response.data;
    if(task.value.state == "FAILURE")
    {
      error.value = true;
      errorMessage.value = task.value.result;
      console.log(errorMessage.value);
    }
    else if(task.value.state == 'SUCCESS') {
      console.log('ok!');
      console.log( task.value.result);

      switch (step.value){
        case 3:
          // processing reliability
          stepUp();
          break;
        case 4:
          // display reliability
          console.log("step 4");

          if(!logChecked.value && !logOnChecking.value){
            dataReliability.value = task.value.result;
            animalsInfo.value = dataReliability.value.mouse;
            for(let animal in animalsInfo.value) {
              if(!animalsInfo.value[animal].hasOwnProperty("AGE")){
                console.log(Object.keys(animalsInfo.value[animal]));
                animalsInfo.value[animal]['AGE'] = "";
              }
              if(!animalsInfo.value[animal].hasOwnProperty("SEX")){
                animalsInfo[animal]['SEX'] = "";
              }
              if(!animalsInfo.value[animal].hasOwnProperty("STRAIN")){
                animalsInfo.value[animal]['STRAIN'] = "";
              }
              if(!animalsInfo.value[animal].hasOwnProperty("SETUP")){
                animalsInfo.value[animal]['SETUP'] = "";
              }
              if(!animalsInfo.value[animal].hasOwnProperty("TREATMENT")){
                animalsInfo.value[animal]['TREATMENT'] = "";
              }
            }
            getLogInfo();
            break;
          }
          else if(!logChecked.value && logOnChecking.value){
            logInfo.value = task.value.result;
            logOnChecking.value = false;
            logChecked.value = true;
            checkRebuildLMTToolkitVersion();
            break;
          }

        case 5:
          // processing rebuild
          stepUp();
          tasksProgression.value = 0;
          rebuildSQLiteFile();
          break;
        case 6:
          console.log("step 6");
          messageStep6.value = task.value.result;
          stepUp();
          break;
        case 8:
          resultsSimplePreset.value = {};
          resultsActivityPerTimeBin.value = {};
          switch(preset.value){
            case "simplePreset":
              resultsSimplePreset.value = task.value.result;
              // // animal info update
              for(let animal in resultsSimplePreset.value){
                  for(let infoAnimal in animalsInfo.value){
                      console.log(infoAnimal);
                      if(animalsInfo.value[infoAnimal]['RFID']==animal){
                          resultsSimplePreset.value[animal]['setup'] = animalsInfo.value[infoAnimal]['SETUP'];
                          resultsSimplePreset.value[animal]['treatment'] = animalsInfo.value[infoAnimal]['TREATMENT'];
                      }
                  }
              }
              stepUp();
              showSimplePreset.value = true;
              break;
            // the following case is not an integer, should be why it is not possible to come back to analysis presets after activity analysis
            case "activityPerTimeBinPreset":
              resultsActivityPerTimeBin.value = task.value.result;
              // // animal info update
              for(let animal in resultsActivityPerTimeBin.value.results){
                  for(let infoAnimal in animalsInfo.value){
                      console.log(infoAnimal.value);
                      if(animalsInfo.value[infoAnimal]['RFID']==resultsActivityPerTimeBin.value.results[animal]['animal']){
                          resultsActivityPerTimeBin.value.results[animal]['genotype'] = animalsInfo.value[infoAnimal]['GENOTYPE'];
                          resultsActivityPerTimeBin.value.results[animal]['name'] = animalsInfo.value[infoAnimal]['NAME'];
                          resultsActivityPerTimeBin.value.results[animal]['age'] = animalsInfo.value[infoAnimal]['AGE'];
                          resultsActivityPerTimeBin.value.results[animal]['sex'] = animalsInfo.value[infoAnimal]['SEX'];
                          resultsActivityPerTimeBin.value.results[animal]['strain'] = animalsInfo.value[infoAnimal]['STRAIN'];
                          resultsActivityPerTimeBin.value.results[animal]['setup'] = animalsInfo.value[infoAnimal]['SETUP'];
                          resultsActivityPerTimeBin.value.results[animal]['treatment'] = animalsInfo.value[infoAnimal]['TREATMENT'];
                      }
                  }
              }
              stepUp();
              showActivityPerTimeBinPreset.value = true;
              break;
          }
      checked.value = true;
      }
    }
    else {
      tasksProgression.value = task.value.progress.percent;
      if((task.value.complete == true) && (task.value.success == false)) {
        console.log('error');
        error.value = true;
        errorMessage.value = task.value.result;
      }
      getProgression();
    }
    tasksProgression.value = response.data.progress.current;
  }
  catch (error) {
    console.log(JSON.stringify(error));
  }
}

const setDurationAnalysis = () => {
  console.log("changed");
  if(minT.value > 0 && unitMinT.value != ''){
    durationAnalysisStart.value = "From "+minT.value+" "+unitMinT.value;
    checkDurationForAnalysis();
  }
  else {
    durationAnalysisStart.value = "From the beginning";
    durationChecker.value = '';
  }
  if((maxT.value != "-" || maxT.value > 0) && unitMaxT.value != '') {
    durationAnalysisEnd.value = "to "+maxT.value+" "+unitMaxT.value;
    checkDurationForAnalysis();
  }
  else {
    durationAnalysisEnd.value = "to the end of the experiment";
    durationChecker.value = '';
  }
}

const checkDurationForAnalysis = () => {
  if(maxT.value*timeUnit.value[unitMaxT.value] - minT.value*timeUnit.value[unitMinT.value] < 0){
    durationChecker.value = 'You select a start after the end! Please change your duration window';
  }
  else {
    durationChecker.value = '';
  }
}

const checkReliability = async () => {
  let formData = new FormData();
  formData.append('file_id', file_id.value);
  try {
    const response = await axios.post(`http://127.0.0.1:8000/api/checkReliability/`, formData);
    task_id.value = response.data.task_id;
    getProgression();
  }
  catch (error) {
    console.log(JSON.stringify(error));
  }
}

const getLogInfo = async () => {
  logOnChecking.value = true;
  let formData = new FormData();
  formData.append('file_id', file_id.value);
  try {
    const response = await axios.post(`http://127.0.0.1:8000/api/logInfo/`, formData);
    task_id.value = response.data.task_id;
    getProgression();
  }
  catch (error) {
    console.log(JSON.stringify(error))
  }
}
const checkRebuildLMTToolkitVersion = () => {
  if(logInfo.value) {
    for(let i=0; i<logInfo.value.length; i++) {
      if(logInfo.value[i]['version'].includes("LMT-toolkit")){
        rebuildVersion.value['version'] = logInfo.value[i]['version'];
        rebuildVersion.value['process'] = logInfo.value[i]['process'];
      }
    }
  }
}
const stepToTimeLine = () => {
  switch (step.value){
    case 4:
      timelineItems.value["reliability"]["color"] = "green";
      break
    case 5:
      timelineItems.value["animalInfo"]["color"] = "purple";
      break
    case 6:
      timelineItems.value["rebuild"]["color"] = "red-lighten-1";
      break
    case 7:
      timelineItems.value["configAnalysis"]["color"] = "amber-lighten-1";
      break
    case 8:
      timelineItems.value["analysis"]["color"] = "cyan-lighten-1";
      break
    case 9:
      timelineItems.value["save"]["color"] = "indigo-lighten-2";
      break
  }
}
const functionToShowReliability = () => {
  reliabilityModalOpen.value = !reliabilityModalOpen.value;
}
const stepUp = () => {
  step.value++;
  stepToTimeLine();
}
const stepDown = () => {
  if(step.value==9){;
    step.value=step.value-2;
    // reinitialize some variables here to avoid nuxt/vue problems
  }
  else{
    step.value--;
  }
  preset.value = null;
  showSimplePreset.value = false;
  showActivityPerTimeBinPreset.value = false;
  console.log("stepDown");
  stepToTimeLine();
}

const saveAnimalInfo = async (rebuild=true) => {
  let formatedAnimalsInfo = {};
  for(let line in animalsInfo.value) {
      console.log(line);
      formatedAnimalsInfo[animalsInfo.value[line]["RFID"]] = animalsInfo.value[line];
  }
  let formData = new FormData();
  formData.append('file_id', file_id.value)
  formData.append('animalsInfo', JSON.stringify( animalsInfo.value))
  try {
    const response = await axios.post(`http://127.0.0.1:8000/api/saveAnimalInfo/`, formData);
    task_id.value = response.data.task_id;
    if(!rebuild){
      stepUp();
    }
    getProgression();
  }
  catch (error) {
    console.log(JSON.stringify(error));
  }
}

const rebuildSQLiteFile = async () => {
  let formData = new FormData();
  formData.append('file_id', file_id.value)
  try {
    const response = await axios.post(
        `http://127.0.0.1:8000/api/rebuild/`,
        formData
    );
    task_id.value = response.data.task_id;
    getProgression();

  }
  catch (errorResp) {
    console.log(JSON.stringify(errorResp));
  }
}

const doAnalysis = async (presetTemp) => {
  preset.value = presetTemp;
  let formData = new FormData();
  switch (preset.value){
    case 'simplePreset':
      formData.append('file_id', file_id.value);
      if(minT.value) {
        formData.append('tmin', parseInt(minT.value));
      }
      else {
        formData.append('tmin', 0);
      }
      if(maxT.value){
        formData.append('tmax', parseInt(maxT.value));
      }
      else {
        formData.append('tmax', -1);
      }
      formData.append('unitMinT', unitMinT.value);
      formData.append('unitMaxT', unitMaxT.value);
      try {
        const response = await axios.post(`http://127.0.0.1:8000/api/extractAnalysis/`, formData);
         console.log('Do analysis simplePreset');
        task_id.value = response.data.task_id;
        stepUp();
        getProgression();
      }
      catch (error) {
        console.log('FAILURE!!');
        console.log(JSON.stringify(error));
        error.value = true;
      }
      break;
    case 'activityPerTimeBinPreset':
      formData.append('file_id', file_id.value);
      formData.append('timeBin', parseInt(timeBin.value));
      try {
        const response = await axios.post(`http://127.0.0.1:8000/api/activityPerTimeBin/`, formData);
        console.log('Do analysis activityPerTimeBinPreset');
        task_id.value = response.data.task_id;
        stepUp();
        getProgression();
      }
      catch (error) {
        console.log('FAILURE!!');
        console.log(JSON.stringify(error));
        error.value = true;
      }
      break;
  }
}

const showPresetInfo = (preset) => {
  console.log(preset);
  currentPresetInfo.value = preset;
  presetInfoToSend.value[preset]["show"] = true;
}

////////////////////////////////
// ONMOUNTED
////////////////////////////////


////////////////////////////////
// WATCHER
////////////////////////////////
watch(() => minT.value, () => {
  setDurationAnalysis();
});
watch(() => maxT.value, () => {
  setDurationAnalysis();
});
watch(() => unitMinT.value, () => {
  setDurationAnalysis();
});
watch(() => unitMaxT.value, () => {
  setDurationAnalysis();
});


</script>


<template>
  <v-main>
    <v-container>
      <h1>Analysis</h1>
       <v-alert
          color="#2A3B4D"
          theme="dark"
          icon="mdi-alert-box"
          prominent
          class="mt-10"
      >
        LMT-toolkit processes LMT experiments automatically, using the Python code
        available on Github (<nuxt-link to="https://github.com/fdechaumont/lmt-analysis" target="_blank"><v-icon icon="mdi-github"></v-icon> https://github.com/fdechaumont/lmt-analysis</nuxt-link>).<br />
        LMT-toolkit extracts the total duration, the number of occurrences and the mean duration of each occurrence
        for the behaviors described <nuxt-link to="https://livemousetracker.org/" target="_blank">here</nuxt-link>.<br />
         Please visit the <nuxt-link to="/versions" target="_blank">version history page</nuxt-link> for information about the code used.
       </v-alert>

      <v-row>
        <v-col>
          <v-timeline direction="horizontal"  class="mt-10 mb-10">
            <v-timeline-item v-for="(item, key) in timelineItems"
              :dot-color="item.color"
              :icon="item.icon"
            >
              {{ item.title }}
            </v-timeline-item>
          </v-timeline>
        </v-col>
      </v-row>

      <v-alert
        v-model="error"
        density="compact"
        color="warning"
      >
        {{ errorMessage }}
      </v-alert>

      <v-window v-model="step">
        <v-window-item :value="1">
          <v-card-text>
            To check the experiment, you have to select a LMT SQLite file:
            <v-file-input
                accept=".sqlite"
                label="Select a file"
                @change="onFilePicked($event)"
            ></v-file-input>
            <v-btn v-if="file && !uploading && !checked" @click="upload"><v-icon icon="mdi-arrow-right-bold"></v-icon> Check the experiment</v-btn>
          </v-card-text>
        </v-window-item>

        <v-window-item :value="2">
          <v-card-title><v-icon icon="mdi-download"></v-icon> LMT-toolkit is uploading your SQLite file</v-card-title>
          <v-card-text>
            <v-progress-linear
                v-model="uploadPercentage"
                color="blue-grey"
                height="25"
              >
                <template v-slot:default="{ value }">
                  <strong>{{ Math.ceil(value) }}%</strong>
                </template>
              </v-progress-linear>
          </v-card-text>
        </v-window-item>

        <v-window-item :value="3">
          <v-card-title><v-icon icon="mdi-download"></v-icon> LMT-toolkit is processing your SQLite file</v-card-title>
          <v-card-text>
            <v-progress-linear
                v-model="tasksProgression"
                color="blue-grey"
                height="25"
              >
                <template v-slot:default="{ value }">
                  <strong>{{ Math.ceil(value) }}%</strong>
                </template>
              </v-progress-linear>
          </v-card-text>
        </v-window-item>

        <v-window-item :value="4">
          <div class="pa-4 text-center">
            <v-btn @click="functionToShowReliability" class="mr-4"><v-icon icon="mdi-database-eye-outline"></v-icon> See reliability</v-btn>
            <v-btn @click="stepUp"><v-icon icon="mdi-arrow-right-bold"></v-icon> Next step: animal information</v-btn>
            <v-dialog v-model="reliabilityModalOpen" scrollable width="850">
              <show-reliability v-bind:data="dataReliability" v-bind:filename="file.name"></show-reliability>
            </v-dialog>
          </div>
        </v-window-item>

        <v-window-item :value="5">
          <v-card>
            <v-card-title>Modify animal information</v-card-title>
            <v-card-text>
              <v-table>
                <thead>
                  <tr>
                    <th v-for="(value, name) in animalsInfo[0]" or>{{ name }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="animal in animalsInfo">
                    <td v-for="(info, key) in animal">
                        <span v-if="key=='ID' || key=='RFID'">
                          {{ info }}
                        </span>
                        <v-text-field v-else
                        v-model="animal[key]"
                        hide-details
                        SingleLine
                        variant="plain"
                      ></v-text-field>
                    </td>
                  </tr>
                </tbody>
              </v-table>
              <v-card v-if="Object.keys(rebuildVersion).length>0">
                <v-card-title>Database already rebuilt</v-card-title>
                <v-card-text>The database was already rebuilt by {{rebuildVersion.version}}</v-card-text>
                <v-card-actions><v-btn @click="saveAnimalInfo(false)" class="mt-4"><v-icon icon="mdi-content-save-outline"></v-icon> Save animals information and Skip the rebuild</v-btn></v-card-actions>
              </v-card>
              <v-btn @click="saveAnimalInfo" class="mt-4"><v-icon icon="mdi-content-save-outline"></v-icon> Save animals information and rebuild database</v-btn>
            </v-card-text>
          </v-card>
        </v-window-item>

        <v-window-item :value="6">
          <v-card-title><v-icon icon="mdi-database-cog"></v-icon> Rebuild of the database</v-card-title>
          <v-card-text>
            <v-col
              class="text-subtitle-1 text-center"
              cols="12"
            >
            </v-col>
            <v-progress-linear
                v-model="tasksProgression"
                color="blue-grey"
                height="25"
              >
                <template v-slot:default="{ value }">
                  <strong>{{ Math.ceil(value) }}%</strong>
                </template>
              </v-progress-linear>
          </v-card-text>
        </v-window-item>

        <v-window-item :value="7">
          <v-card>
            <v-card-title><v-icon icon="mdi-cogs"></v-icon> Configure the analysis</v-card-title>
            <v-card-text class="align-center">
              <v-col>
              <v-row>
              <v-card class="mt-4 mr-4" width="400">
                <v-card-title> Simple preset</v-card-title>
                <v-card-text>
                  <v-alert class="mb-2">
                      By default, the analysis will be done on the total duration of the experiment.<br />
                      You can limit the analysis by filling in the fields below.
                    </v-alert>
                    <v-text-field label="Start time (computed from the launching of the recording)" v-model="minT"></v-text-field>
                    <v-select
                            label="Unit"
                            v-model="unitMinT"
                            :items="unitStartEnd"
                            item-title="text"
                            item-value="value"
                    ></v-select>
                    <v-text-field label="End time (computed from the launching of the recording)" v-model="maxT"></v-text-field>
                    <v-select
                            label="Unit"
                            v-model="unitMaxT"
                            :items="unitStartEnd"
                            item-title="text"
                            item-value="value"
                    ></v-select>

                    <v-alert type="warning" v-if="durationChecker!=''" >
                      {{ durationChecker }}
                    </v-alert>
                    <v-btn v-else @click="doAnalysis('simplePreset')">
                        <v-icon icon="mdi-arrow-right-bold"></v-icon>  Analyse
                    </v-btn>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn class="right-0" style="position: absolute; bottom: 0;" icon="mdi-information" @click="showPresetInfo('simplePreset')"></v-btn>
                </v-card-actions>
              </v-card>

              <v-card class="mt-4 mr-4" width="400">
                <v-card-title> Activity preset</v-card-title>
                <v-card-text>
                  <v-alert class="mb-2">
                      The activity preset will give you the activity (distance travelled in meters) by each animal. <br />
                      By default, the analysis will be done on the total duration of the experiment.<br />
                      You have to select a time bin to proceed.
                    </v-alert>
                    <v-text-field label="Time bin in minutes" type="number" v-model.number="timeBin"></v-text-field>

                    <v-btn v-if="timeBin!=''" @click="doAnalysis('activityPerTimeBinPreset')">
                        <v-icon icon="mdi-arrow-right-bold"></v-icon>  Analyse
                    </v-btn>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn class="right-0" style="position: absolute; bottom: 0;" icon="mdi-information" @click="showPresetInfo('activityPerTimeBinPreset')"></v-btn>
                </v-card-actions>
              </v-card>

              <preset-information v-if="presetInfoToSend[currentPresetInfo]['show']" :presetInfo="presetInfoToSend[currentPresetInfo]"></preset-information>

<!--              <OpenFieldPreset :duration="openfieldDuration"></OpenFieldPreset>-->

<!--              <v-card class="mt-4 mr-4" width="400">-->
<!--                <v-card-title> Dyadic preset</v-card-title>-->
<!--                <v-card-text>-->
<!--                  <v-alert class="mb-2">-->
<!--                      This preset can be used to analyze dyadic experiments with a two animals in the arena.<br />-->
<!--                      By default, the analysis will be done on the total duration of the experiment.<br />-->
<!--                      You can select a duration. The analysis starts at the beginning of the experiment.-->
<!--                  </v-alert>-->
<!--                  <v-text-field label="Duration in minutes" v-model="durationComponent"></v-text-field>-->

<!--                  <v-btn v-if="durationComponent!=''" @click="doAnalysis('openfieldPreset')">-->
<!--                      <v-icon icon="mdi-arrow-right-bold"></v-icon>  Analyse-->
<!--                  </v-btn>-->
<!--                </v-card-text>-->
<!--                <v-card-actions>-->
<!--                  <v-spacer></v-spacer>-->
<!--                  <v-btn class="right-0" style="position: absolute; bottom: 0;" icon="mdi-information"></v-btn>-->
<!--                </v-card-actions>-->
<!--              </v-card>-->

              </v-row>
              </v-col>
            </v-card-text>
          </v-card>
        </v-window-item>

        <v-window-item :value="8">
          <v-card-title><v-icon icon="mdi-chart-line"></v-icon> Results extraction</v-card-title>
          <v-card-text>
            <v-progress-linear
                v-model="tasksProgression"
                color="blue-grey"
                height="25"
              >
                <template v-slot:default="{ value }">
                  <strong>{{ Math.ceil(value) }}%</strong>
                </template>
              </v-progress-linear>
          </v-card-text>
        </v-window-item>

        <v-window-item :value="9">
          <v-card-title><v-icon icon="mdi-content-save"></v-icon> Results</v-card-title>
          <v-card-text>
            <show-analysis v-if="showSimplePreset" :data="resultsSimplePreset" :filename="filename"></show-analysis>

            <showActivityPerTimeBin v-if="showActivityPerTimeBinPreset" :dataActivity="resultsActivityPerTimeBin" :filename="filename" :timeBin="timeBin"></showActivityPerTimeBin>
          </v-card-text>
        </v-window-item>

      </v-window>
      <v-btn v-if="step==9" class="mr-4" @click="stepDown">
        <v-icon icon="mdi-arrow-left-bold"></v-icon>
        Come back to the previous step
      </v-btn>

    </v-container>
  </v-main>
</template>

<style scoped>
</style>