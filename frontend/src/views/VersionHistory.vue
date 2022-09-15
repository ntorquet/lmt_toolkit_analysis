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
        <th>Release</th>
      </tr>
    </thead>
    <tr>
      <td>v0.1</td>
      <td>2022 september</td>
      <td>
        <strong>Pre release version</strong>:<br />
        Initial code for reliability. Analysis code is a fork of <a href="https://github.com/fdechaumont/lmt-analysis" target="_blank">lmt-analysis</a> on July 13, 2022.
      </td>
      <td><a href="https://github.com/ntorquet/lmt_toolkit_analysis/releases/tag/v0.1" target="_blank"><b-icon-github></b-icon-github> LMT-toolkit analysis v0.1</a></td>
    </tr>
  </table>
</template>

<script>
import {BIconGithub} from "bootstrap-icons-vue"
export default {
  name: "VersionHistory",
  components: {
    'BIconGithub': BIconGithub,
  },
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