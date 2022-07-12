<template>
  <b-container>
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">Check the reliability of an experiment</h1>
        <div v-if="!checked && !uploading && !processing">
          <p>To get information about the reliability of the experiment, you have to select a LMT SQLite file:</p>
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
                  {{ file.name }}
                </span>
              </span>
            </label>
          </div>
        </div>
        <br />
        <div class="block" v-if="file && !uploading && !checked">
          <b-button class="button is-success" @click="upload">Check the experiment</b-button>
        </div>

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
    <show-reliability v-bind:data="data" v-bind:filename="file.name"></show-reliability>
  </div>
</template>

<script>
import axios from "axios"
import ShowReliability from "@/components/ShowReliability"
import { BIconFileEarmarkPlus } from 'bootstrap-icons-vue'

export default {
  name: "reliability",
  components: {
    ShowReliability,
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

      // chunk test
      // let size = 1024 * 50  //50KB slice size
      // let fileChunks = []
      // let index = 0 //Slice serial number
      // for(let cur = 0; cur < this.file.size; cur += size){
      //     fileChunks.push({
      //         hash: index++,
      //         chunk: file.slice(cur, cur + size)
      //     })
      // }
      // // Upload slice
      // const uploadList = fileChunks.map((item, index) => {
      //     let formData = new FormData()
      //     formData.append('filename', this.file.name)
      //     formData.append('hash', item.hash)
      //     formData.append('chunk', item.chunk)
      //     return axios({
      //         method: 'post',
      //         url: '/upload',
      //         data: formData
      //     })
      // })
      // await Promise.all(uploadList)
      // // Merge slices
      // await axios({
      //     method: 'POST',
      //     url: '/api/v1/read_file/`',
      //     params: {
      //         filename: file.name
      //     }
      // });
      //
      // for (const [ i, item ] of this.convertedArr.entries()) {
      //   if (this.uploadSuccess === false) return null
      //
      //   try {
      //     await axios({
      //       url: `/api/v1/read_file/`,
      //       method: 'POST',
      //       data: [item]
      //     });
      //   } catch (error) {
      //     console.log(error)
      //   } finally {
      //     if (parseInt(i) === this.convertedArr.length - 1) {
      //       this.nextFunction();
      //     }
      //   }
      // }


      axios.post(`/api/v1/analyse_reliability/`, formData, {
        onUploadProgress: function (progressEvent) {
          this.selectFile = false
          this.uploading = true
          this.uploadPercentage = parseInt(Math.round((progressEvent.loaded / progressEvent.total) * 100))
          // if(this.uploadPercentage == 100) {
          //   this.processing = true
          // }
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
	}


}
</script>

<style scoped>

</style>





<!--<template>-->
<!--  <div class="page-strain">-->
<!--    <div class="columns is-multiline">-->
<!--      <div class="column is-12">-->
<!--        <h1 class="title">Check the reliability of an experiment</h1>-->
<!--        <div v-if="!checked && !uploading">-->
<!--          <p>To get information about the reliability of the experiment, you have to select a LMT SQLite file:</p>-->
<!--          <div class="file">-->
<!--            <label class="file-label">-->
<!--              <input class="form-file" type="file" name="file" @change="onFilePicked($event)">-->
<!--              <span class="file-cta">-->
<!--                <span class="file-icon">-->
<!--                  <i class="fas fa-upload"></i>-->
<!--                </span>-->
<!--                <span class="file-label" v-if="!file">-->
<!--                  <strong> Choose a SQLite file…</strong>-->
<!--                </span>-->
<!--                <span v-else>-->
<!--                  {{ file.name }}-->
<!--                </span>-->
<!--              </span>-->
<!--            </label>-->
<!--          </div>-->
<!--        </div>-->
<!--        <br />-->
<!--        <div class="block" v-if="file && !uploading && !checked">-->
<!--          <b-button class="button is-success" @click="upload">Check the experiment</b-button>-->
<!--        </div>-->

<!--        <div class="block" v-if="uploading && !checked">-->
<!--          <b-spinner label="Loading..."></b-spinner> {{ file.name }}: the file is being processed. Please wait.-->
<!--        </div>-->


<!--      </div>-->
<!--    </div>-->
<!--  </div>-->

<!--  <div v-if="checked">-->
<!--    <show-reliability v-bind:data="data" v-bind:filename="file.name"></show-reliability>-->
<!--  </div>-->
<!--</template>-->

<!--<script>-->
<!--import axios from "axios"-->
<!--import ShowReliability from "@/components/ShowReliability"-->
<!--import { BIconFileEarmarkPlus } from 'bootstrap-icons-vue'-->

<!--export default {-->
<!--  name: "reliability",-->
<!--  components: {-->
<!--    ShowReliability,-->
<!--    'BIconFileEarmarkPlus': BIconFileEarmarkPlus,-->
<!--  },-->
<!--	data:function (){-->
<!--		return{-->
<!--      file: '',-->
<!--      uploading: false,-->
<!--      checked: false,-->
<!--      showReliability: false,-->
<!--      data: {},-->
<!--      filename: '',-->
<!--      // rfidDetection: Object,-->
<!--      // about_rfid_detections: Object,-->
<!--      // match_mismatch_proportion: Object,-->
<!--		}-->
<!--	},-->
<!--	methods:{-->
<!--    onFilePicked (event) {-->
<!--      const files = event.target.files-->
<!--      let filename = files[0].name-->

<!--      if(filename.includes(".sqlite"))-->
<!--      {-->
<!--        this.file = files[0]-->
<!--      }-->
<!--      else-->
<!--      {-->
<!--        this.file = ''-->
<!--        this.$toast.error('Wrong file: we must select a SQLite file')-->
<!--      }-->
<!--    },-->
<!--    upload() {-->
<!--      this.uploading = true-->
<!--      let formData = new FormData();-->
<!--      // formData.append("file_name", this.file.name)-->
<!--      // formData.append("loc", this.file)-->
<!--      formData.append('file', this.file)-->
<!--      // axios.post("/api/v1/analyse_reliability/", formData)-->
<!--      axios.post(`/api/v1/read_file/`, formData,-->
<!--          {-->
<!--            headers: {-->
<!--              // 'Access-Control-Allow-Origin': '*',-->
<!--              // 'Content-Disposition': 'attachment',-->
<!--              // 'X-CSRFToken': await this.getCsrfToken(),-->
<!--            },-->
<!--          })-->
<!--      .then(response => {-->
<!--        console.log('success!!')-->
<!--        console.log(response.data.response)-->
<!--        this.filename = response.data.filename-->
<!--        this.checked = true-->
<!--        this.data = response.data.reliabilityContext-->
<!--        // this.rfidDetection = response.data.rfidDetection-->
<!--        // this.about_rfid_detections = response.data.about_rfid_detections-->
<!--        // this.match_mismatch_proportion = response.data.match_mismatch_proportion-->

<!--      }).catch(error => {-->
<!--          console.log('FAILURE!!')-->
<!--          console.log(JSON.stringify(error))-->
<!--      })-->
<!--    },-->
<!--    submitForm: function() {-->
<!--      axios({-->
<!--        method : "POST",-->
<!--        url:"read_file/", //django path name-->
<!--        headers: {'Content-Disposition': 'attachment'},-->
<!--        data : {"file": this.file},//data-->
<!--      }).then(response => {-->
<!--        console.log('success!!')-->
<!--        this.checking = true-->

<!--      }).catch(error => {-->
<!--          console.log('FAILURE!!')-->
<!--          console.log(JSON.stringify(error))-->
<!--      })-->
<!--    }-->
<!--	}-->


<!--}-->
<!--</script>-->

<!--<style scoped>-->

<!--</style>-->