import json
from bson import ObjectId
from fastapi import APIRouter,Request
from config.db import conn #write this yourself
from schemas.user import serializeDictUser, serializeList, serializeDictData
from urllib.request import urlopen
from pydantic import BaseModel
import logging
from tb_rest_client.rest_client_ce import *
from tb_rest_client.rest import ApiException
from datetime import datetime
import pytz
import requests


user = APIRouter()
 
class TbLocationData(BaseModel):
    latitude: float
    longitude: float

@user.get('/chk/{UName}/{role}/{passw}')
async def exist(UName,role,passw):
    user=conn.PatientData.User2Role.find_one({'UName':UName,'role':role})
    passCheck=conn.PatientData.Users.find_one({'UName':UName,'pass':passw})
    if user!=None and passCheck!=None:
        relations=conn.PatientData.Role2Role.find({'URIdDr':user.get("URId"),'RelRole':role})
        if relations!=None:
            output=serializeList(relations)
        else:
            output="NoRel"
    elif user!=None and passCheck==None:
        output="WrongPass"
    elif user==None and passCheck!=None:
        output="WrongRole"
    else:
        output="NoUser"
    return output 

@user.get('/user/{UName}/{role}/{passw}')
async def getUser(UName,role,passw):
    user=conn.PatientData.User2Role.find_one({'UName':UName,'role':role})
    passCheck=conn.PatientData.Users.find_one({'UName':UName,'pass':passw})
    if user!=None and passCheck!=None:
        output=serializeDictUser(user)
    elif user!=None and passCheck==None:
        output="WrongPass"
    elif user==None and passCheck!=None:
        output="WrongRole"
    else:
        output="NoUser"
    return output 

@user.get('/data/loc/{URIdPatient}/{UName}/{role}/{passw}')
async def getLoc(URIdPatient,UName,role,passw):
    data=None
    accessChk=await exist(UName,role,passw)
    if accessChk is not str:
        for item in accessChk:
            RBaccess=eval(item.get("access"))
            if item.get("URIdPatient")==URIdPatient and RBaccess.get("Telemetry").get("Personal Telemetry").get("Location Telemetry")!="-":
                data=conn.PatientData.WareHouseData.find_one({'URIdPatient':int(URIdPatient)})
                if data!=None:
                    return serializeDictData(data)
                else:
                    return "No Loc Data"
            elif item.get("URIdPatient")==URIdPatient and RBaccess.get("Telemetry").get("Personal Telemetry").get("Location Telemetry")=="-":
                return "No Loc Access"
        if data==None:
            return "Patient Access Revoked !!!"
    else:
        return "User Problem !!!"
    
@user.get('/data/insurance/{UName_URId}/{UName}/{role}/{passw}')
async def getInsurance(UName_URId,UName=" ",role=" ",passw=" "):
    data=None
    if(UName!=" "):
        accessChk=await exist(UName,role,passw)
        if accessChk is not str:
            for item in accessChk:
                RBaccess=eval(item.get("access"))
                if item.get("URIdPatient")==UName_URId and RBaccess.get("Insurance Data")!="-":
                    data=conn.PatientData.Insurance.find_one({'URIdPatient':int(UName_URId)})
                    break
                elif item.get("URIdPatient")==UName_URId and RBaccess.get("Insurance Data")=="-":
                    return "No Access !!!"
        else:
            return "User Problem !!!"
    else:
        patientId=conn.PatientData.User2Role.find_one({'UName':UName_URId}).get("URId")
        data=conn.PatientData.Insurance.find_one({'URIdPatient':patientId})

    if data!=None:
        output=[data]
        for i in output:
            i['_id'] = ""
        return output
    else:
        return "No Data"

