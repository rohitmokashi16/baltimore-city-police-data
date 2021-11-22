<template>
<div>
    <b-tabs content-class="mt-3">
         <b-tab no-body title="D3 Progress">
           <D3Impl/>
                </b-tab>

      <b-tab no-body title="Python Progress">
          <Matplotlib/>
      </b-tab>

        </b-tabs>
    </div>
</template>

<script>
import D3Impl from './d3.vue';
import Matplotlib from './matplotlib.vue'

export default {
  components: {D3Impl, Matplotlib},
}
</script>

<style scoped>

</style>
