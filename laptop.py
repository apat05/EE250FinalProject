import paho.mqtt.client as mqtt

# Set up MQTT client
mqtt_client = mqtt.Client()

# Define MQTT topics
sensor_topic = "door/sensor"
response_topic = "door/response"

# Connect to MQTT broker
mqtt_client.connect("172.20.10.9", 1883, 60)

# Loop to send responses to Pi
while True:
    try:
        # Wait for input from user
        response = input("Approve access? (yes/no): ")

        # Send response to MQTT broker
        mqtt_client.publish(response_topic, response)

    except KeyboardInterrupt:
        break

# Disconnect from MQTT broker
mqtt_client.disconnect()
