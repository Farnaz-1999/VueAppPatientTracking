<template>
    <ion-header>
        <ion-toolbar>
            <ion-title>{{ userData.FName }} {{ userData.LName }} signed in as a {{ userData.role }}</ion-title>
        </ion-toolbar>
    </ion-header>
    
    <ion-content class="ion-padding">
        <ion-header>
            <ion-toolbar>
                <ion-title size="small">Setting</ion-title>                
            </ion-toolbar>
        </ion-header>

        <ion-list v-show="NameEdition">
            <ion-item-divider color="light">
                Edit Your Information
            </ion-item-divider>

            <ion-item>
                <ion-input type="text" required placeholder="FistName" label="FistName" :value="userData.FName"></ion-input>
            </ion-item>
            <ion-item>
                <ion-input type="text" required placeholder="LastName" label="LastName" :value="userData.LName"></ion-input>
            </ion-item>
            <ion-item>
                <ion-input type="password" required placeholder="Password" label="Password" :value="userData.passwd"></ion-input> 
            </ion-item>
            <ion-button expand="block">Edit</ion-button>
        </ion-list>
    
        <ion-list v-show="NameEdition || RelManagement">
            <ion-item-divider color="light">
                Manage Your Relations
            </ion-item-divider>

            <ion-item>
                <ion-select  @ionChange="relation=$event.target.value" :value="relation"  label="Your Related Role">
                    <ion-select-option value="">---</ion-select-option>
                    <ion-select-option value="Dr">Doctor</ion-select-option>
                    <ion-select-option value="Parent">Parent</ion-select-option>
                    <ion-select-option value="Nurse">Nurse</ion-select-option>
                    <ion-select-option value="Surgeon">Surgeon</ion-select-option>
                    <ion-select-option value="Invited Doctor">Invited Doctor</ion-select-option>
                    <ion-select-option value="Family Doctor">Family Doctor</ion-select-option>
                    <ion-select-option value="Lawyer">Lawyer</ion-select-option>
                    <ion-select-option value="Other">Other</ion-select-option>
                </ion-select>
            </ion-item>
                <ion-button @click="OpenManageRel(true)" expand="block" :disabled="relation==''">Manage</ion-button>
        </ion-list>

        <ion-list v-show="!NameEdition">
            <ion-item-divider color="light">
                Manage Fence
            </ion-item-divider>
            
            <ion-button @click="OpenFense(true)" expand="block">Create Fence</ion-button>
        </ion-list>
    
        <ion-modal :is-open="manageRel" @didDismiss="OpenManageRel(false)">
            <ion-header>
                <ion-item>
                    <ion-title>Manage {{ relation }} Permissions</ion-title>
                    <ion-button @click="OpenManageRel(false)" color="light">Done</ion-button>
                </ion-item>
            </ion-header>

            <ion-content class="ion-padding">

                <ion-item-group v-for="item in relsData">
                    <ion-item-divider color="light">
                        <ion-label> {{ item.name }} </ion-label>
                    </ion-item-divider>

                    <ion-list v-for="subItem in item.access" style="padding: 0;">
                        <ion-item-divider v-show="chkAccPrnt(item,subItem)" lines="full">
                           >{{ subItem.prnt }}
                        </ion-item-divider>
                        <ion-item-divider v-show="chkAccPrntChild(item,subItem)" lines="full">
                           >>{{ subItem.PrntChild }}
                        </ion-item-divider>
                        <ion-item>
                            <ion-select @ionChange="subItem.access=$event.target.value" :label="subItem.asset" :value="subItem.access" :disabled="subItem.disabled">
                                <ion-select-option value="-">No access</ion-select-option>
                                <ion-select-option value="R">Just Read</ion-select-option>
                                <ion-select-option value="WR">Update</ion-select-option>
                                <ion-select-option value="R*">Share</ion-select-option>
                                <ion-select-option value="WR*">Update & Share</ion-select-option>
                            </ion-select>
                        </ion-item>                          
                    </ion-list>             

                    <ion-item>
                        <ion-button @click="updateAccess(item)">  
                            Update
                        </ion-button>
                        <ion-button @click="removeRole2Role(item)" color="danger"> 
                            Remove
                        </ion-button>
                    </ion-item>
                </ion-item-group>

                <ion-item-group>
                    <ion-item-divider color="light">
                        <ion-label>New {{relation}} </ion-label>
                    </ion-item-divider>

                    <ion-item>
                        <ion-input v-model="RelUname" label="Username" placeholder="092"/>
                        <ion-button @click="addRole2Role">Add</ion-button>
                    </ion-item>
                </ion-item-group>

            </ion-content>
        </ion-modal>

      <ion-modal :is-open="newFense" @didDismiss="OpenFense(false)">
        <ion-header>
          <ion-item>
            <ion-title>Create Fense</ion-title>
            <ion-button @click="OpenFense(false)" color="light">Done</ion-button>
          </ion-item>
        </ion-header>

        <ion-content class="ion-padding">
            <ion-item>
                <ion-input type="number" min="4" v-model="cornersNO" placeholder="4" label="Select Number of Corners:"></ion-input>
            </ion-item>

            <ion-item>
                <NeshanMap
                    ref="FensMapRef"
                    :map-key="mapKey"
                    :service-key="serviceKey"
                    :traffic="false"
                    :zoom="17"
                    :hide-search-container="true"
                    :map-types="['neshan']"
                    :center="{latitude: 36.31284506713496, longitude: 59.52688883011246}"
                    :markers-icon-callback="omitMarker"
                    @on-click="getPoint"
                >
                </NeshanMap>
            </ion-item>

            <ion-button @click="addFense" expand="block">OK</ion-button>
            <ion-button @click="resetCorners" expand="block" color="light">Reset Points</ion-button><br>
        </ion-content>
      </ion-modal>
      
      <ion-toast :is-open="ErrExist" :message="Err" :duration="5000" @didDismiss="ErrDismiss(false)"></ion-toast>

    </ion-content>
  </template>
  
  <script lang="ts">
    import { defineComponent, ref } from "vue"
    import { HttpResponse } from "@capacitor/core";
    import { Http } from '@capacitor-community/http';
    import NeshanMap from "@neshan-maps-platform/vue3-openlayers"
    import { CreateMarkersPointsItem } from "@neshan-maps-platform/vue3-openlayers/dist/types/components/Map.model";
    import { Geolocation } from '@capacitor/geolocation';
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
            return {
                NameEdition:false,
                RelManagement:false,
                userData:{
                    Uname:null,
                    FName:"",
                    LName:"",
                    role:null,
                    passwd:null,
                    PAccessToken:""
                },           
                relation:"",
                GetRelsUrl:"",
                UpRelsUrl:"",
                InRelsUrl:"",
                DelRelsUrl:"",
                relsData:[
                    {name:"",
                     Uname:"",
                     access:[{PrntChild:"",prnt:"",asset:'',access:"",disabled:false}]}
                ],
                selectedPerson:{
                    DFName: "",
                    DLName: "",
                    PFName: "",
                    PLName: "",
                    URIdDr: "",
                    URIdPatient: "",
                    access: ""
                },
                manageRel:false,
                RelUname:"",
                newFense:false,
                mapKey,
                serviceKey,
                mapInited: false,
                cornersNO:4,
                corners:[],
                features:[],
                layerSource:"",
                Err:"",
                ErrExist:false
            };
        },

        setup() {
            return {}
        },

        watch:{
            relation: function () {
                this.updateRelation(); 
            }
        },

        async mounted () {
            console.log("loadSet");
            this.userData=window['UserData'];
            this.GetRelsUrl="http://192.168.121.135:8000/onceRels/"+this.userData.role+"/"+this.userData.Uname+"/";
            this.UpRelsUrl="http://192.168.121.135:8000/upR2R/"+this.userData.FName+"/"+this.userData.LName+"/"+this.userData.role+"/"+this.userData.Uname+"/";
            this.DelRelsUrl="http://192.168.121.135:8000/delR2R/"+this.userData.role+"/"+this.userData.Uname+"/";
            this.InRelsUrl="http://192.168.121.135:8000/inR2R/"+this.userData.FName+"/"+this.userData.LName+"/"+this.userData.role+"/"+this.userData.Uname+"/";
            if(this.userData.role!="Patient")
                this.selectedPerson=window['selectedPerson'];
            if(typeof(this.selectedPerson)==typeof("") || this.userData.role=="Patient")
                this.NameEdition=true;
            if(this.userData.role=="Parent" || this.userData.role=="Lawyer"){
                this.RelManagement=true;
                this.GetRelsUrl="http://192.168.121.135:8000/onceRels/ /"+this.selectedPerson.URIdPatient+"/";
                this.UpRelsUrl="http://192.168.121.135:8000/upR2R/"+this.selectedPerson.PFName+"/"+this.selectedPerson.PLName+"/ /"+this.selectedPerson.URIdPatient+"/";
                this.DelRelsUrl="http://192.168.121.135:8000/delR2R/ /"+this.selectedPerson.URIdPatient+"/";
                this.InRelsUrl="http://192.168.121.135:8000/inR2R/"+this.selectedPerson.PFName+"/"+this.selectedPerson.PLName+"/ /"+this.selectedPerson.URIdPatient+"/";
            }
        },

        methods: {
            async updateRelation() {
                this.relsData=[];
                // var fixRelAssetOptions:[""]=[];
                var dis=false;

                if (this.relation!=""){
                    // var GetAccessUrl="http://localhost:8000/getAccess/"+this.relation;
                    var url=this.GetRelsUrl+this.relation;
            
                    // const doGetAccess = async() => {
                    //     const options = {
                    //         url: GetAccessUrl,
                    //         headers: { 'X-Fake-Header': 'Max was here' },
                    //         params: { size: 'XL' },
                    //     };
                
                    //     const response: HttpResponse = await Http.get(options);
                    //     for (const [key, value] of Object.entries(response.data))
                    //         if (typeof(value)!=typeof("")){    
                    //             for (const [k, v] of Object.entries(value)){
                    //                 if (typeof(v)!=typeof("")){    
                    //                     for (const [kk, vv] of Object.entries(v)){
                    //                         if (vv !='-')
                    //                             fixRelAssetOptions.push(kk);
                    //                     }
                    //                 }
                    //                 else if (v !='-')
                    //                   fixRelAssetOptions.push(k);
                    //             }
                    //         }
                    //         else if (value !='-'){
                    //             fixRelAssetOptions.push(key);
                    //         }
                    // };

                    const doGetRels = async() => {
                        const options = {
                            url: url,
                            headers: { 'X-Fake-Header': 'Max was here' },
                            params: { size: 'XL' },
                        };
                
                        const response: HttpResponse = await Http.get(options);
                        console.log("rels:",response.data);
                        for (const rel of Object.values(response.data)){
                            var accesses=JSON.parse(rel["access"].replace(/'/g, "\""));        
                            var RelsAccessData=[];
                            for (const [asset, access] of Object.entries(accesses)){
                                if (typeof(access)!=typeof(""))            
                                    for (const [asse, acce] of Object.entries(access)){
                                        if (typeof(acce)!=typeof(""))
                                            for (const [ass, acc] of Object.entries(acce)){
                                                // var dis=fixRelAssetOptions.includes(ass) ? true:false;
                                                RelsAccessData.push({PrntChild:asse,prnt:asset, asset:ass, access:acc, disabled:dis});
                                        
                                            }
                                        else{
                                            // var dis=fixRelAssetOptions.includes(asse) ? true:false;
                                            RelsAccessData.push({PrntChild:"",prnt:asset, asset:asse, access:acce, disabled:dis});
                                        }
                                    }
                                else{     
                                    // var dis=fixRelAssetOptions.includes(asset) ? true:false;
                                    RelsAccessData.push({PrntChild:"",prnt:"", asset:asset, access:access, disabled:dis});
                                }
                            }
                            
                            this.relsData.push({
                                name:rel["DFName"]+" "+rel["DLName"],
                                URId:rel["URIdDr"],
                                access:RelsAccessData
                            });
                        }
                    };

                    // await doGetAccess();
                    await doGetRels();
                }
            },

            OpenManageRel(bool:boolean){
                this.manageRel=bool;
            },

            chkAccPrnt(item:any,subItem:any){
                var output=false;
                let index=item["access"].indexOf(subItem);
                if(subItem.prnt!='' && ((index !=0 && item["access"][index-1].prnt!=subItem.prnt) || index==0))
                    output=true;               
                return output;
            },

            chkAccPrntChild(item:any,subItem:any){
                var output=false;
                let index=item["access"].indexOf(subItem);
                if(subItem.PrntChild!='' && ((index !=0 && item["access"][index-1].PrntChild!=subItem.PrntChild) || index==0))
                    output=true;               
                return output;
            },

            async updateAccess(item:any){
                var access="";
                
                for (const value of Object.values(item["access"])){
                    access = access + value.asset.match(/\b(\w)/g).join('');
                    access=access + " " + value.access + " ";
                }

                var url=this.UpRelsUrl+this.relation+"/"+item.URId+"/"+access;

                const doGet = async() => {
                    const options = {
                        url: url,
                        headers: { 'X-Fake-Header': 'Max was here' },
                        params: { size: 'XL' },
                    };

                    const response: HttpResponse = await Http.get(options);
                };

                await doGet();
                this.updateRelation();
            },

            async removeRole2Role(item:any){
                var url=this.DelRelsUrl+item.URId+"/"+this.relation;
                
                const doGet = async() => {
                    const options = {
                        url: url,
                        headers: { 'X-Fake-Header': 'Max was here' },
                        params: { size: 'XL' },
                    };

                    const response: HttpResponse = await Http.get(options);
                };

                await doGet();
                this.updateRelation();
            },

            async addRole2Role(item:any){
                var url=this.InRelsUrl+this.relation+"/"+this.RelUname;

                const doGet = async() => {
                    const options = {
                        url: url,
                        headers: { 'X-Fake-Header': 'Max was here' },
                        params: { size: 'XL' },
                    };

                    const response: HttpResponse = await Http.get(options);
                    console.log("AddR2R:",response);

                    if (response.data=="done !!!")
                        this.updateRelation();
                    else{
                        this.Err=response.data;    
                        this.ErrExist=true;
                    }               
                };

                await doGet();
                this.RelUname="";
            },

            OpenFense(bool:boolean){
                this.newFense=bool;
                if(!bool)
                    this.mapInited=false;

            },

            InitLayer(){
                let myMap =this.$refs.FensMapRef.state.map;

                this.layerSource =new ol.source.Vector({features: []}); 
                let layer = new ol.layer.Vector({
                    source: this.layerSource,
                    style: new ol.style.Style({
                        image: new ol.style.Icon({
                        color: '#22eeff',
                        crossOrigin: 'anonymous',
                        src: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAAsTAAALEwEAmpwYAAAC+klEQVR4nO2ZzUuUURTGf8lYaf0BQiBGBhWFm6BF/0G7hD5WtSopa1OYLtoUoujSZSAGElIiRJQVQavaROAqaJOFxFAaMo4GhoMTF54ZXl5mrvfGDDJ5HniYyzvPmfPeM/fjnHvBYDAYDAaDwcBu4CbwHHgB3AJa/oO4ZIAbwDPgKXAFaEqL9gLvgWKKH4H9NC72AO8q9Ou1AlPG3QqiEodpXNz39Ot2UvjBI/xE4+Kzp1+uz2V89QiXaFwsefrl+lyGBQAbAfzLFDgGdKrdBbRHDM8zWokzaoeiXb6Q76O1nAJ/gPmIALhVNgcMAuvaY0PQot99KS5qKw7BVfkalO97tQzAFHAkJdxQPlCJcwldwaOrxGzCNhtpW0jYznl0G7EB+KmMKSlcA/qrcFaahUQA+wM4AOT1D+bUHgi0nUr5nPVo12ID8B14FDEFevTizcAocDZwGLvhPg2cEKeVtYWgW76a5du9Q82mwEOgYyfnARMWAGwEdNgUwNaAoi2C2C5QtG0QywOKWyRCB4EDah8G2iKSlNM6nGxSOxRt8oV8u3fYtkRoWN/3Ke++HlENuhrgiZiLqAZ75atPvofqHYAC8KUKSwVJifMebZorCbuVCLt0ub7g0RZqEYBV1eCVOCnNL32OebRJ9qgE/i1m9SzEdizlc9KjXY0NwGOdsIROgTvACNAKPAAuBQ5jd9fwFjgluva+QNvL8tUq324q1GwKFIAfOzkTLFagBYDGhY0AbApgawC2CGK7ALYNUpc8oEs3SQ4ngUOB29Mune+X7ga79SwEnfKFstbSPeG27AKDKmSGdF/nu6RIp8LuPvCVuBiRCl+TryH5du9Q1wBsAstVmEtplyO4nrBbj7RN+sx5dJu1CEAeOFeF49J80+eoR5vkRVWApbtB174QaDua8jnu0ebrPQV6dT+XUWXmnIbAVXIzwHFxRs9CcF5ByMi37xDGMkEsE8QyQSwTxDJBttgFRoA3VegOIRsVY55+uT4bDAaDwWAwsGPxF9RjmnC9KuEbAAAAAElFTkSuQmCC",
                        scale:0.4
                        })
                    })
                })

                myMap.addLayer(layer);
            },

            omitMarker(point: CreateMarkersPointsItem) {
                if (point.isReverseMarker) {
                    return {
                        src: ""
                    }
                } else {
                    return {
                        src: "",
                        iconScale: 0.05
                    }
                }
            },

            getPoint(point:any){
                if(!this.mapInited){
                    this.InitLayer();
                    this.mapInited=true;
                }

                let myMap =this.$refs.FensMapRef.state.map;
                console.log('getPoint:',point);
                this.corners.push([point.coords[1],point.coords[0]]);
                
                let tmp = new ol.Feature({
                            geometry: new ol.geom.Point(ol.proj.fromLonLat([point.coords[0],point.coords[1]]))
                });
                this.features.push(tmp);                        
                this.layerSource.clear(true);
                this.layerSource.addFeatures(this.features);            
                myMap.render();

                console.log("Map Fensed",tmp);
            },

            addFense(){
                this.Err="";
                
                if(this.corners.length==this.cornersNO){
                    var url="http://192.168.121.135:8000/addFenseTo/"+this.selectedPerson.URIdPatient;

                    fetch(url, {
                        method: "POST",
                        headers: {
                        'Content-Type':"application/json"
                        }, 
                        body: JSON.stringify({
                            perimeter:this.corners
                        })
                    })
                    .then(res => res.json())
                        .then(response => {
                            console.log("Add Fense with:",this.corners);
                            console.log("Response:",response);
                    });
                    this.Err="Fence Successfully added !!!"
                }
                else if(this.corners.length>this.cornersNO)
                    this.Err="You choose more points than what you wanted !!!"
                else
                    this.Err="Some Point(s) Remind to select !!!";
                
                this.ErrExist=true;
            },

            resetCorners(){
                this.corners=[];
                this.features=[];
                this.layerSource.clear(true);
            },

            ErrDismiss(x:boolean){
                this.ErrExist=x;
                this.Err="";
            }

            /* async getCurrentPosition() {
                 const coordinates = await Geolocation.getCurrentPosition();
                 console.log('Current', coordinates.coords);
                 return coordinates.coords;
            },*/

        },

    })

  </script>