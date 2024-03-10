<template>
    <ion-header>
      <ion-toolbar>
        <ion-title>{{ userData.FName }} {{ userData.LName }} signed in as a {{ userData.role }}</ion-title>
      </ion-toolbar>
    </ion-header>
  
    <ion-content class="ion-padding">
      <ion-header>
        <ion-toolbar>
          <ion-title size="small">{{ pageHeader }}</ion-title>
        </ion-toolbar>
      </ion-header>

      <ion-grid>
        <ion-row >
            <ion-col v-for="(value, key, index) in pageData[0]" v-show="key!='_id' && key!='URIdPatient' && key!='URIdDr'">
                {{ key }}
            </ion-col>
        </ion-row>
        <ion-row v-for="item in pageData">
            <ion-col v-for="(value, key, index) in item" v-show="key!='_id' && key!='URIdPatient' && key!='URIdDr'">
                {{ value }}
            </ion-col>
        </ion-row>
      </ion-grid>
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
        IonCheckbox,
        IonCol,
        IonGrid,
        IonRow
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
        IonCheckbox,
        IonCol,
        IonGrid,
        IonRow
    },
  
    data() {
      return {
          pageHeader:"",
          userData:{
            Uname:"",
            FName:"",
            LName:"",
            role:"",
            passwd:"",
            PAccessToken:""
          },
          pageData:[]
      };
    }, 
  
     mounted () {
        console.log("loadData");
        this.userData=window['UserData'];
        this.pageData=window['Details'];
        this.pageHeader=window['Details']['PageH'];

        if(this.pageHeader=="Information"){
            this.pageData.forEach((item, index)=>{
                if("bio" in item){
                    for (const [key, value] of Object.entries(item["bio"])){
                        this.pageData[index][key]=value;
                    }
                    delete this.pageData[index]['bio'];
                }
            });
        }
    },
  
    methods: {
    },
  
  })
  
</script> 
  
<style>
  ion-col {
    background-color: #f4f5f8;
    border: solid 1px #fff;
    color: #403d3d;
    text-align: center;
  }
</style>
  
  