"""
Mario Castresana - Discovery journal:  Face Detection and PID controllers

Description:
This program gives a drone the ability to track down your face and follow you around the room.  Using 3 separate
PID controllers we change the speed of the propellers to stabilize flight and follow the user.

Note: for testing purposes you can use the webcam instead of the drone to save some
battery power.

Use
cap = cv2.VideoCapture(0) >> define the camera object with id = 0
...
and then capture the image with
_, img = cap.read()
the rest is the same as previous experiments.


---
Package dependencies and versions used:
mediapipe        0.8.5
djitellopy       2 2.3
cvzone           1.3.7 or above
opencv-python    4.4.0.44

* use Python interpreter 3.7.6 *
"""

from djitellopy import tello
import cv2
import cvzone
from cvzone.FaceDetectionModule import FaceDetector

# enable webcam for testing purposes
# cap = cv2.VideoCapture(0) # webcam testing

# enable face detector with Min. Detection confidence threshold = 70%
detector = FaceDetector(minDetectionCon=0.7)

# define image high and width and channels(unused _)
# _, img = cap.read()      # webcam testing line
# hi, wi, _ = img.shape    # webcam testing line
hi, wi = 480, 640

# Define PID controllers
# PID-x: Kp = 0.22 Ti = 0 Td = 0.1
xPID = cvzone.PID([0.22, 0, 0.1], wi // 2)

# PID-y: Kp=0.27  Ti=0  Td=0.1  axis=1 (y axis = 1 for PID draw() function)
yPID = cvzone.PID([0.27, 0, 0.1], hi // 2, axis=1)

# PID-z: Kp=0.005  Ti=0  Td=0.003  No axis since there is no need to draw
# Kp is 100 times smaller here to avoid fast movements and add limits
# -20 indicates it will move forward faster
# +15 indicates it will move backwards slower
zPID = cvzone.PID([0.005, 0, 0.003], 12000, limit=[-20, 15])

# Create a plot of x, y, z speed values vs time coming from the PID controller.
# Max speed for Tello drone is -100, +100 (sign is for direction)
myPlotX = cvzone.LivePlot(yLimit=[-100, 100], char="X")
myPlotY = cvzone.LivePlot(yLimit=[-100, 100], char="Y")
myPlotZ = cvzone.LivePlot(yLimit=[-100, 100], char="Z")

# Connect to the drone
drone = tello.Tello()
drone.connect()
print(drone.get_battery())

# # start video and take off
drone.streamoff()
drone.streamon()
drone.takeoff()
drone.move_up(80)

while True:
    # _, img = cap.read()    # webcam testing line
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (640, 480))
    img, bboxs = detector.findFaces(img, draw=True)

    xVal = 0
    yVal = 0
    zVal = 0

    # check the coordinates of the bbox to change the way we move the drone.
    if bboxs:
        cx, cy = bboxs[0]['center']
        # the Z axis can be interpreted as the drone´s distance from the face or the bbox area
        x, y, w, h = bboxs[0]['bbox']
        area = w * h

        # Update controller with current value. We cast it to int because we will use it with
        # Tello drone API later.  [xVal, yVal, zVal] are speed values the controller sends to the drone.
        xVal = int(xPID.update(cx))
        yVal = int(yPID.update(cy))
        zVal = int(zPID.update(area))

        # Plots
        imgPlotX = myPlotX.update(xVal)
        imgPlotY = myPlotY.update(yVal)
        imgPlotZ = myPlotZ.update(zVal)

        # update the interface using the draw function with current center value [cx, cy]
        img = xPID.draw(img, [cx, cy])
        img = yPID.draw(img, [cx, cy])
        imgStacked = cvzone.stackImages([img, imgPlotX, imgPlotY, imgPlotZ], 2, 0.75)
        # imgStacked = cvzone.stackImages([img, imgPlotZ], 2, 0.75)
        cv2.putText(imgStacked, str(area), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    else:
        imgStacked = cvzone.stackImages([img], 1, 0.75)

    # send the speed values to the drone (controller's action defined by +1/-1 sign)
    # +xVal -> yaw speed
    # -yVal -> up_down velocity
    # -zVal -> forward_back velocity
    drone.send_rc_control(0, -zVal, -yVal, xVal)

    # Tune each PID axis independently e.g.
    # drone.send_rc_control(0, -zVal, 0, 0)
    cv2.imshow("Tello camera", imgStacked)

    # add delay and keyboard interrupt with q
    if cv2.waitKey(5) & 0xFF == ord('q'):
        drone.land()
        break

# drone.streamoff()
cv2.destroyAllWindows()
