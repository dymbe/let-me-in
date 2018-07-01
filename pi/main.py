import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 65)
pwm.start(5)

try:
	while True:
		pass
except:
	GPIO.cleanup(18)
