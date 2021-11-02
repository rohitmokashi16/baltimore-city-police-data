<template>
    <div>
    <div class="h2 row">
      <p>Baltimore City Police Data CMSC 636</p>
    </div>
     <div class="h6 row">
      <p>Powered By Vue</p>
    </div>
    <TabView/>
    </div>
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

