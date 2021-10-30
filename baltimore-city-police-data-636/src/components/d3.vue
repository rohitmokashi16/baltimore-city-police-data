<template>
  <div>
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
    <div class="row justify-center">
      <p>D3 impl <br /></p>
    </div>
    <div class="container"></div>
  </div>
</template>

<script>
import * as d3 from "d3";
import * as topojson from "topojson";
import crimeData from "@/assets/crime-data-sample.json";
import baltimoreCity from "@/assets/baltimore-city-topo.json";
// import boston from "@/assets/boston_neighborhoods.json";

export default {
  name: "D3Impl",
  data() {
    return {
      baltimoreCity,
      crimeData,
      show: true,
      form: {
          crimeType: null,
          neighborhood: null,
          startDate: null,
          endDate: null,    
      },

      sampleCrimeTypes: [
        'ASSAULT',
        'MURDER',
        'THEFT'
      ],
      sampleNeighborhoods:  [
        'Federal Hill',
        'Sandtown-Winchester',
        'Goucher',
        'Parkville',
        'Barclay',
        'Little Italy'
      ]

    }
  },
  mounted() {
    this.generateArc();
  },
  methods: {

    onSubmit(event) {
      event.preventDefault()
      alert(JSON.stringify(this.form))
      console.log('do a thing!')
      console.log(this.form)
    },

    generateArc() {
      var width = 1000;
      var height = 1100;

      var projection = d3
        .geoAlbers()
        .center([0, 39.3])
        .rotate([76.6, 0])
        .parallels([38, 40])
        .scale(350000)
        .translate([600, 450]);

      var path = d3
        .geoPath()
        .projection(projection)
        .pointRadius((d) => {
          if (d.type === "Point") {
            return 3;
          }
        });

      var container = d3.select(".container");
      var svg = container
        .append("svg")
        .attr("width", width)
        .attr("height", height);

      var zoom = d3
        .zoom()
        .scaleExtent([1, 10])
        .translateExtent([
          [-500, -300],
          [1500, 1000],
        ])
        .on("zoom", () => {
          svg.attr("transform", d3.event.transform);
        });

      container.call(zoom);

      var base = svg.append("g");

      var crime = svg.append("g");

      var baltimore = topojson.feature(
        this.baltimoreCity,
        this.baltimoreCity.objects.neighborhoods
      ).features;

      // base
      //   .append("path")
      //   .datum(topojson.feature(
      //   this.baltimoreCity,
      //   this.baltimoreCity.objects.neighborhoods
      // ).features)
      //   .attr("class", "base")
      //   .attr("d", path);

      base
        .selectAll("path")
        .data(baltimore)
        .enter()
        .append("path")
        .attr("class", "base")
        .attr("d", path);

      crime
        .selectAll("path")
        .data(this.crimeData.features)
        .enter()
        .append("path")
        .attr("class", (d) =>
          d.properties.CrimeCode === "5B" ? "green-dot" : "dot"
        )
        .datum((d) => {
          return {
            type: "Point",
            coordinates: [d.properties.Longitude, d.properties.Latitude],
          };
        })
        .attr("d", path);

      return svg.node();
    }
  },
};
</script>

<style >
.base {
  fill: #999da0;
  stroke: #fff;
  stroke-dasharray: 3, 2;
  stroke-linejoin: round;
}
.dot {
  fill: #ff0000;
  fill-opacity: 0.65;
  /* stroke: #999; */
}
.green-dot {
  fill: #138808;
  fill-opacity: 0.65;
  /* stroke: #999; */
}
.circle {
  fill: #000;
}
</style>
