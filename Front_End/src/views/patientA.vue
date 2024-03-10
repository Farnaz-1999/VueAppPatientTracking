<template>
  <ion-header>
    <ion-toolbar>
      <ion-title>{{ userData.FName }} {{ userData.LName }} signed in as a {{ userData.role }}</ion-title>
    </ion-toolbar>
  </ion-header>

  <ion-content class="ion-padding"> 
    <ion-header v-show="!isPatient">
      <ion-toolbar>
        <ion-title size="small">{{ selectedPerson.PFName }} {{ selectedPerson.PLName }}</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-list>
        <ion-button expand="block" @click="GoInformation" :disabled="!infoAccess">Information</ion-button>
        <ion-button expand="block" @click="GoHInformation" :disabled="!HIAccess">Health Information</ion-button>
        <ion-button expand="block" @click="GoHSInformation" :disabled="!HSAccess">Health Situation</ion-button>
        <ion-button expand="block" @click="GoInsurance" :disabled="!insuAccess">Insurance</ion-button>
        <ion-button expand="block" @click="GetPatientLoc" :disabled="!locAccess" v-show="!isPatient">Location</ion-button>
        <ion-button expand="block" @click="GoSet">Setting</ion-button>
    </ion-list>
  </ion-content>
</template>
  
  <script lang="ts">
  import { defineComponent } from "vue"
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
      IonCheckbox
    } from '@ionic/vue';

  export default defineComponent({
    components: {
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
      IonCheckbox
  },

    data() {
        return {
          locAccess:false,
          HSAccess:true,
          HIAccess:true,
          infoAccess:true,
          insuAccess:true,
          isPatient:false,
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
          }
        };
    },

    async mounted () {
      console.log("loadPerson");
      this.userData=window['UserData'];
      
      if(this.userData.role!="Patient"){
        this.selectedPerson=window['selectedPerson'];

      var accesses=JSON.parse(this.selectedPerson.access.replace(/'/g, "\""));
        if (accesses['Telemetry']['Personal Telemetry']['Location Telemetry']!="-")            
          this.locAccess=true;
        if (accesses['Information']['Personal Information']=="-" && accesses['Information']['Biometric Information']=="-")            
          this.infoAccess=false;
        if (accesses['Insurance Data']=="-")            
          this.insuAccess=false;
        if (accesses['Health Information']['Health Situation']=="-")            
          this.HSAccess=false;
        if (accesses['Health Information']['Health Information Log']=="-")            
          this.HIAccess=false;
      }
      else
        this.isPatient=true;      
    },

    methods: {
      async GoInformation() {
        //http://farnaz-macbook-pro.local
        var url="http://192.168.121.135:8000/data/info/";
        if(this.userData.role=="Patient")
          url=url+this.userData.Uname+"/ / / /";
        else
          url=url+this.selectedPerson.URIdPatient+"/"+this.userData.Uname+"/"+this.userData.role+"/"+this.userData.passwd;

        await fetch(url, {
          method: "GET",
        })
        .then(res => res.json())
          .then(response => {
            console.log("Details:",response);
            window['Details'] = response;
            if (typeof(response)!=typeof("") || response=="No Data"){
              window['Details']['PageH']="Information";           
              this.$router.push("/data");
            }
            else if(response=="No Access !!!")
              this.infoAccess=false;
            else
              this.$router.push("/login");
        });
      },

      async GoHInformation() {
        //http://farnaz-macbook-pro.local
        var url="http://192.168.121.135:8000/data/Hinfo/";
        if(this.userData.role=="Patient")
          url=url+this.userData.Uname+"/ / / /";
        else
          url=url+this.selectedPerson.URIdPatient+"/"+this.userData.Uname+"/"+this.userData.role+"/"+this.userData.passwd;

        await fetch(url, {
          method: "GET",
        })
        .then(res => res.json())
          .then(response => {
            console.log("Details:",response);
            window['Details'] = response;
            if (typeof(response)!=typeof("") || response=="No Data"){
              window['Details']['PageH']="Health Information";             
              this.$router.push("/data");
            }
            else if(response=="No Access !!!")
              this.HSAccess=false;
            else
              this.$router.push("/login");
        });
      },

      async GoHSInformation() {
        //http://farnaz-macbook-pro.local
        var url="http://192.168.121.135:8000/data/HSinfo/";
        if(this.userData.role=="Patient")
          url=url+this.userData.Uname+"/ / / /";
        else
          url=url+this.selectedPerson.URIdPatient+"/"+this.userData.Uname+"/"+this.userData.role+"/"+this.userData.passwd;

        await fetch(url, {
          method: "GET",
        })
        .then(res => res.json())
          .then(response => {
            console.log("Details:",response);
            window['Details'] = response;
            if (typeof(response)!=typeof("") || response=="No Data"){
              window['Details']['PageH']="Health situation";              
              this.$router.push("/data");
            }
            else if(response=="No Access !!!")
              this.HSAccess=false;
            else
              this.$router.push("/login");
        });
      },

      async GoInsurance() {
        //http://farnaz-macbook-pro.local
        var url="http://192.168.121.135:8000/data/insurance/";
        if(this.userData.role=="Patient")
          url=url+this.userData.Uname+"/ / / /";
        else
          url=url+this.selectedPerson.URIdPatient+"/"+this.userData.Uname+"/"+this.userData.role+"/"+this.userData.passwd;

        await fetch(url, {
          method: "GET",
        })
        .then(res => res.json())
          .then(response => {
            console.log("Details:",response);
            window['Details'] = response;
            if (typeof(response)!=typeof("") || response=="No Data"){
              window['Details']['PageH']="Insurance";
              this.$router.push("/data");
            }
            else if(response=="No Access !!!")
              this.insuAccess=false;
            else
              this.$router.push("/login");
        });
      },

      async GetPatientLoc() {
        //http://farnaz-macbook-pro.local
        await fetch("http://192.168.121.135:8000/data/loc/"+this.selectedPerson.URIdPatient+"/"+this.userData.Uname+"/"+this.userData.role+"/"+this.userData.passwd, {
          method: "GET",
        })
        .then(res => res.json())
          .then(response => {
            console.log("Details:",response);
            window['Details'] = response;
            if (response=="No Loc Data" || typeof(response)!=typeof(""))
              this.$router.push("/location");
            else if(response=="No Loc Access")
              this.locAccess=false;
            else if(response=="Patient Access Revoked !!!")
              this.$router.push("/dashboard");
            else
              this.$router.push("/login");
        });
      },

      async GoSet(){
        this.$router.push("/setting");
      },
    },
  
  })
  
  </script> 
  
  
  