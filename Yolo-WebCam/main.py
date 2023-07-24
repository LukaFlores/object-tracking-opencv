from ultralytics import YOLO
import cv2
import cvzone
import math

# Webcam
cap = cv2.VideoCapture(0)
# Set Width
cap.set(3, 1280)
# Set Height
cap.set(4, 720)


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


while True:
    success, img = cap.read()

    results = model(img, stream=True)

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

            # Display Rectangle
            # Open Cv
            # cv2.rectangle(img,(x1,y1),(x2,y2),(0,200,0), 3)

            # CV zone
            cvzone.cornerRect(img, (x1, y1, w, h))

            # Confidence Round 2 Decimal Places
            confidence = math.ceil(box.conf[0]*100)/100

            # Class

            cls = int(box.cls[0])

            cvzone.putTextRect(
                img, f'{classNames[cls]} - {confidence}',
                (max(0, x1), max(35, y1)), scale=1, thickness=1)

    # Open Window
    cv2.imshow("Image", img)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
