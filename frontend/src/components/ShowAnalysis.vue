<template>
  <h3>Analysis</h3>
  <div class="position-relative">
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
        <td>{{ key['WallJump Nb'] }}</td>
        <td>{{ key['WallJump TotalLen'].toFixed(2) }}</td>
        <td>{{ key['WallJump MeanDur'].toFixed(2) }}</td>
        <td>{{ key['Stop isolated Nb'] }}</td>
        <td>{{ key['Stop isolated TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Stop isolated MeanDur'].toFixed(2) }}</td>
      </tr>
      </tbody>
    </table>
    <ScatterPlot selection="Activity" :data="activity_data" :labels="activity_variable"></ScatterPlot>
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
    <ScatterPlot selection="Exploration" :data="exploration_data" :labels="exploration_variable"></ScatterPlot>
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
    <ScatterPlot selection="Exploration" :data="contacts_data" :labels="contacts_variable"></ScatterPlot>
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
    <ScatterPlot selection="Exploration" :data="follows_data" :labels="follows_variable"></ScatterPlot>
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
        <td>{{ key['Group 3 make TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Group 3 make MeanDur'].toFixed(2) }}</td>
        <td>{{ key['Group 4 make Nb'] }}</td>
        <td>{{ key['Group 4 make TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Group 4 make MeanDur'].toFixed(2) }}</td>
      </tr>
      </tbody>
    </table>
    <ScatterPlot selection="Exploration" :data="approaches_data" :labels="approaches_variable"></ScatterPlot>
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
        <td>{{ key['Get away Nb'] }}</td>
        <td>{{ key['Get away TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Get away MeanDur'].toFixed(2) }}</td>
        <td>{{ key['Break contact Nb'] }}</td>
        <td>{{ key['Break contact TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Break contact MeanDur'].toFixed(2) }}</td>
        <td>{{ key['Group 3 break Nb'] }}</td>
        <td>{{ key['Group 3 break TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Group 3 break MeanDur'].toFixed(2) }}</td>
        <td>{{ key['Group 4 break Nb'] }}</td>
        <td>{{ key['Group 4 break TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Group 4 break MeanDur'].toFixed(2) }}</td>
      </tr>
      </tbody>
    </table>
    <ScatterPlot selection="Exploration" :data="escapes_data" :labels="escapes_variable"></ScatterPlot>
  </div>
  <div id="export">
    <b-button>
       <download-csv
           :data = "dataToCSV">
          Download Data as CSV file
       </download-csv>
    </b-button>
  </div>
  <img src="@/assets/img_sap.jpg" />
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
      dataToCSV: [],
      colorList: ['#8B0000', '#006400', '#9400D3', '#FFD700'  ,'#1E90FF', '#FF8C00'],
      activity_variable: ['Total distance (m)', 'Single move Nb', 'Single move TotalLen', 'Single move MeanDur', 'Move in contact Nb', 'Move in contact TotalLen',
      'Move in contact MeanDur', 'Wall jumps Nb', 'Wall jumps TotalLen', 'Wall jumps MeanDur', 'Stop isolated Nb', 'Stop isolated TotalLen', 'Stop isolated MeanDur'],
      activity_data: [],
      exploration_variable: ['Rear isolated Nb', 'Rear isolated TotalLen', 'Rear isolated MeanDur',
        'Rear in contact Nb', 'Rear in contact TotalLen', 'Rear in contact MeanDur'],
      exploration_data: [],
      contacts_variable: ['Contact Nb', 'Contact TotalLen', 'Contact MeanDur',
        'Group of 2 Nb', 'Group of 2 TotalLen', 'Group of 2 MeanDur', 'Group of 3 Nb', 'Group of 3 TotalLen', 'Group of 3 MeanDur',
        'Nose-nose Nb', 'Nose-nose TotalLen', 'Nose-nose MeanDur', 'Nose-anogenital Nb', 'Nose-anogenital TotalLen', 'Nose-anogenital MeanDur',
        'Side-side Nb', 'Side-side TotalLen', 'Side-side MeanDur', 'Side-side Head to tail Nb', 'Side-side Head to tail TotalLen', 'Side-side Head to tail MeanDur'
      ],
      contacts_data: [],
      follows_variable: ['Train 2 Nb', 'Train 2 TotalLen', 'Train 2 MeanDur', 'Follow Nb', 'Follow TotalLen', 'Follow MeanDur'
      ],
      follows_data: [],
      approaches_variable: ['Social approach Nb', 'Social approach TotalLen', 'Social approach MeanDur',
        'Approach contact Nb', 'Approach contact TotalLen', 'Approach contact MeanDur', 'Group 3 make Nb', 'Group 3 make TotalLen', 'Group 3 make MeanDur',
        'Group 4 make Nb', 'Group 4 make TotalLen', 'Group 4 make MeanDur'
      ],
      approaches_data: [],
      escapes_variable: ['Get away Nb',
        'Get away TotalLen',
        'Get away MeanDur',
        'Break contact Nb',
        'Break contact TotalLen',
        'Break contact MeanDur',
        'Group 3 break Nb',
        'Group 3 break TotalLen',
        'Group 3 break MeanDur',
        'Group 4 break Nb',
        'Group 4 break TotalLen',
        'Group 4 break MeanDur'
      ],
      escapes_data: [],
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
                dataToConvert[mouse]['WallJump Nb'], dataToConvert[mouse]['WallJump TotalLen'], dataToConvert[mouse]['WallJump MeanDur'],
                dataToConvert[mouse]['Stop isolated Nb'], dataToConvert[mouse]['Stop isolated TotalLen'], dataToConvert[mouse]['Stop isolated MeanDur']
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

      // Approaches
      this.approaches_data.push(
          {
            label: mouse,
            fill: false,
            borderColor: this.colorList[index],
            backgroundColor: this.colorList[index],
            data: [dataToConvert[mouse]['Social approach Nb'], dataToConvert[mouse]['Social approach TotalLen'], dataToConvert[mouse]['Social approach MeanDur'],
              dataToConvert[mouse]['Approach contact Nb'], dataToConvert[mouse]['Approach contact TotalLen'], dataToConvert[mouse]['Approach contact MeanDur'],
              dataToConvert[mouse]['Group 3 make Nb'], dataToConvert[mouse]['Group 3 make TotalLen'], dataToConvert[mouse]['Group 3 make MeanDur'],
              dataToConvert[mouse]['Group 4 make Nb'], dataToConvert[mouse]['Group 4 make TotalLen'], dataToConvert[mouse]['Group 4 make MeanDur']
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
            data: [ dataToConvert[mouse]['Get away Nb'], dataToConvert[mouse]['Get away TotalLen'], dataToConvert[mouse]['Get away MeanDur'],
              dataToConvert[mouse]['Break contact Nb'], dataToConvert[mouse]['Break contact TotalLen'], dataToConvert[mouse]['Break contact MeanDur'],
              dataToConvert[mouse]['Group 3 break Nb'], dataToConvert[mouse]['Group 3 break TotalLen'], dataToConvert[mouse]['Group 3 break MeanDur'],
              dataToConvert[mouse]['Group 4 break Nb'], dataToConvert[mouse]['Group 4 break TotalLen'], dataToConvert[mouse]['Group 4 break MeanDur']
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
h4 {
  padding-top: 2em;
}

#export {
  padding: 2em;
}

</style>