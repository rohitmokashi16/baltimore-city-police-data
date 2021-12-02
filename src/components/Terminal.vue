<template>
    <b-card>
      <b-card-text class="h2 row ml-6">Baltimore City Police Data CMSC 636</b-card-text>
      <b-card-text class="h6 row ml-6">Powered By Vue, D3.js, Flask, MatPlotLib, and a prayer</b-card-text>
      <TabView/>
    </b-card>
</template>
<script>
import TabView from './TabView.vue'
export default {
  name: 'App',
  components: {
    TabView
  }
}
</script>

