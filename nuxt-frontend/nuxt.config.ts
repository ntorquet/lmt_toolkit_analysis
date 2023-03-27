// Created by Nicolas Torquet at 20/03/2023
// torquetn@igbmc.fr
// Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
// CNRS - Mouse Clinical Institute
// PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
// Code under GPL v3.0 licence

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    css: ['vuetify/lib/styles/main.sass', '@mdi/font/css/materialdesignicons.min.css'],
    // modules: ['@nuxtjs/axios'],
    // axios: {
    //     baseURL: 'http://localhost:8000'
    // },
    build: {
        transpile: ['vuetify', 'chart.js']
    }
})