"""
Mario Castresana - Discovery journal:
Advanced Face Detection using mediapipe wrapper called cvzone

Description:
This program carries out face detection using mediapipe and cvzone libraries.

* Bear in mind these Google libraries require some time to download face detection models and other files.
  this could cause an error the first time you connect to the drone.  Just try to connect a second time if
  that happens.

Package dependencies and versions used:
mediapipe        0.8.5
djitellopy       2 2.3
cvzone           1.3.7 or above
opencv-python    4.4.0.44

* use Python interpreter 3.7.6
"""

from djitellopy import tello
import cv2
from cvzone.FaceDetectionModule import FaceDetector

# Connect to the drone
drone = tello.Tello()
drone.connect()
print(drone.get_battery())

# start video and create a face detector
drone.streamoff()
drone.streamon()

detector = FaceDetector()

while True:
    img = drone.get_frame_read().frame
    img, bboxs = detector.findFaces(img, draw=True)
    cv2.imshow("Tello camera", img)

    # add delay and keyboard interrupt with q
    if cv2.waitKey(5) & 0xFF == ord('q'):
        drone.streamoff()
        break

cv2.destroyAllWindows()