@user.get('/data/info/{UName_URId}/{UName}/{role}/{passw}')
async def getInfo(UName_URId,UName=" ",role=" ",passw=" "):
    data=None
    if(UName!=" "):
        accessChk=await exist(UName,role,passw)
        if accessChk is not str:
            for item in accessChk:
                RBaccess=eval(item.get("access"))
                if item.get("URIdPatient")==UName_URId and RBaccess.get("Information").get("Personal Information")=="-" and RBaccess.get("Information").get("Biometric Information")=="-":
                    return "No Access !!!"
                elif item.get("URIdPatient")==UName_URId and RBaccess.get("Information").get("Personal Information")=="-" and RBaccess.get("Information").get("Biometric Information")!="-":
                    data=conn.PatientData.BioInfo.find_one({'URIdPatient':int(UName_URId)})
                    if data!=None:
                        output=[data]
                        for i in output:
                            i['_id'] = ""
                        return output
                    break
                elif item.get("URIdPatient")==UName_URId and RBaccess.get("Information").get("Personal Information")!="-" and RBaccess.get("Information").get("Biometric Information")=="-":
                    data=conn.PatientData.PersonalInfo.find_one({'URIdPatient':int(UName_URId)})
                    if data!=None:
                        output=[data]
                        for i in output:
                            i['_id'] = ""
                        return output
                    break
                elif item.get("URIdPatient")==UName_URId and RBaccess.get("Information").get("Personal Information")!="-" and RBaccess.get("Information").get("Biometric Information")!="-":
                    pipeline=[
                        {
                            '$match': {
                                'URIdPatient': int(UName_URId)
                            }
                        }, {
                            '$lookup': {
                                'from': 'BioInfo', 
                                'localField': 'URIdPatient', 
                                'foreignField': 'URIdPatient', 
                                'as': 'bio'
                            }
                        }, {
                            '$unwind': {
                                'path': '$bio', 
                                'preserveNullAndEmptyArrays': False
                            }
                        }
                    ]
                    data=conn.PatientData.PersonalInfo.aggregate(pipeline)
                    if data!=None:
                        output=list(data)
                        for i in output:
                            i['_id'] = ""
                            i['bio']['_id']=""
                        return output
                    break
        else:
            return "User Problem !!!"
    else:
        patientId=conn.PatientData.User2Role.find_one({'UName':UName_URId}).get("URId")
        pipeline=[
            {
                '$match': {
                    'URIdPatient': patientId
                }
            }, {
                '$lookup': {
                    'from': 'BioInfo', 
                    'localField': 'URIdPatient', 
                    'foreignField': 'URIdPatient', 
                    'as': 'bio'
                }
            }, {
                '$unwind': {
                    'path': '$bio', 
                    'preserveNullAndEmptyArrays': False
                }
            }
        ]
        data=conn.PatientData.PersonalInfo.aggregate(pipeline)

    if data!=None:
        output=list(data)
        for i in output:
            i['_id'] = ""
            i['bio']['_id']=""
        return output
    
    else:
        return "No Data"

@user.get('/data/Hinfo/{UName_URId}/{UName}/{role}/{passw}')
async def getHinfo(UName_URId,UName=" ",role=" ",passw=" "):
    data=None
    if(UName!=" "):
        accessChk=await exist(UName,role,passw)
        if accessChk is not str:
            for item in accessChk:
                RBaccess=eval(item.get("access"))
                if item.get("URIdPatient")==UName_URId and RBaccess.get("Health Information").get("Health Information Log")!="-":
                    data=conn.PatientData.HealthILog.find_one({'URIdPatient':int(UName_URId)})
                    break
                elif item.get("URIdPatient")==UName_URId and RBaccess.get("Health Information").get("Health Information Log")=="-":
                    return "No Access !!!"
        else:
            return "User Problem !!!"
    else:
        patientId=conn.PatientData.User2Role.find_one({'UName':UName_URId}).get("URId")
        data=conn.PatientData.HealthILog.find_one({'URIdPatient':patientId})

    if data!=None:
        output=[data]
        for i in output:
            i['_id'] = ""
        return output
    else:
        return "No Data"

@user.get('/data/HSinfo/{UName_URId}/{UName}/{role}/{passw}')
async def getHSinfo(UName_URId,UName=" ",role=" ",passw=" "):
    data=None
    if(UName!=" "):
        accessChk=await exist(UName,role,passw)
        if accessChk is not str:
            for item in accessChk:
                RBaccess=eval(item.get("access"))
                if item.get("URIdPatient")==UName_URId and RBaccess.get("Health Information").get("Health Situation")!="-":
                    data=conn.PatientData.HealthISituation.find_one({'URIdPatient':int(UName_URId)})
                    break
                elif item.get("URIdPatient")==UName_URId and RBaccess.get("Health Information").get("Health Situation")=="-":
                    return "No Access !!!"
        else:
            return "User Problem !!!"
    else:
        patientId=conn.PatientData.User2Role.find_one({'UName':UName_URId}).get("URId")
        data=conn.PatientData.HealthISituation.find_one({'URIdPatient':patientId})

    if data!=None:
        output=[data]
        for i in output:
            i['_id'] = ""
        return output
    else:
        return "No Data"

@user.get('/getAccess/{role}')
async def getRoleAccess(role):
    roleData=conn.PatientData.Roles.find_one({'role':role})
    output=roleData.get("access")
    return output

