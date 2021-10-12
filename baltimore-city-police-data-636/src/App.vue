<template>
  <div id="app">
    <div class="h2 row">
      <p>Baltimore City Police Data CMSC 636</p>
    </div>
    <img alt="Vue logo" src="./assets/logo.png">
     <div class="h6 row">
      <p>Powered By Vue</p>
    </div>
    <TabView/>
  </div>
</template>

<script>
import TabView from './components/TabView.vue'
export default {
  name: 'App',
  components: {
    TabView
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
