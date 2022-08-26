<template>
  <h1 class="title">Version history</h1>
  <b-card title="Why this page is important" class="card_info">
    LMT-toolkit uses the LMT-analysis code provided on GitHub <a href="https://github.com/fdechaumont/lmt-analysis" target="_blank">here</a>.<br />
    This code can changed to improve analysis or to correct bugs. As a <strong>LMT-toolkit</strong> user, you should know if you can compare data from different version of the code.<br />
    Some important changes will impact the results. This page gives you an history of all changes so that you know if a new analysis is needed.
  </b-card>

  <table class="table table-striped table-hover">
    <thead>
      <tr>
        <th style="width: 5%">Version</th>
        <th style="width: 10%">Date</th>
        <th>Changes / Notes</th>
      </tr>
    </thead>
    <tr>
      <td>v0.1</td>
      <td>2022 august</td>
      <td>
        <strong>Initial version</strong>:<br />
        Initial code for reliability. Analysis code is a fork of <a href="https://github.com/fdechaumont/lmt-analysis" target="_blank">lmt-analysis</a> on July 13, 2022.
      </td>
    </tr>
  </table>
</template>

<script>
export default {
  name: "VersionHistory"
}
</script>

<style scoped>
.card_info {
  margin: auto;
  width: 100em;
}

table {
  margin: 2.5%;
  width: 95%;
}

</style>