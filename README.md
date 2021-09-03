# Drone Programming Discovery Journal
 Learning process for Computer Vision and drone programming

In this Journal I am trying to document my learning process for several topics related to Computer Vision.  I leverage several resources which I will share in the reference section below in order to learn how to use OpenCV, MediaPipe and other APIs available to develop Computer Vision projects in Python.

# About This Project
This a learning project I decided to start during my free time.  This is basically a guided learning process you can find at www.computervision.zone. In this course, you get to learn the basics of Computer Vision, Image Processing, Face/Body Detection and Gesture Recogition.  I used several tutorials online, but I specially recommend Murtaza's Workshop on YouTube and CVzone to get started and motivated.

# Drone used
For this particular project I used a Tello Drone by Ryze Robotics.  You can see the details here:
https://www.ryzerobotics.com/tello

# Day 1: Face Detection Algorithms
In the first part of the project, I started with some basics from Murtaza's YouTube Channel and CVzone courses.  Basically, you get the basics of OpenCV and DJI Tello library in one hour.  After that you can start playing with the APIs and the different parameters they offer to help you track down the user's face in an image.  Here is an example once you learn how to use DJI Tello camera with OpenCV

![PIDPlot2](https://user-images.githubusercontent.com/21084234/132070961-a2290b08-c97a-432a-973f-7af18bef7644.png)

As you can see, in this image I was trying to get the current position of my face's bounding box and then use that information as the input to a set of PID controllers that stabilize the drone's flight pattern. 

# References
Murtaza's Workshop:
https://www.youtube.com/c/MurtazasWorkshopRoboticsandAI

CVzone courses, materials an more:
https://www.computervision.zone/
