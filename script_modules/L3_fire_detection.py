import Adafruit_BBIO.GPIO as GPIO
import time
import signal
import L2_log as log
import L3_spray as spray
print("loading libraries for color tracking...")
import cv2              # For image capture and processing
import argparse         # For fetching user arguments
import numpy as np      # Kernel
print("loading rcpy.")
import rcpy                 # Import rcpy library
import rcpy.motor as motor  # Import rcpy motor module
print("finished loading libraries.")

camera_input = 0        # Define camera input. Default=0. 0=/dev/video0
size_w  = 240   # Resized image width. This is the image width in pixels.
size_h = 160	# Resized image height. This is the image height in pixels.

#    Color Range, described in HSV for fire detections
v1_min = 0     # Minimum H value
v2_min = 40     # Minimum S value
v3_min = 190    # Minimum V value

v1_max = 25     # Maximum H value
v2_max = 85     # Maximum S value
v3_max = 255    # Maximum V value

#    RGB or HSV
filter = 'HSV'  # Use HSV to describe pixel color values

# IR GPIO inputs
IR1 = 'P9_28'
IR2 = 'GP0_5'
IR3 = 'P9_23'
IR4 = 'GP0_3'

GPIO.setup(IR1, GPIO.IN)
GPIO.setup(IR2, GPIO.IN)
GPIO.setup(IR3, GPIO.IN)
GPIO.setup(IR4, GPIO.IN)

def main():

    camera = cv2.VideoCapture(camera_input)     # Define camera variable
    camera.set(3, size_w)                       # Set width of images that will be retrived from camera
    camera.set(4, size_h)                       # Set height of images that will be retrived from camera

    tc = 70     # Too Close     - Maximum pixel size of object to track
    tf = 6      # Too Far       - Minimum pixel size of object to track
    tp = 65     # Target Pixels - Target size of object to track

    band = 50   #range of x considered to be centered

    x = 0  # will describe target location left to right
    y = 0  # will describe target location bottom to top

    radius = 0  # estimates the radius of the detected target

    duty_l = 0 # initialize motor with zero duty cycle
    duty_r = 0 # initialize motor with zero duty cycle
    
    scale_t = 1.3	# a scaling factor for speeds
    scale_d = 1.3	# a scaling factor for speeds

    # 4 CARLOS - set motor names 
    motor_actuation = 4 # actuator
    motor_spin = 3 # spin
    motor_r = 2 # Right Motor
    motor_l = 1 # left motor

    print("initializing rcpy...")
    rcpy.set_state(rcpy.RUNNING)        # initialize rcpy
    print("finished initializing rcpy.")

    try:

        while rcpy.get_state() != rcpy.EXITING:

            if rcpy.get_state() == rcpy.RUNNING:

                ret, image = camera.read()  # Get image from camera

                height, width, channels = image.shape   # Get size of image

                if not ret:
                    break

                if filter == 'RGB':                     # If image mode is RGB switch to RGB mode
                    frame_to_thresh = image.copy()
                else:
                    frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)    # Otherwise continue reading in HSV

                thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))   # Find all pixels in color range

                kernel = np.ones((5,5),np.uint8)                            # Set gaussian blur strength.
                mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)     # Apply gaussian blur
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]     # Find closed shapes in image
                center = None   # Create variable to store point

                if len(cnts) > 0:   # If more than 0 closed shapes exist

                    c = max(cnts, key=cv2.contourArea)              # Get the properties of the largest circle
                    ((x, y), radius) = cv2.minEnclosingCircle(c)    # Get properties of circle around shape

                    radius = round(radius, 2)   # Round radius value to 2 decimals

                    x = int(x)          # Cast x value to an integer
                    M = cv2.moments(c)  # Gets area of circle contour
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))   # Get center x,y value of circle

                    # handle centered condition
                    if x > ((width/2)-(band/2)) and x < ((width/2)+(band/2)):       # If center point is centered

                        dir = "driving"

                        if radius > tp+2:    # Too Close
                        {
                            case = "too close"
                            duty = -1 * ((radius-tp)/(tc-tp))
                        }

                        elif radius < tp-2:   # Too Far
                        {
                            case = "too far"
                            duty = 1 - ((radius - tf)/(tp - tf))
                            duty = scale_d * duty
                        }
                        # added this elif
                        elif (radius <= (tp+2) && radius >= (tp-2) && GPIO.input(IR2) == 0):
                        {
                            case = "spray"
                            duty = 0
                            motor.set(motor_l, 0)
                            motor.set(motor_r, 0)
                            
                            while (radius <= (tp+2) && radius >= (tp-2) && GPIO.input(IR2) == 0):
                            {
                                spary.sprayCan()
                            }
                        }

                        duty_r = duty
                        duty_l = duty

                    else:
                        case = "turning"

                        duty_l = round((x-0.5*width)/(0.5*width),2)     # Duty Left
                        duty_l = duty_l*scale_t

                        duty_r = round((0.5*width-x)/(0.5*width),2)     # Duty Right
                        duty_r = duty_r*scale_t

                    # Keep duty cycle within range

                    if duty_r > 1:
                        duty_r = 1

                    elif duty_r < -1:
                        duty_r = -1

                    if duty_l > 1:
                        duty_l = 1

                    elif duty_l < -1:
                        duty_l = -1

                    # Round duty cycles
                    duty_l = round(duty_l,2)
                    duty_r = round(duty_r,2)

                    print(case, "\tradius: ", round(radius,1), "\tx: ", round(x,0), "\t\tL: ", duty_l, "\tR: ", duty_r)

                    # Set motor duty cycles
                    motor.set(motor_l, duty_l)
                    motor.set(motor_r, duty_r)
                    
                elif (len(cnts) == 0 && (GPIO.input(IR1) == 0 || GPIO.input(IR3) == 0 || GPIO.input(IR4) == 0)):
                {
                    while (GPIO.input(IR2) == 1):
                    {
                        if (GPIO.input(IR1) == 0): # right side
                        {
                            motor.set(motor_l, 0.6)
                            motor.set(motor_r, -0.6)
                            time.sleep(1.8)
                        }
                        if (GPIO.input(IR3) == 0): # front-left side
                        {
                            motor.set(motor_l, -0.3)
                            motor.set(motor_r, 0.3)
                            time.sleep(0.6)
                        }
                        if (GPIO.input(IR4) == 0): # left side
                        {
                            motor.set(motor_l, -0.6)
                            motor.set(motor_r, 0.6)
                            time.sleep(1.8)
                        } 
                    }
                }
                    

                # Set motor duty cycles
                motor.set(motor_l, duty_l)
                motor.set(motor_r, duty_r)

            elif rcpy.get_state() == rcpy.PAUSED:
                pass

    except KeyboardInterrupt: # condition added to catch a "Ctrl-C" event and exit cleanly
        rcpy.set_state(rcpy.EXITING)
        pass

    finally:

    	rcpy.set_state(rcpy.EXITING)
    	print("Exiting Color Tracking.")

# exiting program will automatically clean up cape

if __name__ == '__main__':
    main()

while True:
    input1 = GPIO.input(IR1)
    print("Input: ", input1, " cm")
    input2 = GPIO.input(IR2)
    print("Input: ", input2, " cm")
    time.sleep(0.1)
    
# i wanted to measure distance but this shit is botched