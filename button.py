# The python-representation of the button for opening my door
import RPi.GPIO as GPIO
import time
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")
NEUTRAL_POSITION = config["pi"]["neutral_position_duty_cycle"]
PRESSED_POSITION = config["pi"]["pressed_position_duty_cycle"]
PWM_PIN = config["pi"]["pwm_pin"]
SERVO_FREQUENCY = config["pi"]["pwm_pin"]


class Button:
    def __enter__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PWM_PIN, GPIO.OUT)
        self.pwm = GPIO.PWM(PWM_PIN, SERVO_FREQUENCY)
        self.pwm.start(0)
        return self

    def press(self):
        self.pwm.ChangeDutyCycle(PRESSED_POSITION)
        time.sleep(1)
        self.pwm.ChangeDutyCycle(NEUTRAL_POSITION)
        time.sleep(1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup(PWM_PIN)
