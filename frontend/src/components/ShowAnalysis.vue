<!--
Created by Nicolas Torquet at 12/07/2022
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->
<template>
  <h3>Analysis</h3>
  <div class="position-relative">
    <b-alert show>
      Analysis of the experiment from frame number {{ tmin }} to frame number {{ tmax }}.<br />
      Period of analysis: {{ analysisPeriod }}
    </b-alert>
    <h4>Activity</h4>
    <table class="table table-striped table-hover">
      <thead>
      <tr>
        <th>RFID</th>
        <th>Name</th>
        <th>Sex</th>
        <th>Genotype</th>
        <th v-for="item in activity_variable">{{item}}</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(key, value) in data.profileData">
        <td>{{ value }}</td>
        <td>{{ key.animal }}</td>
        <td>{{ key.sex }}</td>
        <td>{{ key.genotype }}</td>
        <td>{{ key.totalDistance.toFixed(2) }}</td>
        <td>{{ key['Move isolated Nb'] }}</td>
        <td>{{ key['Move isolated TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Move isolated MeanDur'].toFixed(2) }}</td>
        <td>{{ key['Move in contact Nb'] }}</td>
        <td>{{ key['Move in contact TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Move in contact MeanDur'].toFixed(2) }}</td>
        <td>{{ key['Stop isolated Nb'] }}</td>
        <td>{{ key['Stop isolated TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Stop isolated MeanDur'].toFixed(2) }}</td>
      </tr>
      </tbody>
    </table>
    <b-row>
      <b-col cols="1"><ScatterPlot selection="Activity" :data="activity_data_distance" :labels="activity_variable_distance"></ScatterPlot></b-col>
      <b-col cols="3.5"><ScatterPlot selection="Activity" :data="activity_data_nb" :labels="activity_variable_nb"></ScatterPlot></b-col>
      <b-col cols="3.5"><ScatterPlot selection="Activity" :data="activity_data_total_length" :labels="activity_variable_total_length"></ScatterPlot></b-col>
      <b-col cols="3.5"><ScatterPlot selection="Activity" :data="activity_data_meandur" :labels="activity_variable_meandur"></ScatterPlot></b-col>
    </b-row>
  </div>

  <div>
    <h4>Exploration</h4>
    <table class="table table-striped table-hover">
      <thead>
      <tr>
        <th>RFID</th>
        <th>Name</th>
        <th>Sex</th>
        <th>Genotype</th>
        <th v-for="item in exploration_variable">{{item}}</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(key, value) in data.profileData">
        <td>{{ value }}</td>
        <td>{{ key.animal }}</td>
        <td>{{ key.sex }}</td>
        <td>{{ key.genotype }}</td>
        <td>{{ key['Rear isolated Nb'] }}</td>
        <td>{{ key['Rear isolated TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Rear isolated MeanDur'].toFixed(2) }}</td>
        <td>{{ key['Rear in contact Nb'] }}</td>
        <td>{{ key['Rear in contact TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Rear in contact MeanDur'].toFixed(2) }}</td>
      </tr>
      </tbody>
    </table>
    <b-row>
      <b-col><ScatterPlot selection="Exploration" :data="exploration_data_nb" :labels="exploration_variable_nb"></ScatterPlot></b-col>
      <b-col><ScatterPlot selection="Exploration" :data="exploration_data_total_length" :labels="exploration_variable_total_length"></ScatterPlot></b-col>
      <b-col><ScatterPlot selection="Exploration" :data="exploration_data_meandur" :labels="exploration_variable_meandur"></ScatterPlot></b-col>
    </b-row>
  </div>

  <div>
    <h4>Contacts</h4>
    <table class="table table-striped table-hover">
      <thead>
      <tr>
        <th>RFID</th>
        <th v-for="item in contacts_variable">{{item}}</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(key, value) in data.profileData">
        <td>{{ value }}</td>
        <td>{{ key['Contact Nb'] }}</td>
        <td>{{ key['Contact TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Contact MeanDur'].toFixed(2) }}</td>
        <td>{{ key['Group2 Nb'] }}</td>
        <td>{{ key['Group2 TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Group2 MeanDur'].toFixed(2) }}</td>
        <td>{{ key['Group3 Nb'] }}</td>
        <td>{{ key['Group3 TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Group3 MeanDur'].toFixed(2) }}</td>
        <td>{{ key['Oral-oral Contact Nb'] }}</td>
        <td>{{ key['Oral-oral Contact TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Oral-oral Contact MeanDur'].toFixed(2) }}</td>
        <td>{{ key['Oral-genital Contact Nb'] }}</td>
        <td>{{ key['Oral-genital Contact TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Oral-genital Contact MeanDur'].toFixed(2) }}</td>
        <td>{{ key['Side by side Contact Nb'] }}</td>
        <td>{{ key['Side by side Contact TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Side by side Contact MeanDur'].toFixed(2) }}</td>
        <td>{{ key['Side by side Contact, opposite way Nb'] }}</td>
        <td>{{ key['Side by side Contact, opposite way TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Side by side Contact, opposite way MeanDur'].toFixed(2) }}</td>
      </tr>
      </tbody>
    </table>
    <b-row>
      <b-col><ScatterPlot selection="Exploration" :data="contacts_data_nb" :labels="contacts_variable_nb"></ScatterPlot></b-col>
      <b-col><ScatterPlot selection="Exploration" :data="contacts_data_total_length" :labels="contacts_variable_total_length"></ScatterPlot></b-col>
      <b-col><ScatterPlot selection="Exploration" :data="contacts_data_meandur" :labels="contacts_variable_meandur"></ScatterPlot></b-col>
    </b-row>
  </div>

  <div>
    <h4>Follows</h4>
    <table class="table table-striped table-hover">
      <thead>
      <tr>
        <th>RFID</th>
        <th v-for="item in follows_variable">{{item}}</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(key, value) in data.profileData">
        <td>{{ value }}</td>
        <td>{{ key['Train2 Nb'] }}</td>
        <td>{{ key['Train2 TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Train2 MeanDur'].toFixed(2) }}</td>
        <td>{{ key['FollowZone Isolated Nb'] }}</td>
        <td>{{ key['FollowZone Isolated TotalLen'].toFixed(2) }}</td>
        <td>{{ key['FollowZone Isolated MeanDur'].toFixed(2) }}</td>
      </tr>
      </tbody>
    </table>
    <b-row>
      <b-col><ScatterPlot selection="Exploration" :data="follows_data_nb" :labels="follows_variable_nb"></ScatterPlot></b-col>
      <b-col><ScatterPlot selection="Exploration" :data="follows_data_total_length" :labels="follows_variable_total_length"></ScatterPlot></b-col>
      <b-col><ScatterPlot selection="Exploration" :data="follows_data_meandur" :labels="follows_variable_meandur"></ScatterPlot></b-col>
    </b-row>
  </div>

  <div>
    <h4>Approaches</h4>
    <table class="table table-striped table-hover">
      <thead>
      <tr>
        <th>RFID</th>
        <th v-for="item in approaches_variable">{{item}}</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(key, value) in data.profileData">
        <td>{{ value }}</td>
        <td>{{ key['Social approach Nb'] }}</td>
        <td>{{ key['Social approach TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Social approach MeanDur'].toFixed(2) }}</td>
        <td>{{ key['Approach contact Nb'] }}</td>
        <td>{{ key['Approach contact TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Approach contact MeanDur'].toFixed(2) }}</td>
        <td>{{ key['Group 3 make Nb'] }}</td>
        <td>{{ key['Group 4 make Nb'] }}</td>
      </tr>
      </tbody>
    </table>
    <b-row>
      <b-col><ScatterPlot selection="Exploration" :data="approaches_data_nb" :labels="approaches_variable_nb"></ScatterPlot></b-col>
      <b-col><ScatterPlot selection="Exploration" :data="approaches_data_total_length" :labels="approaches_variable_total_length"></ScatterPlot></b-col>
      <b-col><ScatterPlot selection="Exploration" :data="approaches_data_meandur" :labels="approaches_variable_meandur"></ScatterPlot></b-col>
    </b-row>
  </div>

  <div>
    <h4>Escapes</h4>
    <table class="table table-striped table-hover">
      <thead>
      <tr>
        <th>RFID</th>
        <th v-for="item in escapes_variable">{{item}}</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(key, value) in data.profileData">
        <td>{{ value }}</td>
        <td>{{ key['Break contact Nb'] }}</td>
        <td>{{ key['Break contact TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Break contact MeanDur'].toFixed(2) }}</td>
        <td>{{ key['Group 3 break Nb'] }}</td>
        <td>{{ key['Group 4 break Nb'] }}</td>
      </tr>
      </tbody>
    </table>
    <b-row>
      <b-col><ScatterPlot cols="8" selection="Exploration" :data="escapes_data_nb" :labels="escapes_variable_nb"></ScatterPlot></b-col>
      <b-col><ScatterPlot cols="1" selection="Exploration" :data="escapes_data_total_length" :labels="escapes_variable_total_length"></ScatterPlot></b-col>
      <b-col><ScatterPlot cols="1" selection="Exploration" :data="escapes_data_meandur" :labels="escapes_variable_meandur"></ScatterPlot></b-col>
    </b-row>
  </div>
  <div id="export">
    <b-button>
       <download-csv
           :data = "dataToCSV"
           :name = "name_csv+filename.split('.sqlite')[0]+'.csv'">
          Download Data as CSV file
       </download-csv>
    </b-button>
  </div>
