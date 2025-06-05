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
const showReliability = ref(false);
const data = ref({});
const task = ref({});
const filename = ref('');
const error = ref(false);
const selectFile = ref(false);
const uploadPercentage = ref(0);
const convertChunks = ref(Object);
const convertedArr = ref(Object);
const errorMessage = ref('');
const tasksProgression = ref(0);
const reliabilitySelected = ref(true);
const analysisSelected = ref(false);
const step = ref(1);


////////////////////////////////
// METHODS
////////////////////////////////
const onFilePicked = (event) => {
  const files = event.target.files;
  let filename = files[0].name;

  if(filename.includes(".sqlite"))
  {
    file.value = files[0];
    filename = files[0].name;
    error.value = false;
    errorMessage.value = '';
  }
  else
  {
    file.value = '';
    filename = '';
    error.value = true;
    errorMessage.value = 'Wrong file: we must select a SQLite file';
  }
}
const  upload = async () => {
  step.value = 2;
  uploading.value = true;
  console.log(file);
  let formData = new FormData();
  formData.append('file_name', filename.value);
  formData.append('sqlite', file.value);
  try {
    const response = await axios.post(`http://127.0.0.1:8000/api/reliability/`, formData);
    selectFile.value = false;
    uploading.value = true;
    uploadPercentage.value = parseInt(Math.round((progressEvent.loaded / progressEvent.total) * 100));
  }

  const response = await axios.post(`http://127.0.0.1:8000/api/reliability/`, formData), {
    onUploadProgress: function (progressEvent)
  {
    selectFile.value = false;
    uploading.value = true;
    uploadPercentage.value = parseInt(Math.round((progressEvent.loaded / progressEvent.total) * 100));
  }
      console.log('success!!');
      uploading.value = false;
      processing.value = true;
      console.log("avant data updated");
      // task_id.value = response.data.task_id;
      console.log(response.data);
      filename.value = response.data.filename;
      console.log("avant getProgression");
      getProgression();
    }
  })
  .then(response => {
    console.log('success!!');
    uploading.value = false;
    processing.value = true;
    console.log("avant data updated");
    // task_id.value = response.data.task_id;
    console.log(response.data);
    filename.value = response.data.filename;
    console.log("avant getProgression");
    getProgression();
  }).catch(error => {
      console.log('FAILURE!! gna');
      console.log(JSON.stringify(error));
      error.value = true;
  })
}
const getProgression = () => {
  console.log("getProgression")
  console.log(`http://127.0.0.1:8000/celery-progress/${task_id.value}/`)
   axios.get(`http://127.0.0.1:8000/celery-progress/${task_id.value}/`)
    .then(response => {
      task.value = response.data;
      if(task.value.state == "FAILURE")
      {
        processing.value = false;
        error.value = true;
        errorMessage.value = task.value.result;
        console.log(errorMessage.value);
      }
      else if(task.value.state == 'SUCCESS') {
        console.log('ok!');
        console.log( task.value.result);
        step.value = 3;
        data.value = task.value.result;
        processing.value = false;
        checked.value = true;
        // this.data['name_experiment'] = this.filename.split('.sqlite')[0]
      }
      else {
        tasksProgression.value = task.value.progress.percent
        if((task.value.complete == true) && (task.value.success == false)) {
          console.log('error');
          processing.value = false;
          error.value = true;
          errorMessage.value = task.value.result;
        }
        getProgression();
      }
      // console.log(response.data.state)
      tasksProgression.value = response.data.progress.current;
    })
    .catch(error => {
      console.log(JSON.stringify(error));
    })
}




    onFilePicked (event) {
      const files = event.target.files
      let filename = files[0].name

      if(filename.includes(".sqlite"))
      {
        this.file = files[0]
        this.filename = files[0].name
        this.error = false
        this.errorMessage = ''
      }
      else
      {
        this.file = ''
        this.filename = ''
        this.error = true
        this.errorMessage = 'Wrong file: we must select a SQLite file'
      }
    },
    async upload() {
      this.step = 2
      this.uploading = true
      console.log(this.file)
      let formData = new FormData();
      formData.append('file_name', this.filename)
      formData.append('sqlite', this.file)

      axios.post(`http://127.0.0.1:8000/api/reliability/`, formData, {
        onUploadProgress: function (progressEvent) {
          this.selectFile = false
          this.uploading = true
          this.uploadPercentage = parseInt(Math.round((progressEvent.loaded / progressEvent.total) * 100))

        }.bind(this)
      })
      .then(response => {
        console.log('success!!')
        this.uploading = false
        // this.filename = response.data.filename
        this.processing = true
        // this.data = response.data.reliabilityContext
        this.task_id = response.data.task_id
        this.getProgression()
        // console.log('success!!')
        this.filename = response.data.filename
      }).catch(error => {
          console.log('FAILURE!!')
          console.log(JSON.stringify(error))
        this.error = true
      })
    },
    getProgression() {
       axios.get(`http://127.0.0.1:8000/celery-progress/${this.task_id}/`)
        .then(response => {
          this.task = response.data
          if(this.task.state == "FAILURE")
          {
            this.processing = false
            this.error = true
            this.errorMessage = this.task.result
            console.log(this.errorMessage)
          }
          else if(this.task.state == 'SUCCESS') {
            console.log('ok!')
            console.log( this.task.result)
            this.step = 3
            this.data = this.task.result
            this.processing = false
            this.checked = true
            // this.data['name_experiment'] = this.filename.split('.sqlite')[0]
          }
          else {
            this.tasksProgression = this.task.progress.percent
            if((this.task.complete == true) && (this.task.success == false)) {
              console.log('error')
              this.processing = false
              this.error = true
              this.errorMessage = this.task.result
            }
            this.getProgression()
          }
          // console.log(response.data.state)
          this.tasksProgression = response.data.progress.current
        })
        .catch(error => {
          console.log(JSON.stringify(error))
        })
    },
	},


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
                accept="sqlite"
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

        <v-window-item :value="3">
          <div class="pa-4 text-center">
            <show-reliability v-bind:data="data" v-bind:filename="file.name"></show-reliability>
          </div>
        </v-window-item>
      </v-window>




    </v-container>
  </v-main>
