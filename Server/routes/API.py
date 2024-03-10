import json
from bson import ObjectId
from fastapi import APIRouter,Request
from config.db import conn #write this yourself
# from schemas.user import serializeDictUser, serializeList, serializeDictData
from urllib.request import urlopen
from pydantic import BaseModel
# import logging
from tb_rest_client.rest_client_ce import *
from tb_rest_client.rest import ApiException
# from datetime import datetime
import pytz
import requests 

user = APIRouter()
 
class TbLocationData(BaseModel):
    latitude: float
    longitude: float

#sign_up
@user.post('/signup/{UserName}/{role}/{passw}/{FName}/{LName}/{Birthday}/')
async def signup(UserName,role,passw,FName,LName,Birthday):
    output=1

    #chk DB for same Uname, if no same Uname was founded, create new user 
    #   & output=0 

    return output 

#sign_in
@user.get('/signin/{UserName}/{role}/{passw}')
async def userExist(UserName,role,passw):
    #chk DB for this user with this role

    # if user wasn't found:
    #     output="NoUser"
    # elif passw was incorrect:
    #     output="IncorrectPassw"
    # elif role was incorrect:
    #     output="WrongRole"
    # else:
    #     output=fetchPersonalInfo()

    return "replace output value" 

#fetchPersonalInfo
@user.get('/user/info/{UName}/{role}/{passw}')#{URIdPatient}/
async def fetchPersonalInfo(UName,role,passw):

    #data=get the data of user and own accesses, which is included its relations from DB

    return "replace data variable"
    
#fetchRelsInfo
@user.get('/user/info/{UName}/{role}/{passw}/{relRole}/{relUserName}')
async def fetchRelsInfo(UName,role,passw,relRole,relUserName):
    data=userExist(UName,role,passw)

    #if relUserName in data.rels.UserName:
    #   chk & find role & UserName of rel 
    #   userAccess2relData= data.user.access2thatRelData
    #       then data=fetch its data according to userAccess to data of that rel 
    
    return "repalce data variable"

#ACderive
@user.post('/AC/{UName}/{role}/{passw}/{relRole}/{relUserName}/{newAC}/')
async def ACderive(UName,role,passw,relRole,relUserName,newAC):
    data=fetchRelsInfo(UName,role,passw,relRole,relUserName)
    #if (newAC>data.access && newAC< relRole.parent.dataAC(should fetch it seperately)) or newAC<data.access:
    #   data.access= newAC
    #else customise 1; should chk and specify that (it's fix or not) 
    #   if isn't add role at the higher layer
    return fetchRelsInfo(UName,role,passw,relRole,relUserName)#mean refresh

#AddRel
@user.post('/add/rel/{UserName}/{role}/{passw}/{relRole}/{relUserName}')
async def addRels(UserName,role,passw,relRole,relUserName):
    data=userExist(UserName,role,passw)
    #if relUserName exists add it as a relRole to user relations(rels): data.rels.add(relUserName,relRole)

#RevokeRel
@user.post('/revoke/rel/{UserName}/{role}/{passw}/{relRole}/{relUserName}')
async def revokeRels(UserName,role,passw,relRole,relUserName):
    data=userExist(UserName,role,passw)
    #if relUserName in data.rels.UserName: 
    #  chk & find role & UserName of rel 
    #   revoke this relation

#changeMyData
@user.post('/data/{UserName}/{role}/{passw}/{partofData}/{newData}')
async def changeData(UserName,role,passw,partofData,newData):
    data=userExist(UserName,role,passw)
    #chk access, some data may shouldn't change, if data.access was fetched for change(W) partofData
    data.partofData=newData
    
#changeRelData
@user.post('/data/{UserName}/{role}/{passw}/{relRole}/{relUserName}/{partofData}/{newData}')
async def changeRelData(UserName,role,passw,relRole,relUserName,partofData,newData):
    data=userExist(UserName,role,passw)
    #if relUserName in data.rels.UserName:
    #   chk & find role & UserName of rel 
    #   userAccess2relpartofData= data.user.access2RelpartofData
    #       then if userAccess2relpartofData in change  partofData:
    data.partofData=newData
