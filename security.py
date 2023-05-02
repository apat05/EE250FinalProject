import time
import grovepi
import paho.mqtt.client as mqtt

# Set the ultrasonic sensor and LED port numbers
ultrasonic_sensor_port = 4
green_led_port = 2
red_led_port = 3

# Set up MQTT client
mqtt_client = mqtt.Client()

# Define MQTT topics
sensor_topic = "door/sensor"
response_topic = "door/response"

# Connect to MQTT broker
mqtt_client.connect("172.20.10.9", 1883, 60)

# Initialize the previous distance measurement
prev_distance = -1

# Turn on the LEDs appropriately
# Callback function for MQTT message received
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

# Loop to read ultrasonic sensor and send MQTT messages
while True:
    try:
        # Read distance from ultrasonic sensor
        distance = grovepi.ultrasonicRead(ultrasonic_sensor_port)

        # Check if distance has changed since previous measurement
        if distance <= prev_distance - 10:
            # Send distance measurement to MQTT broker
            mqtt_client.publish(sensor_topic, distance)

            # Update previous distance measurement
            prev_distance = distance

        # Print distance measurement on terminal
        print("Distance: {} cm".format(distance))

        # Wait for 1 second before reading sensor again
        time.sleep(1)

    except KeyboardInterrupt:
        break

# Disconnect from MQTT broker
mqtt_client.disconnect()


