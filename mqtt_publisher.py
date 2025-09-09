#
# Copyright 2021 HiveMQ GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import time
import paho.mqtt.client as paho
from paho import mqtt
import json

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    # msg_payload = json.loads(msg.payload)
    # print("Temperature: " + str(msg_payload["temperature"]))
    

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("sommer", "Leo12345")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("0cc31c1eab774486bc76fad0f7527c3c.s1.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("teste_leo/#", qos=1)

client.subscribe("cliente/teste/lampada1", qos=1)
client.subscribe("cliente/teste/lampada2", qos=1)

ping_pong_flag = True
temperature = 0

def publish_temperature(client):
    global temperature
    global ping_pong_flag
    if(ping_pong_flag):
        temperature += 1
        if(temperature > 40):
            ping_pong_flag = False
    else:
        temperature -= 1
        if(temperature <= 0):
            ping_pong_flag = True
    client.publish("teste_leo/temperature", payload=json.dumps({"temperature": temperature}), qos=1)

lamp1_state = False
lamp2_state = False

def toggle_lamp(client, lamp_number):
    global lamp1_state
    global lamp2_state
    if lamp_number == 1:
        lamp1_state = not lamp1_state
        topic = "cliente/teste/lampada1"
        if lamp1_state:
            client.publish(topic, payload="on", qos=1)
        else:
            client.publish(topic, payload="off", qos=1)
    elif lamp_number == 2:
        lamp2_state = not lamp2_state
        topic = "cliente/teste/lampada2"
        if lamp2_state:
            client.publish(topic, payload="on", qos=1)
        else:
            client.publish(topic, payload="off", qos=1)

while True:
    client.loop_start()
    # publish_temperature(client)
    toggle_lamp(client, 1)
    toggle_lamp(client, 2)
    time.sleep(1)
    client.loop_stop()
# blocking call that processes network traffic, dispatches callbacks and handles reconnecting
