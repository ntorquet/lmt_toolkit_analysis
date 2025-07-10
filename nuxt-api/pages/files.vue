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
import axios from "axios";
import {ref, onMounted} from "vue";


////////////////////////////////
// DATA
////////////////////////////////
const files = ref([]);
const fields = ref(['File name', 'Rebuild', 'Upload date', 'Download', 'Analyse', 'Delete']);
const filesItems = ref([]);
const downloadableLinks = ref([]);
const showSimplePreset = ref(false);


////////////////////////////////
// METHODS
////////////////////////////////
const getFiles = () => {
  files.value = [];
  filesItems.value = [];
  axios.get(`http://127.0.0.1:8000/api/files`)
  .then(response => {
    files.value = response.data;
    organizeFiles();
  })
  .catch(error => {
      console.log(JSON.stringify(error))
  })
}

const organizeFiles = () => {
  filesItems.value = []
  for(let i=0; i<files.value.length;i++){
    filesItems.value.push({
      'File name': files.value[i]['file_name'],
      'Rebuild': files.value[i]['rebuild'],
      'Upload date': files.value[i]['created_at'],
      'Link': "http://127.0.0.1:8000/media"+files.value[i]['sqlite'].split('/media')[1],
    })
  }
}

const deleteFile = (fileId) => {
  console.log(`delete file ${fileId}`)
  axios.delete(`http://127.0.0.1:8000/api/files/${fileId}/`)
  .then(response => {
    getFiles();
    // $refs.fileTable.refresh();
  })
  .catch(error => {
      console.log(JSON.stringify(error))
    })
}

const checkReliability = (fileId) => {
  let formData = new FormData();
  formData.append('file_id', fileId)
  axios.post(`http://127.0.0.1:8000/api/checkReliability/`, formData)
  .then(response => {
    taskId.value = response.data.taskId;
  })
  .catch(error => {
    console.log(JSON.stringify(error))
  })
}

////////////////////////////////
// ONMOUNTED
////////////////////////////////
onMounted(() => getFiles());

</script>

<template>
  <v-main>
    <v-container>
      <h1 class="title">Saved SQLite databases</h1>
      <div v-if="files.length>0">
        <v-table fixed-header width="800px">
          <thead>
            <tr>
              <th v-for="field in fields">
                {{ field }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="file, index in files">
              <td>{{ file.file_name }}</td>
              <td>{{ file.rebuild }}</td>
              <td>{{ file.created_at.split("T")[0] }}</td>
              <td>
                <v-btn size="sm" :href="filesItems[index]['Link']">
                  <v-icon icon="mdi-download"></v-icon>
                   Download
                </v-btn>
              </td>
              <td>
<!--                <v-chip class="mr-1" color="primary">Simple preset</v-chip>-->
<!--                <v-chip class="mr-1" color="secondary">Activity per time bin preset</v-chip>-->
              </td>
              <td>
                <v-btn size="sm" @click="deleteFile(files[index]['id'])">
                  <v-icon icon="mdi-delete"></v-icon>
                </v-btn>
              </td>
            </tr>
          </tbody>
        </v-table>


        <v-table ref="fileTable" striped="even" :items="filesItems" :fields="fields">
          <template #cell(Download)="row">
            <v-btn size="sm" :href="filesItems[row.index]['Link']">
              <v-icon icon="mdi-download"></v-icon>
               Download
            </v-btn>
          </template>
          <template #cell(Delete)="row">
            <v-btn size="sm" @click="deleteFile(files[row.index]['id'])">
              <v-icon icon="mdi-trash"></v-icon>
            </v-btn>
          </template>
        </v-table>
      </div>
      <div v-else>
        <p>There is no SQLite database in LMT-toolkit</p>
      </div>
    </v-container>
  </v-main>

<!--  <simple-preset v-show="false"></simple-preset>-->

</template>

<style scoped>

</style>