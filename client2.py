from paho.mqtt.client import Client

from app.utils import on_log, on_message, on_subscribe


# The callback for when the client receives a CONNACK response from the server.
def on_connect_sub(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("transport/stop/0320")


client = Client()
client.on_connect = on_connect_sub
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_log = on_log

client.connect("broker.hivemq.com")

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
