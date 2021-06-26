###############################################
# Definitions related to AWS cloud components i.e. IOT core end point definitions
# Define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT, MESSAGE, TOPIC, and RANGE
ECC_CERT_DIR ="certificates"
ENDPOINT = "a1jblcy2osi0b6-ats.iot.ap-south-1.amazonaws.com"
CLIENT_ID = "clientid-0001"
PATH_TO_CERT = "certificates/8f093dc9e2-certificate.pem.crt"
PATH_TO_KEY = "certificates/8f093dc9e2-private.pem.key"
PATH_TO_ROOT = "certificates/root.pem"
# Below topic is the topic which will be publised and same shall be subscribed at aws IoT core.
TOPIC_DATA = "SID1234567890/Data"
TOPIC_FL ="topic-0001"
TOPIC_CONTROL = "SID1234567890/Control"
FRAME_SIZE = 1024
WAITING_FOR_DATA =900

local_host="192.168.43.231" # Local host IP address for Raspberri Pi communication
aws_ec2_host="15.206.164.57"    # Cloud EC2 instance public IP address
aws_ec2_sahngdong="13.234.136.125"
PORT = 5002
MAX_GATEWAY_CLIENTS = 60
# Backlog is parameter in listen socket indicating max no of queued connection
# and we are keeping it at 100
SOCK_BACKLOG =100
# ServiceID is unique for a cutomer
ServiceID = "12345678"
SiteID="1122100000"
ECC_List = [12]


# A class is defined to represent a physical thing ie.e DG set which
# has 8 sensors and other parts to it.
#siteid,noofsensors,serviceID,ThingName,Component,Subcomponent,Part,cert,key,root_pem

class PhysicalThing:
    noOfSensors =8
    topicID = [8]
    certPath = [8]
    keyPath = [8]
    rootCA = [8]
    def __init__(self,siteID,noOfSensors, topicID, certPath, keyPath,rootCA ):
        self.siteID =siteID
        self.noOfSensors = noOfSensors
        self.topicID.append(topicID)
        self.certPath.append(certPath)
        self.keyPath.append(keyPath)
        self.rootCA.append(rootCA)

    def printValues(self):
        print(self.siteID,self.noOfSensors,self.topicID,self.certPath,self.keyPath,self.rootCA)

certificates = {
        "privateCert":"",
        "privatekey":"",
        "rootCA":""
        }
# Sensor data dictionary. Data that is received from Controller
# Serial stream contains all the 6 sensor data
sensorRxData={
#   "Key":"",
   "Site ID":"",      # Max 10 Bytes
   "Function Code":"",  # 1 Byte
   "Sensor1 Data":"",    #  AN1/LubeOildPressure
   "Sensor2 Data":"",    # AN2/Shelter Temperature
   "Sensor3 Data":"",    #  AN3/BTS Volt
   "Sensor4 Data":"",    # AN4/DG Battery Volt
   "Sensor5 Data":"",    # AN5/Fuel
   "Sensor6 Data":"",     # AN6/Dynamo Alternator Volt
   "LRC1":"",            # LRC1  1 Byte
   "LRC2":""             #  LRC2  1 Byte
       }

KeepAliveData = {
   "SiteID":"",        # Max 10 Bytes
   "ts":"",             # Unique key comprised of string Date and time+SiteID+Sensor number
   "KeepAlive":"KeepAlive"    #  AN1/LOp
   }
#Deriving object of SensorClass type for different sensors from DG
DG_Lube_Oil_Pressure_Data = {
   "SiteID":"",        # Max 10 Bytes
   "ts":"",             # Unique key comprised of string Date and time+SiteID+Sensor number
   "LubeOilPressure":""
   }

DG_Shelter_Temperature_Data = {
   "SiteID":"",        # Max 10 Bytes
   "ts":"",             # Unique key comprised of string Date and time+SiteID+Sensor number
   "EngineWaterTemp":""  # "Engine water Temperature":"",    #  AN1/LOp
   }

DG_BTS_Volt_Data ={ 
   "SiteID":"",        # Max 10 Bytes
   "ts":"",             # Unique key comprised of string Date and time+SiteID+Sensor number
   "DGVoltage":""       #"DG Voltage":"",    #  AN1/LOp
   }

DG_Battery_Volt_Data = {
   "SiteID":"",        # Max 10 Bytes
   "ts":"",             # Unique key comprised of string Date and time+SiteID+Sensor number
   "BatteryVoltage":""  #"DG Battery Volt":"",    #  AN1/LOp
   }

DG_Fuel_Level_Data = {
   #"Key":"",
  # "ServiceID":"",
   "SiteID":"",        # Max 10 Bytes
   "ts":"",             # Unique key comprised of string Date and time+SiteID+Sensor number
   "FuelLevel":""       #"DG Fuel Level":"",    #  AN1/LOp
   }

DG_Dynamo_Alternator_Volt_Data ={ 
   "SiteID":"",        # Max 10 Bytes
   "ts":"",             # Unique key comprised of string Date and time+SiteID+Sensor number
   "DynamoVoltage":""   #"DG Dynamo Alternator Volt":"",    #  AN1/LOp
   }

DG_EB_Voltage ={ 
   "SiteID":"",        # Max 10 Bytes
   "ts":"",             # Unique key comprised of string Date and time+SiteID+Sensor number
   "EBVoltage":""       #"EB Voltage":"",    #  AN1/LOp
   }

DG_Load_Current ={ 
   "SiteID":"",        # Max 10 Bytes
   "ts":"",             # Unique key comprised of string Date and time+SiteID+Sensor number
   "LoadCurrentVariation":""  #"% Phase-Wise Load Current Variation":"",    #  AN1/LOp
   }
ECC_config = {
        "siteID":"",
        "noOfSensors":"",
        "topicID":"",
        "thingName":"",
      