@user.get('/onceRels/{role}/{UName_URIdPatient}/{relRole}')
async def getPRels(role,UName_URIdPatient,relRole):
    if(role!=" "):
        patientID=conn.PatientData.User2Role.find_one({'UName':UName_URIdPatient,'role':role}).get("URId")
        rels=conn.PatientData.Role2Role.find({'URIdPatient':patientID,'RelRole':relRole})
    else:
        rels=conn.PatientData.Role2Role.find({'URIdPatient':int(UName_URIdPatient),'RelRole':relRole})
    output=serializeList(rels)
    return output

@user.get('/upR2R/{FName}/{LName}/{role}/{UName_URId}/{RelRole}/{RelUId}/{access}')
async def updateR2R(FName,LName,role,UName_URId,RelRole,RelUId,access):
    accessInputArray=access.split(' ')
    DrRoleAccess=await getRoleAccess(RelRole)

    for key, value in DrRoleAccess.items():
        if type(value)!=dict:
            asset= ''.join(l[0] for l in key.split())
            for i in range(0,len(accessInputArray),2):
                if accessInputArray[i]==asset:
                    DrRoleAccess[key]=accessInputArray[i+1]
        else:            
            for k, v in value.items():
                if type(v)!=dict:
                    asset= ''.join(l[0] for l in k.split())
                    for i in range(0,len(accessInputArray),2):
                        if accessInputArray[i]==asset:
                            DrRoleAccess[key][k]=accessInputArray[i+1]
                else:
                    for kk, vv in v.items():
                        asset= ''.join(l[0] for l in kk.split())
                        for i in range(0,len(accessInputArray),2):
                            if accessInputArray[i]==asset:
                                DrRoleAccess[key][k][kk]=accessInputArray[i+1]

    Druser2role=conn.PatientData.User2Role.find_one({'URId':int(RelUId)})
    if(role!=" "):
        Puser2roleId=conn.PatientData.User2Role.find_one({'role':role,'UName':UName_URId}).get("URId")
    else:
        Puser2roleId=int(UName_URId)

    conn.PatientData.Role2Role.update_one({'URIdPatient': Puser2roleId,'URIdDr': int(RelUId)},
                                          { "$set":{'URIdPatient': Puser2roleId,'URIdDr': int(RelUId),
                                           'access': DrRoleAccess,
                                           'PFName':FName,'PLName':LName,'DFName':Druser2role.get("FName"),'DLName':Druser2role.get("LName"),'RelRole':RelRole}})
    return

@user.get('/delR2R/{role}/{UName_URId}/{RelUId}/{RelRole}')
async def delR2R(role,UName_URId,RelUId,RelRole):
    if(role!=" "):
        Puser2roleId=conn.PatientData.User2Role.find_one({'role':role,'UName':UName_URId}).get("URId")
    else:
        Puser2roleId=int(UName_URId)
    conn.PatientData.Role2Role.delete_one({'URIdPatient': Puser2roleId,'URIdDr': int(RelUId),'RelRole':RelRole})
    return

@user.get('/inR2R/{FName}/{LName}/{role}/{UName_URId}/{RelRole}/{RelUName}')
async def insertR2R(FName,LName,role,UName_URId,RelRole,RelUName):
    DrRoleAccess=await getRoleAccess(RelRole)
                
    Druser2role=conn.PatientData.User2Role.find_one({'role':RelRole,'UName':RelUName})
    if(role!=' '):
        Puser2roleId=conn.PatientData.User2Role.find_one({'role':role,'UName':UName_URId}).get("URId")
    else:
        Puser2roleId=int(UName_URId)

    if(Druser2role!=None):
        conn.PatientData.Role2Role.insert_one({'URIdPatient': Puser2roleId,'URIdDr': Druser2role.get("URId"),
                                           'access': DrRoleAccess,
                                           'PFName':FName,'PLName':LName,'DFName':Druser2role.get("FName"),'DLName':Druser2role.get("LName"),'RelRole':RelRole})
        output="done !!!"
    else:
        output="Wrong UserName !!!"
    return output

@user.post('/api/data/{deviceName}')
async def set_location_data(deviceName,request: Request):
    patientID=conn.PatientData.User2Role.find_one({'UName':deviceName[11:],'role':"Patient"}).get("URId")
    data=await request.json()
    data.update({'URIdPatient':patientID})
    isthere=conn.PatientData.WareHouseData.find_one({'URIdPatient':patientID})
    if(isthere!=None):
        conn.PatientData.WareHouseData.update_one({'URIdPatient':patientID},{"$set":data})
    else:
        conn.PatientData.WareHouseData.insert_one(data)

