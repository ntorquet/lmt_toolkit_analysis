<template>
  <h3>Analysis</h3>
  <p class="me-auto">Coucouc</p>
  <div class="position-relative">
    <h4>Activity</h4>
    <table class="table table-striped table-hover">
      <thead>
      <tr>
        <th>RFID</th>
        <th>Name</th>
        <th>Sex</th>
        <th>Genotype</th>
        <th>Total distance (m)</th>
        <th>Single move Nb</th>
        <th>Single move TotalLen</th>
        <th>Single move MeanDur</th>
        <th>Move in contact Nb</th>
        <th>Move in contact TotalLen</th>
        <th>Move in contact MeanDur</th>
        <th>Wall jumps Nb</th>
        <th>Wall jumps TotalLen</th>
        <th>Wall jumps MeanDur</th>
        <th>Stop isolated Nb</th>
        <th>Stop isolated TotalLen</th>
        <th>Stop isolated MeanDur</th>
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
        <th>Rear isolated Nb</th>
        <th>Rear isolated TotalLen</th>
        <th>Rear isolated MeanDur</th>
        <th>Rear in contact Nb</th>
        <th>Rear in contact TotalLen</th>
        <th>Rear in contact MeanDur</th>
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
  </div>

  <div>
    <h4>Contacts</h4>
    <table class="table table-striped table-hover">
      <thead>
      <tr>
        <th>RFID</th>
        <th>Name</th>
        <th>Sex</th>
        <th>Genotype</th>
        <th>Contact Nb</th>
        <th>Contact TotalLen</th>
        <th>Contact MeanDur</th>
        <th>Group of 2 Nb</th>
        <th>Group of 2 TotalLen</th>
        <th>Group of 2 MeanDur</th>
        <th>Group of 3 Nb</th>
        <th>Group of 3 TotalLen</th>
        <th>Group of 3 MeanDur</th>
        <th>Nose-nose Nb</th>
        <th>Nose-nose TotalLen</th>
        <th>Nose-nose MeanDur</th>
        <th>Nose-anogenital Nb</th>
        <th>Nose-anogenital TotalLen</th>
        <th>Nose-anogenital MeanDur</th>
        <th>Side-side Nb</th>
        <th>Side-side TotalLen</th>
        <th>Side-side MeanDur</th>
        <th>Side-side Head to tail Nb</th>
        <th>Side-side Head to tail TotalLen</th>
        <th>Side-side Head to tail MeanDur</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(key, value) in data.profileData">
        <td>{{ value }}</td>
        <td>{{ key.animal }}</td>
        <td>{{ key.sex }}</td>
        <td>{{ key.genotype }}</td>
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
  </div>

  <div>
    <h4>Follows</h4>
    <table class="table table-striped table-hover">
      <thead>
      <tr>
        <th>RFID</th>
        <th>Name</th>
        <th>Sex</th>
        <th>Genotype</th>
        <th>Train 2 Nb</th>
        <th>Train 2 TotalLen</th>
        <th>Train 2 MeanDur</th>
        <th>Follow Nb</th>
        <th>Follow TotalLen</th>
        <th>Follow MeanDur</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(key, value) in data.profileData">
        <td>{{ value }}</td>
        <td>{{ key.animal }}</td>
        <td>{{ key.sex }}</td>
        <td>{{ key.genotype }}</td>
        <td>{{ key['Train2 Nb'] }}</td>
        <td>{{ key['Train2 TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Train2 MeanDur'].toFixed(2) }}</td>
        <td>{{ key['FollowZone Isolated Nb'] }}</td>
        <td>{{ key['FollowZone Isolated TotalLen'].toFixed(2) }}</td>
        <td>{{ key['FollowZone Isolated MeanDur'].toFixed(2) }}</td>
      </tr>
      </tbody>
    </table>
  </div>

  <div>
    <h4>Approches</h4>
    <table class="table table-striped table-hover">
      <thead>
      <tr>
        <th>RFID</th>
        <th>Name</th>
        <th>Sex</th>
        <th>Genotype</th>
        <th>Social approach Nb</th>
        <th>Social approach TotalLen</th>
        <th>Social approach MeanDur</th>
        <th>Approach contact Nb</th>
        <th>Approach contact TotalLen</th>
        <th>Approach contact MeanDur</th>
        <th>Group 3 make Nb</th>
        <th>Group 3 make TotalLen</th>
        <th>Group 3 make MeanDur</th>
        <th>Group 4 make Nb</th>
        <th>Group 4 make TotalLen</th>
        <th>Group 4 make MeanDur</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(key, value) in data.profileData">
        <td>{{ value }}</td>
        <td>{{ key.animal }}</td>
        <td>{{ key.sex }}</td>
        <td>{{ key.genotype }}</td>
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
  </div>

  <div>
    <h4>Escapes</h4>
    <table class="table table-striped table-hover">
      <thead>
      <tr>
        <th>RFID</th>
        <th>Name</th>
        <th>Sex</th>
        <th>Genotype</th>
        <th>Get away Nb</th>
        <th>Get away TotalLen</th>
        <th>Get away MeanDur</th>
        <th>Break contact Nb</th>
        <th>Break contact TotalLen</th>
        <th>Break contact MeanDur</th>
        <th>Group 3 break Nb</th>
        <th>Group 3 break TotalLen</th>
        <th>Group 3 break MeanDur</th>
        <th>Group 4 break Nb</th>
        <th>Group 4 break TotalLen</th>
        <th>Group 4 break MeanDur</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(key, value) in data.profileData">
        <td>{{ value }}</td>
        <td>{{ key.animal }}</td>
        <td>{{ key.sex }}</td>
        <td>{{ key.genotype }}</td>
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
  </div>
  <b-button>
     <download-csv
         :data = "dataToCSV">
        Download Data as CSV file
     </download-csv>
  </b-button>
</template>

<script>
import JsonCSV from 'vue-json-csv'
export default {
  name: "ShowAnalysis",
  props: {
    filename: String,
    data: Object,
  },
  components: {
     'downloadCsv': JsonCSV
  },
  data() {
    return {
      dataToCSV: []
    }
  },
  methods: {
    convertJsonToCSVFormat() {
      let dataToConvert = this.data.profileData
      for(let mouse in dataToConvert){
        console.log(dataToConvert[mouse])
        this.dataToCSV.push(dataToConvert[mouse])
      }
    },
  },
  mounted() {
    this.convertJsonToCSVFormat()
  },
}
</script>

<style scoped>

</style>