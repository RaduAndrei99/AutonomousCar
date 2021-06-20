import RPi.GPIO as GPIO
from time import sleep
import threading
import sys

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setwarnings(False)


def rear_lights_on():
    GPIO.output(37, 1)
    GPIO.output(35, 1)


def rear_lights_off():
    GPIO.output(37, 0)
    GPIO.output(35, 0)


def leds_on_right():
    while True:
        for i in [7, 5, 3]:
            GPIO.output(i, 1)
            sleep(0.3)
        GPIO.setwanings(False)
        for j in [7, 5, 3]:
            GPIO.output(j, 0)
        GPIO.setwarnings(False)
        sleep(0.3)


def leds_on_left():
    while True:
        for i in [19, 21, 23]:
            GPIO.output(i, 1)
            sleep(0.3)
        GPIO.setwanings(False)
        for j in [19, 21, 23]:
            GPIO.output(j, 0)
        GPIO.setwarnings(False)
        sleep(0.3)


def emergency_leds():
    while True:
        for i in [(7, 19), (5, 21), (3, 23)]:
            GPIO.output(i[0], 1)
            GPIO.output(i[1], 1)
            sleep(0.3)
        GPIO.setwarnings(False)
        for j in [(7, 19), (5, 21), (3, 23)]:
            GPIO.output(j[0], 0)
            GPIO.output(j[1], 0)
        GPIO.setwarnings(False)
        sleep(0.3)


def leds_on():
    for i in [(7, 19), (5, 21), (3, 23)]:
        GPIO.output(i[0], 1)
        GPIO.output(i[1], 1)
    GPIO.setwarnings(False)


def leds_off():
    for i in [(7, 19), (5, 21), (3, 23)]:
        GPIO.output(i[0], 0)
        GPIO.output(i[1], 0)
    GPIO.setwarnings(False)

def leds_off_left():
    for i in [7, 5, 3, ]:
        GPIO.output(i, 0)
    GPIO.setwarnings(False)
def leds_off_right():
    for i in [19, 21, 23]:
        GPIO.output(i, 0)
    GPIO.setwarnings(False)

def main():
    # main loop of program
    # Print blank line before and after message.
    print("\nPress Ctrl C to quit \n")

    try:
        while True:
            received_message = sys.stdin.readline()

            if not received_message or "esc" in received_message:
                break

            # DO SOMETHING WITH DATA
            print("Mesaj primit: " + received_message)
            # received_message.strip()
            command = received_message.split(':')
            key = command[0]
            state = command[1]
            if key == "daytimeLights":
                if state == "on\n":
                    leds_on()
                elif state == "off\n":
                    leds_off()

            if key == "brakeLights":
                if state == "on\n":
                    rear_lights_on()
                elif state == "off\n":
                    rear_lights_off()

            if key == "leftSignal":
                if state == "on\n":
                    leds_on_left()
                elif state == "off\n":
                    leds_off_left()
			
            if key == "rightSignal":
                if state == "on\n":
                    leds_on_right()
                elif state == "off\n":
                    leds_off_right()

    except Exception as ex:
        print(ex)
    finally:
        leds_off()
        rear_lights_off()


if __name__ == '__main__':
    main()
