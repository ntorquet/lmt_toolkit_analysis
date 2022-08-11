<template>
  <div>
      <div>
        <h1 class="title">Credits</h1>
        <div id="content">

            <h2 class="subtitle"><i class="long arrow alternate right icon"></i>LMT toolkit</h2>
            <p>
                LMT toolkit is developed by <a href="mailto:nicolas.torquet@igbmc.fr">Nicolas Torquet</a> (<a href="http://www.ics-mci.fr" target="_blank">Mouse Clinical Institute</a>).<br />
                <a href="https://github.com/ntorquet"><b-icon-github></b-icon-github> Github</a>
            </p>
            <br />
          <h2 class="subtitle"><i class="long arrow alternate right icon"></i>Live Mouse Tracker</h2>
            <p>
                Live Mouse Tracker (LMT) is developed by <a href="mailto:fabrice.de-chaumont@pasteur.fr">Fabrice de Chaumont</a> (<a href="https://www.pasteur.fr" target="_blank">Institut Pasteur</a>).<br />
                You can find <a href="https://livemousetracker.org/" target="_blank">here</a> some information about LMT.
            </p>
            <br />
            <br />
            <figure>
              <img src="@/assets/phenomin_ics.png" />
              <img src="@/assets/igbmc2009.png">
              <img src="@/assets/logo_cnrs.png">
              <img src="@/assets/logo_unistra.png">
              <img src="@/assets/logo-inserm-rvb.png">
            </figure>
        </div>
      </div>
    </div>
</template>

<script>
import {BIconGithub} from "bootstrap-icons-vue"
export default {
  name: "about",
  components: {
    'BIconGithub': BIconGithub,
  },
}
</script>

<style scoped>
figure{
  padding: 5em;
}
img{
  height: 5em;
  padding-left: 2em;
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
</style>