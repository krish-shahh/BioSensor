import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    client.subscribe("/esp8266/health")

def on_message(client, userdata, message):
    print("Received message '" + str(message.payload.decode()) + "' on topic '" + message.topic)
    

def main():
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "client_id")
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect('168.122.159.92', 1883) 
    # Connect to the MQTT server and process messages in a background thread. 
    mqtt_client.loop_start() 

if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()

