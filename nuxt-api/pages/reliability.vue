<!--
Created by Nicolas Torquet at 20/03/2023
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
import axios from "axios";
import {ref, onMounted} from "vue";


////////////////////////////////
// DATA
////////////////////////////////
const file = ref('');
const uploading = ref(false);
const checked = ref(false);
const processing = ref(false);
const data = ref({});
const task = ref({});
const filename = ref('');
const error = ref(false);
const selectFile = ref(false);
const uploadPercentage = ref(0);
const errorMessage = ref('');
const tasksProgression = ref(0);
const step = ref(1);
const task_id = ref('');


////////////////////////////////
// METHODS
////////////////////////////////
const onFilePicked = (event) => {
  const files = event.target.files;
  filename.value = files[0].name;

  if(filename.value.includes(".sqlite"))
  {
    file.value = files[0];
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
const  upload = async () => {
  step.value = 2;
  uploading.value = true;
  console.log(file.value);
  let formData = new FormData();
  formData.append('file_name', filename.value);
  formData.append('sqlite', file.value);

  try {
    const response = await axios.post(
      `http://127.0.0.1:8000/api/reliability/`,
      formData,
      {
        onUploadProgress: function (progressEvent) {
          selectFile.value = false;
          uploading.value = true;
          uploadPercentage.value = parseInt(
            Math.round((progressEvent.loaded / progressEvent.total) * 100)
          );
        }
      }
    );
    console.log('success!!');
    uploading.value = false;
    processing.value = true;
    task_id.value = response.data.task_id;
    filename.value = response.data.filename;
    getProgression();
  } catch (errorResp) {
    console.log('FAILURE!!');
    console.log(JSON.stringify(errorResp));
    error.value = true;
    uploading.value = false;
    processing.value = false;
  }
};

const getProgression = () => {
  console.log("getProgression");
  console.log(`http://127.0.0.1:8000/celery-progress/${task_id.value}/`);
  axios
    .get(`http://127.0.0.1:8000/celery-progress/${task_id.value}/`)
    .then((response) => {
      task.value = response.data;
      if (task.value.state == "FAILURE") {
        processing.value = false;
        error.value = true;
        errorMessage.value = task.value.result;
        console.log(errorMessage.value);
      } else if (task.value.state == "SUCCESS") {
        data.value = task.value.result;
        console.log(task.value.result);
        processing.value = false;
        checked.value = true;
        step.value = 3;
      } else {
        // tasksProgression.value = task.value.progress?.percent ?? 0;
        if (task.value.complete == true && task.value.success == false) {
          console.log("error");
          processing.value = false;
          error.value = true;
          errorMessage.value = task.value.result;
        } else {
          setTimeout(getProgression, 1000);
        }
      }
      // or tasksProgression.value = task.value.progress?.percent ?? 0;
      tasksProgression.value = response.data.progress.current;
    })
    .catch((errorResp) => {
      console.log(JSON.stringify(errorResp));
    });
}


</script>

<template>
  <v-main>
    <v-container>
      <h1>Check the reliability of an experiment</h1>

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
            <v-btn v-if="file && !uploading && !checked" @click="upload">Check the experiment</v-btn>
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

        <v-window-item class="d-flex justify-center align-center" :value="3">
          <div class="pa-4 text-center">
            <show-reliability v-bind:data="data" v-bind:filename="file.name"></show-reliability>
          </div>
        </v-window-item>
      </v-window>
    </v-container>
  </v-main>
</template>

<style scoped>

</style>