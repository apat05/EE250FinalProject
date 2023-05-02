import paho.mqtt.client as mqtt

# Set up MQTT client
mqtt_client = mqtt.Client()

# Define MQTT topics
sensor_topic = "door/sensor"
response_topic = "door/response"

# Connect to MQTT broker
mqtt_client.connect("mqtt.eclipse.org", 1883, 60)

# Loop to receive responses from laptop and send MQTT messages
while True:
    try:
        # Wait for response from laptop
        response = input("Approve access? (yes/no): ")

        # Send response to MQTT broker
        mqtt_client.publish(response_topic, response)

        # Wait for response from Raspberry Pi
        mqtt_client.subscribe(sensor_topic)
        message = mqtt_client.on_message
        if message is not None:
            # Convert payload to integer
            distance = int(message.payload.decode())

            # Check if distance is less than or equal to 50 cm
            if distance <= 50:
                # Request access from owner
                print("Someone is at the door! Requesting access...")

    except KeyboardInterrupt:
        break

# Disconnect from MQTT broker
mqtt_client.disconnect()
