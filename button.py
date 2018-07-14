# The python-representation of the button for opening my door
import os
import RPi.GPIO as GPIO
import time
from configparser import ConfigParser

config_path = os.path.realpath(__file__).rsplit("/", 1)[0] + "/config.ini"

config = ConfigParser()
config.read(config_path)

neutral_postition = float(config["pi"]["neutral_position_duty_cycle"])
pressed_postition = float(config["pi"]["pressed_position_duty_cycle"])
pwm_pin = int(config["pi"]["pwm_pin"])
servo_frequency = float(config["pi"]["servo_frequency"])


class Button:
    def __enter__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pwm_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pwm_pin, servo_frequency)
        self.pwm.start(0)
        return self

    def press(self):
        self.pwm.ChangeDutyCycle(pressed_postition)
        print("Pressing button")
        time.sleep(1)
        self.pwm.ChangeDutyCycle(neutral_postition)
        time.sleep(1)
        print("Button pressed")

    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup(pwm_pin)
