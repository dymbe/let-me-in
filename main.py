#import paho.mqtt.client as mqtt
from configparser import ConfigParser
#from button import Button


config = ConfigParser()
config.read("config.ini")


def on_connect(client, userdate, flags, rc):
    client.subscribe("teknobyen/doors/front/open")


def on_message(client, userdata, msg):
    with Button() as button:
        button.press()


username = config["credentials"]["username"]
password = config["credentials"]["password"]
host = config["server"]["host"]
port = config["server"]["port"]

client = mqtt.Client()
client.username_pw_set(username=username, password=password)
client.tls_set()

client.on_connect = on_connect
client.on_message = on_message

client.connect(host=host, port=port)
client.loop_forever()
