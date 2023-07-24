from ultralytics import YOLO
import cv2


# Install Model Weights Yolo Version 8 Nano
model = YOLO('../Yolo-Weights/yolov8l.pt')

firstImage = model("./Images/1.png", show=True)
secondImag = model("./Images/2.png", show=True)

cv2.waitKey(0)




