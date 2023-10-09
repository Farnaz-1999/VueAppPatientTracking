<template>
    <ion-header>
      <ion-toolbar>
        <ion-title>Sign Up</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <form v-on:submit.prevent="Register">
        <ion-list>
          <ion-item>
            <ion-input type="text" required label="FirstName" placeholder="FistName" v-model="FName"></ion-input>
          </ion-item>
          <ion-item>
            <ion-input type="text" required label="LastName" placeholder="LastName" v-model="LName"></ion-input>
          </ion-item>
          <ion-item>
            <ion-input type="text" :required="true" label="UserName" placeholder="UserName" v-model="UName"></ion-input>
          </ion-item>
          <ion-item>
            <ion-input type="password" required placeholder="Password" label="Password" v-model="passwd"></ion-input>
          </ion-item>
          <ion-item>
            <ion-select  @ionChange="role=$event.target.value" required v-model="role"  label="Role">
              <ion-select-option value="">---</ion-select-option>
              <ion-select-option value="Patient">Patient</ion-select-option>
              <ion-select-option value="Dr">Doctor</ion-select-option>
              <ion-select-option value="Parent">Parent</ion-select-option>
              <ion-select-option value="Nurse">Nurse</ion-select-option>
              <ion-select-option value="Surgeon">Surgeon</ion-select-option>
              <ion-select-option value="Invited Doctor">Invited Doctor</ion-select-option>
              <ion-select-option value="Family Doctor">Family Doctor</ion-select-option>
              <ion-select-option value="Lawyer">Lawyer</ion-select-option>
              <ion-select-option value="115">115</ion-select-option>
              <ion-select-option value="125">125</ion-select-option>
              <ion-select-option value="110">110</ion-select-option>
              <ion-select-option value="Social Services">Social Services</ion-select-option>
              <ion-select-option value="Other">Other</ion-select-option>
            </ion-select>
          </ion-item>
          
          <ion-button expand="block" type="submit">Sign Up</ion-button>
          
        </ion-list>

        <ion-toast :is-open="ErrExist" :message="Err" :duration="5000" @didDismiss="ErrDismiss"></ion-toast>

      </form>
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
      IonToast
    } from '@ionic/vue';
  import { Http } from '@capacitor-community/http';
  import { HttpResponse } from "@capacitor/core";
  
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
      IonToast
  },

    data() {
      return {
        FName: "",
        LName: "",
        UName:"",
        role: "",
        passwd:"",
        Err:"",
        ErrExist:false
      };
    },

    mounted () {
        console.log("loadReg");
    },

    methods: {
      async Register() {
        var url="http://192.168.121.135:8000/in/"+this.FName+"/"+this.LName+"/"+this.role+"/"+this.passwd+"/"+this.UName;
  
        const doGet = async() => {
          const options = {
              url: url,
              headers: { 'X-Fake-Header': 'Max was here' },
              params: { size: 'XL' },
          };
  
          const response: HttpResponse = await Http.get(options);
          console.log("In:",response);
          if (response.data=="User Exist!!!"){
            this.Err="User with this UserName exist now !!!";
            this.ErrExist=true;
          }
          else if(response.status==200){
            window['UserData'] = {
              Uname:this.UName,
              FName:this.FName,
              LName:this.LName,
              role:this.role,
              passwd:this.passwd,
              PAccessToken:response.data
            };
            this.$router.push("/login");
          }
          else{
            console.log(response,typeof(response),response.data,typeof(response.data),response.status);
            this.Err="Try later !!!";
            this.ErrExist=true;
          }
        };
        
        if(this.role==""){
          this.Err="Select Your Role :/"
          this.ErrExist=true;
        } 
        else
          await doGet();

      },

      ErrDismiss(){
          this.ErrExist=false;
          this.Err=""
      }

    },
  
  })
  
  </script> 