<template>
  <div>
    <p> D3 Visualizations </p>
    <b-form @submit="onSubmit" v-if="show">
      <div class="row">
        <div class="col">
          <b-form-group label="Crime Type:">
            <b-form-select
              v-model="form.crimeType"
              :options="crimeTypes"
            ></b-form-select>
          </b-form-group>
        </div>
        <div class="col">
          <b-form-group label="Neighborhood">
            <b-form-select
              v-model="form.neighborhood"
              :options="neighborhoods"
            ></b-form-select>
          </b-form-group>
        </div>
        <!-- <div class="col">
          <b-form-group label="Start Date:">
            <b-form-datepicker
              v-model="form.startDate"
              class="mb-2"
            ></b-form-datepicker>
          </b-form-group>
        </div>
        <div class="col">
          <b-form-group label="End Date:">
            <b-form-datepicker
              v-model="form.endDate"
              class="mb-2"
            ></b-form-datepicker>
          </b-form-group>
        </div> -->
      </div>
      <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
    <div class="align-center">
    <div class="container"></div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import * as topojson from "topojson";
import crimeData from "@/assets/crime-data-sample.json";
import baltimoreCity from "@/assets/baltimore-city-topo.json";
import baltimoreCityGeo from "@/assets/baltimore-city.json";
import constData from "../constants/d3Constants.js";
// import boston from "@/assets/boston_neighborhoods.json";

