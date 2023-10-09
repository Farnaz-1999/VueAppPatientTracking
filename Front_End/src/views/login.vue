<template>
  <ion-header>
    <ion-toolbar>
      <ion-title>Sign In</ion-title>
    </ion-toolbar>
  </ion-header>

  <ion-content class="ion-padding">
    <form v-on:submit.prevent="Login">
      <ion-list>

        <ion-item>
          <ion-input type="text" required label="UserName" placeholder="UserName" v-model="UName"></ion-input>
        </ion-item>
        <ion-item>
          <ion-input type="password" required placeholder="Password" label="Password" v-model="passwd"></ion-input>
        </ion-item>
        <ion-item>
          <ion-select  @ionChange=" role=$event.target.value" required v-model="role"  label="Role">
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

          <ion-button type="submit" color="light" expand="block">Sign In</ion-button>
          <ion-button @click="register" expand="block">Sign Up</ion-button>

      </ion-list>
      
      <ion-toast :is-open="ErrExist" :message="Err" :duration="5000" @didDismiss="ErrDismiss(false)"></ion-toast>

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
      UName:"",
      role: "",
      passwd:"",
      Err:"",
      ErrExist:false
    };
  },

  setup() {
      return {}
  },

  mounted () {
      console.log("loadLogin");
  },

  methods: {
    async Login() {
      var url="http://192.168.121.135:8000/chk/"+this.UName+"/"+this.role+"/"+this.passwd;

      const doGet = async() => {
        const options = {
            url: url,
            headers: { 'X-Fake-Header': 'Max was here' },
            params: { size: 'XL' },
        };

        const response: HttpResponse = await Http.get(options);
        console.log("Get:",response.data);

        if (response.data=="NoUser"){
          this.Err="There is not any user with this UserName !!!";
          this.ErrExist=true;
        }
        else if(response.data=="WrongPass"){
          this.Err="Wrong Password !!!";
          this.ErrExist=true;
        }
        else if(response.data=="WrongRole"){
          this.Err="Wrong Role !!!";
          this.ErrExist=true;
        }
        else if(this.role==""){
          this.Err="Select Your Role :/"
          this.ErrExist=true;
        }
        else {
          await fetch("http://192.168.121.135:8000/user/"+this.UName+"/"+this.role+"/"+this.passwd, {
            method: "GET",
          })
          .then(res => res.json())
            .then(response => {
              window['UserData'] = {
                Uname:this.UName,
                FName:response["FName"],
                LName:response["LName"],
                role:this.role,
                passwd:this.passwd,
                PAccessToken:response["AccessToken"]
              };
            });
            if(this.role=="Patient"){
                this.$router.push("/person");
              }
              else{
                window['loginData'] = response.data;
                this.$router.push("/dashboard");
              }
        }


      };

      await doGet();

    },

    register(){
      this.$router.push("/register");
    },

    ErrDismiss(x:boolean){
        this.ErrExist=x;
    }

  },

})

</script> 