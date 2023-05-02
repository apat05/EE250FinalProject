import paho.mqtt.client as mqtt

# Set up MQTT client
mqtt_client = mqtt.Client()

# Define MQTT topics
sensor_topic = "door/sensor"
response_topic = "door/response"

# Callback function for MQTT message received
def on_message(client, userdata, message):
    if message.topic == sensor_topic:
        # Print distance measurement received from Raspberry Pi
        distance = int(message.payload)
        print("Distance: {} cm".format(distance))

        # Prompt user for response
        response = input("Approve access? (yes/no): ")

        # Send response to Raspberry Pi
        mqtt_client.publish(response_topic, response)

# Connect to MQTT broker
mqtt_client.connect("172.20.10.9", 1883, 60)

# Subscribe to sensor topic
mqtt_client.subscribe(sensor_topic)

# Set up callback function for MQTT message received
mqtt_client.on_message = on_message

# Loop to receive responses from user
mqtt_client.loop_forever()

# Disconnect from MQTT broker
mqtt_client.disconnect()
