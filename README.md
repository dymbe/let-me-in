# Let-me-in

A IoT-project for opening my door using a cellphone. The project can easily be used for similar tasks. For this task I utilized the [MQTT](http://mqtt.org)-protocol with [Mosquitto](https://mosquitto.org/) as the MQTT-broker. SSL certificates from [Let's Encrypt](https://letsencrypt.org/) is used to secure all MQTT communications. The whole system is controllable through [MQTT Dash](https://play.google.com/store/apps/details?id=net.routix.mqttdash&hl=en)

## Getting started

### What you need

* A Debian-based server. I used the cheapest [DigitalOcean](https://www.digitalocean.com) Ubuntu-server.
* A Raspberry Pi. I used a Raspberry Pi 3 Model B.
* A servo-motor. I used a really cheap 9G micro-servo from ebay.
* Some wires.

**Note:** The project is easily doable with other equipment, but you might not be able to follow this guide as easily then.

### Setting up the server

#### Step 1 - Installing Mosquitto

1. Start by making sure everything is up-to-date:

```console
$ sudo apt-get update
$ sudo apt-get upgrade
```

2. Install Mosquitto:

```console
$ sudo apt-get install mosquitto mosquitto-clients
```

#### Step 2 - Installing Certbot for Let's Encrypt Certificates

Let's Encrypt is a service offering free SSL certificates through an automated API. To utilize this we have to install Certbot, the official Let's Encrypt-client.

1. Add the repository:

```console
$ sudo add-apt-repository ppa:certbot/certbot
```

2. Update, then install:

```console
$ sudo apt-get update
$ sudo apt-get install certbot
```