</template>

<script>
import JsonCSV from 'vue-json-csv'
import ScatterPlot from "@/components/ScatterPlot"
export default {
  name: "ShowAnalysis",
  props: {
    filename: String,
    data: Object,
  },
  components: {
    'downloadCsv': JsonCSV,
    ScatterPlot,
  },
  data() {
    return {
      tmin: '',
      tmax: '',
      analysisPeriod: '',
      dataToCSV: [],
      name_csv: 'LMT_v1_0_3-toolkit_v0-1-2_',
      colorList: ['#8B0000', '#006400', '#9400D3', '#FFD700'  ,'#1E90FF', '#FF8C00'],
      analysis_parameters_variable: ['Start frame', 'End frame', 'Period of analysis'],
      analysis_parameters_data: [],
      activity_variable: ['Total distance (m)', 'Single move Nb', 'Single move TotalLen', 'Single move MeanDur', 'Move in contact Nb', 'Move in contact TotalLen',
      'Move in contact MeanDur', 'Stop isolated Nb', 'Stop isolated TotalLen', 'Stop isolated MeanDur'],
      activity_variable_distance: ['Total distance (m)'],
      activity_variable_nb: ['Single move Nb', 'Move in contact Nb', 'Stop isolated Nb'],
      activity_variable_total_length: ['Single move TotalLen', 'Move in contact TotalLen', 'Stop isolated TotalLen'],
      activity_variable_meandur: ['Single move MeanDur', 'Move in contact MeanDur', 'Stop isolated MeanDur'],
      activity_data: [],
      activity_data_distance: [],
      activity_data_nb: [],
      activity_data_total_length: [],
      activity_data_meandur: [],
      exploration_variable: ['Rear isolated Nb', 'Rear isolated TotalLen', 'Rear isolated MeanDur',
        'Rear in contact Nb', 'Rear in contact TotalLen', 'Rear in contact MeanDur'],
      exploration_variable_nb: ['Rear isolated Nb', 'Rear in contact Nb'],
      exploration_variable_total_length: ['Rear isolated TotalLen', 'Rear in contact TotalLen'],
      exploration_variable_meandur: ['Rear isolated MeanDur', 'Rear in contact MeanDur'],
      exploration_data: [],
      exploration_data_nb: [],
      exploration_data_total_length: [],
      exploration_data_meandur: [],
      contacts_variable: ['Contact Nb', 'Contact TotalLen', 'Contact MeanDur',
        'Group of 2 Nb', 'Group of 2 TotalLen', 'Group of 2 MeanDur', 'Group of 3 Nb', 'Group of 3 TotalLen', 'Group of 3 MeanDur',
        'Nose-nose Nb', 'Nose-nose TotalLen', 'Nose-nose MeanDur', 'Nose-anogenital Nb', 'Nose-anogenital TotalLen', 'Nose-anogenital MeanDur',
        'Side-side Nb', 'Side-side TotalLen', 'Side-side MeanDur', 'Side-side Head to tail Nb', 'Side-side Head to tail TotalLen', 'Side-side Head to tail MeanDur'
      ],
      contacts_variable_nb: ['Contact Nb',
        'Group of 2 Nb', 'Group of 3 Nb',
        'Nose-nose Nb', 'Nose-anogenital Nb',
        'Side-side Nb', 'Side-side Head to tail Nb'
      ],
      contacts_variable_total_length: ['Contact TotalLen', 'Group of 2 TotalLen', 'Group of 3 TotalLen',
        'Nose-nose TotalLen', 'Nose-anogenital TotalLen',
        'Side-side TotalLen', 'Side-side Head to tail TotalLen'
      ],
      contacts_variable_meandur: ['Contact MeanDur', 'Group of 2 MeanDur', 'Group of 3 MeanDur',
        'Nose-nose MeanDur', 'Nose-anogenital MeanDur',
        'Side-side MeanDur', 'Side-side Head to tail MeanDur'
      ],
      contacts_data: [],
      contacts_data_nb: [],
      contacts_data_total_length: [],
      contacts_data_meandur: [],
      follows_variable: ['Train 2 Nb', 'Train 2 TotalLen', 'Train 2 MeanDur', 'Follow Nb', 'Follow TotalLen', 'Follow MeanDur'],
      follows_variable_nb: ['Train 2 Nb', 'Follow Nb'],
      follows_variable_total_length: ['Train 2 TotalLen', 'Follow TotalLen'],
      follows_variable_meandur: ['Train 2 MeanDur', 'Follow MeanDur'],
      follows_data: [],
      follows_data_nb: [],
      follows_data_total_length: [],
      follows_data_meandur: [],
      approaches_variable: ['Social approach Nb', 'Social approach TotalLen', 'Social approach MeanDur',
        'Approach contact Nb', 'Approach contact TotalLen', 'Approach contact MeanDur', 'Group 3 make Nb', 'Group 4 make Nb'
      ],
      approaches_variable_nb: ['Social approach Nb', 'Approach contact Nb', 'Group 3 make Nb', 'Group 4 make Nb'],
      approaches_variable_total_length: ['Social approach TotalLen', 'Approach contact TotalLen'],
      approaches_variable_meandur: ['Social approach MeanDur', 'Approach contact MeanDur'],
      approaches_data: [],
      approaches_data_nb: [],
      approaches_data_total_length: [],
      approaches_data_meandur: [],
      escapes_variable: [
        'Break contact Nb',
        'Break contact TotalLen',
        'Break contact MeanDur',
        'Group 3 break Nb',
        'Group 4 break Nb',
      ],
      escapes_variable_nb: [
        'Break contact Nb',
        'Group 3 break Nb',
        'Group 4 break Nb',
      ],
      escapes_variable_total_length: [
        'Break contact TotalLen',
      ],
      escapes_variable_meandur: [
        'Break contact MeanDur',
      ],
      escapes_data: [],
      escapes_data_nb: [],
      escapes_data_total_length: [],
      escapes_data_meandur: [],
    }
  },
  methods: {
    convertJsonToCSVFormat() {
      let dataToConvert = this.data.profileData
      for(let mouse in dataToConvert){
        // console.log(dataToConvert[mouse])
        this.dataToCSV.push(dataToConvert[mouse])
      }
    },
  },
  mounted() {
    this.convertJsonToCSVFormat()
    let dataToConvert = this.data.profileData
    let index = 0
    for(let mouse in dataToConvert){
      this.tmin = dataToConvert[mouse]['Start frame']
      this.tmax = dataToConvert[mouse]['End frame']
      this.analysisPeriod = dataToConvert[mouse]['Period of analysis']
      // Analysis parameters
      this.analysis_parameters_data.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [dataToConvert[mouse]['Start frame'], dataToConvert[mouse]['End frame'], dataToConvert[mouse]['Period of analysis']],
            showLine: false
          }
      )
      // Activity
      this.activity_data.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [
                dataToConvert[mouse].totalDistance, dataToConvert[mouse]['Move isolated Nb'], dataToConvert[mouse]['Move isolated TotalLen'], dataToConvert[mouse]['Move isolated MeanDur'],
                dataToConvert[mouse]['Move in contact Nb'], dataToConvert[mouse]['Move in contact TotalLen'], dataToConvert[mouse]['Move in contact MeanDur'],
                dataToConvert[mouse]['Stop isolated Nb'], dataToConvert[mouse]['Stop isolated TotalLen'], dataToConvert[mouse]['Stop isolated MeanDur']
            ],
            showLine: false
          }
      )
      // Activity distance
      this.activity_data_distance.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [
                dataToConvert[mouse].totalDistance
            ],
            showLine: false
          }
      )
      // Activity number
      this.activity_data_nb.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [
                dataToConvert[mouse]['Move isolated Nb'],
                dataToConvert[mouse]['Move in contact Nb'],
                dataToConvert[mouse]['Stop isolated Nb']
            ],
            showLine: false
          }
      )
      // Activity totalLen
      this.activity_data_total_length.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [
                dataToConvert[mouse]['Move isolated TotalLen'],
                dataToConvert[mouse]['Move in contact TotalLen'],
                dataToConvert[mouse]['Stop isolated TotalLen']
            ],
            showLine: false
          }
      )
      // Activity meandur
      this.activity_data_meandur.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [
                dataToConvert[mouse]['Move isolated MeanDur'],
                dataToConvert[mouse]['Move in contact MeanDur'],
                dataToConvert[mouse]['Stop isolated MeanDur']
            ],
            showLine: false
          }
      )

      // Exploration
      this.exploration_data.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [dataToConvert[mouse]['Rear isolated Nb'], dataToConvert[mouse]['Rear isolated TotalLen'], dataToConvert[mouse]['Rear isolated MeanDur'],
              dataToConvert[mouse]['Rear in contact Nb'], dataToConvert[mouse]['Rear in contact TotalLen'], dataToConvert[mouse]['Rear in contact MeanDur']
            ],
            showLine: false
          }
      )
      // Exploration nb
      this.exploration_data_nb.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [dataToConvert[mouse]['Rear isolated Nb'], dataToConvert[mouse]['Rear in contact Nb']],
            showLine: false
          }
      )
      // Exploration totalLen
      this.exploration_data_total_length.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [dataToConvert[mouse]['Rear isolated TotalLen'], dataToConvert[mouse]['Rear in contact TotalLen']],
            showLine: false
          }
      )
      // Exploration meanDur
      this.exploration_data_meandur.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [dataToConvert[mouse]['Rear isolated MeanDur'], dataToConvert[mouse]['Rear in contact MeanDur']],
            showLine: false
          }
      )

      // Contacts
      this.contacts_data.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [dataToConvert[mouse]['Contact Nb'], dataToConvert[mouse]['Contact TotalLen'], dataToConvert[mouse]['Contact MeanDur'],
              dataToConvert[mouse]['Group2 Nb'], dataToConvert[mouse]['Group2 TotalLen'], dataToConvert[mouse]['Group2 MeanDur'],
              dataToConvert[mouse]['Group3 Nb'], dataToConvert[mouse]['Group3 TotalLen'], dataToConvert[mouse]['Group3 MeanDur'],
              dataToConvert[mouse]['Oral-oral Contact Nb'], dataToConvert[mouse]['Oral-oral Contact TotalLen'], dataToConvert[mouse]['Oral-oral Contact MeanDur'],
              dataToConvert[mouse]['Oral-genital Contact Nb'], dataToConvert[mouse]['Oral-genital Contact TotalLen'], dataToConvert[mouse]['Oral-genital Contact MeanDur'],
              dataToConvert[mouse]['Side by side Contact Nb'], dataToConvert[mouse]['Side by side Contact TotalLen'], dataToConvert[mouse]['Side by side Contact MeanDur'],
              dataToConvert[mouse]['Side by side Contact, opposite way Nb'], dataToConvert[mouse]['Side by side Contact, opposite way TotalLen'], dataToConvert[mouse]['Side by side Contact, opposite way MeanDur']
            ],
            showLine: false
          }
      )
      // Contacts nb
      this.contacts_data_nb.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [dataToConvert[mouse]['Contact Nb'],
              dataToConvert[mouse]['Group2 Nb'],
              dataToConvert[mouse]['Group3 Nb'],
              dataToConvert[mouse]['Oral-oral Contact Nb'],
              dataToConvert[mouse]['Oral-genital Contact Nb'],
              dataToConvert[mouse]['Side by side Contact Nb'],
              dataToConvert[mouse]['Side by side Contact, opposite way TotalLen']
            ],
            showLine: false
          }
      )
      // Contacts totalLen
      this.contacts_data_total_length.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [dataToConvert[mouse]['Contact TotalLen'],
              dataToConvert[mouse]['Group2 TotalLen'],
              dataToConvert[mouse]['Group3 TotalLen'],
              dataToConvert[mouse]['Oral-oral Contact TotalLen'],
              dataToConvert[mouse]['Oral-genital Contact TotalLen'],
              dataToConvert[mouse]['Side by side Contact TotalLen'],
              dataToConvert[mouse]['Side by side Contact, opposite way TotalLen']
            ],
            showLine: false
          }
      )
      // Contacts meanDur
      this.contacts_data_meandur.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [dataToConvert[mouse]['Contact MeanDur'],
              dataToConvert[mouse]['Group2 MeanDur'],
              dataToConvert[mouse]['Group3 MeanDur'],
              dataToConvert[mouse]['Oral-oral Contact MeanDur'],
              dataToConvert[mouse]['Oral-genital Contact MeanDur'],
              dataToConvert[mouse]['Side by side Contact MeanDur'],
              dataToConvert[mouse]['Side by side Contact, opposite way MeanDur']
            ],
            showLine: false
          }
      )

      // Follows
      this.follows_data.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [dataToConvert[mouse]['Train2 Nb'], dataToConvert[mouse]['Train2 TotalLen'], dataToConvert[mouse]['Train2 MeanDur'],
              dataToConvert[mouse]['FollowZone Isolated Nb'], dataToConvert[mouse]['FollowZone Isolated TotalLen'], dataToConvert[mouse]['FollowZone Isolated MeanDur']
            ],
            showLine: false
          }
      )
      // Follows nb
      this.follows_data_nb.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [dataToConvert[mouse]['Train2 Nb'],
              dataToConvert[mouse]['FollowZone Isolated Nb']
            ],
            showLine: false
          }
      )
      // Follows totalLen
      this.follows_data_total_length.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [dataToConvert[mouse]['Train2 TotalLen'],
              dataToConvert[mouse]['FollowZone Isolated TotalLen']
            ],
            showLine: false
          }
      )
      // Follows meanDur
      this.follows_data_meandur.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [dataToConvert[mouse]['Train2 MeanDur'],
              dataToConvert[mouse]['FollowZone Isolated MeanDur']
            ],
            showLine: false
          }
      )

      // Approaches
      this.approaches_data.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [dataToConvert[mouse]['Social approach Nb'], dataToConvert[mouse]['Social approach TotalLen'], dataToConvert[mouse]['Social approach MeanDur'],
              dataToConvert[mouse]['Approach contact Nb'], dataToConvert[mouse]['Approach contact TotalLen'], dataToConvert[mouse]['Approach contact MeanDur'],
              dataToConvert[mouse]['Group 3 make Nb'], dataToConvert[mouse]['Group 4 make Nb']
            ],
            showLine: false
          }
      )
      // Approaches nb
      this.approaches_data_nb.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [dataToConvert[mouse]['Social approach Nb'],
              dataToConvert[mouse]['Approach contact Nb'],
              dataToConvert[mouse]['Group 3 make Nb'], dataToConvert[mouse]['Group 4 make Nb']
            ],
            showLine: false
          }
      )
      // Approaches totalLen
      this.approaches_data_total_length.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [dataToConvert[mouse]['Social approach TotalLen'],
              dataToConvert[mouse]['Approach contact TotalLen']
            ],
            showLine: false
          }
      )
      // Approaches meanDur
      this.approaches_data_meandur.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [dataToConvert[mouse]['Social approach MeanDur'],
              dataToConvert[mouse]['Approach contact MeanDur']
            ],
            showLine: false
          }
      )

      // Escapes
      this.escapes_data.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [
              dataToConvert[mouse]['Break contact Nb'], dataToConvert[mouse]['Break contact TotalLen'], dataToConvert[mouse]['Break contact MeanDur'],
              dataToConvert[mouse]['Group 3 break Nb'], dataToConvert[mouse]['Group 4 break Nb']
            ],
            showLine: false
          }
      )
      // Escapes nb
      this.escapes_data_nb.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [
              dataToConvert[mouse]['Break contact Nb'],
              dataToConvert[mouse]['Group 3 break Nb'], dataToConvert[mouse]['Group 4 break Nb']
            ],
            showLine: false
          }
      )
      // Escapes totalLen
      this.escapes_data_total_length.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [
              dataToConvert[mouse]['Break contact TotalLen']
            ],
            showLine: false
          }
      )
      // Escapes meanDur
      this.escapes_data_meandur.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [
              dataToConvert[mouse]['Break contact MeanDur']
            ],
            showLine: false
          }
      )

      index += 1
    }
  },
}
</script>

<style scoped>
h3 {
  padding-top: 2em;
}

h4 {
  padding-top: 2em;
}

#export {
  padding: 2em;
}

</style>