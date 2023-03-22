<!--
Created by Nicolas Torquet at 20/03/2023
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->
<template>
  <v-main>
    <v-container>
      <h1>Check the reliability of an experiment</h1>

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
        <v-card-text>
          <v-text-field
            label="Password"
            type="password"
          ></v-text-field>
          <v-text-field
            label="Confirm Password"
            type="password"
          ></v-text-field>
          <span class="text-caption text-grey-darken-1">
            Please enter a password for your account
          </span>
        </v-card-text>
      </v-window-item>

      <v-window-item :value="3">
        <div class="pa-4 text-center">
          <v-img
            class="mb-4"
            contain
            height="128"
            src="https://cdn.vuetifyjs.com/images/logos/v.svg"
          ></v-img>
          <h3 class="text-h6 font-weight-light mb-2">
            Welcome to Vuetify
          </h3>
          <span class="text-caption text-grey">Thanks for signing up!</span>
        </div>
      </v-window-item>
    </v-window>

      <v-row class="mt-10" v-if="!checked && !uploading && !processing">
        <v-col>
          To check the experiment, you have to select a LMT SQLite file:
        </v-col>
        <v-col>
          <v-file-input
              accept="sqlite"
              label="Select a file"
              @change="onFilePicked($event)"
          ></v-file-input>
        </v-col>
        <v-col v-if="!file">
          <strong> Choose a SQLite file…</strong>
        </v-col>
        <v-col v-else>
            {{ file.name }}<br />
            <v-btn v-if="file && !uploading && !checked" @click="upload">Check the experiment</v-btn>
        </v-col>
      </v-row>

      <div v-if="!checked && !uploading && !processing">
        <p>To check the experiment, you have to select a LMT SQLite file:</p>
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
                  <b-button class="button is-success" @click="upload">Check the experiment</b-button>
                </div>
              </span>
            </span>
          </label>
        </div>
      </div>
    </v-container>
  </v-main>
</template>

<script>
export default {
  name: "reliability",
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
      step: 1
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

      axios.post(`http://127.0.0.1:8000/api/v1/reliability/`, formData, {
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
	},
  computed: {
      currentTitle () {
        switch (this.step) {
          case 1: return 'Sign-up'
          case 2: return 'Create a password'
          default: return 'Account created'
        }
      },
    },
}
</script>

<style scoped>

</style>