import sys
import time
from picamera import PiCamera

DEFAULT_IMAGE_LOCATION = './public/SavedImage/image.jpg'

if __name__ == '__main__':
	# start=time.time()	
	camera = PiCamera()

	location = DEFAULT_IMAGE_LOCATION
	if len(sys.argv) > 1:
		location = sys.argv[1]

	camera.capture(location)
	#end=time.time()
	#print(end-start)
