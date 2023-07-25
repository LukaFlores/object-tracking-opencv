from ultralytics import YOLO
import cv2
import cvzone
import math
import numpy as np
from sort import *

# Import Video
cap = cv2.VideoCapture("./Video/1.mp4")
model = YOLO("../Yolo-Weights/yolov8n.pt")


# Label Array
classNames = [
    "person", "bicycle", "car", "motorbike", "aeroplane", "bus",
              "train", "truck", "boat", "traffic light", "fire hydrant",
              "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra",
              "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase",
              "frisbee", "skis", "snowboard", "sports ball", "kite",
              "baseball bat", "baseball glove", "skateboard", "surfboard",
              "tennis racket", "bottle", "wine glass", "cup", "fork", "knife",
              "spoon", "bow", "banana", "apple", "sandwich", "orange",
              "broccoli", "carrot", "hot dog", "pizza", "donut", "cake",
              "chair", "sofa", "pottedplant", "bed", "diningtable",
              "toilet", "tvmonitor", "Laptop", "mouse", "remote",
              "keyboard", "cell phone", "microwave", "oven", "toaster",
              "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
]


mask = cv2.imread("./Video/mask2.png")

# Tracking
tracker = Sort(max_age=20, min_hits=2, iou_threshold=0.3)

# Line of tracking
limitsSouth = [200, 200, 575, 200]
limitsNorth = [700, 200, 1100, 200]

totalCountSouth = []
totalCountNorth = []

# For saving Video
# VideoResult = cv2.VideoWriter('./Video/VideoResult.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, (1280, 720))


while True:
    success, img = cap.read()

    # Overlay Mask with bitwise and
    imgRegion = cv2.bitwise_and(img, mask, mask = None)

    results = model(imgRegion, stream=True)

    detections = np.empty((0, 5))

    for r in results:
        boxes = r.boxes
        for box in boxes:

            # Bounding Box
            # Get Coords Boxes from Model x1y1x2y2
            x1, y1, x2, y2 = box.xyxy[0]
            # Convert to Int
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Get Width , Height
            w, h = x2-x1, y2-y1

            # Confidence Round 2 Decimal Places
            confidence = math.ceil(box.conf[0]*100)/100

            # Class
            cls = int(box.cls[0])

            currentClass = classNames[cls]

            # Rectangle CvZone
            # If Detection is Vehicle and confidence level greater than 0.3
            if currentClass == "car" or currentClass == "truck" \
                or currentClass == "bus" or currentClass == "motorbike" \
                    and confidence > 0.5:

                # cvzone.putTextRect(
                #    img, f'{currentClass} - {confidence}',
                #    (max(0, x1), max(35, y1)), scale=1, thickness=1,
                #    offset=4)

                cvzone.cornerRect(img, (x1, y1, w, h), l=9)

                currentArray = np.array([x1, y1, x2, y2, confidence])

                detections = np.vstack((detections, currentArray))

    trackerResults = tracker.update(detections)

    cv2.line(img, (limitsSouth[0], limitsSouth[1]), (limitsSouth[2], limitsSouth[3]), (0, 0, 255), 5)
    cv2.line(img, (limitsNorth[0], limitsNorth[1]), (limitsNorth[2], limitsNorth[3]), (0, 0, 255), 5)

    for result in trackerResults:
        x1, y1, x2, y2, id = result
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        print(result)
        w, h = x2-x1, y2-y1
        # Showing rectangles around tracker, the id will remain the same across
        # multiple frames
        cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=4, colorR=(255, 0, 0))
        cvzone.putTextRect(img, f'{id}',
                           (max(0, x1), max(35, y1)), scale=1,
                           thickness=1, offset=4)

        # Center of box
        cx, cy = x1+w//2, y1+h//2
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        if limitsSouth[0] < cx < limitsSouth[2] and limitsSouth[1] < cy < limitsSouth[1] + 20:
            # if id is not in the list then add new id
            if totalCountSouth.count(id) == 0:
                totalCountSouth.append(id)
                cv2.line(img, (limitsSouth[0], limitsSouth[1]), (limitsSouth[2], limitsSouth[3]), (0, 255, 0), 5)

        if limitsNorth[0] < cx < limitsNorth[2] and limitsNorth[1] - 20 < cy < limitsNorth[1]:
            # if id is not in the list then add new id
            if totalCountNorth.count(id) == 0:
                totalCountNorth.append(id)
                cv2.line(img, (limitsNorth[0], limitsNorth[1]), (limitsNorth[2], limitsNorth[3]), (0, 255, 0), 5)

        cvzone.putTextRect(img, f'South Count: {len(totalCountSouth)}', (50, 700))
        cvzone.putTextRect(img, f'North Count: {len(totalCountNorth)}', (850, 50))

    # Open Window
    cv2.imshow("Image", img)
    #cv2.imshow("ImageRegion", imgRegion)

    # For saving video
    #VideoResult.write(img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# For saving video
# VideoResult.release()

cv2.destroyAllWindows()
print("The video was successfully saved")
