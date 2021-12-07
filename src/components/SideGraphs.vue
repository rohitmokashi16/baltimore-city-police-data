<template>
  <b-col>
    <b-form @submit="getCharts">
        <b-card no-body class="mb-1">
            <b-card-header header-tag="header" class="p-1" role="tab">
                <b-row v-b-toggle.accordion><b-col>Params</b-col></b-row>
            </b-card-header>
            <b-collapse id="accordion" v-model="visible" role="tabpanel">
                <b-card-body>
                    <div class="col">
                     <b-form-group label="Neighborhood:">
                        <b-form-select
                            v-model="form.neighborhood2"
                            :options="neighborhoods"
                        ></b-form-select>
                    </b-form-group>
                    <b-form-group label="Crime Type:">
                        <b-form-select
                            v-model="form.crimeType"
                            :options="crimeTypes"
                        ></b-form-select>
                    </b-form-group>
                    <div class="row">
                        <div class="col">
                            <b-form-group
                                label="Start Year:"
                            >
                                <b-form-select v-model="form.startDate" :options="getAvailableYears()"></b-form-select>
                            </b-form-group>
                        </div>
                        <div class="col">
                            <b-form-group
                                label="End Year:"
                            >
                                <b-form-select v-model="form.endDate" :options="getAvailableYears()"></b-form-select>
                            </b-form-group>
                        </div>
                    </div> 
                    </div>
                </b-card-body>
            </b-collapse>
            <b-card-header header-tag="header" class="p-1" role="tab">
                <b-row v-b-toggle.accordion2><b-col>Charts</b-col></b-row>
            </b-card-header>
            <b-collapse id="accordion2" v-model="visible1" role="tabpanel">     
                <b-card-body>
                    <b-form-group>
                        <b-form-checkbox-group
                            id="checkbox-group-2"
                            v-model="selected"
                         >
                            <b-form-checkbox value=0>Centroid Map</b-form-checkbox>
                            <b-form-checkbox value=1>Crimes by Week Day</b-form-checkbox>
                            <b-form-checkbox value=2>Crimes Indoors vs Outdoors</b-form-checkbox>
                            <b-form-checkbox value=3>Calendar</b-form-checkbox>
                        </b-form-checkbox-group>
                    </b-form-group>
                </b-card-body>
            </b-collapse>
        </b-card>
        <b-button class="justify-start" @click="getCharts" variant="primary">Update</b-button>
    </b-form>

    <b-card no-body v-if="selected.indexOf('0') !== -1">
        <b-img :src="'data:image/png;base64,'+ options[0].img"/>
    </b-card>
    <b-card no-body v-if="selected.indexOf('1') !== -1">
        <b-img :src="'data:image/png;base64,'+ options[1].img"/>
    </b-card>

    <b-card no-body v-if="selected.indexOf('2') !== -1">
        <b-img :src="'data:image/png;base64,'+ options[2].img"/>
    </b-card>
    <b-card no-body v-if="selected.indexOf('3') !== -1">
        <b-img :src="'data:image/png;base64,'+ options[3].img"/>
    </b-card>

  </b-col>
</template>

<script>
import axios from 'axios';
import constData from "../constants/d3Constants.js";

export default {
  name: 'SideBar',
  props: {
      nieghborhood: String,
  },
  data() {
    return {
        selected: [], // Must be an array reference!
        options: [
          { text: ' Centroid Map', url: '/j/crime_centroid', value: 0, img: null },
          { text: ' Crimes by Week Day', url: '/v/day_of_the_week_boxplot', value: 1, img: null },
          { text: ' Crimes Indoors vs Outdoors', url: '/v/indoor_outdoor_crimes_trends', value: 2, img: null },
          { text: ' Calendar', url: '/d/crime_calendar', value: 3, img: null }
        ],
        visible1: true,
        visible: true,
        dayOfTheWeekBoxPlot: false,
        crimeCalendar: false,
        dotwImage: null,
        calendarImage: null,
        imageFromPython: null,
        neighborhoods: constData.neighborhoods,
        msg: '',
        form: {
            crimeType: null,
            startDate: 2016,
            endDate: 2020,
            neighborhood2: null
        },
        boxImg: null,
        indoorImg: null,
        centroidImg: null,
        crimeTypes: Object.keys(constData.crimeCodes),
    }
  },

    watch: {
        neighborhood: {
            handler () {
                this.form.neighborhood2 = this.neighborhood
            }
        }
    },

  methods: {
    getMessage() {
      const path = 'https://vis636-baltcity-police.herokuapp.com/ping';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getAvailableYears() {
      let returning = []
      for (let i = 2021; i > 2010; i--) {
          returning.push(i)      
      }
      return returning
    },
    getCharts() {
        let promises = []
        
        for (let s of this.selected) {
            const path = this.options[s].url;
            this.options[s].img = JSON.parse(JSON.stringify(''))
            let p = axios.get(path, {params: {
                lower: this.form.startDate,
                upper: this.form.endDate,
                swarm: true, // swarm: swarm === 'True' ? "True" : ""
                crime_type: this.form.crimeType,
                neighborhood: this.form.neighborhood2
            },
            host: process.env.BASE_URL});
            promises.push(p);
        }

        this.$emit('updateMapPoints', this.form)

        Promise.all(promises).then((values) => {
            let i = 0
            for (let s of this.selected) {
                this.options[s].img = values[i].data
                i++
            }
        }); 
     },
  },
};
</script>