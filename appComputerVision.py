import cv2
import jetson.inference
import jetson.utils
import time
import datetime
import json
from dotenv import dotenv_values
import os

envconfig = dotenv_values(".env")

datasetName = envconfig["BQ_DATASET_NAME"]
iotid = envconfig["IOT_ID"]
filename = envconfig["CV_FILENAME"]
uploaded_filename= envconfig["UPLOADED_BOOL_FILENAME"]

#check whether the file path exists. if not generate a new one.
is_uploaded_exist = os.path.exists(uploaded_filename)
if not is_uploaded_exist:
    dataText = open(uploaded_filename, 'w+')
    dataText.write(0)
    dataText.close()
is_exist = os.path.exists(filename)
if not is_exist:
    dataText = open(filename, 'w+')
    dataText.write({})
    dataText.close()

class DetectionModel():
    def __init__(self, net_path, threshold):
        self.net_path = net_path
        self.threshold = threshold
        self.net = jetson.inference.detectNet(argv = self.net_path, threshold = self.threshold) # argv is a parameter that accepts an array of command line parsing commands

    def detect(self, img, display=False):
        imgCuda = jetson.utils.cudaFromNumpy(img) # convert numpy array to cuda format
        detections = self.net.Detect(imgCuda, overlay = 'none') # overlay = "OVERLAY_NONE", to make bbox not appear, because we are doing it ourselves via OpenCV functionality
            
        # list of detections
        return detections

if __name__ == '__main__':
    ### to count how many detected faces
    net_ls = ['--model=models/HumanHead20220527/mb1-ssd-Epoch-25-Loss-3.31245219707489.onnx', '--labels=models/HumanHead20220527/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes']
    cap = cv2.VideoCapture(0)
    model = DetectionModel(net_ls, 0.7)

    #cv display/monitor size
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    print(width)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(height)

    #Boolean/flag switch to upload per minute.
    currentDateString = None
    currentObject = []

    while True:
        #detection stuff.
        time.sleep(float(envconfig["CV_SLEEP"]))
        success, frame = cap.read()
        if not (success):
            continue
        detections = model.detect(frame)
        count = len(detections)
        if len(detections) > 0:
            var = detections[0]

        #DATE purposes to upload. Will batch upload if minute changes.
        date_now = datetime.datetime.utcnow()
        yearVal = date_now.year
        monthVal = ("0" + str(date_now.month))[-2:]
        dayVal = ("0" + str(date_now.day))[-2:]
        hourVal = ("0" + str(date_now.hour))[-2:]
        minuteVal = ("0" + str(date_now.minute))[-2:]
        dateString = "{}_{}_{}_{}_{}".format(yearVal, monthVal, dayVal, hourVal, minuteVal)

        #detections is the variable which contains the result of CV detection.
        #ROI is Region of interest and confidence will be recorded in "detections" variable.
        ROI = []
        Confidence = []
        for i in detections:
            ROI = []
            for j in i.ROI:
                ROI.append(round(j,2))

            Confidence.append(round(i.Confidence,2))

        #content to upload to firebase/storage
        content={
                "timestamp": time.time(),
                "count" : len(detections),
                "ROI": ROI,
                "confidence": Confidence
            }
        
        #Batch minute logic. Boolean switch manipulation
        if(not currentDateString ) or (dateString == currentDateString):
            currentObject.append(content)
            currentDateString = dateString

        #if date string changes, meaning the minuteVal also changes. been 1 minute, time to upload!!
        else :
            #json dump. tag uploaded.txt which triggers cvUpload.py and upload to firebase.
            #can't directly upload bcs firebase python need to be python3.8 while computer vision only acceps python3.6
            with open(filename, 'w') as file_out:
                json.dump(currentObject, file_out,indent=2)
            with open(uploaded_filename, 'w') as f:
                f.write("0")

            currentDateString = dateString
            currentObject = [content]
        #if failed
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
    
    cap.release()
    cv2.destroyAllWindows()