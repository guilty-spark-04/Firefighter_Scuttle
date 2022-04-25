import L2_vector as v
import L1_lidar as lidar
import numpy as np
import time
import csv
import rcpy
import rcpy.motor as motor
print("finished loading motor libraries")

motor_r = 2
motor_l = 1
MIN_DISTANCE = 0.2
MAX_DISTANCE = 5
TARGET_DISTANCE = 0.3
print("initializing rcpy...")
rcpy.set_state(rcpy.RUNNING)
print("Successfully set to running state")

#left is positive theta. right is negative theta
try:
    while(rcpy.get_state() != rcpy.EXITING):
        scan = lidar.polarScan()
        valid = v.getValid(scan)
        nearest = v.nearest(valid)
        coordinates = v.polar2cart(nearest[0],nearest[1])
        print(f"Nearest object is at\nx: {coordinates[0]}\ny:{coordinates[1]}\nangle is:{nearest[1]}")
        duty = 0
        if(nearest[1] < 30 and nearest[1] > -30): #obstacle is mostly centered. distance only affects velocity
            if(coordinates[0] < TARGET_DISTANCE): #too close
                print("item is close")
                duty = -1 * (coordinates[0]-TARGET_DISTANCE)/(MIN_DISTANCE-TARGET_DISTANCE)
            else: #prob make it turn 90 degrees or something
                duty = 0.6
            duty_l = duty
            duty_r = duty
        else:
            duty_l = round((0.0-nearest[1])/abs(nearest[1]),2)
            duty_r = round((nearest[1]-0.0)/abs(nearest[1]),2)
            print(f"duty l is {duty_l} duty_r is {duty_r}")
            duty_l = 0.5*duty_l
            duty_r = 0.5*duty_r
            
            print("turning")
        
        if duty_r > 1:
            duty_r = 1

        elif duty_r < -1:
            duty_r = -1

        if duty_l > 1:
            duty_l = 1

        elif duty_l < -1:
            duty_l = -1
        
        duty_l = round(duty_l,2)
        duty_r = round(duty_r,2)
        print(f"settings {duty_l} and {duty_r}")
        if(duty_l < 0 and duty_r > 0):
             print("left")
        if(duty_l > 0 and duty_r < 0):
             print("right")
        motor.set(motor_l, duty_l)
        motor.set(motor_r, duty_r)
        time.sleep(2)
except KeyboardInterrupt:
    rcpy.set_state(rcpy.EXITING)
    pass
finally:
    rcpy.set_state(rcpy.EXITING)
    print("exiting program")

