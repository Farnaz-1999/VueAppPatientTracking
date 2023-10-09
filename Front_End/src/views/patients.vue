<template>
  <ion-header>
    <ion-toolbar>
      <ion-title>{{ userData.FName }} {{ userData.LName }} signed in as a {{ userData.role }}</ion-title>
    </ion-toolbar>
  </ion-header>

  <ion-content class="ion-padding">
    <ion-button :onclick="Go2Notif" expand="block">
        My Notifications
    </ion-button>
    <ion-button expand="block" :onclick="Go2Setting">
        My Setting
    </ion-button>
    
    <ion-list>
      <ion-header>
        <ion-toolbar>
          <ion-title size="small">{{ PTag }}</ion-title>
        </ion-toolbar>
      </ion-header>
      <ion-item v-for="item in loginData" v-on:click="next(item)" style="text-decoration: underline;color:#3880ff;">
        {{ item.PFName }} {{ item.PLName}} 
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
        loginData:[{
          PFName:"",
          PLName:""
        }],
        PTag:"Patients:",
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
      console.log("loadPeople");
      this.loginData=window['loginData'];
      this.userData=window['UserData'];
      if(this.userData.role=="125"||this.userData.role=="110"||this.userData.role=="Lawyer"||this.userData.role=="Social Services")
        this.PTag="Clients:"
      else if(this.userData.role=="Parent")
        this.PTag="Childs:"
  },

  methods: {
    async next(input:any) {
       var url="http://192.168.121.135:8000/chk/"+this.userData.Uname+"/"+this.userData.role+"/"+this.userData.passwd;
       
       await fetch(url, {
        method: "GET",
       })
       .then(res => res.json())
        .then(response => {
          console.log("Refresh:",response);
          window['loginData'] = response;
          if (typeof(response)!=typeof("")){
            for (var i = 0; i < response.length; i++){
                if(response[i].URIdPatient==input.URIdPatient){
                    window['selectedPerson']=input;
                    this.$router.push("/person");
                    return;
                }
            }
            this.$router.go(0);
          }
          else
            this.$router.push("/login");
      });
    },

    Go2Setting(){
      window['selectedPerson']='';
      this.$router.push("/setting");
    },

    async Go2Notif(){
      var url="http://192.168.121.135:8000/notifs/"+this.userData.Uname+"/";
       
      await fetch(url, {
      method: "GET",
      })
      .then(res => res.json())
      .then(response => {
        console.log("Notifs:",response);
        window['Notifs']=response;
        this.$router.push("/notifications");
      });
    }
  },

})

</script> 


