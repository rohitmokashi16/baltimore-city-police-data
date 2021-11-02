<template>
    <div>
      <p> Python Visualizations </p>
       <b-img v-if="imageFromPython" :src="'data:image/png;base64,'+ imageFromPython"/>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "MatPlotLib",
    data () {
        return {
            imageFromPython: null
        }
    },
    async created () {
        await this.getImage()
    },
    methods: {
        getImage() {
            const path = 'http://localhost:5000/vue';
            axios.get(path)
                .then((res) => {
                this.imageFromPython = res.data;
            })
            .catch((error) => {
             // eslint-disable-next-line
            console.error(error);
        });
    },
    }
}
</script>

<style scoped>

</style>
