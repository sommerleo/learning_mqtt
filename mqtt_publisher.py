import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_publish(client, userdata, mid):
    print("Message Published")

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

client.connect("mqtt.eclipse.org", 1883, 60)
client.publish("test/topic", "Hello MQTT")

client.loop_forever()
