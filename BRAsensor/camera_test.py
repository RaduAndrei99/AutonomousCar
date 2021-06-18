import sys
from picamera import PiCamera

DEFAULT_IMAGE_LOCATION = '/home/pi/image.jpg'

if __name__ == '__main__':
	camera = PiCamera()

	location = DEFAULT_IMAGE_LOCATION
	if len(sys.argv) > 1:
		location = sys.argv[1]

	camera.capture(location)
