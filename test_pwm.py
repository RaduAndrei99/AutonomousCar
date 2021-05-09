#  MBTechWorks.com 2016
#  Pulse Width Modulation (PWM) demo to cycle brightness of an LED

import RPi.GPIO as GPIO   # Import the GPIO library.
import time               # Import time library
import socket

HOST = '192.168.43.166'
PORT = 5678

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


def create_and_bind_server_socket(SERVER_IP, PORT, CONCURENT_CONNECTIONS=1):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, PORT))
    print("S-a facut bind la " + str((SERVER_IP, PORT)))

    server_socket.listen(CONCURENT_CONNECTIONS)
    return server_socket

def close_socket(sock):
    if sock is not None:
        sock.close()

def main():
	init()


	# main loop of program
	print("\nPress Ctl C to quit \n")  # Print blank line before and after message.
	dc=0                               # set dc variable to 0 for 0%
	pwm_A.start(dc)                      # Start PWM with 0% duty cycle
	pwm_B.start(dc)

	server_socket = None
	conn = None

	try:
		server_socket = create_and_bind_server_socket(SERVER_IP=HOST, PORT=PORT)

		conn, addr = server_socket.accept()
		while True:
			received_data = conn.recv(1024).decode()

			if not received_data or "esc" in received_data:
				break

			# DO SOMETHING WITH DATA
			print(received_data)

			if received_data == 'w:pressed':
				move_forward(50)

			if received_data.split(':')[1] == 'released':
				stop_motors()

	except Exception as ex:
		print(ex)
	finally:
		clean()
		close_socket(sock=server_socket)
		close_socket(sock=conn)


if __name__ == '__main__':
	main()
