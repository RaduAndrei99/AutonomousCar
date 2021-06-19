import RPi.GPIO as GPIO
import sys
import threading
import traceback
import logging

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

forward_thread = None
left_forward_thread = None
right_forward_thread = None

backward_thread = None
left_backward_thread = None
right_backward_thread = None

running_w = False
running_aw = False
running_dw = False

running_s = False
running_as = False
running_ds = False


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

    while running_w:
        pass
    print("Forward execution stopped")

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

    while running_s:
        pass
    print("Backward execution stopped")



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

    pwm_A.ChangeDutyCycle(speed-30)
    pwm_B.ChangeDutyCycle(speed)

    while running_aw:
        pass
    print("Forward left execution stopped")


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
    pwm_B.ChangeDutyCycle(speed-30)

    while running_dw:
        pass
    print("Forward right execution stopped")


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

    pwm_A.ChangeDutyCycle(speed-30)
    pwm_B.ChangeDutyCycle(speed)

    while running_as:
        pass

    print("Backward left execution stopped")


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
    pwm_B.ChangeDutyCycle(speed-30)

    while running_ds:
        pass

    print("Backward right execution stopped")


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
    print("Cleanup pins..")


def stop_motors():
    global pwm_A
    global pwm_B

    pwm_A.ChangeDutyCycle(0)
    pwm_B.ChangeDutyCycle(0)

    print("Motors execution stopped")

def prepare():
    init()
    dc = 0                               # set dc variable to 0 for 0%
    pwm_A.start(dc)                      # Start PWM with 0% duty cycle
    pwm_B.start(dc)

directions = set()

def main():
    prepare()

    # main loop of program
    # Print blank line before and after message.
    print("\nPress Ctrl C to quit \n")

    logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

    speed = 50

    global forward_thread
    global left_forward_thread
    global right_forward_thread

    global backward_thread
    global left_backward_thread
    global right_backward_thread

    global running_w
    global running_aw
    global running_dw

    global running_s
    global running_as
    global running_ds

    try:
        while True:
            try:
                received_message = sys.stdin.readline()
            except:
                print("Stopped reading from STDIN")
                break

            if not received_message or "esc" in received_message:
                break

            # DO SOMETHING WITH DATA
            logging.debug("Mesaj primit: " + received_message)

            command = received_message.split(':')
            key = command[0]
            state = command[1]

            if state == "pressed\n" and len(directions) <= 2:
                if not (('w' in directions and key == 's') or ('s' in directions and key == 'w') or ('a' in directions and key == 'd') or ('d' in directions and key == 'a')):
                    directions.add(key)

            if state == "released\n" and key in directions:
                directions.remove(key)

                if running_w:
                    running_w = False
                    forward_thread.join()

                if running_aw:
                    running_aw = False
                    left_forward_thread.join()

                if running_dw:
                    running_dw = False
                    right_forward_thread.join()

                if running_s:
                    running_s = False
                    backward_thread.join()

                if running_as:
                    running_as = False
                    left_backward_thread.join()

                if running_ds:
                    running_ds = False
                    right_backward_thread.join()


            print("Current directions: ", directions)

            if "w" in directions and "a" in directions:
                if running_w:
                    running_w = False
                    forward_thread.join()

                running_aw = True
                left_forward_thread = threading.Thread(target=move_to_the_left_forward, args=(speed,))
                left_forward_thread.start()


            if "w" in directions and "d" in directions:
                if running_w:
                    running_w = False
                    forward_thread.join()

                running_dw = True
                right_forward_thread = threading.Thread(target=move_to_the_right_forward, args=(speed,))
                right_forward_thread.start()


            if "s" in directions and "a" in directions:
                if running_s:
                    running_s = False
                    backward_thread.join()

                running_sa = True
                left_backward_thread = threading.Thread(target=move_to_the_left_backward, args=(speed,))
                left_backward_thread.start()


            if "s" in directions and "d" in directions:
                if running_s:
                    running_s = False
                    backward_thread.join()
                
                running_sd = True
                right_backward_thread = threading.Thread(target=move_to_the_right_backward, args=(speed,))
                right_backward_thread.start()

            if "w" in directions and len(directions) == 1:
                running_w = True
                forward_thread = threading.Thread(target=move_forward, args=(speed,))
                forward_thread.start()

            if "s" in directions and len(directions) == 1:
                running_s = True
                backward_thread = threading.Thread(target=move_backward, args=(speed,))
                backward_thread.start()

            if len(directions) == 0:
                stop_motors()

    except Exception as ex:
        print(ex)
    finally:
        clean()


if __name__ == '__main__':
    main()
