<template>
  <ion-header>
    <ion-toolbar>
      <ion-title>{{ userData.FName }} {{ userData.LName }} signed in as a {{ userData.role }}</ion-title>
    </ion-toolbar>
  </ion-header>

  <ion-content class="ion-padding">
    <ion-header>
      <ion-toolbar>
        <ion-title size="small">My Notifications</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-list>
      <ion-item v-for="item in notifs">
        {{ item.r2r.PFName}} {{ item.r2r.PLName }} leave the Fence at {{ item.notif.Time}} 
      </ion-item>
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
        notifs:[{
          r2r:{PFName:"",PLName:""},
          notif:{Time:"",URIdPatient:""}
        }],
        userData:{
          Uname:"",
          FName:"",
          LName:"",
          role:"",
          passwd:"",
          PAccessToken:""
        }
    };
  }, 

   mounted () {
      console.log("loadNotifs");
      this.userData=window['UserData'];
      this.notifs=window['Notifs'];
  },

  methods: {
  },

})

</script> 


