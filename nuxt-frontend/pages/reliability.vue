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
      <div v-if="!checked && !uploading && !processing">
        <p>To check the experiment, you have to select a LMT SQLite file:</p>
        <div class="file">
          <label class="file-label">
            <v-file-input
                accept="sqlite"
                label="Select a file"
            ></v-file-input>
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
  name: "reliability"
}
</script>

<style scoped>

</style>