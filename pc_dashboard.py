import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
TOPIC = "smartroom/light/status"

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected to MQTT Broker")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print("Room Light Status:", msg.payload.decode())

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_forever()