</template>

<!--<script>-->
<!--import axios from "axios";-->
<!--export default {-->
<!--  name: "reliability",-->
<!--  data:function (){-->
<!--		return{-->
<!--      file: '',-->
<!--      uploading: false,-->
<!--      checked: false,-->
<!--      processing: false,-->
<!--      showReliability: false,-->
<!--      data: {},-->
<!--      task: {},-->
<!--      filename: '',-->
<!--      error: false,-->
<!--      uploadPercentage: 0,-->
<!--      convertChunks: Object,-->
<!--      convertedArr: Object,-->
<!--      errorMessage: '',-->
<!--      tasksProgression: 0,-->
<!--      reliabilitySelected: true,-->
<!--      analysisSelected: false,-->
<!--      step: 1-->
<!--		}-->
<!--	},-->
<!--	methods:{-->
    onFilePicked (event) {
      const files = event.target.files
      let filename = files[0].name

      if(filename.includes(".sqlite"))
      {
        this.file = files[0]
        this.filename = files[0].name
        this.error = false
        this.errorMessage = ''
      }
      else
      {
        this.file = ''
        this.filename = ''
        this.error = true
        this.errorMessage = 'Wrong file: we must select a SQLite file'
      }
    },
    async upload() {
      this.step = 2
      this.uploading = true
      console.log(this.file)
      let formData = new FormData();
      formData.append('file_name', this.filename)
      formData.append('sqlite', this.file)

      axios.post(`http://127.0.0.1:8000/api/reliability/`, formData, {
        onUploadProgress: function (progressEvent) {
          this.selectFile = false
          this.uploading = true
          this.uploadPercentage = parseInt(Math.round((progressEvent.loaded / progressEvent.total) * 100))

        }.bind(this)
      })
      .then(response => {
        console.log('success!!')
        this.uploading = false
        // this.filename = response.data.filename
        this.processing = true
        // this.data = response.data.reliabilityContext
        this.task_id = response.data.task_id
        this.getProgression()
        // console.log('success!!')
        this.filename = response.data.filename
      }).catch(error => {
          console.log('FAILURE!!')
          console.log(JSON.stringify(error))
        this.error = true
      })
    },
    getProgression() {
       axios.get(`http://127.0.0.1:8000/celery-progress/${this.task_id}/`)
        .then(response => {
          this.task = response.data
          if(this.task.state == "FAILURE")
          {
            this.processing = false
            this.error = true
            this.errorMessage = this.task.result
            console.log(this.errorMessage)
          }
          else if(this.task.state == 'SUCCESS') {
            console.log('ok!')
            console.log( this.task.result)
            this.step = 3
            this.data = this.task.result
            this.processing = false
            this.checked = true
            // this.data['name_experiment'] = this.filename.split('.sqlite')[0]
          }
          else {
            this.tasksProgression = this.task.progress.percent
            if((this.task.complete == true) && (this.task.success == false)) {
              console.log('error')
              this.processing = false
              this.error = true
              this.errorMessage = this.task.result
            }
            this.getProgression()
          }
          // console.log(response.data.state)
          this.tasksProgression = response.data.progress.current
        })
        .catch(error => {
          console.log(JSON.stringify(error))
        })
    },
	},

<!--}-->
<!--</script>-->

<style scoped>

</style>