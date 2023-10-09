<template>
  <ion-header>
    <ion-toolbar>
      <ion-title>{{ userData.FName }} {{ userData.LName }} signed in as a {{ userData.role }}</ion-title>
    </ion-toolbar>
  </ion-header>
  
  <ion-content class="ion-padding"> 
    <ion-header>
      <ion-toolbar>
        <ion-title size="small">{{ selectedPerson.PFName }} {{ selectedPerson.PLName }}</ion-title>
      </ion-toolbar>
    </ion-header>

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
      :center="center"
      :map-types="['neshan']"
      @vnode-mounted="preInitBilbilack"
    >
    </NeshanMap>

    <ion-toast :is-open="ErrExist" :message="Err" :duration="5000" @didDismiss="ErrDismiss(false)"></ion-toast>

  </ion-content>
</template> 

<script lang="ts">
import NeshanMap from "@neshan-maps-platform/vue3-openlayers"
import {
      IonButtons,
      IonButton,
      IonModal,
      IonHeader,
      IonContent,
      IonToolbar,
      IonTitle,
      IonItem,
      IonInput,
      IonLabel,
      IonItemDivider,
      IonList,
      IonSelect,
      IonSelectOption,
      IonItemGroup,
      IonCheckbox,
      IonToast
    } from '@ionic/vue';
import { defineComponent } from "vue"
import { Geolocation } from '@capacitor/geolocation';

const watchCoords = Geolocation.watchPosition({}, (position, err) => {
  if(window['UserData']!=undefined && window['UserData'].role=="Patient"){
    var latitude=position?.coords.latitude;
    var longitude=position?.coords.longitude;
    console.log("watch:[",latitude,",",longitude,"]");

    fetch("http://192.168.121.135:9090/api/v1/"+window['UserData'].PAccessToken+"/attributes", {
      method: "POST",
      headers: {
        'Content-Type':"application/json"
      }, 
      body: JSON.stringify({
        "latitude": latitude,
        "longitude": longitude,
      })
    }).then(response => {
    });
  }
});

const mapKey = "web.333a847c2d214d5f9ef0acd862f8d9a2"
const serviceKey="service.6fabb675c273413f86aab9e261aa1a67"

export default defineComponent({

  components: {
    NeshanMap,
    IonButtons,
    IonButton,
    IonModal,
    IonHeader,
    IonContent,
    IonToolbar,
    IonTitle,
    IonItem,
    IonInput,
    IonLabel,
    IonItemDivider,
    IonList,
    IonSelect,
    IonSelectOption,
    IonItemGroup,
    IonCheckbox,
    IonToast
  },

  data() {
    var loc=window['Details'];
    var positionUpdater = setInterval(() => {this.updatePosition()}, 8000);
    return {
      watchCoords,
      userData:{
        Uname:"",
        FName:"",
        LName:"",
        role:"",
        passwd:"",
        PAccessToken:""
      },
      selectedPerson:{
        DFName: "",
        DLName: "",
        PFName: "",
        PLName: "",
        URIdDr: "",
        URIdPatient: "",
        access: ""
      },
      mapKey,
      serviceKey,
      center:{ latitude: loc.latitude, longitude: loc.longitude },
      mapInited: false,
      layerSource:"",
      Err:"",
      ErrExist:false,
      positionUpdater
    };
  },

  async mounted () {
      console.log("loadLocation");
      this.userData=window['UserData'];
      this.selectedPerson=window['selectedPerson'];
  },

  unmounted () {
      clearInterval(this.positionUpdater);
  },

  methods: {
    preInitBilbilack(){
      setTimeout(()=>{
        if ( this.$refs.mapRef && this.$refs.mapRef.state && this.$refs.mapRef.state.map) {
          this.initBilbilack();
        } else {
          this.preInitBilbilack();
        }
      },100)
    },

    initBilbilack(){
      let myMap =this.$refs.mapRef.state.map;
       this.layerSource =new ol.source.Vector({features: []}); 
      let layer = new ol.layer.Vector({
        source: this.layerSource,
        style: new ol.style.Style({
          image: new ol.style.Icon({
            color: '#22eeff',
            crossOrigin: 'anonymous',
            src: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAABBklEQVR4nOXUTytEURjH8Y/LguIdWPAaLGehlDIUe8VLkKzkz5atrZWNlTdhY2el7GTBsJEoRSmMpp7F6TazmDv3lPKr062n2/d7znnuffjvWcIDWmjmELTQjnU/KGw4l2AcO3jBFQ7QCGEzJB34Qr/gMWzhKdlluh4Hvff1BHaBOazgO6m/YaqqYARnWExq211Oco5CDZnAcwn+E8/NOgS7Jfgr1nr0p1JuS5C9qJ/UJbgrQSZlGAufieCoLnCBVQzFz/Qegi/MVAF2a1o72XEjGtypXfYYIX0LPjCbvLOcfEmjMuQwBMc54EUMt3ZcV+2ZD/hNNL72nIZgX6Zs4BrTuQR/K7/frmU5K2K4hwAAAABJRU5ErkJggg=="
          })
        })
      })

      myMap.addLayer(layer);
      this.mapInited=true;
      console.log("Map Inited");
      this.updatePosition();
    },

    async updatePosition() {
      if(this.mapInited){
        await fetch("http://192.168.121.135:8000/data/loc/"+this.selectedPerson.URIdPatient+"/"+this.userData.Uname+"/"+this.userData.role+"/"+this.userData.passwd, {
          method: "GET",
        })
        .then(res => res.json())
          .then(response => {
            console.log("ServerData:",response);
            if(response=="No Loc Data"){
              this.Err="There is not location data available, The location sensor might hava a problem."
              this.ErrExist=true;
            }
            else if(response=="No Loc Access")
              this.$router.push("/person");
            else if(response=="Patient Access Revoked !!!")
              this.$router.push("/dashboard");
            else if(response=="User Problem !!!")
              this.$router.push("/login");
            else{
              let myMap =this.$refs.mapRef.state.map;
              var features = [new ol.Feature({geometry: new ol.geom.Point(ol.proj.fromLonLat([response.longitude,response.latitude]))})]; 
              this.layerSource.clear(true);
              this.layerSource.addFeatures(features);
              myMap.render();
            }
        });
      }
    },

    ErrDismiss(x:boolean){
        this.ErrExist=x;
        this.Err="";
    }

    /* markersIconCallback(point:any) {
       console.log('callB:',point.coords[0],point.coords[1]);
       return;
     },*/
  },

})
</script>

<style>
@import url("@neshan-maps-platform/vue3-openlayers/dist/style.css");
</style>


