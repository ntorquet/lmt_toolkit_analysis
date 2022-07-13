<template>
  <nav class="navbar navbar-dark bg-dark">
    <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>LMT-Toolkit analysis</strong></router-link>
    </div>
    <div class="navbar-menu">
        <div class="navbar-end">
          <a href="/results" class="navbar-item">Analysis</a>
        </div>
    </div>
  </nav>

  <section class="section">
      <router-view/>
  </section>

  <footer class="bg-dark text-center text-white">
      <p><router-link to="/about" class="text">About</router-link> - Copyright © ICS 2022</p>
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
