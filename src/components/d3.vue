<template>
  <div>
    <b-col v-if="!selectedNeighborhood && crimeArray.length > 0" class="align-center">
      <div class="container"></div>
    </b-col>
    <b-col v-if="crimeData" v-show="selectedNeighborhood">
      <b-button
        @click="
          selectedNeighborhood = null;
          $router.go();
        "
        variant="primary"
        >Back</b-button
      >
      <div id="neighborhood-map" class="align-center"></div>
      <div id="neighborhood-container"></div>
    </b-col>
    <b-sidebar
      id="sidebar-1"
      width="325px"
      right
      v-model="sidebarClicked"
      title="Query"
      shadow
    >
      <div class="mx-3 py-2">
        <SideGraphs
          @updateMapPoints="updateDataFromSide($event)"
          :neighborhood="selectedNeighborhood"
        />
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
import SideGraphs from "./SideGraphs.vue";
import L from "leaflet";
import axios from "axios";
import "leaflet/dist/leaflet.css";
import "leaflet/dist/leaflet.js";
import _ from "lodash";

export default {
  name: "D3Impl",
  components: { SideGraphs },
  data() {
    return {
      fullView: true,
      baltimoreCity,
      baltimoreCityGeo,
      startDate: 2016,
      endDate: 2020,
      crimeData: {
        type: "FeatureCollection",
        features: [],
      },
      crimeArray: [],
      crimeColumns: null,
      sidebarClicked: true,
      crimeTypes: Object.keys(constData.crimeCodes),
      neighborhoods: constData.neighborhoods,
      selectedNeighborhood: null,
      crimeType: null,
    };
  },
  async mounted() {
    await this.updateData(this.selectedNeighborhood);
  },

  updated () {
    this.generateArc()
  },

  watch: {
    crimeArray: {
      handler() {
        console.log('change')
        this.generateArc()
      },
    },
    selectedNeighborhood: {
      async handler() {
        console.log(this.selectedNeighborhood)      
      },
    },
  },

  methods: {
    async updateDataFromSide(data) {
      this.selectedNeighborhood = data.neighborhood2;
      this.startDate = data.startDate;
      this.endDate = data.endDate;
      this.crimeType = data.crimeType;
      await this.onSelect(data.neighborhood2);
    },
    async updateData(neighborhood) {
      await axios
        .get("/r/map_data", {
          params: {
            lower: this.startDate,
            upper: this.endDate,
            crime_type: this.crimeType,
            neighborhood: neighborhood,
          },
          host: process.env.BASE_URL,
        })
        .then((response) => {
          if (response) {
           // d3.selectAll("div.neighborhood-container").remove();
            this.crimeArray = this.processData(response.data);
          }
        });
    },

    processData(resonseData) {
      let featureData = [];
      Object.keys(resonseData).forEach((key) => {
        featureData.push({
          type: "Feature",
          properties: resonseData[key],
          geometry: {
            type: "Point",
            coordinates: [
              resonseData[key].Longitude,
              resonseData[key].Latitude,
            ],
          },
        });
      });
      return featureData;
    },

    onSubmit() {},

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

      let path = d3.geoPath().projection(projection).pointRadius(3.5);

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
        .on("click", async (event) => {
          event.preventDefault();
          this.selectedNeighborhood = event.target.id;
          await this.updateData();
          await this.onSelect(event.target.id);
        });

      crime
        .selectAll("path")
        .data(this.crimeArray)
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
      let returning = [];
      for (let i = 2021; i > 2010; i--) {
        returning.push(i);
      }
      return returning;
    },
    async onSelect(neighborhoodName) {
      d3.selectAll("div.neighborhood-container").remove();
      this.sidebarClicked = true;
      document.getElementById("neighborhood-map").innerHTML = '<div id="neighborhood-container"></div>';
      this.selectedNeighborhood = neighborhoodName;
      await this.updateData(this.selectedNeighborhood)
      let tempCrimeData = _.clone(this.crimeArray, true);
      tempCrimeData = tempCrimeData.filter((crime) => {
        if (crime.properties.Neighborhood && neighborhoodName) {
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

      map.on("load", function () {
        setTimeout(() => {
          map.invalidateSize();
        }, 1);
      });

      let osmTiles = new L.TileLayer(bwOsmURL, {
        minZoom: 14,
        maxZoom: 19,
        attribution: osmAttrs,
      });

      const polyData = baltimoreCityGeo.features.filter(
        (neighborhood) =>
          neighborhood.properties.NBRDESC.toLowerCase() ===
          neighborhoodName.toLowerCase()
      );

      const center = this.getCenterOfPolygon(polyData);

      let neighborhoodCenter = new L.LatLng(center[0], center[1]);

      map.setView(neighborhoodCenter, 14.5); // latlng, zoom level
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

      L.geoJson(polyData, { style: polystyle }).addTo(map);

      L.geoJson(tempCrimeData, {
        style: () => {
          return {
            color: "#DC143C",
            opacity: 1,
            radius: 1.5,
            fillColor: "#DC143C",
            fillOpacity: 0.6,
          };
        },
        onEachFeature: (feature, layer) => {
          const dateTimeString = this.getFormattedDateTime(
            feature.properties.CrimeDateTime
          );
          layer.bindTooltip(
            "<div><div>Date &amp; Time: " +
              dateTimeString +
              "</div><div>Location: " +
              feature.properties.Location +
              "</div><div>Crime Type: " +
              feature.properties.Description +
              "</div><div>District: " +
              feature.properties.District +
              "</div></div>"
          );
        },
        pointToLayer: (feature, latlng) => {
          return L.circleMarker(latlng);
        },
      }).addTo(map);
    },
    getFormattedDateTime(crimeDateTime) {
      const dateTime = new Date(crimeDateTime);
      const dateTimeString =
        dateTime.getMonth() +
        "/" +
        dateTime.getDate() +
        "/" +
        dateTime.getFullYear() +
        " " +
        (dateTime.getHours() < 10 ? "0" : "") +
        dateTime.getHours() +
        ":" +
        (dateTime.getMinutes() < 10 ? "0" : "") +
        dateTime.getMinutes() +
        ":" +
        (dateTime.getSeconds() < 10 ? "0" : "") +
        dateTime.getSeconds();
      return dateTimeString;
    },
    getCenterOfPolygon(polyData) {
      let latitudes = polyData[0].geometry.coordinates[0].map(
        (latlon) => latlon[1]
      );
      let longitudes = polyData[0].geometry.coordinates[0].map(
        (latlon) => latlon[0]
      );

      latitudes.sort();
      longitudes.sort();

      const lowX = latitudes[0];
      const highX = latitudes[latitudes.length - 1];

      const lowY = longitudes[0];
      const highY = longitudes[longitudes.length - 1];

      const centerX = lowX + (highX - lowX) / 2;
      const centerY = lowY + (highY - lowY) / 2;
      return [centerX, centerY];
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
