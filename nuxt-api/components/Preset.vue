<!--
Created by Nicolas Torquet at 25/09/2025
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->

<script>
////////////////////////////////
// IMPORT
////////////////////////////////
import {ref} from "vue";
import axios from "axios";

////////////////////////////////
// PROPS
////////////////////////////////
const props = defineProps({
  preset: {
    type: Object,
    required: true,
  },
});

////////////////////////////////
// DATA
////////////////////////////////
const timeBin = ref(10);
const showDescription = ref(false);

////////////////////////////////
// METHODS
////////////////////////////////


// const doAnalysis = async () => {
//   formData.append('file_id', file_id.value);
//   formData.append('timeBin', parseInt(timeBin.value));
//   try {
//     const response = await axios.post(`http://127.0.0.1:8000/api/distancePerTimeBin/`, formData);
//     console.log('Do analysis activityPerTimeBinPreset');
//     task_id.value = response.data.task_id;
//     stepUp();
//     getProgression();
//   }
//   catch (error) {
//     console.log('FAILURE!!');
//     console.log(JSON.stringify(error));
//     error.value = true;
//   }
// }

const showPresetInfo = () => {
  showDescription.value = !showDescription.value;
}

</script>


<template>
  <v-card class="mt-4 mr-4" width="400">
    <v-card-title> Distance preset</v-card-title>
    <v-card-text>
      <v-alert class="mb-2">
        The distance preset will give you the activity (distance travelled in meters) by each animal. <br/>
        By default, the analysis will be done on the total duration of the experiment.<br/>
        You have to select a time bin to proceed.
      </v-alert>
      <v-text-field label="Time bin in minutes" type="number" v-model.number="timeBin"></v-text-field>

      <v-btn v-if="timeBin!=''"
      @click="doAnalysis('activityPerTimeBinPreset')">
      <v-icon icon="mdi-arrow-right-bold"></v-icon> Analyse
    </v-btn>
  </v-card-text>
  <v-card-actions>
    <v-spacer></v-spacer>
    <v-btn class="right-0" style="position: absolute; bottom: 0;" icon="mdi-information"
    @click="showPresetInfo"></v-btn>
  </v-card-actions>
  </v-card>

  <v-dialog v-model:max-width="showDescription">
    {{ props.data.description }}
  </v-dialog>
</template>


<style scoped>

</style>