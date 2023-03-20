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
                <td>{{ file.tmin }}</td>
                <td>{{ file.tmax }}</td>
                <td>{{ file.created_at }}</td>
                <td>
                  <v-btn size="sm" :href="filesItems[index]['Link']">
                    <v-icon icon="mdi-download"></v-icon>
                     Download
                  </v-btn>
                </td>
                <td>
                  <v-btn size="sm" @click="deleteFile(files[index]['id'])">
                    <v-icon icon="mdi-delete"></v-icon>
                  </v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>


          <v-table ref="fileTable" striped hover :items="filesItems" :fields="fields">
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
  </v-main>
</template>

<script>
import axios from "axios";
export default {
  name: "files",
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
      axios.get(`http://127.0.0.1:8000/api/v1/files`)
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
      axios.delete(`http://127.0.0.1:8000/api/v1/files/${fileId}/`)
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