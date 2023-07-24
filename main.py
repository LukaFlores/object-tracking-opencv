from ultralytics import YOLO
import cv2


# Install Model Weights Yolo Version 8 Nano
model = YOLO('./Yolo-Weights/yolov8m.pt')

results = model("Images/2.png", show=True)

cv2.waitKey(0)




