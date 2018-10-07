# Open-sesame

A IoT-project for opening a door using a mobile phone. For this task I utilized the [MQTT](http://mqtt.org)-protocol with [Mosquitto](https://mosquitto.org/) as the MQTT-broker. SSL certificates from [Let's Encrypt](https://letsencrypt.org/) is used to secure all MQTT communications. The whole system is controllable through [MQTT Dash](https://play.google.com/store/apps/details?id=net.routix.mqttdash&hl=en)

## What you need

* An Ubuntu server. I used the cheapest [DigitalOcean](https://www.digitalocean.com) server.
* A domain name that points at your server. Will be necessary for using Let's Encrypt.
* A Raspberry Pi. I used a Raspberry Pi 3 Model B.
* A servo-motor. I used a cheap 9G micro-servo from ebay.
* Some wires.

**Note:** The project can be done with other equipment, but then you might not be able to follow this guide step by step.

## Setting up the server

### Step 1 - Installing Mosquitto

1. Start by making sure everything is up-to-date:

```console
$ sudo apt-get update
$ sudo apt-get upgrade
```

2. Install Mosquitto:

```console
$ sudo apt-get install mosquitto mosquitto-clients
```

### Step 2 - Installing Certbot

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

### Step 3 - Getting Your First Let's Encrypt Certificate

Let's Encrypt issues certificates that you can use to prove that you have control over your domain. Let's Encrypt does not issue certificates directly to IP-addresses, and this is why we need a domain name.

To get our first certificate, Certbot needs to answer a cryptographic challenge issued by Let's Encrypt in order to prove to them that we control our domain. We will use the  `--standalone` option to tell Certbot to handle the HTTP challenge request on its own. `-d` is used to specify the domain you want a certificate for:

```console
$ sudo certbot certonly --standalone -d example.com
```

You will be prompted to enter an email address when running this command and agree to the terms of service. After doing so, you should see a message telling you the process was successful and where your certificates are stored.

### Step 4 - Setting up Automatic Certificate Renewal

Your Let's Encrypt certificate will expire in 90 days. Unless you want do do the previous step manually, you should automate this process.

For this we will use `cron`, a standard system service for running periodic jobs. To tell `cron` what to do you will have to edit a file called a `crontab`. To do this, just type:

```console
$ sudo crontab -e
```

You will be prompted to select a text editor, choose whatever text-editor you prefer, then paste in the following text at the end of the file:

```
30 2 * * * certbot renew --noninteractive --post-hook "systemctl restart mosquitto"
```

The `30 2 * * *` part of this line means "run the following command at 02:30, every day". The `renew`command for Certbot will check all certificates installed on the system and update any that are set to expire in less than thirty days. `--noninteractive` tells Certbot not to wait for user input. `--post-hook "systemctl restart mosquitto"` will restart Mosquitto to pick up the new certificate, but only if the certificate was renewed.

### Step 5 - Configuring MQTT Passwords and MQTT SSL

To make Mosquitto more secure we want to configure it to use passwords. To do this we can use Mosquitto's own utility, `mosquitto_passwd`, for generating a password file. The following command will prompt you to enter and reenter a password for your new user, and place the result in `/etc/mosquitto/passwd`:

```console
$ sudo mosquitto_passwd -c /etc/mosquitto/passwd my-new-user
```

Now we will create a new configuration file for Mosquitto and tell it to use the password-file we just created to authorize users (I use `vim` here, but use whatever you want, `nano` is a good choice for beginners):

```console
sudo vim /etc/mosquitto/conf.d/default.conf
```

This should be an empty file (because we just created it). Paste in the following:

```
allow_anonymous false
password_file /etc/mosquitto/passwd
```

 `allow_anonymous false` will make Mosquitto refuse all non-authenticated connections, and `password_file /etc/mosquitto/passwd` tells Mosquitto in which file to look for user and password information.

We also want to configure SSL, so paste the following into the same file (`/etc/mosquitto/conf.d/default.conf`):

```
listener 8883
certfile /etc/letsencrypt/live/mqtt.example.com/cert.pem
cafile /etc/letsencrypt/live/mqtt.example.com/chain.pem
keyfile /etc/letsencrypt/live/mqtt.example.com/privkey.pem
```

`listener 8883` tells Mosquitto to start listening for new connections on port 8883, which is the standard port for MQTT with SSL. The standard port for MQTT without SSL is 1338. The next three lines, `certfile`, `cafile`, and `keyfile`, all point Mosquitto to the appropriate Let's Encrypt files to set up the encrypted connections.

Now, save and exit the file, then restart Mosquitto to update the settings:

```console
$ sudo systemctl restart mosquitto
```

Now let's finally test if the Mosquitto is working properly. The MQTT protocol communicates through "topics". If a client subscribes to a particular topic, it will received all messages other clients publish to that topic. Let's try to subscribe to "test":

```console
mosquitto_sub -h example.com -t test -p 8883 -u my-new-user -P my-new-password --capath /etc/ssl/certs/
```

 `-h` specifies the hostname of the MQTT-broker (the domain name pointing to your Ubuntu-server), `-t` specifies what topic, `-p` specifies which port, `-u` is the username of the user you made in earlier, `-P` (capitalized) is the password of the user.

Finally, the `--capath /etc/ssl/certs/` option enables SSL for `mosquitto_sub`, and tells it where to look for root certificates. These are typically installed by your operating system, so the path is different for Mac OS, Windows, etc. `mosquitto_pub` uses the root certificate to verify that the Mosquitto server's certificate was properly signed by the Let's Encrypt certificate authority. It's important to note that `mosquitto_pub` and `mosquitto_sub` will not attempt an SSL connection without this option, even if you're connecting to port 8883, the standard port for MQTT + SSL.

If everything goes well, **nothing will happen**. Your console is now listening to messages for the "test"-topic. Now open another console window and publish a message to the "test"-topic:

```console
mosquitto_pub -h example.com -t test -p 8883 -u my-new-user -P my-new-password --capath /etc/ssl/certs/ -m "hello world!"
```

If everything is working properly you should now see a "hello world!" inside the subscribing console.

**Congratulations, you now have a fully functional and secure MQTT-broker!**

## Setting up the Raspberry Pi

Install [paho-mqtt](https://pypi.org/project/paho-mqtt/) for Python 3:

```con
$ pip3 install paho-mqtt
```

Then simply run the main.py script:

```console
$ python3 main.py
```

... and everything should be working.