<template>
    <div>
      <p> Python Visualizations </p>
      <br>
      <p>This is fragile. Make sure that start date is before end date. Generally, more reliable data points are from 2014 onwards.</p>
         <b-form @submit="onSubmit" v-if="show">
    <div class="row">
      <div class="col">
      <b-form-group
        label="Chart Domain:"
      >
        <b-form-select v-model="form.chartDomain" :options="chartTypes"></b-form-select>
      </b-form-group>
      </div>
      <div class="col">
      <b-form-group
        label="Group Results By:"
      >
        <b-form-select v-model="form.groupBy" :options="['Month_Number', 'Year']"></b-form-select>
      </b-form-group>
      </div>
      <div class="col">
      <b-form-group
        label="Start Year:"
      >
              <b-form-select v-model="form.startYear" :options="getAvailableYears()"></b-form-select>
      </b-form-group>
      </div>
        <div class="col">
      <b-form-group
        label="End Year:"
      >
        <b-form-select v-model="form.endYear" :options="getAvailableYears()"></b-form-select>
      </b-form-group>
      </div>
         <div class="col">
      <b-form-group
        label="Swarm Plot:"
      >
        <b-form-select v-model="form.swarm" :options="['True', 'False']"></b-form-select>
      </b-form-group>
      </div>
    </div>
    <b-button v-b-toggle.sidebar-1>Toggle Sidebar</b-button>
    <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
    <div class="row">
      <div class="col">
       <b-img v-if="imageFromPython" :src="'data:image/png;base64,'+ imageFromPython"/>
      </div>
    </div>
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
                chartDomain: null,
                groupBy: null,
                startYear: null,
                endYear: null,   
                swarm: false
            },
            chartTypes: [
                "Crimes by Day of Week (Box Plot)",
                "Crimes by District (Box Plot)",
                "Crimes by District (Bar Chart)",
                "Crime Trend by being Indoors/Outdoors",
            ],
            chartRoutes: [
                "/v/day_of_the_week_boxplot",
                "/v/district_wise_boxplot",
                "/v/district_crime_bar_charts",
                "/v/indoor_outdoor_crimes_trends"
            ]
        }
    },
    async created () {
        // await this.getChart(null, "Year", 2016, 2017, false)
    },
    watch: {
        imageFromPython: {
            handler () {
                console.log('changed')
            }
        }
    },
    methods: {
        getImage() {
            const path = '/vue';
            axios.get(path)
                .then((res) => {
                this.imageFromPython = res.data;
            })
            .catch((error) => {
             // eslint-disable-next-line
            console.error(error);
        })
        },
        getChart(type, ym, lower, upper, swarm) {
            const path = type;
            this.imageFromPython = JSON.parse(JSON.stringify(''))
            axios.get(path, {params: {
                ym: ym,
                lower: lower,
                upper: upper,
                swarm: swarm === 'True' ? "True" : ""
            },
            host: process.env.BASE_URL})
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
            this.getChart(
                this.chartRoutes[this.chartTypes.indexOf(this.form.chartDomain)],
                this.form.groupBy,
                this.form.startYear,
                this.form.endYear,
                this.form.swarm)
        },
        getAvailableYears() {
            let returning = []
            for (let i = 2021; i > 2010; i--) {
                returning.push(i)
            }
            return returning
        }
    }
}
</script>

<style scoped>

</style>
