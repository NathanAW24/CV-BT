import subprocess
import pexpect
import uuid 
import requests
from macaddressreader import readMacAddress

envconfig = dotenv_values(".env")

def readMacAddress():
    out = pexpect.run('ifconfig', encoding="utf-8")
    # for i in ['wlan0', 'eth0', 'lo']:
    #     x = out.split('wlan0')[1].split("ether ")[1].split(" ")[0]
    x1= out.split('flags')
    mac_list = []
    for i in range(len(x1)):
        
        if "wlan0" in x1[i]:
            if i > (len(x1) -1):
                return
            mac = x1[i+1].split('ether ')[1].split(' ')[0]
        if "172.29" in x1[i]:
            ip = ("172.29" + x1[i].split("172.29")[1].split(" ")[0])
    
    
    return mac, ip


def uploadToFirebase():
    channelId = envconfig["CHANNEL_ID"]
    iotId = envconfig["IOT_ID"]
    mac, ip = readMacAddress()
    print("Uploading UUID record to database ...")
    data = {
            u"channelId" : channelId,
            u"macaddress" : mac,
            u"authenticated" : False,
            u"iotId" : iotId,
            u"ipaddress" : ip
        }
    print(data)
    url = "https://iot-config-service-3f34abr6ha-as.a.run.app/uuid"
    x = requests.post(url, params= data)
    print(x, x.text)

if __name__ == "__main__":
    uploadToFirebase()

##DEPRECATED !!
"""def generateUUID():
    try :
        billboardUuidFile = open("billboarduuid.txt", "r")
        billboardUuid = billboardUuidFile.read()

        uuidFile = open("uuid.txt", "a")
        newuuid = str(uuid.uuid4())
        uuidFile.write(newuuid)
        uuidFile.close()
        print("Uploading UUID record to database ...")
        macReading = readMacAddress()
        data = {
            u"billboardId" : billboardUuid,
            u"macaddress" : macReading[0],
            u"authenticated" : False,
            u"iotId" : newuuid,
            u"ipaddress" : macReading[1]
        }
        print(data)
        url = "https://iot-config-service-3f34abr6ha-as.a.run.app/uuid"
        x = requests.post(url, params= data)
        print(x, x.text)

    except Exception as e: 
        print(e)
        
    #print(data)

def checkAndGenerateUUID():
    try:
        uuidFile = open("uuid.txt", "r")
        uuidRead = uuidFile.read()
        if (len(uuidRead) != 36):
            generateUUID()
        print("This device's UUID is", uuidRead)
    except:
        print("UUID not found. Generating new one ...")
        generateUUID()"""


