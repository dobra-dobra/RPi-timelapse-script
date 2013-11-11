# Script used to take pictures with RPi camera module
# which can be used to make timelapses
# To stop script connect GPIO pin 3 to ground (i.e. pin 4)

# Import modules
import subprocess
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Definition of fixed values
SLEEP_TIME = 2
DIRECTORY = '/home/pi/timelapses'

# Definition of variables
image_counter = 1

# Helper function to format number as 4-digit
def format_number(number):
    if (number < 10):
        number = 3 * str(0) + str(number)
    elif (number < 100):
        number = 2 * str(0) + str(number)
    elif (number < 1000):
        number = str(0) + str(number)
    else:
        number = str(number)
    return number

# Helper function to check if camera is supported and connected
#def camera_available():
#    response = ''
#    camera_supported = 0
#    camera_detected = 0
#    response = subprocess.check_output(['vcgencmd', 'get_camera'])
#    camera_supported = int(chr(response[10]))
#    camera_detected = int(chr(response[-2]))
#    if camera_supported == 1 and camera_detected == 1:
#        return True
#    else:
#        return False

# Helper function to determine if jumper is in or out
def tl_jumper_in():
    if GPIO.input(3) == 1:
        return True
    else:
        return False

if tl_jumper_in():
    file = open(DIRECTORY + '/timelapse_number.txt', 'r')
    tl_number = file.read()
    file.close()
    tl_number = int(tl_number) + 1
    file = open(DIRECTORY + '/timelapse_number.txt', 'w')
    file.write(format_number(tl_number))
    file.close()
    while tl_jumper_in():
        file_name = DIRECTORY + '/tl' + format_number(tl_number) + '_im' + format_number(image_counter) + '.jpg'
        subprocess.call(['raspistill', '-o', file_name, '-t', '2000', '-n', '-ex', 'antishake', '-w', '1440', '-h', '900', '-rot', '270'])
        image_counter += 1
        sleep(SLEEP_TIME)

print ('Timelapse script was stopped')
GPIO.cleanup()
