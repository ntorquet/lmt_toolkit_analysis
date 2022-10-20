<!--
Created by Nicolas Torquet at 12/07/2022
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->
<template>
  <b-container>
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">Analyse an experiment and check its reliability</h1>
        <div v-if="!checked && !uploading && !processing">
          <p>To analyse the experiment, you have to select a LMT SQLite file:</p>
          <div class="file">
            <label class="file-label">
              <input class="form-file" type="file" name="file" @change="onFilePicked($event)">
              <span class="file-cta">
                <span class="file-icon">
                  <i class="fas fa-upload"></i>
                </span>
                <span class="file-label" v-if="!file">
                  <strong> Choose a SQLite file…</strong>
                </span>
                <span v-else>
                  {{ file.name }}<br />
                  <div class="block" v-if="file && !uploading && !checked">
                    <b-button class="button is-success" @click="upload">Analyse the experiment</b-button>
                  </div>
                </span>
              </span>
            </label>
          </div>
        </div>
        <br />

        <div class="block" v-if="uploading && !checked">
<!--          <b-spinner label="Loading..."></b-spinner> {{ file.name }}: the file is being processed. Please wait.-->
          <h5>Uploading:</h5>
          <b-progress :value="uploadPercentage" variant="success" ></b-progress>
        </div>
        <br />
        <div v-if="processing">
<!--          <b-spinner label="Loading..."></b-spinner> -->
          <h5>Processing</h5>
          <b-progress :value="tasksProgression" variant="success" ></b-progress>
          {{ file.name }}: the file is being processed. Please wait.
        </div>

        <b-alert variant="danger" v-if="error" show>
          Error: something wrong happened: please retry or contact an administrator
        </b-alert>


      </div>
    </div>
  </b-container>

  <div v-if="checked">
    <b-nav tabs fill>
      <b-nav-item :active="reliabilitySelected" @click="selectReliability">Reliability</b-nav-item>
      <b-nav-item :active="analysisSelected" @click="selectAnalysis">Analysis</b-nav-item>
    </b-nav>
    <b-container v-if="reliabilitySelected">
      <show-reliability v-bind:data="data" v-bind:filename="file.name"></show-reliability>
    </b-container>
    <b-container v-if="analysisSelected" fluid>
      <show-analysis v-bind:data="data" v-bind:filename="file.name"></show-analysis>
    </b-container>
  </div>
</template>

<script>
import axios from "axios"
import ShowReliability from "@/components/ShowReliability"
import ShowAnalysis from "@/components/ShowAnalysis"
import { BIconFileEarmarkPlus } from 'bootstrap-icons-vue'

export default {
  name: "reliability",
  components: {
    ShowReliability,
    ShowAnalysis,
    'BIconFileEarmarkPlus': BIconFileEarmarkPlus,
  },
	data:function (){
		return{
      file: '',
      uploading: false,
      checked: false,
      processing: false,
      showReliability: false,
      data: {},
      task: {},
      filename: '',
      error: false,
      uploadPercentage: 0,
      // rfidDetection: Object,
      // about_rfid_detections: Object,
      // match_mismatch_proportion: Object,
      convertChunks: Object,
      convertedArr: Object,
      errorMessage: '',
      tasksProgression: 0,
      reliabilitySelected: true,
      analysisSelected: false,
		}
	},
	methods:{
    onFilePicked (event) {
      const files = event.target.files
      let filename = files[0].name

      if(filename.includes(".sqlite"))
      {
        this.file = files[0]
        this.filename = files[0].name
      }
      else
      {
        this.file = ''
        this.filename = ''
        this.$toast.error('Wrong file: we must select a SQLite file')
      }
    },
    async upload() {
      this.uploading = true
      console.log(this.file)
      let formData = new FormData();
      formData.append('file_name', this.filename)
      formData.append('sqlite', this.file)

      axios.post(`/api/v1/analyse_reliability/`, formData, {
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
       axios.get(`celery-progress/${this.task_id}/`)
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
    selectReliability() {
      this.reliabilitySelected = true
      this.analysisSelected = false
    },
    selectAnalysis() {
      this.reliabilitySelected = false
      this.analysisSelected = true
    }
	}


}
</script>

<style scoped>
#test {
  border-color: #42b983;
  border: 12px solid;
  width: 100%;
}
</style>