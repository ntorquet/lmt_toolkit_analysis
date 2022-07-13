<template>
  <h4>Analysis</h4>
    <div id="animals">
    <table id="animalTable" class="table">
      <thead>
      <tr>
        <th>RFID</th>
        <th>Name</th>
        <th>Sex</th>
        <th>Genotype</th>
        <th>Distance (m)</th>
        <th>Number of contact</th>
        <th>Total time in contact</th>
        <th>Contact MeanDur</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(key, value) in data.distanceAndTimeInContact">
        <td>{{ value }}</td>
        <td>{{ key.animal }}</td>
        <td>{{ key.sex }}</td>
        <td>{{ key.genotype }}</td>
        <td>{{ key.totalDistance.toFixed(2) }}</td>
        <td>{{ key['Contact Nb'] }}</td>
        <td>{{ key['Contact TotalLen'].toFixed(2) }}</td>
        <td>{{ key['Contact MeanDur'].toFixed(2) }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "ShowAnalysis",
  props: {
    filename: String,
    data: Object,
  },
}
</script>

<style scoped>

</style>