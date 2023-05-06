# EE250FinalProject - Aum Patel and Chengzhong Luo

Home Security System - A sensor that detects when somebody is by a door. A message is sent from a raspberry pi to an owner's computer,
and the owner types yes to allow them to enter or no to prevent them from entering (entering is represented by green light and preventing is red light).
Uses raspberry pi, grove pi board, grove pi ultrasonic sensor, grove pi green light, and grove pi red light.

Type the following into terminal for the libraries and installation needed:
  sudo apt-get update
  sudo apt-get install grovepi
  sudo pip install paho-mqtt
  
Instructions to compile -
  1. Connect to raspberry pi
  2. Clone Github repo and run security.py
  3. On your local computer, run laptop.py
  4. 
