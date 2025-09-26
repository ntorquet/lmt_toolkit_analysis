/*
Created by Nicolas Torquet at 25/09/2025
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
*/

import {ref} from 'vue';
import axios from 'axios';

const presets = ref({})

export function getPresets() {
  axios.get(`http://127.0.0.1:8000/api/presets/`)
  .then(response => {
    presets.value = response.data;
  })
  .catch(error => {
    console.log(JSON.stringify(error));
  })
  return presets;
}