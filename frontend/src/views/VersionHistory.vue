<!--
Created by Nicolas Torquet at 12/07/2022
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->
<template>
  <h1 class="title">Version history</h1>
  <b-card title="Why this page is important" class="card_info">
    LMT-toolkit uses the LMT-analysis code provided on GitHub <a href="https://github.com/fdechaumont/lmt-analysis" target="_blank">here</a>.<br />
    This code can changed to improve analysis or to correct bugs. As a <strong>LMT-toolkit</strong> user, you should know if you can compare data from different version of the code.<br />
    Some important changes will impact the results. This page gives you an history of all changes so that you know if a new analysis is needed.
  </b-card>
  <br />
  <b-container>
    <b-table-simple hover small caption-top responsive>
      <b-thead>
        <b-tr>
          <b-th style="width: 5%">Version</b-th>
          <b-th style="width: 10%">Date</b-th>
          <b-th>LMT-toolkit Changes / Notes</b-th>
          <b-th>LMT-analysis Changes / Notes</b-th>
          <b-th>LMT-analysis release</b-th>
        </b-tr>
      </b-thead>
      <b-tbody>
        <b-tr>
          <b-td valign="middle">
            <a href="https://github.com/ntorquet/lmt_toolkit_analysis/releases/tag/v0.1.3" target="_blank">
            <b-badge variant="dark" pill><b-icon-github></b-icon-github> v0.1.3</b-badge></a>
          </b-td>
          <b-td valign="middle">2022 October</b-td>
          <b-td>
            <b-list-group>
              <b-list-group-item>Reliability section added</b-list-group-item>
              <b-list-group-item>Selection of events changed</b-list-group-item>
              <b-list-group-item>Documentation updated</b-list-group-item>
              <b-list-group-item>CSV results file with version name of LMT-toolkit and the name of the experiment</b-list-group-item>
              <b-list-group-item>Bugs corrections</b-list-group-item>
            </b-list-group>
          </b-td>
          <b-td>
            No changes
          </b-td>
          <b-td valign="middle">
            <a href="https://github.com/fdechaumont/lmt-analysis/releases/tag/v1.0.3" target="_blank"><b-badge variant="secondary" pill><b-icon-github></b-icon-github> v1.0.3</b-badge></a>
          </b-td>
        </b-tr>
        <b-tr>
          <b-td valign="middle">
            <a href="https://github.com/ntorquet/lmt_toolkit_analysis/releases/tag/v0.1.2" target="_blank">
            <b-badge variant="dark" pill><b-icon-github></b-icon-github> v0.1.2</b-badge></a>
          </b-td>
          <b-td valign="middle">2022 October</b-td>
          <b-td>
            Version updates
          </b-td>
          <b-td>
            No changes
          </b-td>
          <b-td valign="middle">
            <a href="https://github.com/fdechaumont/lmt-analysis/releases/tag/v1.0.3" target="_blank"><b-badge variant="secondary" pill><b-icon-github></b-icon-github> v1.0.3</b-badge></a>
          </b-td>
        </b-tr>
        <b-tr>
          <b-td valign="middle">
            <a href="https://github.com/ntorquet/lmt_toolkit_analysis/releases/tag/v0.1.1" target="_blank">
            <b-badge variant="dark" pill><b-icon-github></b-icon-github> v0.1.1</b-badge></a>
          </b-td>
          <b-td valign="middle">2022 october</b-td>
          <b-td>
            <strong>Pre release version</strong>:<br />
            Wrong message color if temperature higher than 26°C corrected<br />
            BootstrapVue3 updated to v0.3.11
          </b-td>
          <b-td>
            LMT-analysis upgraded (v1.0.0 to v1.0.3):
            <b-list-group>
              <b-list-group-item class="d-flex justify-content-between align-items-center">
                Event "approach contact" corrected
                <a href="https://github.com/fdechaumont/lmt-analysis/releases/tag/v1.0.1" target="_blank"><b-badge variant="secondary" pill><b-icon-github></b-icon-github> v1.0.1</b-badge></a>
              </b-list-group-item>
              <b-list-group-item class="d-flex justify-content-between align-items-center">
                Events "follow zone" and "side walk" updated: they no longer compute on a detection where the head and tail are not detected
                <a href="https://github.com/fdechaumont/lmt-analysis/releases/tag/v1.0.1" target="_blank"><b-badge variant="secondary" pill><b-icon-github></b-icon-github> v1.0.1</b-badge></a>
              </b-list-group-item>
              <b-list-group-item class="d-flex justify-content-between align-items-center">
                Fix a problem with the Nest3_ event. The stop condition necessary is now considered correctly
                <a href="https://github.com/fdechaumont/lmt-analysis/releases/tag/v1.0.2" target="_blank"><b-badge variant="secondary" pill><b-icon-github></b-icon-github> v1.0.2</b-badge></a>
              </b-list-group-item>
              <b-list-group-item class="d-flex justify-content-between align-items-center">
                Fix an head/tail problem condition in the followzone event
                <a href="https://github.com/fdechaumont/lmt-analysis/releases/tag/v1.0.3" target="_blank"><b-badge variant="secondary" pill><b-icon-github></b-icon-github> v1.0.3</b-badge></a>
              </b-list-group-item>
            </b-list-group>
          </b-td>
          <b-td valign="middle">
            <a href="https://github.com/fdechaumont/lmt-analysis/releases/tag/v1.0.3" target="_blank"><b-badge variant="secondary" pill><b-icon-github></b-icon-github> v1.0.3</b-badge></a>
          </b-td>
        </b-tr>
        <b-tr>
          <b-td valign="middle">
            <a href="https://github.com/ntorquet/lmt_toolkit_analysis/releases/tag/v0.1" target="_blank">
            <b-badge variant="dark" pill><b-icon-github></b-icon-github> v0.1</b-badge></a>
          </b-td>
          <b-td valign="middle">2022 september</b-td>
          <b-td>
            <strong>Pre release version</strong><br />
          </b-td>
          <b-td>
            Initial code for reliability. Analysis code is a fork of <a href="https://github.com/fdechaumont/lmt-analysis" target="_blank">lmt-analysis</a> on July 13, 2022.
          </b-td>
          <b-td valign="middle">Pre release corresponding to <a href="https://github.com/fdechaumont/lmt-analysis/releases/tag/v1.0.0" target="_blank"><b-badge variant="secondary" pill><b-icon-github></b-icon-github> v1.0.0</b-badge></a></b-td>
        </b-tr>
      </b-tbody>
    </b-table-simple>
  </b-container>
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

b-table-simple {
  margin: 2.5%;
  width: 95%;
}


</style>