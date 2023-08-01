<template>
  <NeshanMap v-bind:ref="mapRef"
    :map-key="mapKey"
    :service-key="serviceKey"
    :poi="true"
    :traffic="false"
    :zoom="17"
    :activeMarker="true"
    :singleMarker="true"
    :hide-search-container="true"
  >
  </NeshanMap>
  <button v-on:click="test">Test Button</button>
  <button v-on:click="changePage">Login</button>
</template>
<!-- :map-types="['neshan']" -->
<!-- :hide-layers="true" -->
<!-- :center="{ latitude: 35.69672648316882, longitude: 51.36281969540723 }" -->
<!-- :markers-icon-callback="markersIconCallback" -->
<!-- @longitude="getLongitude" -->
<!-- :options="options" -->

<script lang="ts">
  import HomP from "./views/HomePage.vue"
  import NeshanMap from "@neshan-maps-platform/vue3-openlayers"
  import { CreateIconProps, CreateLayerProps, CreateMarkersPointsItem, CreateMarkers, MarkersIconCallback, Ol } from "@neshan-maps-platform/vue3-openlayers/dist/types/components/Map.model"
  import { ref, watch, defineComponent } from "vue"
  import { VNodeRef } from "@vue/runtime-core/dist/runtime-core";
  import { Geolocation } from '@capacitor/geolocation';
// import { load } from "google-maps";
  // import { View, Feature, geom, proj, source, layer } from "openlayers";

  const mapRef = ref<InstanceType<typeof NeshanMap>>() as VNodeRef
  const mapKey = "web.333a847c2d214d5f9ef0acd862f8d9a2"
  const serviceKey="service.6fabb675c273413f86aab9e261aa1a67"
  const x={ latitude: 36.69672648316882, longitude: 51.36281969540723 }

  // const watchId = navigator.geolocation.watchPosition(position => {
  //   var latitude=position.coords.latitude
  //   var longitude=position.coords.longitude
  //   console.log("watch:[",latitude,",",longitude,"]")
  // });

  export default defineComponent({
    components: {
      NeshanMap,
      HomP
    },

    data() {
      return {
        mapKey,
        serviceKey,
        mapRef,
        x,
        CurrentComponet:null
        // watchId
      };
    },

    mounted () {
    		// const myMap: InstanceType<typeof NeshanMap> = this.$refs.myMap as any
        // myMap.search({
      	// 		term: "آتش نشانی"
    		// });
        console.log("load")//,mapRef);
  	},

    methods: {
      markersIconCallback(point: CreateMarkersPointsItem) {
          console.log('callB:',point.coords);
        // if (point.isReverseMarker) {
        //   return {
        //     src: "https://img.icons8.com/arcade/344/experimental-marker-arcade.png"
        //   }
        // } 
        // else {
        //   return {
        //     src: "https://img.icons8.com/fluency/344/find-clinic.png",
        //     iconScale: 0.05
        //   }
        // }
      },
      
      CreateMarkers(point: CreateMarkersPointsItem) {
          console.log('create:',point.coords);
          // var marker = new Feature({
          //   geometry: new geom.Point(
          //     proj.fromLonLat(point.coords) // جایی که میخواید براتون نشون بده
          //   ),  
          // });
          // var vectorSource = new source.Vector({
          //   features: [marker]
          // });
          // var markerVectorLayer = new layer.Vector({
          //   source: vectorSource,
          // });
          // .addLayer(markerVectorLayer);
        },

      async test() {
        // let coordX=[35.69672648316882, 51.36281969540723];
        // const markerX={
        //   iconUrl: "",
        //   iconScale: 0.05,
        //   text: "patient",
        //   coords: coordX,
        //   isReverseMarker: false,
        //   props: null
        // };
        // this.CreateMarkers(markerX as CreateMarkersPointsItem);
        // this.markersIconCallback(markerX as CreateMarkersPointsItem);
        console.log("test:");
        
        // const printCurrentPosition = async () => { 
        //   const coordinates = await Geolocation.getCurrentPosition();
        //   console.log('Current position:', coordinates.coords); 
        // };
        // printCurrentPosition();
      },

      changePage(){
        // this.$router(HomeP);
        // this.$router.push("./views/HomePage.vue");
        // this.$emit("view","./views/HomePage.vue");
        // this.CurrentComponet=HomP;
        console.log("NextP");
        // const routes = [{ path: './views/HomePage.vue'}]
        // this.$router.push('./views/HomePage.vue') ;
        // router.push({ path: "./views/HomePage.vue" })
      }

  	},

    setup() {
      
    },

  })

</script>

<style>
  @import url("@neshan-maps-platform/vue3-openlayers/dist/style.css");
</style>

  <!-- //    const	reverseOnPoint: (coords: Coordinate, { useMarker, usePopup,
  // customText }?: ReverseOnPointOptions) => Promise<{
// 		marker: ol.layer.Vector | null;
//  	coords: ol.Coordinate;
//   	data: PrimaryReverseResult;
// } 
// [6626979.195791826, 4346352.948333034] 
//Gapi: api-key="AIzaSyDOFlx7_zAF2nBL2D8rdhJTREPgnGgvtKk"  -->

<!-- <template>
  <GoogleMap
    api-key="AIzaSyDOFlx7_zAF2nBL2D8rdhJTREPgnGgvtKk"
    style="width: 100%; height: 500px"
    :center="center"
    :zoom="15"
  >
    <Marker :options="{ position: center }" />
  </GoogleMap>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { GoogleMap, Marker } from "vue3-google-map";

export default defineComponent({
  components: { GoogleMap, Marker },
  setup() {
    const center = { lat: 40.689247, lng: -74.044502 };
    return { center };
  },
});
</script> -->