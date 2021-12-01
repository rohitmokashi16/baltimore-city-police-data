<template>
  <div>
    <p>D3 Visualizations</p>
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
        <div class="col">
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
        </div>
      </div>
      <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
    <div class="align-center">
      <div class="container"></div>
    </div>
    <div id="neighborhood-map" class="align-center">
      
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
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet/dist/leaflet.js";
// import cookie from "vue-cookies";
// import boston from "@/assets/boston_neighborhoods.json";

export default {
  name: "D3Impl",
  data() {
    return {
      fullView: true,
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
        // console.log(tempCrimeData);
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

      let base = svg.append("g");

      // var labels = svg.append("g");

      let crime = svg.append("g");

      let baltimore = topojson.feature(
        this.baltimoreCity,
        this.baltimoreCity.objects.neighborhoods
      );

      base
        .selectAll(".province")
        .data(baltimore.features)
        .enter()
        .append("path")
        .attr("id", (d) => d.properties.LABEL)
        .attr("class", (d) => {
          return (
            "province " +
            d.properties.LABEL.replace(/\s/g, "").replace(/\//g, "")
          );
        })
        .attr("d", path)
        .on("mouseover", (event, d) => {
          event.preventDefault();
          let mouse = d3.pointer(event, svg.node()).map((d) => {
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
        })
        .on("click", (event) => {
          event.preventDefault();
          this.onSelect(event.target.id);
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
          let mouse = d3.pointer(event, svg.node()).map((d) => {
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

    onSelect(neighborhoodName) {
      // d3.selectAll("svg").remove();
      // d3.selectAll(".hidden").remove();
      // d3.selectAll("div.tooltip").remove();
      // this.fullView = false;
      console.log(neighborhoodName)
      document.getElementById("neighborhood-map").innerHTML = '<div id="neighborhood-container"></div>';
      let tempCrimeData = JSON.parse(JSON.stringify(this.crimeData.features));
      tempCrimeData = tempCrimeData.filter((crime) => {
        if (crime.properties.Neighborhood) {
          return (
            crime.properties.Neighborhood.toLowerCase() ===
            neighborhoodName.toLowerCase()
          );
        }
      });

      let map = L.map("neighborhood-container"),
        bwOsmURL = "http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png",
        osmAttrs =
          "Map data © <a href='http://openstreetmap.org'>OpenStreetMap</a>";

      map.on("load", function() {
        setTimeout(() => {
          map.invalidateSize();
        }, 1);
      });

      let osmTiles = new L.TileLayer(bwOsmURL, {
        minZoom: 11,
        maxZoom: 17,
        attribution: osmAttrs,
      });

      // Center view on ~NYC
      let neighborhoodCenter = new L.LatLng(39.3, -76.6);

      map.setView(neighborhoodCenter, 11); // latlng, zoom level
      map.addLayer(osmTiles);

      function polystyle() {
        return {
          fillColor: "#dedede",
          weight: 1,
          opacity: 1,
          color: "#8a8a8a", //Outline color
          fillOpacity: 0.4,
        };
      }

      const polyData = baltimoreCityGeo.features.filter(
        (neighborhood) =>
          neighborhood.properties.NBRDESC.toLowerCase() ===
          neighborhoodName.toLowerCase()
      );
      L.geoJson(polyData, { style: polystyle }).addTo(map);

      L.geoJson(tempCrimeData, {
        style: () => {
          return {
            color: "#808080",
            opacity: 1,
            radius: 0.8,
            fillColor: "#dedede",
            fillOpacity: 0.7,
          };
        },
        onEachFeature: (feature, layer) => {
          layer.bindPopup(feature.properties.Location);
        },
        pointToLayer: (feature, latlng) => {
          console.log(feature.properties.Location);
          return L.circleMarker(latlng);
        },
      }).addTo(map);
    },
  },
};
</script>

<style>
#neighborhood-container {
  display: inline-block;
  height: 450px;
  width: 700px;
}
.base {
  fill: #dedede;
  stroke: #fff;
  stroke-dasharray: 3, 2;
  stroke-linejoin: round;
}

.province {
  fill: #000;
  stroke: #fff;
  stroke-dasharray: 0.5, 3;
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
