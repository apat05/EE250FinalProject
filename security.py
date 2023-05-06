import time
import grovepi
import paho.mqtt.client as mqtt

# Set the ultrasonic sensor and LED port numbers
ultrasonic_sensor_port = 4
green_led_port = 2
red_led_port = 3

# Set up MQTT
mqtt_client = mqtt.Client()
sensor_topic = "door/sensor"
response_topic = "door/response"
mqtt_client.connect("172.20.10.9", 1883, 60)

# This is the max distance of the Ultrasonic Sensor in cm
prev_distance = 160

grovepi.pinMode(green_led_port, "OUTPUT")
grovepi.pinMode(red_led_port, "OUTPUT")

# Callback function for MQTT message received and check to see which light to turn on
def on_message(client, userdata, message):
    if message.topic == response_topic:
        if message.payload.decode() == "yes":
            # Turn on green LED if owner approves
            grovepi.digitalWrite(green_led_port, 1)
            grovepi.digitalWrite(red_led_port, 0)
            print("Owner approved access!")
        else:
            # Turn on red LED if owner denies access
            grovepi.digitalWrite(green_led_port, 0)
            grovepi.digitalWrite(red_led_port, 1)
            print("Owner denied access!")

# Connect to MQTT broker and subscribe to response topic
mqtt_client.on_message = on_message
mqtt_client.subscribe(response_topic)
mqtt_client.loop_start()
# Loop to read ultrasonic sensor and send MQTT messages
while True:
    try:
        # Read distance from ultrasonic sensor
        distance = grovepi.ultrasonicRead(ultrasonic_sensor_port)

        # The distance reading can alter a few cm by itself, so we have to account for the fact that not 
        # every change in distance is someone coming to the door. We give about 10 cm of running room 
        # (as as person cannot fit withing 10 cm)
        if distance <= prev_distance - 10:
            # Send distance measurement to MQTT broker
            mqtt_client.publish(sensor_topic, distance)

            
            # This is in case we want to save changes in distance to use later. 
            # However, we do not so the following line is not needed.
            prev_distance = 160

        # Print distance measurement on terminal
        print("Distance: {} cm".format(distance))

        # Wait for 1 second before reading sensor again
        time.sleep(1)
    # ^C
    except KeyboardInterrupt:
        break
mqtt_client.loop_stop()

mqtt_client.disconnect()

