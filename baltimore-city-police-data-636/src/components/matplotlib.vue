<template>
    <div>
      <p> Python Visualizations </p>
         <b-form @submit="onSubmit" v-if="show">
    <div class="row">
      <div class="col">
      <b-form-group
        label="Crime Type:"
      >
        <b-form-select v-model="form.crimeType" :options="sampleCrimeTypes"></b-form-select>
      </b-form-group>
      </div>
      <div class="col">
      <b-form-group
        label="Neighborhood"
      >
        <b-form-select v-model="form.neighborhood" :options="sampleNeighborhoods"></b-form-select>
      </b-form-group>
      </div>
      <div class="col">
      <b-form-group
        label="Start Date:"
      >
          <b-form-datepicker v-model="form.startDate" class="mb-2"></b-form-datepicker>
      </b-form-group>
        </div>
              <div class="col">
      <b-form-group
        label="End Date:"
      >
          <b-form-datepicker v-model="form.endDate" class="mb-2"></b-form-datepicker>
      </b-form-group>
        </div>
    </div>
    <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
       <b-img v-if="imageFromPython" :src="'data:image/png;base64,'+ imageFromPython"/>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "MatPlotLib",
    data () {
        return {
            imageFromPython: null,
            show: true,
            form: {
                crimeType: null,
                neighborhood: null,
                startDate: null,
                endDate: null,    
            }
        }
    },
    async created () {
        await this.getChart(null, "Year", 2016, 2017, false)
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
        getChart(type, ym, lower, upper, swarm) {
            const path = 'http://localhost:5000/v/district_wise_boxplot';
            axios.get(path, {params: {
                ym: ym,
                lower: lower,
                upper: upper,
                swarm: swarm
            },
            host: 'localhost:8080'})
                .then((res) => {
                this.imageFromPython = res.data;
            })
            .catch((error) => {
             // eslint-disable-next-line
            console.error(error);
            })
         },
        onSubmit(event) {
            event.preventDefault()
        },
    }
}
</script>

<style scoped>

</style>
