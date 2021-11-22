<template>
    <div class="justify-content-center align-center">
        <Tableau 
            :url="url" 
            :height="1000" 
            :width="1000" 
            :filters="{
                'Storm Name': ['CELIA', 'BLAS', 'AGATHA'], 'Basin': 'East Pacific' 
                }" 
            ref="tableau">
        </Tableau>
    </div>
</template>

<script>

export default {
    data() {
        return {
            msg: 'Hello Tableau Fans!',
            url: "http://public.tableau.com/views/RegionalSampleWorkbook/Storms"
        };
    },
    methods: {
      
    },
    mounted () {
    }
}

</script>

<style scoped>

</style>
