

import cv2
import numpy as np
import time

import requests

net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = f.read().strip().split("\n")

#cap = cv2.VideoCapture(0)  # 0 for the default webcam

def recImage(mainCV2, cap):
    print("--- DOUBLE BLINKED AAA")
    ret, frame = cap.read()

    # cv2.imwrite("frame.png", frame)
    # image = Image.open("frame.png")
    # text = pytesseract.image_to_string(image)
    # print("rwar")
    # print(text)
    
    if not ret:
        return

    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(net.getUnconnectedOutLayersNames())

    # Process detections
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.8:
                # Object detected
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                w = int(detection[2] * frame.shape[1])
                h = int(detection[3] * frame.shape[0])

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Draw bounding boxes and labels
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    highestConfidence = 0
    highestBox = None
    highestLabel = None
    for i in range(len(boxes)):
        if i in indexes:
            if confidences[i] > highestConfidence:
                highestConfidence = confidences[i]
                highestBox = boxes[i]
                highestLabel = class_ids[i]
    x, y, w, h = highestBox
    label = str(classes[highestLabel])
    color = colors[highestLabel]
    mainCV2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    mainCV2.putText(frame, label, (x, y + 30), font, 3, color, 2)
    
    # send label name to web
    jsonResponse = {"label": label}
    requests.post("http://10.33.143.72:5001/update", json=jsonResponse)
    

    # Display the output
    mainCV2.imshow("Webcam", frame)
    
    key = cv2.waitKey(1)
    if key == 27:  # Press 'Esc' to exit
        return
    #time.sleep(4)
    #cap.release()
   # cv2.destroyAllWindows()