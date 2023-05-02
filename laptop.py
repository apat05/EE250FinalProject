import paho.mqtt.client as mqtt

# Set up MQTT client
mqtt_client = mqtt.Client()

# Define MQTT topics
sensor_topic = "door/sensor"
response_topic = "door/response"

# Callback function for MQTT message received
def on_message(client, userdata, message):
    if message.topic == sensor_topic:
        distance = int(message.payload.decode())
        if distance < 50:
            # Request access from owner if someone is near the door
            response = input("Someone is at the door. Request access? (yes/no): ")

            # Send response to MQTT broker
            mqtt_client.publish(response_topic, response)

# Connect to MQTT broker and subscribe to sensor topic
mqtt_client.on_message = on_message
mqtt_client.connect("172.20.10.9", 1883, 60)
mqtt_client.subscribe(sensor_topic)
mqtt_client.loop_start()

# Loop to receive responses from owner
while True:
    try:
        # Wait for response from owner
        mqtt_client.loop(timeout=1.0)

    except KeyboardInterrupt:
        break

# Disconnect from MQTT broker and stop loop
mqtt_client.loop_stop()
mqtt_client.disconnect()
