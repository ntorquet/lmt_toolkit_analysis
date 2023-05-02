<!--
Created by Nicolas Torquet at 21/03/2023
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->
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
            <v-btn @click="functionToShowReliability">See reliability</v-btn>
            <v-btn @click="stepUp">Next step: animal information</v-btn>
            <v-dialog v-model="reliabilityModalOpen" scrollable width="800">
              <show-reliability v-bind:data="data" v-bind:filename="file.name"></show-reliability>
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
                    <th v-for="(value, name) in data.mouse[0]" or>{{ name }}</th>
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
              <v-btn @click="saveAnimalInfo">Save animals information</v-btn>
            </v-card-text>
          </v-card>
        </v-window-item>

        <v-window-item :value="6">
          <v-card-title><v-icon icon="mdi-database-cog"></v-icon> Rebuild of the database</v-card-title>
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

        <v-window-item :value="7">
            <v-card>
          <v-card-title><v-icon icon="mdi-cogs"></v-icon> Configure the analysis</v-card-title>
          <v-card-text>
            <v-card>
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
                        Analyse
                    </v-btn>
                </v-card-text>
            </v-card>
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
            <show-analysis :data="results" :filename="filename"></show-analysis>
          </v-card-text>
        </v-window-item>

      </v-window>

    </v-container>
  </v-main>
</template>

