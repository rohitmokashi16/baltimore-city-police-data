<template>
  <div>
    <b-col v-if="!selectedNeighborhood && crimeData" class="align-center">
      <div class="container"></div>
    </b-col>
    <b-col v-if="crimeData" v-show="selectedNeighborhood">
      <b-button @click="selectedNeighborhood = null; $router.go()" variant="primary">Back</b-button>
      <div id="neighborhood-map" class="align-center"> </div>
      <div id="neighborhood-container"></div>
    </b-col>
     <b-sidebar id="sidebar-1" width="325px" right v-model="sidebarClicked" title="Query" shadow>
      <div class="mx-3 py-2">
        <SideGraphs @updateMapPoints="updateDataFromSide($event)" :nieghborhood="selectedNeighborhood" />
      </div>
    </b-sidebar>
  </div>
</template>

<script>
import * as d3 from "d3";
import * as topojson from "topojson";
import baltimoreCity from "@/assets/baltimore-city-topo.json";
import baltimoreCityGeo from "@/assets/baltimore-city.json";
import constData from "../constants/d3Constants.js";
import SideGraphs from "./SideGraphs.vue"
import L from "leaflet";
import axios from 'axios';
import "leaflet/dist/leaflet.css";
import "leaflet/dist/leaflet.js";

export default {
  name: "D3Impl",
  components: {SideGraphs},
  data() {
    return {
      fullView: true,
      baltimoreCity,
      baltimoreCityGeo,
      startDate: 2016,
      endDate: 2020,
      crimeData: null,
      crimeColumns: null,
      sidebarClicked: true,
      crimeTypes: Object.keys(constData.crimeCodes),
      neighborhoods: constData.neighborhoods,
      selectedNeighborhood: null,
      crimeType: null
    };
  },
  async mounted() {
    await this.updateData();
  },

  watch: {
    crimeData: {
      handler () {
        console.log('update')
        if (this.crimeData){
          this.generateArc();
        }
      }
    },
    selectedNeighborhood: {
      handler () {
        this.updateData();
        if (this.selectedNeighborhood) {
           this.onSelect(this.selectedNeighborhood)
        }
      }
    }
  },

  methods: {
    updateDataFromSide(data) {
      this.selectedNeighborhood = data.neighborhood2
      this.startDate = data.startDate
      this.endDate = data.endDate
      this.crimeType = data.crimeType
    },
    async updateData() {
       await axios.get('/r/map_data', {params: {
              lower: this.startDate,
              upper: this.endDate,
              crime_type: this.crimeType,
              neighborhood: this.selectedNeighborhood
            },
            host: process.env.BASE_URL}).then(d => {
              console.log('hit')
              this.crimeColumns = d.data.columns
              this.crimeData = d.data.data
            });
    },

    onSubmit() {
    },

    generateArc() {
      d3.selectAll("svg").remove();
      d3.selectAll(".hidden").remove();
      d3.selectAll("div.tooltip").remove();

      var width = 1300; //1300
      var height = 1600;

      let projection = d3
        .geoAlbers()
        .center([0, 39.3])
        .rotate([76.6, 0])
        .parallels([38, 40])
        .scale(250000) // 500000
        .translate([500, 400]); //.translate([780, 670])

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
          this.selectedNeighborhood = event.target.id;
          this.updateData();
          this.onSelect(event.target.id)
        });

      crime
        .selectAll("path")
        .data(this.crimeData)
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
    getAvailableYears() {
      let returning = []
      for (let i = 2021; i > 2010; i--) {
          returning.push(i)      
      }
      return returning
    },
    onSelect(neighborhoodName) {

      this.sidebarClicked = true
      this.selectedNeighborhood = neighborhoodName

      let tempCrimeData = Object.assign([], this.crimeData);
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
  height: 800px;
  width: 100%;
}
.base {
  fill: #dedede;
  stroke: #fff;
  stroke-dasharray: 3, 2;
  stroke-linejoin: round;
}

.province {
  fill: #dedede;
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