@user.post('/addFenseTo/{urId}')
async def getPRels(urId,request: Request):
    data=await request.json()
    patientToken=conn.PatientData.User2Role.find_one({'URId':int(urId)}).get("AccessToken")        

    json_data = data
    response = requests.post("http://mytb:9090/api/v1/"+patientToken+"/telemetry", json=json_data)

@user.post('/api/alert/{deviceName}/')
async def needAlert(deviceName):
    user=conn.PatientData.User2Role.find_one({'UName':deviceName[11:]})
    timeStr=datetime.now(pytz.timezone('Iran')).strftime("%Y:%m:%d %H:%M:%S")
    data=conn.PatientData.Notifs.find_one({'URIdPatient':user.get("URId"), "Time":timeStr})
    if(data==None):
        conn.PatientData.Notifs.insert_one({'URIdPatient':user.get("URId"), "Time":timeStr})

@user.get('/notifs/{UName}/')
async def getNotifs(UName):
    pipeline = [
        {
            '$match': {
                'UName': "093"
            }
        }, {
            '$lookup': {
                'from': 'Role2Role', 
                'localField': 'URId', 
                'foreignField': 'URIdDr', 
                'as': 'r2r'
            }
        }, {
            '$unwind': {
                'path': '$r2r', 
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$match': {
                'r2r.access.Telemetry.Personal Telemetry.Location Telemetry': {
                    '$in': [
                        'R', 'WR', 'WR*'
                    ]
                }
            }
        }, {
            '$lookup': {
                'from': 'Notifs', 
                'localField': 'r2r.URIdPatient', 
                'foreignField': 'URIdPatient', 
                'as': 'notif'
            }
        }, {
            '$unwind': {
                'path': '$notif', 
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$sort': {
                'notif._id': -1
            }
        }
    ]
    relations=conn.PatientData.User2Role.aggregate(pipeline)
    if relations!=None:
        rels=list(relations)
        for rel in rels:
            rel['_id'] = ""
            rel['notif']['_id']=""
            rel['r2r']["_id"] =""   

    return rels

@user.get('/in/{FName}/{LName}/{role}/{passw}/{UName}')
async def insert(FName,LName,role,passw,UName):
    chkExist=await exist(UName,role,passw)
    if chkExist=="NoUser":
        conn.PatientData.Users.insert_one({'FName':FName,'LName':LName,'UName':UName,'pass':passw})
    elif chkExist=="WrongRole":
        pass
    else:
        return "User Exist!!!"
    
    PAccessToken=""

    if(role=="Patient"):
        logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

        # ThingsBoard REST API URL
        url = "http://mytb:9090"
        # Default Tenant Administrator credentials
        username = "tenant@thingsboard.org"
        password = "tenant"

        # Creating the REST client object with context manager to get auto token refresh
        with RestClientCE(base_url=url) as rest_client:
            try:
                # Auth with credentials
                rest_client.login(username=username, password=password)

                device = Device(name="PatientLoc_"+UName, label=""+UName,
                                device_profile_id=DeviceProfileId('33046c80-3057-11ee-a1e5-87c44a77d0e1','DEVICE_PROFILE'))
                device = rest_client.save_device(device)

                # Creating relations from device to asset
                relation = EntityRelation(_from=device.id, to=device.id, type="Contains")
                relation = rest_client.save_relation(relation)

                PAccessToken=rest_client.get_device_credentials_by_device_id(device.id).credentials_id

            except ApiException as e:
                logging.exception(e)

    roleData=conn.PatientData.Roles.find_one({'role':role})
    user2roleIndex=conn.PatientData.User2Role.estimated_document_count()+1
    conn.PatientData.User2Role.insert_one({'FName':FName,'LName':LName,'UName':UName,'role':role,'RId':roleData.get("RId"),'URId':user2roleIndex,'AccessToken':PAccessToken})

    return PAccessToken

# @user.put('/{id}')
# async def update_user(id, user:User):
#     conn.shop.users.find_one_and_update(
#         {'_id':ObjectId(id)},
#         {'$set':dict(user)})
#     return serializeDict(conn.shop.users.find_one({'_id':ObjectId(id)}))

# @user.delete('/{id}')
# async def delete_user(id):
#     return serializeDict(conn.shop.users.find_one_and_delete({'_id':ObjectId(id)}