<script>
import axios from "axios";
import {th} from "vuetify/locale";
export default {
  name: "analysis",
  data:function (){
		return{
       timelineItems: {
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
      },
      step: 1,
      file: '',
      uploading: false,
      checked: false,
      // processing: false,
      showReliability: false,
      data: {},
      task: {},
      filename: '',
      error: false,
      uploadPercentage: 0,
      // rfidDetection: Object,
      // about_rfid_detections: Object,
      // match_mismatch_proportion: Object,
      // convertChunks: Object,
      // convertedArr: Object,
      errorMessage: '',
      tasksProgression: 0,
      // reliabilitySelected: true,
      // analysisSelected: false,
      unitStartEnd: [
        {value: '', text: 'By default ...'},
        {value: 'frame(s)', text: 'frame(s)'},
        {value: 'second(s)', text: 'second(s)'},
        {value: 'minute(s)', text: 'minute(s)'},
        {value: 'hour(s)', text: 'hour(s)'},
        {value: 'day(s)', text: 'day(s)'},
      ],
      minT: 0,
      unitMinT: '',
      maxT: -1,
      unitMaxT: '',
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
      durationChecker: '',
      deleteFile: 'unselected',
      fileURL: '',
      task_id: '',
      file_id: '',
      reliabilityModalOpen: false,
      animalsInfo: {},
      messageStep6: '',
      results: {},
      // djangoRestURL: axios.defaults.baseURL,
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
      // formData.append('tmin', parseInt(this.minT))
      // formData.append('tmax', parseInt(this.maxT))
      // formData.append('unitMinT', this.unitMinT)
      // formData.append('unitMaxT', this.unitMaxT)
      // formData.append('deleteFile', this.deleteFile)

      axios.post(`http://127.0.0.1:8000/api/v1/files/`, formData, {
        onUploadProgress: function (progressEvent) {
          this.selectFile = false
          this.uploading = true
          this.uploadPercentage = parseInt(Math.round((progressEvent.loaded / progressEvent.total) * 100))

        }.bind(this)
      })
      .then(response => {
        console.log('success!!')
        this.uploading = false


        // get the new id from http://127.0.0.1:8000/api/v1/files/
        this.file_id = response.data.file_id
        this.checkReliability(this.file_id)
        this.step = 3
        // this.filename = response.data.filename
        // this.processing = true
        // this.data = response.data.reliabilityContext
        console.log(response.data)
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
            // this.processing = false
            this.error = true
            this.errorMessage = this.task.result
            console.log(this.errorMessage)
          }
          else if(this.task.state == 'SUCCESS') {
            console.log('ok!')
            console.log( this.task.result)
            // this.stepUp()
            // this.step = 4
            // this.stepToTimeLine()

            switch (this.step){
              case 3:
                this.stepUp()
                break
              case 4:
                this.data = this.task.result
                console.log("step 4")
                this.animalsInfo = this.data.mouse
                for(let animal in this.animalsInfo) {
                  console.log(Object.keys(this.animalsInfo[animal]))
                  if(!"age" in Object.keys(this.animalsInfo[animal])){
                    this.animalsInfo[animal]['age'] = ""
                  }
                  if(!"sex" in Object.keys(this.animalsInfo[animal])){
                    this.animalsInfo[animal]['sex'] = ""
                  }
                  if(!"strain" in Object.keys(this.animalsInfo[animal])){
                    this.animalsInfo[animal]['strain'] = ""
                  }
                  if(!"setup" in Object.keys(this.animalsInfo[animal])){
                    this.animalsInfo[animal]['setup'] = ""
                  }
                  if(!"treatment" in Object.keys(this.animalsInfo[animal])){
                    this.animalsInfo[animal]['treatment'] = ""
                  }
                }
                this.fileURL = "http://127.0.0.1:8000/api/v1/files/".concat(this.data.file_url)
                break
              case 5:
                this.stepUp()
                this.tasksProgression = 0
                this.rebuildSQLiteFile()
                break
              case 6:
                console.log("step 6")
                this.messageStep6 = this.task.result
                this.stepUp()
                break
              case 8:
                console.log("step 8")
                // console.log(this.animalsInfo)
                this.results = this.task.result
                // // animal info update
                let index = 0
                for(let animal in this.results){
                    console.log(this.results[animal]['rfid'])
                    for(let infoAnimal in this.animalsInfo){
                        console.log(infoAnimal)
                        if(this.animalsInfo[infoAnimal]['RFID']==animal){
                            this.results[animal]['setup'] = this.animalsInfo[infoAnimal]['SETUP']
                            this.results[animal]['treatment'] = this.animalsInfo[infoAnimal]['TREATMENT']
                        }
                    }
                }
                // this.results.forEach((animal, index) => {
                //     console.log(animal)
                //   // this.results[animal]['setup'] = this.animalsInfo[index]['SETUP']
                //   // this.results[animal]['treatment'] = this.animalsInfo[index]['TREATMENT']
                // })
                this.stepUp()
                break

            // this.processing = false
            this.checked = true

            }

            // this.data['name_experiment'] = this.filename.split('.sqlite')[0]
            // this.downloadFile(this.data.file_id)
          }
          else {
            this.tasksProgression = this.task.progress.percent
            if((this.task.complete == true) && (this.task.success == false)) {
              console.log('error')
              // this.processing = false
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
    // selectReliability() {
    //   this.reliabilitySelected = true
    //   this.analysisSelected = false
    // },
    // selectAnalysis() {
    //   this.reliabilitySelected = false
    //   this.analysisSelected = true
    // },
    setDurationAnalysis() {
      console.log("changed")
      if(this.minT > 0 && this.unitMinT != ''){
        this.durationAnalysisStart = "From "+this.minT+" "+this.unitMinT
        this.sendMinT = this.minT+" "+this.unitMinT
        this.checkDurationForAnalysis()
      }
      else {
        this.durationAnalysisStart = "From the beginning"
        this.durationChecker = ''
      }
      if((this.maxT != "-" || this.maxT > 0) && this.unitMaxT != '') {
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
    },
    downloadFile(fileId) {
      axios.get(`http://127.0.0.1:8000/api/v1/files/${fileId}/`)
      .then(response => {
        // this.fileURL = window.URL.createObjectURL(new Blob([response.data]))
        var fileURL = window.URL.createObjectURL(new Blob([response.data]));
        var fileLink = document.createElement('a');

        fileLink.href = fileURL;
        fileLink.setAttribute('download', `${response.data.file_name}`);

        document.body.appendChild(fileLink);

        fileLink.click();
      })
      .catch(error => {
          console.log(JSON.stringify(error))
        })
    },
    checkReliability() {
      let formData = new FormData();
      formData.append('file_id', this.file_id)
      axios.post(`http://127.0.0.1:8000/api/v1/checkReliability/`, formData)
      .then(response => {
        this.task_id = response.data.task_id
        this.getProgression()
      })
      .catch(error => {
        console.log(JSON.stringify(error))
      })
    },
    stepToTimeLine() {
      switch (this.step){
        case 4:
          this.timelineItems["reliability"]["color"] = "green"
          break
        case 5:
          this.timelineItems["animalInfo"]["color"] = "purple"
          break
        case 6:
          this.timelineItems["rebuild"]["color"] = "red-lighten-1"
          break
        case 7:
          this.timelineItems["configAnalysis"]["color"] = "amber-lighten-1"
          break
        case 8:
          this.timelineItems["analysis"]["color"] = "cyan-lighten-1"
          break
        case 9:
          this.timelineItems["save"]["color"] = "indigo-lighten-2"
          break
      }
    },
    functionToShowReliability() {
      this.reliabilityModalOpen = !this.reliabilityModalOpen
    },
    stepUp() {
      this.step++
      this.stepToTimeLine()
    },
    stepDown() {
      this.step--
      this.stepToTimeLine()
    },
    saveAnimalInfo() {
      let formatedAnimalsInfo = {}
      for(let line in this.animalsInfo) {
          console.log(line)
          formatedAnimalsInfo[this.animalsInfo[line]["RFID"]] = this.animalsInfo[line]
      }
      let formData = new FormData();
      formData.append('file_id', this.file_id)
      formData.append('animalsInfo', JSON.stringify( this.animalsInfo))
      axios.post(`http://127.0.0.1:8000/api/v1/saveAnimalInfo/`, formData)
      .then(response => {
        this.task_id = response.data.task_id
        this.getProgression()
      })
      .catch(error => {
        console.log(JSON.stringify(error))
      })
    },
    rebuildSQLiteFile() {
      let formData = new FormData();
      formData.append('file_id', this.file_id)
      axios.post(`http://127.0.0.1:8000/api/v1/rebuild/`, formData)
      .then(response => {
        this.task_id = response.data.task_id
        this.getProgression()
      })
      .catch(error => {
        console.log(JSON.stringify(error))
      })
    },
    doAnalysis(preset){
      switch (preset){
        case 'simplePreset':
          let formData = new FormData();
          formData.append('file_id', this.file_id)
          formData.append('tmin', parseInt(this.minT))
          formData.append('tmax', parseInt(this.maxT))
          formData.append('unitMinT', this.unitMinT)
          formData.append('unitMaxT', this.unitMaxT)
          axios.post(`http://127.0.0.1:8000/api/v1/extractAnalysis/`, formData)
          .then(response => {
            console.log('Do analysis')
            // this.data = response.data.reliabilityContext
            this.task_id = response.data.task_id
            this.stepUp()
            this.getProgression()
            // console.log('success!!')

          }).catch(error => {
            console.log('FAILURE!!')
            console.log(JSON.stringify(error))
            this.error = true
          })
          break
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

</style>