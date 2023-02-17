<!--
Created by Nicolas Torquet at 16/02/2023
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->
<template>
<!--  <b-container>-->
<!--    <div class="columns is-multiline">-->
<!--      <div class="column is-12">-->
        <h1 class="title">Saved SQLite databases</h1>
        <div v-if="files.length>0">
          <b-table ref="fileTable" striped hover :items="filesItems" :fields="fields">
            <template #cell(Download)="row">
              <b-button size="sm" :href="filesItems[row.index]['Link']">
                <b-icon-download></b-icon-download>
                 Download
              </b-button>
            </template>
            <template #cell(Delete)="row">
              <b-button size="sm" @click="deleteFile(files[row.index]['id'])">
                <b-icon-trash3></b-icon-trash3>
              </b-button>
            </template>
          </b-table>
        </div>
        <div v-else>
          <p>There is no SQLite database in LMT-toolkit</p>
        </div>

<!--      </div>-->
<!--    </div>-->
<!--  </b-container>-->
</template>

<script>
import {
  BIconDownload,
  BIconTrash3,
} from "bootstrap-icons-vue";
import axios from "axios";

export default {
  name: "Files",
  components: {
    BIconDownload,
    BIconTrash3,
  },
  data:function (){
		return{
      files: [],
      fields: ['File name', 'Start time rebuild', 'End time rebuild', 'Upload date', 'Download', 'Delete'],
      filesItems: [],
      downloadableLinks: [],
    }
  },
  methods: {
    getFiles() {
      this.files = []
      this.filesItems = []
      axios.get(`api/v1/files`)
      .then(response => {
        this.files = response.data
        this.organizeFiles()
      })
      .catch(error => {
          console.log(JSON.stringify(error))
      })
    },
    organizeFiles(){
      for(let i=0; i<this.files.length;i++){
        this.filesItems.push({
          'File name': this.files[i]['file_name'],
          'Start time rebuild': this.files[i]['tmin'],
          'End time rebuild': this.files[i]['tmax'],
          'Upload date': this.files[i]['created_at'],
          'Link': "http://127.0.0.1:8000/media"+this.files[i]['sqlite'].split('/media')[1],
        })
      }
    },
    deleteFile(fileId){
      console.log(`delete file ${fileId}`)
      axios.delete(`api/v1/files/${fileId}/`)
      .then(response => {
        this.getFiles()
        this.$refs.fileTable.refresh()
      })
      .catch(error => {
          console.log(JSON.stringify(error))
        })
    }
  },
  mounted() {
    this.getFiles()
  }
}
</script>

<style scoped>

</style>