export default {
  name: "D3Impl",
  data() {
    return {
      baltimoreCity,
      baltimoreCityGeo,
      crimeData,
      show: true,
      form: {
        crimeType: null,
        neighborhood: null,
        startDate: null,
        endDate: null,
      },
      crimeTypes: Object.keys(constData.crimeCodes),
      neighborhoods: constData.neighborhoods,
    };
  },
  mounted() {
    this.generateArc();
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();
      var tempCrimeData = JSON.parse(JSON.stringify(this.crimeData.features));
      if (this.form.crimeType) {
        tempCrimeData = tempCrimeData.filter(
          (crime) =>
            crime.properties.Description.toLowerCase() ===
            this.form.crimeType.toLowerCase()
        );
      }
      if (this.form.neighborhood) {
        tempCrimeData = tempCrimeData.filter((crime) => {
          if (crime.properties.Neighborhood) {
            return (
              crime.properties.Neighborhood.toLowerCase() ===
              this.form.neighborhood.toLowerCase()
            );
          }
        });
        console.log(tempCrimeData);
      }
      this.generateArc(tempCrimeData);
    },

    generateArc(filteredCrimeData = this.crimeData.features) {
      d3.selectAll("svg").remove();
      d3.selectAll(".hidden").remove();
      d3.selectAll("div.tooltip").remove();

      var width = 1300;
      var height = 1600;

      let projection = d3
        .geoAlbers()
        .center([0, 39.3])
        .rotate([76.6, 0])
        .parallels([38, 40])
        .scale(500000)
        .translate([780, 670]);

      let path = d3
        .geoPath()
        .projection(projection)
        .pointRadius(3.5);

      let container = d3.select(".container");
      let svg = container
        .append("svg")
        .attr("width", width)
        .attr("height", height);

      let tooltip = d3
        .select(".container")
        .append("div")
        .attr("class", "hidden tooltip");

      // var zoom = d3
      //   .zoom()
      //   .scaleExtent([1, 10])
      //   .translateExtent([
      //     [-500, -300],
      //     [1500, 1000],
      //   ])
      //   .on("zoom", () => {
      //     svg.attr("transform", d3.event.transform);
      //   });

      // container.call(zoom);

      let base = svg.append("g");

      // var labels = svg.append("g");

      let crime = svg.append("g");

      let baltimore = topojson.feature(
        this.baltimoreCity,
        this.baltimoreCity.objects.neighborhoods
      );

      // var mouseOver = (event) => {
      //   event.preventDefault()
      //   d3.selectAll(".base")
      //     .transition()
      //     .duration(200)
      //     .style("opacity", 0.5);
      // };

      // var mouseLeave = (event) => {
      //   event.preventDefault()
      //   d3.selectAll(".base")
      //     .transition()
      //     .duration(200)
      //     .style("opacity", 0.8);

      // };

      base
        .selectAll(".province")
        .data(baltimore.features)
        .enter()
        .append("path")
        .attr("class", (d) => {
          return (
            "province " +
            d.properties.LABEL.replace(/\s/g, "").replace(/\//g, "")
          );
        })
        .attr("d", path)
        .on("mouseover", (event, d) => {
          event.preventDefault();
          var mouse = d3.pointer(event, svg.node()).map((d) => {
            return parseInt(d);
          });

          tooltip
            .classed("hidden", false)
            .attr(
              "style",
              "left:" + (mouse[0] + 125) + "px; top:" + (mouse[1] + 195) + "px"
            )
            .html(d.properties.LABEL);
        })
        .on("mouseout", (event) => {
          event.preventDefault();
          tooltip.classed("hidden", true);
        });

      // labels
      //   .selectAll("path")
      //   .data(baltimore.features)
      //   .enter()
      //   .append("text")
      //   .attr("id", (d) =>
      //     d.properties.LABEL.replace(/\s/g, "")
      //       .replace(/\//g, "")
      //       .replace(/'/g, "")
      //   )
      //   .attr("class", "subunit-label")
      //   .attr("transform", (d) => "translate(" + path.centroid(d) + ")")
      //   .attr("dy", ".35em")
      //   .text("");
      // .on("mouseover", (event, d) => {
      //   event.preventDefault();
      //   return d3
      //     .select(
      //       "#" +
      //         d.properties.LABEL.replace(/\s/g, "")
      //           .replace(/\//g, "")
      //           .replace(/'/g, "")
      //     )
      //     .style("font-size", "14px")
      //     .style("fill-opacity", "1");
      // })
      // .on("mouseout", (event, d) => {
      //   event.preventDefault();
      //   return d3
      //     .select(
      //       "#" +
      //         d.properties.LABEL.replace(/\s/g, "")
      //           .replace(/\//g, "")
      //           .replace(/'/g, "")
      //     )
      //     .style("font-size", "10px")
      //     .style("fill-opacity", "0.5");
      // });

      crime
        .selectAll("path")
        .data(filteredCrimeData)
        .enter()
        .append("path")
        .style("fill", (d) => constData.crimeCodes[d.properties.Description])
        .attr("class", "dot")
        .attr("d", path)
        .on("mouseover", (event, d) => {
          event.preventDefault();
          var mouse = d3.pointer(event, svg.node()).map((d) => {
            return parseInt(d);
          });

          tooltip
            .classed("hidden", false)
            .attr(
              "style",
              "left:" + (mouse[0] + 125) + "px; top:" + (mouse[1] + 195) + "px"
            )
            .html(d.properties.Location + ": " + d.properties.Description);
        })
        .on("mouseout", (event) => {
          event.preventDefault();
          tooltip.classed("hidden", true);
        });

      return svg.node();
    },
  },
};
</script>

<style>
.base {
  fill: #dedede;
  stroke: #fff;
  stroke-dasharray: 3, 2;
  stroke-linejoin: round;
}

.province {
  fill: #dedede;
  stroke: #fff;
  stroke-dasharray: 3, 2;
  stroke-linejoin: round;
}
.province:hover {
  fill: #8a8a8a;
}
.hidden {
  display: none;
}
div.tooltip {
  color: #fff;
  background-color: #666;
  padding: 0.5em;
  text-shadow: #f5f5f5 0 1px 0;
  border-radius: 2px;
  opacity: 0.9;
  position: absolute;
}

.dot {
  /* fill: #ff0000; */
  fill-opacity: 1;
  /* stroke: #999; */
}
.subunit-label {
  fill: #fff;
  fill-opacity: 0.4;
  font-size: 10px;
  font-weight: 500;
  text-anchor: middle;
  transition: 0.5ms;
}
.circle {
  fill: #000;
}
</style>
