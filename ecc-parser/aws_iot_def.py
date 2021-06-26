
from datetime import datetime
from pytz import timezone
# Definitions related to AWS cloud components i.e. IOT core end point definitions
# Define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a1jblcy2osi0b6-ats.iot.ap-south-1.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERT = "certificates/b1e904c318-certificate.pem.crt"
PATH_TO_KEY = "certificates/b1e904c318-private.pem.key"
PATH_TO_ROOT = "certificates/root.pem"
# Below topic is the topic which will be publised and same shall be subscribed at aws IoT core.
TOPIC_DATA = "SID1234567890"

local_host="192.168.43.231" # Local host IP address for Raspberri Pi communication
aws_ec2_host="15.206.164.57"    # Cloud EC2 instance public IP address
aws_ec2_sahngdong="13.234.136.125"
PORT = 5001
MAX_GATEWAY_CLIENTS = 60

ServiceID = "12345678"
SiteID="9811781304"

def get_time_stamp():
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"

    now_time = datetime.now(timezone('ASIA/Calcutta'))

    #  print (now_time.strftime(fmt))
    return(now_time.strftime(fmt))

def get_key(ServiceID,SiteID,SensorName):
    time = get_time_stamp();
    key = ServiceID +'-' + SiteID + '-' + SensorName + '-' + time
     # print(key)
    return(key)


