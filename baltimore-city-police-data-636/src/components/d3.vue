<template>
  <div>
    <div>
      <div class="row justify-center">
        <p>D3 impl <br /></p>
      </div>
      <div id="arc" />
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import * as topojson from "topojson";
import crimeData from "@/assets/crime-data.json";
import baltimoreCity from "@/assets/baltimore-city-topo.json";
// import boston from "@/assets/boston_neighborhoods.json";

export default {
  name: "D3Impl",
  data() {
    return {
      baltimoreCity,
      crimeData,
    };
  },
  mounted() {
    this.generateArc();
  },
  methods: {
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

      var path = d3.geoPath().projection(projection);

      var svg = d3
        .select("div")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

      var base = svg.append("g");

      var border = svg.append("g");

      var crime = svg.append("g"); 

      var baltimore = topojson.feature(
        this.baltimoreCity,
        this.baltimoreCity.objects.neighborhoods
      );

      var mesh = topojson.mesh(
        this.baltimoreCity,
        this.baltimoreCity.objects.neighborhoods
      );

      base
        .append("path")
        .datum(baltimore)
        .attr("class", "base")
        .attr("d", path);

      border
        .append("path")
        .datum(mesh)
        .attr("d", path)
        .attr("class", "boundary");

      crime
        .selectAll("path")
        .data(this.crimeData.features)
        .enter()
        .append("path")
        .attr("class", "dot")
        .attr("d", path);

      return svg.node();
    },
  },
};
</script>

<style >
.base {
  fill: #ddc;
}
.boundary {
  fill: #ddc;
  stroke: #fff;
  stroke-dasharray: 2, 2;
  stroke-linejoin: round;
}
.dot {
  fill: rgb(182, 18, 18);
  fill-opacity: 0.45;
  /* stroke: #999; */
}
</style>
