# Importing necessary libraries
from ultralytics import YOLO
import cv2
import time 
import threading

# set the model 
model = YOLO('yolov8s_custom.pt')
# set the source of detection
cap = cv2.VideoCapture('2.mp4')

last_check_time = time.time()

while True:
    _, frame = cap.read()
    results = model(frame, verbose=False)
    classes = []
    safety = ['Glass', 'Gloves', 'Helmet', 'Safety-Vest', 'helmet']

    for r in results:
        for c in r.boxes:
            if model.names[int(c.cls)] in safety : 
                class_name = model.names[int(c.cls)]
                classes.append(model.names[int(c.cls)])
                x1, y1, x2, y2 = map(int, c.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
                cv2.putText(frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

    cv2.imshow('FRAME', frame)

    current_time = time.time()
    if current_time - last_check_time >= 15:
        for elm in safety :
            if elm not in classes : 
                now = time.localtime()
                filename = f"WORKERS/NO_SAFETY/{now.tm_year}{now.tm_mon}{now.tm_mday}_{now.tm_hour}{now.tm_min}{now.tm_sec}.jpg"
                cv2.imwrite(filename, frame)
                break
        last_check_time = current_time

    
    if cv2.waitKey(1) & 0xFF == 27:
        break
