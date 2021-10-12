<template>
<div>
    <b-tabs content-class="mt-3">
         <b-tab no-body title="Picture 1">
           <D3Impl/>
                </b-tab>

      <b-tab no-body title="Picture 2">
          <Tableau/>
      </b-tab>

      <b-tab no-body title="Picture 3">
          <Matplotlib/>
      </b-tab>

        </b-tabs>
    </div>
</template>

<script>
import D3Impl from './d3.vue';
import Tableau from './tableu.vue';
import Matplotlib from './matplotlib.vue'

export default {
  components: {D3Impl, Tableau, Matplotlib},
}
</script>

<style scoped>

</style>
