<template>
<h1 class="title">Welcome to LMT-toolkit</h1>
    <div class="content">
      <p><strong><a href="https://livemousetracker.org/" target="_blank">Live Mouse Tracker (LMT)</a></strong> is a powerful tool to investigate the behavior of mice and in particular their social behavior.<br />
        <strong>LMT</strong> provides tracking data in a database as a SQLite file. Exploiting them requires computer skills.<br />
        <strong>LMT-toolkit</strong> was created to help LMT users to explore their own data autonomously. <strong>LMT-toolkit</strong>
        allows to check the reliability of the LMT experiments and extract behavioral data.<br />
        The data extracted during the processing can be downloaded into a CSV file for each experiment.<br />
        In the future, <strong>LMT-toolkit</strong> will also offer the possibility to organise and manage LMT experiments for each project.
      </p>

      <b-card-group deck>
        <b-card header="Reliability" header-front-weight="bold" class="card_info">
          <b-icon-check2-square></b-icon-check2-square> LMT-toolkit checks the reliability of your experiments:
          rate of detection, identity corrections and whenever available through the sensor temperature, humidity, light and ambient noise.
        </b-card>
        <b-card header="Analysis" class="card_info">
          <b-icon-graph-up></b-icon-graph-up> LMT-toolkit processes LMT experiments automatically, using the Python code
          available on Github (<a href="https://github.com/fdechaumont/lmt-analysis" target="_blank"><b-icon-github></b-icon-github> https://github.com/fdechaumont/lmt-analysis</a>).<br />
          LMT-toolkit extracts the total duration, the number of occurrences and the mean duration of each occurrence
          for the behaviors described <a href="https://livemousetracker.org/" target="_blank">here</a>.<br />
          Please visit the <router-link to="/versions">version history page</router-link> for information about the code used.
        </b-card>
      </b-card-group>
      <h2><a href="/results">Try now !</a></h2>
    </div>
</template>

<script>
import {
  BIconGithub,
  BIconCheck2Square,
  BIconGraphUp,
} from "bootstrap-icons-vue"
export default {
  name: 'HomeView',
  components: {
    'BIconGithub': BIconGithub,
    'BIconCheck2Square': BIconCheck2Square,
    'BIconGraphUp': BIconGraphUp,
  }
}
</script>
<style scoped>
.card_info {
  margin: 1em;
}

a{
  font-weight: bold;
  color:   #797d7f ;
  text-decoration: none;
}
a:hover{
  color: #000000;
  text-decoration: underline;
}
h2 {
  padding-top: 2em;
}
</style>