import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("esp8266/health")  # Make sure this is the correct topic

def on_message(client, userdata, msg):
    print(f"Message received: {msg.topic} {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect("128.197.55.102", 1883, 60)  # Connect to the broker
    client.loop_forever()  # Process network traffic and dispatch callbacks
except Exception as e:
    print(f"Error connecting to MQTT broker: {e}")
