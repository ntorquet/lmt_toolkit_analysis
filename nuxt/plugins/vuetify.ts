// Created by Nicolas Torquet at 20/03/2023
// torquetn@igbmc.fr
// Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
// CNRS - Mouse Clinical Institute
// PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
// Code under GPL v3.0 licence


import {createVuetify} from "vuetify"
import * as components from "vuetify/components"
import * as directives from "vuetify/directives"

export default defineNuxtPlugin(nuxtApp => {
    const vuetify = createVuetify({
        components,
        directives
    })

    nuxtApp.vueApp.use(vuetify)
})