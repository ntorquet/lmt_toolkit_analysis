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
            <input class="form-file" type="file" name="file" @change="onFilePicked($event)" />
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
                  <div class="form_analysis">
                    <b-alert show class="info">
                      By default, the analysis will be done on the total duration of the experiment.<br />
                      You can limit the analysis by filling in the fields below.
                    </b-alert>
                    <b-form-group label="Start">
                      <div class="row">
                        <div class="col-lg-3">
                          Start time (computed from the launching of the recording)
                        </div>
                        <div class="col-lg-1">
                          <b-form-input type="number" v-model="minT"></b-form-input>
                        </div>
                        <div class="col-lg-2">
                          <b-form-select  v-model="unitMinT" :options="unitStartEnd">
                          </b-form-select>
                        </div>
                      </div>
                    </b-form-group>
                    <b-form-group label="End">
                      <div class="row">
                        <div class="col-lg-3">
                          End time (computed from the launching of the recording)
                        </div>
                        <div class="col-lg-1">
                          <b-form-input type="number" v-model="maxT"></b-form-input>
                        </div>
                        <div class="col-lg-2">
                          <b-form-select  v-model="unitMaxT"  :options="unitStartEnd">
                          </b-form-select>
                        </div>
                        <div class="col-lg-5">
                          <strong>Duration selected</strong><br />
                          {{ durationAnalysisStart }} {{ durationAnalysisEnd }}<br />
                        </div>
                      </div>
                    </b-form-group>
                  </div>
                <div v-if="durationChecker==''">
                  <b-button class="button is-success" @click="upload">Analyse the experiment</b-button>
                </div>
                <b-alert class="alert-danger" v-else show>
                  {{ durationChecker }}
                </b-alert>
              </div>
            </span>
          </span>
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
      <b-nav-item class="tab_title" :active="reliabilitySelected" @click="selectReliability">Reliability</b-nav-item>
      <b-nav-item class="tab_title" :active="analysisSelected" @click="selectAnalysis">Analysis</b-nav-item>
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
  name: "Results",
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
      unitStartEnd: [
        {value: null, text: 'By default ...'},
        {value: 'frame(s)', text: 'frame(s)'},
        {value: 'second(s)', text: 'second(s)'},
        {value: 'minute(s)', text: 'minute(s)'},
        {value: 'hour(s)', text: 'hour(s)'},
        {value: 'day(s)', text: 'day(s)'},
      ],
      minT: 0,
      unitMinT: null,
      maxT: -1,
      unitMaxT: null,
      durationAnalysisStart: 'From the beginning',
      durationAnalysisEnd: 'to the end of the experiment',
      timeUnit: {
        'frame(s)': 1,
        'second(s)': 30,
        'minute(s)': 30*60,
        'hour(s)': 30*60*60,
        'day(s)': 30*60*60*24,
        'week(s)': 30*60*60*24*7,
      },
      durationChecker: ''
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
      formData.append('tmin', parseInt(this.minT))
      formData.append('tmax', parseInt(this.maxT))
      formData.append('unitMinT', this.unitMinT)
      formData.append('unitMaxT', this.unitMaxT)

      axios.post(`/api/v1/analyse/`, formData, {
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
    },
    setDurationAnalysis() {
      console.log("changed")
      if(this.minT > 0 && this.unitMinT != null){
        this.durationAnalysisStart = "From "+this.minT+" "+this.unitMinT
        this.sendMinT = this.minT+" "+this.unitMinT
        this.checkDurationForAnalysis()
      }
      else {
        this.durationAnalysisStart = "From the beginning"
        this.durationChecker = ''
      }
      if((this.maxT != "-" || this.maxT > 0) && this.unitMaxT != null) {
        this.durationAnalysisEnd = "to "+this.maxT+" "+this.unitMaxT
        this.sendMaxT = this.maxT+" "+this.unitMaxT
        this.checkDurationForAnalysis()
      }
      else {
        this.durationAnalysisEnd = "to the end of the experiment"
        this.durationChecker = ''
      }
    },
    checkDurationForAnalysis() {
      if(this.maxT*this.timeUnit[this.unitMaxT] - this.minT*this.timeUnit[this.unitMinT] < 0){
        this.durationChecker = 'You select a start after the end! Please change your duration window'
      }
      else {
        this.durationChecker = ''
      }
    }
	},
  watch: {
    minT() {
      this.setDurationAnalysis()
    },
    maxT() {
      this.setDurationAnalysis()
    },
    unitMinT() {
      this.setDurationAnalysis()
    },
    unitMaxT() {
      this.setDurationAnalysis()
    },
  }

}
</script>

<style scoped>
#test {
  border-color: #42b983;
  border: 12px solid;
  width: 100%;
}

.tab_title {
  font-size: 1.5em;
  font-weight: bold;
  color: black;
}

.form_analysis{
  margin: 2em;
}

</style>