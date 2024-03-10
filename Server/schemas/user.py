def serializeDictRelations(item) -> dict:
    return{
        'id':str(item['_id']),
        'URIdPatient': item['URIdPatient'],
        'URIdDr': item['URIdDr'],
        'access': {
                "Biometric Information": item["Biometric Information"],
                "Health Situation": item["Health Situation"],
                "Health Information Log": item["Health Information Log"],
                "Insurance Data": item["Insurance Data"],
                "Personal Information": item["Personal Information"],
                "Telemetry": {
                    "Personal Telemetry":{"Location Telemetry": item["Location Telemetry"]},
                    "Health Telemetry": item["Health Telemetry"]
                }
            },
        'PFName':item['PFName'],
        'PLName':item['PLName'],
        'DFName':item['DFName'],
        'DLName':item['DLName'],
        'RelRole':item['RelRole']
    }

def serializeDictData(item) -> dict:
    return{
        'id':str(item['_id']),
        'URIdPatient': item['URIdPatient'],
        'latitude': item['latitude'],
        'longitude':item['longitude']
    }

def serializeDictUser(item) -> dict:
    return{
        'id':str(item['_id']),
        'role': item['role'],
        'FName': item['FName'],
        'LName': item['LName'],
        'UName':item['UName'],
        'AccessToken':item['AccessToken']
    }

def serializeList(entity) -> list:
    return [serializeDictRelations(item) for item in entity]

def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id'}, **{i:str(a[i]) for i in a if i!='_id'}}

def serializeList(entity) -> list:
    return[serializeDict(a) for a in entity]