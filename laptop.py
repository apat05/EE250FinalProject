import paho.mqtt.client as mqtt

# Set up MQTT client
mqtt_client = mqtt.Client()

# Define MQTT topics
sensor_topic = "door/sensor"
response_topic = "door/response"

# Connect to MQTT broker
mqtt_client.connect("172.20.10.9", 1883, 60)

# Callback function for MQTT message received
def on_message(client, userdata, message):
    if message.topic == sensor_topic:
        # Print distance measurement on terminal
        distance = message.payload.decode()
        print("Distance: {} cm".format(distance))

        # Wait for owner response
        owner_response = None
        while owner_response not in ["yes", "no"]:
            owner_response = input("Owner response required. Approve access? (yes/no): ")

        # Send owner response to MQTT broker
        mqtt_client.publish(response_topic, owner_response)

# Connect to MQTT broker and subscribe to sensor topic
mqtt_client.on_message = on_message
mqtt_client.subscribe(sensor_topic)
mqtt_client.loop_start()

# Loop to send responses to Pi
while True:
    try:
        # Wait for 1 second before sending another response
        time.sleep(1)

    except KeyboardInterrupt:
        break

# Disconnect from MQTT broker and stop loop
mqtt_client.loop_stop()
mqtt_client.disconnect()
