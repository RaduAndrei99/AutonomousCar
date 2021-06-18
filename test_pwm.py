#  MBTechWorks.com 2016
#  Pulse Width Modulation (PWM) demo to cycle brightness of an LED

import RPi.GPIO as GPIO   # Import the GPIO library.
import time               # Import time library
from server import Server

HOST = '192.168.100.47'
PORT = 1234

motor_A_0 = 16
motor_A_1 = 18
motor_B_0 = 22
motor_B_1 = 24
pwm_motor_A = 12
pwm_motor_B = 26

GPIO.setmode(GPIO.BOARD)

GPIO.setup(pwm_motor_A, GPIO.OUT)
GPIO.setup(pwm_motor_B, GPIO.OUT)

pwm_A = GPIO.PWM(pwm_motor_A, 1000)
pwm_B = GPIO.PWM(pwm_motor_B, 1000)

def move_forward(speed):
	global motor_A_0
	global motor_A_1
	global motor_B_0
	global motor_B_1
	global pwm_A
	global pwm_B

	GPIO.output(motor_A_0, GPIO.HIGH)
	GPIO.output(motor_A_1, GPIO.LOW)
	GPIO.output(motor_B_0, GPIO.HIGH)
	GPIO.output(motor_B_1, GPIO.LOW)

	pwm_A.ChangeDutyCycle(speed)
	pwm_B.ChangeDutyCycle(speed)

def move_backward(speed):
	global motor_A_0
	global motor_A_1
	global motor_B_0
	global motor_B_1
	global pwm_A
	global pwm_B

	GPIO.output(motor_A_0, GPIO.LOW)
	GPIO.output(motor_A_1, GPIO.HIGH)
	GPIO.output(motor_B_0, GPIO.LOW)
	GPIO.output(motor_B_1, GPIO.HIGH)

	pwm_A.ChangeDutyCycle(speed)
	pwm_B.ChangeDutyCycle(speed)

def move_to_the_left_forward(speed):
	global motor_A_0
	global motor_A_1
	global motor_B_0
	global motor_B_1
	global pwm_A
	global pwm_B

	GPIO.output(motor_A_0, GPIO.HIGH)
	GPIO.output(motor_A_1, GPIO.LOW)
	GPIO.output(motor_B_0, GPIO.HIGH)
	GPIO.output(motor_B_1, GPIO.LOW)

	pwm_A.ChangeDutyCycle(speed-10)
	pwm_B.ChangeDutyCycle(speed)

def move_to_the_right_forward(speed):
	global motor_A_0
	global motor_A_1
	global motor_B_0
	global motor_B_1
	global pwm_A
	global pwm_B

	GPIO.output(motor_A_0, GPIO.HIGH)
	GPIO.output(motor_A_1, GPIO.LOW)
	GPIO.output(motor_B_0, GPIO.HIGH)
	GPIO.output(motor_B_1, GPIO.LOW)

	pwm_A.ChangeDutyCycle(speed)
	pwm_B.ChangeDutyCycle(speed-10)

def move_to_the_left_backward(speed):
        global motor_A_0
        global motor_A_1
        global motor_B_0
        global motor_B_1
        global pwm_A
        global pwm_B

        GPIO.output(motor_A_0, GPIO.LOW)
        GPIO.output(motor_A_1, GPIO.HIGH)
        GPIO.output(motor_B_0, GPIO.LOW)
        GPIO.output(motor_B_1, GPIO.HIGH)

        pwm_A.ChangeDutyCycle(speed-10)
        pwm_B.ChangeDutyCycle(speed)

def move_to_the_right_backward(speed):
        global motor_A_0
        global motor_A_1
        global motor_B_0
        global motor_B_1
        global pwm_A
        global pwm_B

        GPIO.output(motor_A_0, GPIO.LOW)
        GPIO.output(motor_A_1, GPIO.HIGH)
        GPIO.output(motor_B_0, GPIO.LOW)
        GPIO.output(motor_B_1, GPIO.HIGH)

        pwm_A.ChangeDutyCycle(speed)
        pwm_B.ChangeDutyCycle(speed-10)

def init():
	global motor_A_0
	global motor_A_1
	global motor_B_0
	global motor_B_1
	global pwm_motor_A
	global pwm_motor_B

	GPIO.setup(motor_A_0, GPIO.OUT)
	GPIO.setup(motor_A_1, GPIO.OUT)
	GPIO.setup(motor_B_0, GPIO.OUT)
	GPIO.setup(motor_B_1, GPIO.OUT)
	GPIO.setup(pwm_motor_A, GPIO.OUT)
	GPIO.setup(pwm_motor_B, GPIO.OUT)

def clean():
	pwm_A.stop()
	pwm_B.stop()
	GPIO.cleanup()

def stop_motors():
	global pwm_A
	global pwm_B

	pwm_A.ChangeDutyCycle(0)
	pwm_B.ChangeDutyCycle(0)

directions = set()

def main():
	init()


	# main loop of program
	print("\nPress Ctl C to quit \n")  # Print blank line before and after message.
	dc=0                               # set dc variable to 0 for 0%
	pwm_A.start(dc)                      # Start PWM with 0% duty cycle
	pwm_B.start(dc)

	server = None
	conn = None
	speed = 50

	try:
		server = Server(SERVER_IP=HOST, PORT=PORT)
		conn, addr = server.accept_connection()

		while True:
			received_message = server.receive_message(conn)

			if not received_message or "esc" in received_message:
				break

			# DO SOMETHING WITH DATA
			print("Mesaj primit: " + received_message)

			command = received_message.split(':')
			key = command[0]
			state = command[1]

			if state == "pressed" and len(directions) <= 2:
				if not (('w' in directions and key == 's') or ('s' in directions and key == 'w') or ('a' in directions and key == 'd') or ('d' in directions and key == 'a')):
					directions.add(key)

			if state == "released" and key in directions:
				directions.remove(key)

			print(directions)

			if "w" in directions and "a" in directions:
				move_to_the_left_forward(speed)

			if "w" in directions and "d" in directions:
				move_to_the_right_forward(speed)

			if "s" in directions and "a" in directions:
				move_to_the_left_backward(speed)

			if "s" in directions and "d" in directions:
				move_to_the_right_backward(speed)
			
			if "w" in directions:
				move_forward(speed)

			if "s" in directions:
                                move_backward(speed)

			if len(directions) == 0:
			 	stop_motors()

	except Exception as ex:
		print(ex)
	finally:
		clean()
		server.close_socket()
		if conn is not None:
			conn.close()


if __name__ == '__main__':
	main()

