<!--
Created by Nicolas Torquet at 12/07/2022
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->
<template>
  <nav class="navbar navbar-dark bg-dark">
    <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>LMT-Toolkit</strong></router-link>
    </div>
    <div class="navbar-menu">
        <div class="navbar-end">
          <a href="/reliability" class="navbar-item">Reliability</a>
          <a href="/results" class="navbar-item">Analysis</a>
          <a href="/files" class="navbar-item">File list</a>
          <a href="/documentation" target="_blank" class="navbar-item">Documentation</a>
          <a href="/versions" class="navbar-item">Version history</a>
        </div>
    </div>
  </nav>

  <section class="section">
      <router-view/>
  </section>

  <footer class="bg-dark text-center text-white">
    <p><router-link to="/about" class="text">About</router-link> - Copyright © CNRS - INSERM - UNISTRA - ICS - IGBMC 2022 - <router-link to="/versions">v1</router-link></p>
  </footer>
</template>

<style lang="scss">
h1{
  padding: 1em;
}
#app {
  //font-family: Avenir, Helvetica, Arial, sans-serif;
  //-webkit-font-smoothing: antialiased;
  //-moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  a{
    font-weight: bold;
    color:  #a6acaf ;

    &.router-link-exact-active {
      color:  #a6acaf ;
    }
  }
  a:hover{
    color: #FFFFFF;
  }
}

.navbar-item{
  text-decoration: none;
  padding: 30px;
}
.text{
  text-decoration: none;
}
.button{
  text-decoration: none;
}

footer{
  margin-top: 5em;
  padding: 2em;
  a{
    font-weight: bold;
    color:  #a6acaf  ;

    &.router-link-exact-active {
      color:  #a6acaf  ;
    }
  }
  a:hover{
    color: #FFFFFF;
  }
}
</style>
