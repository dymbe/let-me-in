import os
import paho.mqtt.client as mqtt
from configparser import ConfigParser
from button import Button

config_path = os.path.realpath(__file__).rsplit("/", 1)[0] + "/config.ini"

print(config_path)

config = ConfigParser()
config.read(config_path)

username = config["mqtt"]["username"]
password = config["mqtt"]["password"]
topic = config["mqtt"]["topic"]
host = config["server"]["host"]
port = int(config["server"]["port"])


def on_connect(client, userdate, flags, rc):
    print("Connected to host")
    client.subscribe(topic)


def on_message(client, userdata, msg):
    print("Received message")
    with Button() as button:
        button.press()


client = mqtt.Client()
client.username_pw_set(username=username, password=password)
client.tls_set()

client.on_connect = on_connect
client.on_message = on_message

client.connect(host=host, port=port)
client.loop_forever()
