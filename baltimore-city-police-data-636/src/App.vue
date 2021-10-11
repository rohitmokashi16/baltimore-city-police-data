<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
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
