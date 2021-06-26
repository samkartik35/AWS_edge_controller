# FILE name: "shangdong_def.py
# Revision:1.A.ECC.2.IN.POWERHF
from sensordata import *
from datetime import datetime
from pytz import timezone
import logging
import time as t
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import socket
import os
import csv
import re # importing regex module for string procesing
# Function to rad cert.txt file and return list of certificates, key and root.ca files
def get_certificates(debug):
    certfile = "cert.txt"
    with open(certfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                if(debug == True):
                    print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                if(debug == True):
                    print("Here is row")
                    print(row)
                certificates["privateCert"] = row[0]
                certificates["privatekey"] = row[1]
                certificates["rootCA"] = row[2]
    return(certificates)
# remove blank from topic
def topic_cleanup(topic_list,debug):
    cleaned_topic_list = []
    search_pattern = '//'
    replace_patter ='/'
    for string in topic_list:
        cleaned_topic_list.append( re.sub('//','/', string))
    if(debug == True):
        print("original topic list:")
        print(topic_list)
        print("Removed spaces from topic list")
        print(cleaned_topic_list)
    return(cleaned_topic_list)



# function to return topic and no of sensors from a file when siteid and config file name is passed.
def parse_config_file(siteid, config_file, debug):
    topicid_list = []
    param_list = []
    numberOfSensors =8
    with open(config_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                if(debug == True):
                    print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                if(debug == True):
                    print("Here is row")
                    print(row)
                if(siteid == row[0]):
                    if(debug == True):
                        print("Line count:",line_count)
                    #topicid_list.append(row[2] + '/' + row[3] + '/' + row[4]+'/'+ row[5] + '/' + row[6] + '/' + row[7])
                    topicid_list.append(row[2] + '/' + row[3] )
                    numberOfSensors = row[1]
                    param_list.append(row[7]) #Create list of parameters
                line_count += 1
            if(debug == True):    
                print("topic list, param list and no of sensors:")
                print(topicid_list,param_list, numberOfSensors)
    return(topicid_list,param_list,numberOfSensors)

# Function to change time to IST
# eg. "2020-10-07 13:18:23"
def get_time_stamp():
    fmt = "%Y-%m-%d %H:%M:%S"

    now_time = datetime.now(timezone('ASIA/Calcutta'))
    time = now_time.strftime(fmt)
    return(time)

# Function takes serial data string and returns site id
def get_siteid(data, debug):
    list = data.split(",")
    if(debug ==True):
        print("Here is data received:")
        print(list)
        print("\n")
    if(data[0]=='&'):
        if(debug ==True):
            print("valid data string siteid:",list[1])
        return(list[1])
    elif(data[:4]=="keep"):
        if(debug ==True):
            print("Keep alive siteid",data[4:])
        return(data[4:])
    else:
        return("")
#ServiceID/fm<siteid>/control
def generate_gw_topic(siteid, topic_list,debug):
    param = topic_list[0]    # read any parameter of sensor to get serviceid
    serviceid = param.split('/')
    topic = serviceid[0] + '/fm' + siteid +'/control'
    if(debug == True):
        print("parameter_list:", topic_list)
        print(" param_list[0]",param)
        print(" service id:", serviceid)

        print("Gateway Topic is :", topic)
    return(topic)

def check_keepalive(data,topic_list,debug):

    substring ='keep'
    found = list(filter(lambda x: substring in x, data))
    if(debug == True):
        print("data received is:",data)
        print("string keep found:",found)
    return(found)

def process_gateway_data(data,siteid,param_list,client, debug):
    KeepAliveData = {}
    list = data.split(",")
    if(debug == True):
        print("Processing Gateay data")
        print("Here is data received:")
        print(list)
        print("\n")
    # check if keep alive message from gateway then just send keep alive
    topic = generate_gw_topic(siteid, param_list,debug)
    if(len(data) ==0):
        if(debug == True):
            print(" Empty list received")
        KeepAliveData["KeepAlive"] ="KeepAlive"

    elif(data[:4] == "keep"):
        if(debug == True):
            print("Keep alive received")
         
        KeepAliveData["ts"]=get_time_stamp()
        KeepAliveData["KeepAlive"] ="KeepAlive"
        if(debug == True):
            print("Keep Alive:")
    else:
        if(debug == True):
            print("unknown data string")
    publish_sensor_data(topic,KeepAliveData,client,debug)

# function to process seial data comming from sensors
# splitting the serial data with , and filling into sensors data structures
# We segrigate keep alive , junk and sensor data in this function
def process_sensor_data(data, noOfSensors,siteID,param_list,topic_list,client, debug):

    index = 0
    thing_data = {}
    if(len(topic_list) == 0 or len(param_list) ==0):
        print("Error topic list or param list empty", topic_list,param_list)
        return()
    topic = topic_list[0]

    if(debug == True):
        print("Topic list in process_sensor_data:", topic_list)
        print("param_list:",param_list)
        print("data:",data)
    if(len(topic_list) == 0 or len(param_list) == 0 ):
        print("topic list or param list empty exiting!")
        return()

    list = data.split(",")
    if(debug == True):
        print("Here is data received:")
        print(list)

    if(siteID == None):#
        if(debug == True):
            print(" Site ID not found!")
        return(print("Config file malformed!"))
    count = int(noOfSensors)
    data_values = len(list) -3
    if(count > data_values):
            print("noof sensors are more than data samples!",count, data_values)
            return()
    thing_data["ts"] = get_time_stamp()

    while (index < count):
        data = list[index+3]
        process_data(thing_data,data,param_list[index],debug)
        index = index +1
    publish_sensor_data(topic,thing_data,client,debug)


def process_data(thing_data,data,param,debug):

    
    thing_data[param] = data
    if(debug == True):
        print("SiteID:",siteid)
        print("Process sensordata:",json_data)
        print("Here is parameter :", param)
        print("Here is topic list:", topic)
        print("client:",client)
        


def process_junk_data(siteid, data):
    print("Junk Received:")
    print(data)
    sensorRxData["Site ID"] ="Junk"
    sensorRxData["Function Code"]=data
    sensorRxData["Sensor1 Data"] =""
    sensorRxData["Sensor2 Data"] =""
    sensorRxData["Sensor3 Data"] =""
    sensorRxData["Sensor4 Data"] =""
    sensorRxData["Sensor5 Data"] = ""
    sensorRxData["Sensor6 Data"] =""


# mqtt interface initialisation
def init_mqtt_interface(certPath, mqtt_client,end_point,debug):
    myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(mqtt_client)   # Client id is same as thing name
    myAWSIoTMQTTClient.configureEndpoint(end_point, 8883)            # Configure IoT Core End point
    PATH_TO_ROOT =ECC_CERT_DIR + "/"  + certPath["rootCA"]
    PATH_TO_KEY =ECC_CERT_DIR + "/" +   certPath["privatekey"]
    PATH_TO_CERT = ECC_CERT_DIR+ "/" +  certPath["privateCert"]
    if(debug == True):
        print("certificate files are:")
        print(PATH_TO_ROOT,PATH_TO_KEY,PATH_TO_CERT)

    myAWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)# Configure private key and cert
    try:
        myAWSIoTMQTTClient.connect() # Connect to end point
        print("MQTT connection successfull")
    except:
        print("MQTT Connection failed")
    return  (myAWSIoTMQTTClient)

# Function to publish the data,. it takes topic, data, client id
def publish_sensor_data(topic,data,myAWSIoTMQTTClient,debug):
        if(debug == True):
            print("Publishing data",data) 
        myAWSIoTMQTTClient.publish(topic, json.dumps(data), 1)
        t.sleep(0.5)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             nt("************************")
        print("\n")

    elif(ECC["noOfSensors"] =='8'):
        print("Publishing data Frames for 8 sensors")
        if(DG_Lube_Oil_Pressure_Data["ThingData"]!=0):
            myAWSIoTMQTTClient.publish(TOPIC_FL, json.dumps(DG_Lube_Oil_Pressure_Data), 1)
            t.sleep(0.5)
        if(DG_Shelter_Temperature_Data["ThingData"]!=0):
            myAWSIoTMQTTClient.publish(TOPIC_FL, json.dumps(DG_Shelter_Temperature_Data), 1)
            t.sleep(0.5)
        if(DG_BTS_Volt_Data["ThingData"]!=0):
            myAWSIoTMQTTClient.publish(TOPIC_FL, json.dumps(DG_BTS_Volt_Data), 1)
            t.sleep(0.5)
        if(DG_Battery_Volt_Data["ThingData"]!=0):
            myAWSIoTMQTTClient.publish(TOPIC_FL, json.dumps(DG_Battery_Volt_Data), 1)
            t.sleep(0.5)
        if(DG_Fuel_Level_Data["ThingData"]!=0):
            t.sleep(0.5)
            myAWSIoTMQTTClient.publish(TOPIC_FL, json.dumps(DG_Fuel_Level_Data), 1)
        t.sleep(0.5)
        myAWSIoTMQTTClient.publish(TOPIC_DATA, json.dumps(DG_Dynamo_Alternator_Volt_Data), 1)
        t.sleep(0.5)
        print("Published data")
        print("************************")
        print("\n")
    else:

        print("Publishing Keep Alive",KeepAliveData)
        print(KeepAliveData)
        #  myAWSIoTMQTTClient.publish(TOPIC_CONTROL, json.dumps(KeepAliveData), 0)

    t.sleep(0.3)
    myAWSIoTMQTTClient.disconnect()

