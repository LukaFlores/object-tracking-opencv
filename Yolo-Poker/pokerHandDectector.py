from ultralytics import YOLO
import cv2
import cvzone
import math
import pokerHandFunction

# Webcam
cap = cv2.VideoCapture(1)
# Set Width
cap.set(3, 1280)
# Set Height
cap.set(4, 720)

model = YOLO("./playingCards.pt")

# Label Array
classNames = ['10C', '10D', '10H', '10S',
              '2C', '2D', '2H', '2S',
              '3C', '3D', '3H', '3S',
              '4C', '4D', '4H', '4S',
              '5C', '5D', '5H', '5S',
              '6C', '6D', '6H', '6S',
              '7C', '7D', '7H', '7S',
              '8C', '8D', '8H', '8S',
              '9C', '9D', '9H', '9S',
              'AC', 'AD', 'AH', 'AS',
              'JC', 'JD', 'JH', 'JS',
              'KC', 'KD', 'KH', 'KS',
              'QC', 'QD', 'QH', 'QS'
              ]

# For saving Video
# VideoResult = cv2.VideoWriter('./Video/VideoResult.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, (1280, 720))

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    hand = []

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

            if confidence > 0.8:
                hand.append(classNames[cls])

    hand = list(set(hand))

    if len(hand) == 5:
        results = pokerHandFunction.findPokerHand(hand)
        print(results)
        cvzone.putTextRect(
            img, f'Your Hand: {results}',
            (300, 100), scale=3, thickness=1)

    # For saving video
    # VideoResult.write(img)

    # Open Window
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# For saving video
# VideoResult.release()
