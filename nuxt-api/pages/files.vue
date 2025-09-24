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
const fields = ref(['File name', 'Rebuild', 'Upload date', 'Download', 'Tasks', 'Analyse', 'Delete']);
const filesItems = ref([]);
const downloadableLinks = ref([]);
const showSimplePreset = ref(false);
const dictTasks = ref({
  'lmt_toolkit_analysis.tasks.getReliability': ['mdi-database-check', "Control & Quality"],
  'lmt_toolkit_analysis.tasks.getLogInfoTask': ['mdi-database-search', "Get info from database"],
  'lmt_toolkit_analysis.tasks.saveAnimalInfoTask': ['mdi-database-edit', "Animal info saved"],
  'lmt_toolkit_analysis.tasks.rebuildSQLite': ['mdi-database-cog', "Rebuild database"],
  'lmt_toolkit_analysis.tasks.buildNightEventTask': ['mdi-weather-night', 'Night rebuild'],
  'lmt_toolkit_analysis.tasks.analyseProfileFromStartTimeToEndTime': ['mdi-database-export', "General preset"],
  'lmt_toolkit_analysis.tasks.activityPerTimeBin': ['mdi-database-export', 'Activity preset']
});


////////////////////////////////
// METHODS
////////////////////////////////
const getFiles = () => {
  files.value = [];
  filesItems.value = [];
  axios.get(`http://127.0.0.1:8000/api/files/`)
  .then(response => {
    files.value = response.data;
    // console.log(files.value);
    organizeFiles();
    getTasks();
  })
  .catch(error => {
    console.log(JSON.stringify(error));
  })
}


const getTasks = () => {
  // convert task.result into dictionary
  for(let i=0; i<files.value.length; i++) {
    if (files.value[i]['tasks'].length > 0) {
      for (let j = 0; j < files.value[i]['tasks'].length; j++) {
        if(files.value[i]['tasks'][j]['status'] == "PROGRESS") {
          files.value[i]['tasks'][j]['result'] = JSON.parse(files.value[i]['tasks'][j]['result']);
          getProgression(files.value[i]['tasks'][j]);
        }
      }
    }
    // console.log(files.value[i]);
  }
}


const organizeFiles = () => {
  filesItems.value = [];
  for(let i=0; i<files.value.length; i++){
    let itemsToPush = {
      'File name': files.value[i]['file_name'],
      'Rebuild': files.value[i]['rebuild'],
      'Upload date': files.value[i]['created_at'],
      'Link': "http://127.0.0.1:8000/media"+files.value[i]['sqlite'].split('/media')[1],
    };
    filesItems.value.push(itemsToPush);
  }
}


const deleteFile = (fileId) => {
  console.log(`delete file ${fileId}`);
  axios.delete(`http://127.0.0.1:8000/api/files/${fileId}/`)
  .then(response => {
    getFiles();
    // $refs.fileTable.refresh();
  })
  .catch(error => {
      console.log(JSON.stringify(error));
    })
}

const getProgression = async (taskToCheck) => {
  // console.log(taskToCheck);
  try {
    const task_id = taskToCheck.task_id;
    const response = await axios.get(`http://127.0.0.1:8000/celery-progress/${task_id}/`);
    const taskProg = response.data;

    taskToCheck.result.percent = taskProg.progress.percent;
    taskToCheck.result.description = taskProg.progress.description;
    taskToCheck.status = taskProg.state;
    if(taskProg.state == "FAILURE")
    {
      console.log("FAILURE");
      taskToCheck.status = "FAILURE";
      getFiles();
    }
    else if(taskProg.state == 'SUCCESS') {
      console.log("yo!");
      taskToCheck.status = "SUCCESS";
      getFiles();
    }
    else {
      if((taskProg.complete == true) && (taskProg.success == false)) {
        console.log('error');
        taskToCheck.status = "FAILURE";
      }
      else{
        getProgression(taskToCheck);
      }
    }
  }
  catch (error) {
    console.log(JSON.stringify(error));
  }
}

const checkReliability = (fileId) => {
  let formData = new FormData();
  formData.append('file_id', fileId);
  axios.post(`http://127.0.0.1:8000/api/checkReliability/`, formData)
  .then(response => {
    taskId.value = response.data.taskId;
  })
  .catch(error => {
    console.log(JSON.stringify(error));
  })
}

const revokeTask = (task_id) => {
  console.log("task revokator");
  console.log(task_id);
  console.log("go!")
  let formData = new FormData();
  formData.append('task_id', task_id);
  axios.post(`http://127.0.0.1:8000/api/revokeTask/`, formData)
  .then(response => {
    console.log("task deleted");
    getFiles();
  })
  .catch(error => {
    console.log(JSON.stringify(error));
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
                <v-list v-if="file.tasks.length>0">
                  <v-list-item v-for="task in file.tasks">
                    <div class="d-flex ga-2 align-center" v-if="task.status=='PENDING'">
                      <v-chip class="ma-2" color="primary"><v-icon :icon=dictTasks[task.task_name][0] class="mr-2"></v-icon>{{ dictTasks[task.task_name][1] }}<v-icon icon="mdi-clock-outline" class="ml-2"></v-icon></v-chip>
                    </div>
                    <div class="d-flex ga-2 align-center" v-if="task.status=='PROGRESS'">
                      <v-chip class="ma-2" color="purple"><v-icon :icon=dictTasks[task.task_name][0] class="mr-2"></v-icon>{{ dictTasks[task.task_name][1] }}</v-chip>
                      <v-progress-linear
                        color="purple"
                        height="10"
                        :model-value="task.result.percent"
                        striped
                      ></v-progress-linear>
<!--                      <v-btn size="sm" variant="plain" prepend-icon="mdi-close-circle-outline" @click="revokeTask(task.task_id)"></v-btn>-->
                    </div>
                    <div class="d-flex ga-0 align-center" v-if="task.status=='SUCCESS'">
                      <v-chip color="success"><v-icon :icon=dictTasks[task.task_name][0] class="mr-2"></v-icon>{{ dictTasks[task.task_name][1] }}<v-icon icon="mdi-check" class="ml-2"></v-icon></v-chip>
                    </div>
                    <div class="d-flex ga-0 align-center" v-if="task.status=='FAILURE'">
                      <v-chip class="ma-2" color="alert"><v-icon :icon=dictTasks[task.task_name][0] class="mr-2"></v-icon>{{ dictTasks[task.task_name][1] }}<v-icon icon="mdi-alert-octagon" class="ml-2"></v-icon></v-chip>
                    </div>
                  </v-list-item>
                </v-list>
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
.v-list-item {
    min-height: 20px !important;
    padding-top: 4px;
    padding-bottom: 0;
}

.v-progress-linear {
  max-width: 50%;
}
</style>