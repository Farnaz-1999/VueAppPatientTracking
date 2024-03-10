<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-title>Salam</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">Byee</ion-title>
        </ion-toolbar>
      </ion-header>

      <div id="container">
        <strong>Ready to create an app?</strong>
        <p>Start with Ionic <a target="_blank" rel="noopener noreferrer" href="https://ionicframework.com/docs/components">UI Components</a></p>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar } from '@ionic/vue';
</script>

<style scoped>
#container {
  text-align: center;
  
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
}

#container strong {
  font-size: 20px;
  line-height: 26px;
}

#container p {
  font-size: 16px;
  line-height: 22px;
  
  color: #8c8c8c;
  
  margin: 0;
}

#container a {
  text-decoration: none;
}
</style>


<!-- AllBackUp -->
<!-- <template>
  <NeshanMap 
    ref="mapRef"
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
</template> -->
<!-- :map-types="['neshan']" -->
<!-- :hide-layers="true" -->
<!-- :center="{ latitude: 35.69672648316882, longitude: 51.36281969540723 }" -->
<!-- :markers-icon-callback="markersIconCallback" -->
<!-- @longitude="getLongitude" -->
<!-- :options="options" -->
<!-- 
<script lang="ts">
import HomP from "./views/HomePage.vue"
import NeshanMap from "@neshan-maps-platform/vue3-openlayers"
import { CreateIconProps, CreateLayerProps, CreateMarkersPointsItem, CreateMarkers, MarkersIconCallback, Ol } from "@neshan-maps-platform/vue3-openlayers/dist/types/components/Map.model"
import { ref, watch, defineComponent } from "vue"
import { VNodeRef } from "@vue/runtime-core/dist/runtime-core";
import { Geolocation } from '@capacitor/geolocation';
// import  {Feature, geom, proj, source, style, layer}  from "ol";
import ol from "@neshan-maps-platform/vue3-openlayers"
import { defineOverlayContainer } from "@ionic/vue/dist/types/vue-component-lib/overlays";
import axios from 'axios'; 

const mapKey = "web.333a847c2d214d5f9ef0acd862f8d9a2"
const serviceKey="service.6fabb675c273413f86aab9e261aa1a67"

const watchId = navigator.geolocation.watchPosition(position => {
  var latitude=position.coords.latitude
  var longitude=position.coords.longitude
  console.log("watch:[",latitude,",",longitude,"]") 
  fetch("http://localhost:9090/api/v1/gw55E3HHk5hKfckXkBjr/attributes", {
    method: "POST",
    headers: {
      'Content-Type':"application/json"
    },
    body: JSON.stringify({
      "latitude": latitude,
       "longitude":longitude
    })
  })
  .then(res => res.json())
    .then(response => {
      console.log("Response:",response);
  });

//   fetch("http://localhost:9090/api/v1/gw55E3HHk5hKfckXkBjr/attributes?clientKeys=latitude,longitude", {
//     method: "GET",
//   })
//   .then(res => res.json())
//     .then(response => {
//       console.log("ServerData:",response);
//   });
});

export default defineComponent({
  components: {
    NeshanMap,
    HomP
  },

  data() {
    return {
      mapKey,
      serviceKey,
      CurrentComponet:null
      // watchId
    };
  },

  mounted () {
      console.log("load");
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
        // map.addLayer(markerVectorLayer);
      },

    async test() {
      // console.log("All:",this.$refs.mapRef);
      // var Gin =this.$refs.mapRef;
      // Gin.state.mainMarkerCoords=[51.36281969540723, 35.69672648316882];
      // window['Gin'] = Gin;
      // console.log("map:",Gin.state.map);

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

      //GetAccess
      // fetch("http://localhost:8000/chk/Maryam/Mali/Dr/tadaaa", {
      //   method: "GET",
      // })
      // .then(res => res.json())
      //   .then(response => {
      //     console.log("get:",response);
      // });

      //GetPatientLoc
      // fetch("http://localhost:8000/data/1", {
      //   method: "GET",
      // })
      // .then(res => res.json())
      //   .then(response => {
      //     console.log("get:",response);
      // });

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

})

</script> -->

<!-- <style>
@import url("@neshan-maps-platform/vue3-openlayers/dist/style.css");
</style> -->


