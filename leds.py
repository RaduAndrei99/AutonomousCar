import RPi.GPIO as GPIO
from time import sleep
import threading
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

thread_right =  threading.Thread

def leds_on_right():
	while True:
		for i in [7, 5, 3]:
			GPIO.output(i,1)
			sleep(0.3)
		GPIO.setwanings(False)
		for j in [7, 5, 3]:
			GPIO.output(j, 0)
		GPIO.setwarnings(False)
		sleep(0.3)

def leds_on_left():
	while True:
		for i in [ 19, 21, 23]:
			GPIO.output(i,1)
			sleep(0.3)
		GPIO.setwanings(False)
		for j in [19, 21, 23]:
			GPIO.output(j, 0)
		GPIO.setwarnings(False)
		sleep(0.3)

def emergency_leds():
	while True:
		for i in [ (7,19), (5,21), (3,23)]:
			GPIO.output(i[0],1)
			GPIO.output(i[1],1)
			sleep(0.3)
		GPIO.setwarnings(False)
		for j in [ (7,19), (5,21), (3,23)]:
			GPIO.output(j[0], 0)
			GPIO.output(j[1], 0)
		GPIO.setwarnings(False)
		sleep(0.3)


def leds_on():
	for i in [(7,19), (5, 21), (3, 23)]:
		GPIO.output(i[0], 1)
		GPIO.output(i[1], 1)
	GPIO.setwarnings(False)

	"""
	GPIO.output(3,1) # sting LED
	GPIO.output(5,1)
	GPIO.output(7,1)
	GPIO.setwarnings(False)
	"""
def leds_off():
	for i in [(7,19), (5,21), (3,23)]:
		GPIO.output(i[0], 0)
		GPIO.output(i[1], 0)
	GPIO.setwarnings(False)

while True:
	try:
		#emergency_leds()
		leds_on()
	except:
		print("Leds off")
		break


leds_off()



