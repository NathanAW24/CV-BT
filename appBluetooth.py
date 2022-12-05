from bluetooth.bleclass import Bluetoothctl, BluetoothctlError
from firebaseSetUp import storage
import datetime
import json
from dotenv import dotenv_values
import time
import os

#ENV CONFIG

envconfig = dotenv_values(".env")
blesleep = int(envconfig["SLEEP"])
iotid = envconfig["IOT_ID"]


#check if Datapoint.json exist.
filename = envconfig["BLUETOOTH_FILENAME"]
is_exist = os.path.exists(filename)
if not is_exist:
    dataText = open(filename, 'w+')
    dataText.write({})
    dataText.close()


if __name__ == "__main__":
    
    
    bl = Bluetoothctl()
    bl.set_transport_le()
    bl.start_scan()

    upload_data = [] 
    
    currentDateString = None
    currentObject = []
    while True:
        
        try:
            #print("hello")
            bl.start_scan()
            time.sleep(blesleep)
            raw_devices = bl.get_discoverable_devices()
            detected = []

            if len(raw_devices) == 0:
                bl.restart()
                continue
            
            for i in raw_devices:
                if not(i["mac_address"] in detected):
                    detected.append(i["mac_address"])
                    bl.delete_devices(i["mac_address"])

            
            content = {
                "timestamp": time.time_ns(),
                "count" : len(detected)
            }

            date_now = datetime.datetime.utcnow()
            yearVal = date_now.year
            monthVal = ("0" + str(date_now.month))[-2:]
            dayVal = ("0" + str(date_now.day))[-2:]
            hourVal = ("0" + str(date_now.hour))[-2:]
            minuteVal = ("0" + str(date_now.minute))[-2:]

            dateString = str(yearVal) + "_" + str(monthVal) + "_" + str(dayVal) + "_" + str(hourVal)+ "_" + str(minuteVal)
            #Batch minute
            if(not currentDateString ) or (dateString == currentDateString):
                currentObject.append(content)
                currentDateString = dateString
               
            else :
                with open(filename, 'w') as file_out:
                    json.dump(currentObject, file_out, indent=2)
                storage.blob( iotid+ "/"+ currentDateString +".json").upload_from_filename(filename)
                currentDateString = dateString
                currentObject = [content]
                
        except Exception as e:
            try:
                bl.restart()
            except Exception as e2:
                print(e,e2)
                continue
