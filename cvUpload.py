import json
from firebaseSetUp import storagecv
import time
import datetime
from dotenv import dotenv_values

#config vars
envconfig = dotenv_values(".env")
iotId = envconfig["IOT_ID"]
filename = envconfig["CV_FILENAME"]

#boolean flag switch
uploaded = None

while True:
    try:
        with open("uploaded.txt", "r") as f:
            uploaded = f.read()
            
        #if not uploaded, upload to firebase.
        if uploaded == "0":
            uploaded = 1
            with open("uploaded.txt", "w") as f:
                f.write("1")
            date_now = datetime.datetime.utcnow()
            yearVal = date_now.year
            monthVal = ("0" + str(date_now.month))[-2:]
            dayVal = ("0" + str(date_now.day))[-2:]
            hourVal = ("0" + str(date_now.hour))[-2:]
            minuteVal = ("0" + str(date_now.minute-1))[-2:]
            secondVal = ("0" + str(date_now.second))[-2:]
            dateString = "{}_{}_{}_{}_{}".format(yearVal, monthVal, dayVal, hourVal, minuteVal)

            storagecv.blob( iotId+ "/"+ dateString +".json").upload_from_filename(filename)
        time.sleep(1)
    except Exception as e:
        print(e)
        continue
            